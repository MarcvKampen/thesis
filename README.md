# Marc van Kampen's Masterthesis Repository
Welcome to the repository of Marc van Kampen regarding his master thesis.

## About
In this repository, you will find all the code used to reanalyze a spectral dataset using an optimized open modification search (OMS) engine: ANN-SoLo. Utilizing this OMS resulted in acquired post-translational modifications grouped in co-expressed modules and by disease stage.

## Resources
ANN-SoLo: https://github.com/bittremieux/ANN-SoLo
Higgintbotham et al:
  The paper: https://pubmed.ncbi.nlm.nih.gov/31461916/
  The spectral dataset: https://www.ebi.ac.uk/pride/archive/projects/PXD014376
OpenMS: https://openms.de/install/
Protein Inference Algorithm (PIA): https://github.com/mpc-bioinformatics/pia

## Workflow
1. Prepare ANN-SoLo (install/convert .raw file to .mgf/prepare spectral library, etc.), see ANN-SoLo wiki: https://github.com/bittremieux/ANN-SoLo/wiki
2. Run ANN-SoLo

3. Convert .mztab to .csv and map the modifications using /thesis/modifications_mapping/1_mztab_to_csv.py
4. Extract the post-translational modifications using /thesis/modifications_mapping/2_modifications_filter.py

5. Convert .mztab to idxml using /thesis/protein_interference/mztab_to_idXML.py
6. Use PeptideIndexer from OpenMS to refresh target/decoy information and mapping of the peptides.
7. Use the Protein Inference Algorithm (PIA) to convert .idXML to .xml
8. Use PIA to identify the proteins of a partial peptide sequence. Hereby, use the .JSON file: /thesis/protein_interference/UWA.JSON
9. Convert the .mzid file derived from step 8 to a CSV using: /thesis/protein_interference/mzid_to_csv.py
10. Match your protein IDs from step 9 with the protein IDs from Higginbotham (/thesis/protein_interference/Higginbotham.csv) via the Python script /thesis/protein_interference/compare.py.

11. Match the post-translational modifications from step 4 with the protein interference output from step 10 using: /thesis/combine_prev_steps/1_match_mod_map_w_prot_i.py
12. Add the disease stages using: /thesis/combine_prev_steps/2_add_study_group.py

This workflow results in a CSV file, containing among others: the unique protein ID, the modification, disease stage, the module, etc.

## Conclusion
This repository provides an efficient and reliable approach to re-analyse spectral data sets using open-source tools. Feel free to explore the code and datasets to gain insights into the analysis process.




  
 
  





