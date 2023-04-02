import argparse
import pandas as pd

# define command-line arguments
parser = argparse.ArgumentParser()
parser.add_argument("file1", help="path to input file 1")
parser.add_argument("file2", help="path to input file 2")
parser.add_argument("output", help="path to output file")
args = parser.parse_args()

# read input files into dataframes
df1 = pd.read_csv(args.file1)
df2 = pd.read_csv(args.file2)

# extract accession and protein ID columns
acc_col = "accession"
pid_col = "Protein_Unique_ID"
acc_series = df1[acc_col].apply(lambda x: [acc.strip(" '") for acc in x[2:-2].split(',')])
print(acc_series)
pid_series = df2[pid_col].apply(lambda x: x.split('|')[1] if '|' in x else x)
print(pid_series)

# create a new dataframe to hold combined rows
combined_df = pd.DataFrame()

# loop through accession column and compare against protein ID column
for acc_list in acc_series:
    for acc in acc_list:
        for pid in pid_series:
            if acc in pid:
                # match found, combine rows
                acc_rows = df1[df1[acc_col].apply(lambda x: acc in x)]
                pid_rows = df2[df2[pid_col].str.contains(pid)]
                for _, acc_row in acc_rows.iterrows():
                    for _, pid_row in pid_rows.iterrows():
                        combined_row = pd.concat([acc_row, pid_row], ignore_index=True)
                        combined_df = combined_df.append(combined_row, ignore_index=True)

# rename columns in combined dataframe
combined_df.columns = [
    "spectrum_id", "scan_start_time", "location", "charge_state", "experimental_mz",
    "rank", "pass_threshold", "psm_lvl_fdr_score", "psm_level_q_value", "peptide_sequence",
    "is_decoy", "accession", "protein_description", "aa_sequence", "start", "end",
    "length", "modification", "Protein Unique ID", "Module Assignment (Number)",
    "Module Assigment (Color)", "kME Dark Orange", "kME Dark Turquoise", "kME Brown",
    "kME Red", "kME Turquoise", "kME Light Green", "kME White", "kME Black",
    "kME Green Yellow", "kME Cyan", "kME Salmon", "kME Dark Red", "kME Pink",
    "kME Tan", "kME Magenta", "kME Light Cyan", "kME Royal Blue", "kME Midnight Blue",
    "kME Purple", "kME Light Yellow", "kME Grey60", "kME Blue", "kME Yellow",
    "kME Dark Green", "kME Dark Grey", "kME Green", "kME Orange", "kME Grey",
    "kME Table Sort Vector"
]

# write combined dataframe to output file
if not combined_df.empty:
    combined_df[["peptide_sequence", "Protein Unique ID", "charge_state", "modification", "Module Assignment (Number)", "Module Assigment (Color)"]].to_csv(args.output, index=False)
    print("Output file saved successfully!")
else:
    print("No matches found. Output file not saved.")

# python compare.py ditisdeoutput.csv test1b.csv klaar.csv
