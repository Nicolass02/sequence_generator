#!/usr/bin/env python3

from tqdm import tqdm 

import tmap as tm

import numpy as np

from faerun import Faerun

import pandas as pd

import os
import webbrowser
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import sys



tqdm.pandas()


#choose file
file_path = askopenfilename(title="choose samples", filetypes=[("pickled files", "*.pkl")])


if not file_path:
    
    sys.exit("no file chosen")
    

filename = file_path.split("/")[-1:]


#choose pickeled file
df = pd.read_pickle(file_path)
df = df.drop_duplicates(subset=['SMILES'], ignore_index=True)

#calculate tmap setups
lf = tm.LSHForest(1024, 64)
ap = np.array(df['MAP4'].values.tolist())
fps = []

for i in ap:
    vec = tm.VectorUint(i)
    fps.append(vec)
    

lf.batch_add(fps)
lf.index()
cfg = tm.LayoutConfiguration() #configuration parameters for tmap layout
cfg.node_size = 1 / 30 #size of nodes which affects the magnitude of their repelling force. Decreasing this values generally resolves overlaps in a very crowded tree
cfg.mmm_repeats = 2 #number of repeats of the per-level layout algorithm
cfg.sl_extra_scaling_steps = 5 #sets the number of repeats of the scaling
cfg.k = 15 #number of nearest neighbours used to create the k-nearest neighbour graph
cfg.sl_scaling_type = tm.RelativeToAvgLength #Defines the relative scale of the graph
x, y, s, t, _ = tm.layout_from_lsh_forest(lf, cfg)


f = Faerun(
    view="front",
    coords=False,
    title="combined_tmap"
)

#set descriptor data
descriptors = ['NumAromatic', 'fCsp3', 'cLogP', 'TPSA', 'Carbons', 'Heavyatoms', 'Rotatable', 'Rings', 'AromaticRings', 'AliphaticRings', 'H_bond_donners', 'H_bond_acceptors', 'valence_electron', 'Heteroatoms']
colors = ['rainbow', 'rainbow', 'rainbow', 'rainbow', 'rainbow', 'rainbow', 'rainbow', 'rainbow', 'rainbow', 'rainbow', 'rainbow', 'rainbow', 'rainbow', 'rainbow']
cat = [False, False, False, False, False, False, False, False, False, False, False, False, False, False]
needl = [None, None, None, None, None, None, None, None, None, None, None, None, None, None] 
sername = ['NumAromatic', 'fCsp3', 'cLogP', 'TPSA', 'Carbon Atoms', 'Heavyatoms', 'Rotatable Atoms', 'Rings', 'Aromatic Rings', 'Aliphatic Rings', 'Hydrogen bond donners', 'Hydrogen bond acceptors', 'valence electron', 'Heteroatoms']


values = list()
need_labels = list()
categories = list()
set_colors = list()
series_name = list()

#add Molecular weight data
values.insert(len(values), df['MW'].values.tolist())
set_colors.insert(len(set_colors), 'rainbow')
categories.insert(len(categories), False)
need_labels.insert(len(need_labels), None)
series_name.insert(len(series_name), "MW")

#add descriptors if present in the dataframe
for id, desname in enumerate(descriptors):

    values.insert(len(values), df[desname].values.tolist())
    set_colors.insert(len(set_colors), colors[id])
    categories.insert(len(categories), cat[id])
    need_labels.insert(len(need_labels), needl[id])
    series_name.insert(len(series_name), sername[id])


    
#crate tmap
f.add_scatter(
    "TITLE",
    {
        "x": x,
        "y": y,
        "c": values,
        "labels": df['SMILES'].values.tolist(),
    },
    shader="sphere",
    point_scale=1,
    max_point_size=20,
    legend_labels=need_labels,
    categorical=categories,
    colormap=set_colors,
    series_title=series_name,
    has_legend=True,
)
f.add_tree("TITLE_tree", {"from": s, "to": t}, point_helper="TITLE")

#choose filename
filename = str(filename).strip(".pkl")

#convert tmap to html file
f.plot(f"tmaps/{filename}", template='smiles')

webbrowser.open('file://' + os.path.realpath(f"tmaps/{filename}.html"))