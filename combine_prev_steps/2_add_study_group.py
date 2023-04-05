import argparse
import csv

# define the parameters
asymptomatic = ['UWA626', 'UWA596', 'UWA419', 'UWA422', 'UWA556', 'UWA558']
control = ['UWA479', 'UWA420', 'UWA506', 'UWA531', 'UWA431', 'UWA623']
symptomatic = ['UWA576', 'UWA579', 'UWA580', 'UWA612', 'UWA614', 'UWA530']

# define the input arguments
parser = argparse.ArgumentParser(description='rewrite PSM_ID column to study group')
parser.add_argument('input_file', type=str, help='path to .csv file')
parser.add_argument('output_file', type=str, help='path to .csv file')
args = parser.parse_args()

# read the .csv file and write the updated rows to a new file
with open(args.input_file, newline='') as infile, open(args.output_file, 'w', newline='') as outfile:
    reader = csv.DictReader(infile)
    fieldnames = ['study_group'] + [f for f in reader.fieldnames if f != 'PSM_ID']
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()
    # iterate through each row
    for row in reader:
        # extract the UWAxxx part from the PSM_ID column
        uwa_id = row['PSM_ID'].split('.')[0].split('_')[0]
        # check if the UWAxxx matches any of the parameters
        if uwa_id in asymptomatic:
            row['study_group'] = 'Asymptomatic AD'
        elif uwa_id in control:
            row['study_group'] = 'Control'
        elif uwa_id in symptomatic:
            row['study_group'] = 'Symptomatic AD'
        # write the updated row to the output file
        writer.writerow({k: row[k] for k in fieldnames})
