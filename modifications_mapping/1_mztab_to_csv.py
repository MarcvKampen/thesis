import os
import operator
import numpy as np
import argparse
import pathlib
import pandas as pd
import pyteomics.auxiliary
import io

def script1(mztab_path):
    with open(mztab_path, 'r') as f:
        lines = []
        for line in f:
            if line.startswith('MTD'):
                continue
            else:
                lines.append(line)
    # convert the list of lines to a pandas DataFrame
    mztab = pd.read_csv(io.StringIO('\n'.join(lines)), sep='\t')
    return mztab

def script2(mztab, mass_tolerance):
    mztab_mtol = mztab[['sequence', 'PSM_ID', 'exp_mass_to_charge', 'calc_mass_to_charge', 'charge']].copy()
    mztab_mtol['mass_diff'] = (mztab_mtol['exp_mass_to_charge'] - mztab_mtol['calc_mass_to_charge']) * mztab_mtol['charge']
    mztab_mtol['exp_mass'] = mztab_mtol['exp_mass_to_charge'] * mztab_mtol['charge']
    mztab_mtol['mass_tol'] = mass_tolerance * mztab_mtol['exp_mass'] * 10**-6
    mztab_mtol['mass_tol_pos'] = mztab_mtol['mass_diff'] + mztab_mtol['mass_tol']
    mztab_mtol['mass_tol_neg'] = mztab_mtol['mass_diff'] - mztab_mtol['mass_tol']
    mztab_mtol = mztab_mtol.query("mass_tol_neg < 0 | mass_tol_pos > 0")
    mztab_mtol = mztab_mtol.sort_values('mass_tol_pos')
    return mztab_mtol

def script3(psms_modified, output_path, unimod_path):
    output_path_mt = pathlib.Path(output_path)
    output_path_mod = output_path_mt.with_suffix('.mod.csv')
    unimod = pd.read_csv(unimod_path)
    mod_names, mod_masses = [], []
    if 'mass_tol_neg' not in psms_modified.columns or 'mass_tol_pos' not in psms_modified.columns:
        raise ValueError('`mass_tol_neg` and `mass_tol_pos` columns are missing from the input file.')

    for row in psms_modified.itertuples(index=False):
        mass_tol_neg, mass_tol_pos = row.mass_tol_neg, row.mass_tol_pos
        idx_start, idx_stop = unimod['mod_mass'].searchsorted([mass_tol_neg, mass_tol_pos])
        if idx_stop > idx_start:
            potential_mods = unimod.loc[idx_start:idx_stop-1, ['mod_mass', 'mod_name']]
            mod_names.append(' / '.join(potential_mods['mod_name'].astype(str)))
            mod_masses.append(' / '.join(potential_mods['mod_mass'].astype(str)))
        else:
            mod_names.append('No direct match found in Unimod')
            mod_masses.append('')

    psms_modified['mod'] = mod_names
    psms_modified['mod_mass'] = mod_masses
    psms_modified.to_csv(output_path_mod, sep=",", index=False)

if __name__ == '__main__':
    # Parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('mztab', nargs='+', type=pathlib.Path)
    parser.add_argument('--mass_tolerance', type=float, default=0.2)
    parser.add_argument('unimod_path', type=pathlib.Path)
    parser.add_argument('--output_path', type=pathlib.Path, default='./output')
    args = parser.parse_args()

    # Initialize an empty list to store the merged dataframes
    merged_df_list = []

    # Loop over all input mztab files and run the scripts
    for mztab_path in args.mztab:
        data1 = script1(mztab_path)
        data2 = script2(data1, args.mass_tolerance)

        # Add a new column to the dataframe to indicate the input file name
        data2['file_name'] = mztab_path.name

        # Append the modified dataframe to the list of dataframes
        merged_df_list.append(data2)

    # Concatenate all dataframes in the list into a single dataframe
    merged_df = pd.concat(merged_df_list, ignore_index=True)

    # Run script3 on the merged dataframe
    output_path_file = args.output_path / 'merged_output.csv'
    script3(merged_df, output_path_file, args.unimod_path)

    print(f'Merged output saved to (+.mod){output_path_file}')
