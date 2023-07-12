# Sequence Generator

## First step 
If you haven't installed your environment yet it would be recommended to do it now (folder "environment" outside of this directory) as the files are most likly not going to work otherwise. Else feal free to proceed. 


## Samples
### sample_generator.py
Unless you already have a SMILES sample, you can start with either "sample_generator.py" or "close_sequences.py". The first file is used for random sequences, while the other creates sequences that are close to a sequence of your choice. 

If you choose sample_generator.py, use the text file "bb.txt". It contains a list with custom SMILES building blocks. Here is a example:
```
N(CC1=CC(Cl)=CC(Cl)=C1)CC(=O)
N(CC1=CC=C(O)C=C1)CC(=O)
N(CCC(C)(C))CC(=O)
N(CC1=CC=C(C)C=C1)CC(=O)
N(C(C)C1=CC=C(C)C=C1)CC(=O)
```

You can also create your own building blocks if you wish but bear in mind taht only SMILES that can be read by MOL will be used the others will be ignored. Please note that it is recommended to construct the building blocks with "(=O)" and that they do not contain the number 9 as it would otherwise prevent the code from working if you chosse to make "cyclic sequences" (for the option "cyclic" see further below).

On the lines 43 to 45 of the file "sample_generator.py" you can change the values depending what kind of result you wish for. On line 43 you determin how many sequences you will have in your text file. Line 44 decides how many building blocks each sequence is made of. Last but not least, choosing between "linear" and "cyclic" decides if the sequence has a beginning and an end like a straight line or if the end of the sequence ends up attached to the beginning ending up forming somthing like a circle.

At the end the file will be saved in the "samples" directory. The name will contain numbers representing the date it was created as well as other information based on what kind of choices you made as well as a 5 letter ID in order to prevent the files getting deleted and rewriten (that would happen if the files had the exact same names).

### close_sequences.py
If you choose "close_sequences.py" use the text file "aminoacids.txt". It contains a list of SMILES building blocks just like the file "bb.txt" however each building block now has an ID in form of a capital letter. This is due to the fact that this python file will create sequences resembling one you determin yourself (see more details further below). 

Here is an example:
```
W: N[C@@H](CC1=CNC2=C1C=CC=C2)C(=O)
S: N[C@@H](CO)C(=O)
T: N[C@@H](C(C)O)C(=O)
N: N[C@@H](CC(N)=O)C(=O)
```

As before, you can create your own building blocks if you wish. If you need more building blocks then there are letters, you can add small letters to the capital letters. "Al" and "Ad" would then be read as two different building block IDs

Here is an example:
```
Ad: N[C@@H](CC1=CNC2=C1C=CC=C2)C(=O)
Al: N[C@@H](CO)C(=O)
T: N[C@@H](C(C)O)C(=O)
N: N[C@@H](CC(N)=O)C(=O)
```
Using this file you will set an standart sequence (more details how todo it further below) which as a result will generate a list of sequences that contain the original as well as all sequences with 1 and 2 differneces to the original (how many that ends up to be allways depends and is not set beforhand)

Please note that it is recommended to construct the building blocks with "(=O)" and that they do not contain the number 9 as it would otherwise prevent the code from working if you chosse to make "cyclic sequences" (for the option "cyclic" see further below). Also make sure that the original sequence ,matches the IDs in the list you selected as it would not work otherwise.

On the lines 46 and 47 of the file "close_sequences.py" you can change the values depending what kind of result you wish for. Line 46 decides how many building blocks each sequence is made of. Last but not least, choosing between "linear" and "cyclic" decides if the sequence has a beginning and an end like a straight line or if the end of the sequence ends up attached to the beginning ending up forming somthing like a circle. As for line 47 determins what the original sequence will be.

At the end the file will be saved in the "samples" directory. The name will contain numbers representing the date it was created as well as other information based on what kind of choices you made as well as a 5 letter ID in order to prevent the files getting deleted and rewriten (that would happen if the files had the exact same names).

## Map4/descriptor generator
After creating your sample, the text file must undergo certain calculations. Starting with Map4, which is a molecular fingerprint (map4_generator.py). The calculated data will be saved as a pickled file in the "samples_map4" folder. That pickled file can then be used for the descriptor generator in order to calculate several aspects of the sequences. The data is then once again pickled but in the "map4_plus_descriptors" folder. 

Other then choosing the files from the right folder there is nothing you need to do other than wait that the calculation are finished.

## Tamp generator
For using the last python script (tmap_generator.ipynb) the final step the pickled file from the directory "map4_plus_descriptors" is then used to create a tmap. The tmap is then converted into an HTML file that can be opened locally. 

Depending on how many sequences the pickled file contains, the structure of the tmap may need to be adjusted. The numbers in the lines from 53 to 56 can be changed in order to show more compatible results to a certain file.

Due to some circumstances the script could only be used inside a jupyter notbook file. It is recommended to use Visual Studio Code to execute taht file. If you do please install the extensions for Jupyter Notebook and Python to prevent any problem. Also make sure that the kernel in which you run the code is the conda environment that was previously set up.