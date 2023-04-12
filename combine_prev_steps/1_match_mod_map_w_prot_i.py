import argparse
import csv

# Set up argparse to take input file paths as arguments
parser = argparse.ArgumentParser()
parser.add_argument('file1', type=str, help='Path to first input CSV file')
parser.add_argument('file2', type=str, help='Path to second input CSV file')
parser.add_argument('output', type=str, help='Path to output CSV file')
args = parser.parse_args()

# Open the input files
with open(args.file1, 'r') as file1, open(args.file2, 'r') as file2:
    # Create CSV reader objects for both files
    reader1 = csv.DictReader(file1)
    reader2 = csv.DictReader(file2)
    
    # Create a list and a set to store the matched rows and their hashes
    matched_rows = []
    matched_hashes = set()
    
    # Iterate through the rows of file1
    for row1 in reader1:
        # Iterate through the rows of file2
        for row2 in reader2:
            # Compare the 'sequence' column from file1 with the 'peptide_sequence' column from file2
            if row1['sequence'] == row2['peptide_sequence']:
                # If there is a match, merge the entire row from both files and append to matched_rows list
                matched_row = {**row1, **row2}
                matched_row_hash = hash(frozenset(matched_row.items()))
                if matched_row_hash not in matched_hashes:
                    matched_hashes.add(matched_row_hash)
                    matched_rows.append(matched_row)
                
        # Reset the reader2 to the beginning of the file for each row in reader1
        file2.seek(0)
        
# Write the matched rows to the output file, but exclude the 'peptide_sequence' column
with open(args.output, 'w', newline='') as output_file:
    # Get the fieldnames for the output file from the first row of the matched_rows list
    fieldnames = matched_rows[0].keys()
    
    # Remove the 'peptide_sequence' column from the fieldnames
    fieldnames = [field for field in fieldnames if field != 'peptide_sequence']
    
    # Create a CSV writer object for the output file
    writer = csv.DictWriter(output_file, fieldnames)
    
    # Write the fieldnames to the first row of the output file
    writer.writeheader()
    
    # Write the matched rows to the output file, but exclude the 'peptide_sequence' column
    for row in matched_rows:
        row.pop('peptide_sequence')
        writer.writerow(row)
