# Sequence Generator

## Purpose
After creating a list of SMILES sequences, the list undergoes two calculation files before being converted into an HTML file showing the result as a TMAP

## Environment
In order to use the python file without problems, please create a conda environment using the file environment_1.yml which contain the necessary installations

## Samples
Unless you already have a SMILES sample, you can start with either "sample_generator.py" or "close_sequences.py". The first file is used for random sequences, while the other creates sequences that are close to a sequence of your choice. 

If you choose sample_generator.py, use the text file "bb.txt". It contains a list of SMILES building blocks. You can create your own building blocks if you wish (only SMILES that can be read by MOL will be used)

If you choose "close_sequences.py" use the text file "aminoacids.txt". It contains a list of capital letters representing the natural amino acids and the corresponding SMILES building blocks. As before, you can create your own building blocks if you wish (if necessary, you can add small letters to the capital letters. "Al" and "Ad" would then be read as two different building block shorts)

## Map4/descriptor generator
After creating your sample, the text file must undergo certain calculations. Starting with Map4, which is a molecular fingerprint (map4_generator.py). The calculated data will be saved as a pickled file in the "samples_map4" folder. That pickled file can then be used for the descriptor generator in order to calculate several aspects of the sequences. The data is then once again pickled but in the "map4_plus_descriptors" folder. 

## Tamp generator
For using the last python script (tmap_generator.py) the final step the pickled file from the directory "map4_plus_descriptors" is then used to create a tmap. The tmap is then converted into an HTML file that can be opened locally. 

Depending on how many sequences the pickled file contains, the structure of the tmap may need to be adjusted. The numbers in the lines from 53 to 56 can be changed in order to show more compatible results to a certain file.