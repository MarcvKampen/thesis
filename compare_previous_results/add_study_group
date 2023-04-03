import argparse
import csv

# define the parameters
asymptomatic = ['UWA626', 'UWA596', 'UWA419', 'UWA422', 'UWA556', 'UWA558']
control = ['UWA479', 'UWA420', 'UWA506', 'UWA531', 'UWA431', 'UWA623']
symptomatic = ['UWA576', 'UWA579', 'UWA580', 'UWA612', 'UWA614', 'UWA530']

# define the argument parser
parser = argparse.ArgumentParser(description='Update PSM_ID column in a CSV file.')
parser.add_argument('input_file', type=str, help='path to the input CSV file')
parser.add_argument('output_file', type=str, help='path to the output CSV file')
args = parser.parse_args()

# read the CSV file and write the updated rows to a new file
with open(args.input_file, newline='') as infile, open(args.output_file, 'w', newline='') as outfile:
    reader = csv.DictReader(infile)
    fieldnames = reader.fieldnames
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()
    # iterate through each row
    for row in reader:
        # extract the UWAxxx part from the PSM_ID column
        uwa_id = row['PSM_ID'].split('.')[0].split('_')[0]
        # check if the UWAxxx matches any of the parameters
        if uwa_id in asymptomatic:
            row['PSM_ID'] = 'Asymptomatic AD'
        elif uwa_id in control:
            row['PSM_ID'] = 'Control'
        elif uwa_id in symptomatic:
            row['PSM_ID'] = 'Symptomatic AD'
        # write the updated row to the output file
        writer.writerow({k: row[k] if k != 'PSM_ID' else row['PSM_ID'].split('.')[0] for k in fieldnames})
