import pandas as pd
import sys
import os
import glob
os.environ['KMP_DUPLICATE_LIB_OK']='True'
import pyopenms as pyms
import argparse, pathlib

parser = argparse.ArgumentParser()
parser.add_argument('mztab_dir', type=pathlib.Path)
parser.add_argument('idxml_file', type=pathlib.Path, help="Output file path and name")
args = parser.parse_args()

mztab_files = glob.glob(str(args.mztab_dir / '*.mztab'))

run_name = 'unknown'
peptide_ids = []

for mztab_file in mztab_files:
    with open(mztab_file) as f_in:
        skiplines = 0
        line = next(f_in)
        while line.split('\t', 1)[0] != 'PSH':
            if 'ms_run[1]-location' in line:
                run_name = line.split('\t')[2]
            line = next(f_in)
            skiplines += 1

        psms = pd.read_csv(mztab_file, sep='\t', header=skiplines, index_col='PSM_ID')

        for _, psm in psms.iterrows():
            peptide_id = pyms.PeptideIdentification()
            peptide_id.setRT(psm['retention_time'])
            peptide_id.setMZ(psm['exp_mass_to_charge'])
            peptide_id.setScoreType('q-value')
            peptide_id.setHigherScoreBetter(False)
            peptide_id.setIdentifier(run_name)
            peptide_hit = pyms.PeptideHit()
            peptide_hit.setScore(psm['search_engine_score[2]'])
            peptide_hit.setRank(1)
            peptide_hit.setCharge(psm['charge'])
            peptide_hit.setSequence(pyms.AASequence.fromString(psm['sequence']))
            peptide_id.setHits([peptide_hit])
            peptide_ids.append(peptide_id)

protein_id = pyms.ProteinIdentification()
protein_id.setIdentifier(run_name)
pyms.IdXMLFile().store(str(args.idxml_file), [protein_id], peptide_ids)

