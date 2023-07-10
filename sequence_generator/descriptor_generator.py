#!/usr/bin/env python3

from rdkit import Chem 
from rdkit.Chem import rdMolDescriptors
from rdkit.Chem import DataStructs
from rdkit.Chem import Descriptors
from tqdm import tqdm 
import numpy as np
import pandas as pd
from tqdm import tqdm 
import os
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import sys

root = Tk()
root.withdraw()
#set up tqdm, Dataframes and Arrays
tqdm.pandas()
temp = list()
df = pd.DataFrame()


#NumAromatic calculation method
def NumAromatic(mol):
    smarts = Chem.MolFromSmarts('[a]')
    return len(mol.GetSubstructMatches(smarts, uniquify=True))

#count number of carbon atoms method
def NumCarbons(smiles):
    count = 0
    

    for c in smiles:
        if (c == "c"):
            count += 1
        
        elif  (c == "C"):
            count += 1

    return count



#descriptor calculation methods
def calc_descriptors(f, fname):
    

    #load dataframe from file
    df = pd.read_pickle(f)

    #calculate descriptors
    df['NumAromatic'] = df['MOL'].progress_apply(NumAromatic)
    df['Carbons'] = df['SMILES'].progress_apply(NumCarbons)
    df['Heavyatoms'] = df['MOL'].progress_apply(rdMolDescriptors.CalcNumHeavyAtoms)
    df['cLogP'] = df['MOL'].progress_apply(Descriptors.MolLogP)
    df['fCsp3'] = df['MOL'].progress_apply(rdMolDescriptors.CalcFractionCSP3)
    df['TPSA'] = df['MOL'].progress_apply(rdMolDescriptors.CalcTPSA)
    df['Rotatable'] = df['MOL'].progress_apply(rdMolDescriptors.CalcNumRotatableBonds)
    df['Rings'] = df['MOL'].progress_apply(rdMolDescriptors.CalcNumRings)
    df['AromaticRings'] = df['MOL'].progress_apply(rdMolDescriptors.CalcNumAromaticRings)
    df['AliphaticRings'] = df['MOL'].progress_apply(rdMolDescriptors.CalcNumAliphaticRings)
    df['H_bond_donners'] = df['MOL'].progress_apply(rdMolDescriptors.CalcNumLipinskiHBD)
    df['H_bond_acceptors'] = df['MOL'].progress_apply(rdMolDescriptors.CalcNumHBA)
    df['valence_electron'] = df['MOL'].progress_apply(Descriptors.NumValenceElectrons)
    df['Heteroatoms'] = df['MOL'].progress_apply(rdMolDescriptors.CalcNumHeteroatoms)

    

    #save calculations to file
    df.to_pickle(f"map4_plus_descriptors/{fname}")
    
#choose file
file_path = askopenfilename(title="choose samples", filetypes=[("pickled files", "*.pkl")])


if not file_path:
    
    sys.exit("no file chosen")
    

filename = file_path.split("/")[-1:]





#call descriptors calculation method
calc_descriptors(file_path, filename)
