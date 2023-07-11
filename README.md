# Sequence Generator
The purpose of the sequence generator is to generate a list of SMILES sequences that, after being processed, are used to create a TMAP in an HTML file (the example placed in the folder sequence_generator/tmaps can be locally opened on your browser). Using a list of SMILES molecular structures as building blocks, a list of combinations is created and saved into a text file. Here are some examples for SMILES sequences: 
- N(CC1=CC(Cl)=CC(Cl)=C1)CC(=O)
- N(CC1=CC=C(O)C=C1)CC(=O)
- N(CCC(C)(C))CC(=O)
- N(CC1=CC=C(C)C=C1)CC(=O)
- N(C(C)C1=CC=C(C)C=C1)CC(=O)

After creating a list with combination of the SMILES building blocks (example: 
N(CC1=CC=C(O)C=C1)CC(=O)N(CC1=CC(Cl)=CC(Cl)=C1)CC(=O)N(CC1=CC=C(C)C=C1)CC(=O)) said list will process in order to calculate a molecular fingerprint for each sequence as well as calculating several descriptors. 

The molecular fingerprint "MAP4" is basically an array of numbers which will later be of use in order to categorise the sequences when creating the tmap.

The descriptors on the other hand are used in order to define different aspects of the sequence such as Molecular weight, Number of Carbon atoms and several more. Then, depending on which descriptor you wish to see, you will have different colour distribution.

At the end the processed file can be used to create a TMAP wich is converted into an HTML file. That file can be opened on a local browser anytime.


# Folder "environments"
The folder "environments" contains conda installation environments in order to use the python files without problems, as well as another README file with further instructions how to do the installations.

# Folder "sequence_generator"
In the folder "sequence_generator" are the python files, as well as another README file with further instructions how to use them.