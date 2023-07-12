#!/usr/bin/env python3

from rdkit import Chem 
from rdkit.Chem import Descriptors
from tqdm import tqdm 
from map4 import MAP4Calculator
import numpy as np
import pandas as pd
from tqdm import tqdm 
import os
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import sys

root = Tk()
root.withdraw()
#set up lists and calculation methods
df = pd.DataFrame()
tqdm.pandas()
map4 = MAP4Calculator()


#map4 calculation method
def calc_map4(f, fname):

    #declare dataframe and list
    df = pd.DataFrame()
    smiles = list()
    
    #load sequence smaples
    with open(f, 'r') as file:
        file_lines = file.readlines()
        for line in tqdm(file_lines):
            line = line.strip()
            mol = Chem.MolFromSmiles(line)
            if mol != None:
                smiles.append(line)               
        file.close()

    #set sequence in dataframe
    df['SMILES'] = smiles
    #claculate MOL
    df['MOL'] = df['SMILES'].progress_apply(Chem.MolFromSmiles)
    #calculate Molecular weight
    df['MW'] = df['MOL'].progress_apply(Descriptors.ExactMolWt)
    #calculate map4
    df['MAP4'] = df['MOL'].progress_apply(map4.calculate)
    df['MAP4'] = df['MAP4'].progress_apply(lambda x: np.array(x))

    #save dataframe
    fname = fname.strip(".txt")
    df.to_pickle(f"samples_map4s/{fname}.pkl")
 

#choose file
file_path = askopenfilename(title="choose samples", filetypes=[("text files", "*.txt")])


if not file_path:
    
    sys.exit("no file chosen")
    

#choose textfile 
filename = file_path.split("/")[-1]

#call map4 calculation method
calc_map4(file_path, filename)
