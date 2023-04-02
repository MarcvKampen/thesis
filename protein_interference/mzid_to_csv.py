import argparse
import pandas as pd
from pyteomics import mzid
import os

# Define command-line arguments
parser = argparse.ArgumentParser(description='Process a .mzid file and save results as a .csv file.')
parser.add_argument('input_file', type=str, help='Path to the input .mzid file')
parser.add_argument('output_file', type=str, help='Name of the output .csv file')

# Parse command-line arguments
args = parser.parse_args()

# Read mzid file
piafile = mzid.DataFrame(args.input_file)

# Define columns of interest
columns_of_interest = ['spectrumID', 'scan start time', 'location', 'chargeState', 'experimentalMassToCharge', 'rank',
       'passThreshold', 'PSM-level FDRScore', 'PSM-level q-value',
       'PeptideSequence', 'isDecoy', 'accession', 'protein description',
       'AA sequence', 'start', 'end', 'length', 'Modification']

# Filter piafile by columns of interest
piafile_filtered = piafile[columns_of_interest]

# Rename columns for consistency
piafile_filtered.columns = ['spectrum_id', 'scan_start_time', 'location', 'charge_state', 'experimental_mz', 'rank',
       'pass_threshold', 'psm_lvl_fdr_score', 'psm_level_q_value', 'peptide_sequence', 'is_decoy', 'accession', 'protein_description',
       'aa_sequence', 'start', 'end', 'length', 'modification']

# Write filtered dataframe to csv file
piafile_filtered.to_csv(args.output_file, index=False)
