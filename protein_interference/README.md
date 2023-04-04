# Workflow for MS-Based Protein Inference and Identification Analysis

## Introduction
In this guide, we present a step-by-step workflow for MS-based protein inference and identification analysis. The workflow involves the conversion of mztab files to idXML files, using openMS to refresh target/decoy information, and conducting statistical analyses using PIA (Protein Interference Algorithms).

## Workflow
Step 1: Convert mztab files to idXML files
The first step is to convert mztab files to idXML files. To do this, use the following script:
/thesis/protein_interference/mztab_to_idXML.py

Step 2: Use PeptideIndexer from openMS
PeptideIndexer is a tool from openMS that refreshes target/decoy information and mapping of peptides to proteins. It allows for ambiguous amino acids (B|J|Z|X) in the protein database and peptide sequence. The target/decoy information is crucial for the TOPP_FalseDiscoveryRate tool. For FDR calculations, peptides hitting both target and decoy proteins are counted as target hits.

To use PeptideIndexer, provide the refseq protein .fasta file from NIH. 
Example:
PeptideIndexer -in output_step1/UWA_output1.idXML -fasta fasta1.fasta -out output_step2/UWA_output2.idXML -missing_decoy_action 'error' -IL_equivalent -enzyme:specificity 'none'

Step 3: Use PIA to convert idXML files to xml files
PIA (Protein Interference Algorithms) is a toolbox for MS-based protein inference and identification analysis. It allows you to inspect the results of common proteomics spectrum identification search engines, combine them seamlessly, and conduct statistical analyses. PIA focuses on the integrated inference algorithms, i.e., concluding the proteins from a set of identified spectra.
Example:
java -jar pia-1.4.7.jar -c -n=test1 -o=output_step3/UWA_output3.xml output_step2/UWA_output2.idXML

Step 4: Use PIA to identify the proteins from the peptide sequence
To identify the proteins from the peptide sequence, use PIA and the following input example command:
java -jar pia-1.4.7.jar test1.json output_step3/UWA_output3.xml

Step 5: Convert mzid files to csv files
Convert the mzid file from Step 4 to a csv file. An python script provided:
/thesis/protein_interference/mzid_to_csv.py

Step 6: Compare proteins against the reference file
Finally, compare the identified proteins against a reference file, such as the Higginbotham.csv file, using the compare.py script:
/thesis/protein_interference/compare.py

## Conclusion
By following this workflow, you can effectively analyze and infer proteins from MS-based data. It involves converting mztab files to idXML files, using PeptideIndexer to refresh target/decoy information, and conducting statistical analyses using PIA.



