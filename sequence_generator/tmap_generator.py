#!/usr/bin/env python3

from tqdm import tqdm 

import tmap as tm
import jinja2
import numpy as np
import copy
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

#altered code from faerun
def plot(
    self,
    file_name: str = "index",
    path: str = "./",
    template: str = "default",
    notebook_height: int = 500,):
    """Plots the data to an HTML / JS file.

    Keyword Arguments:
        file_name (:obj:`str`, optional): The name of the HTML / JS file
        path (:obj:`str`, optional): The path to which to write the HTML / JS file
        template (:obj:`str`, optional): The name or path of the template to use
        notebook_height: (:obj`int`, optional): The height of the plot when displayed in a jupyter notebook
    """
    self.notebook_height = notebook_height

    script_path = os.path.dirname(os.path.abspath(__file__))
    if template in ["default", "reaction_smiles", "smiles", "url_image"]:
        template = "template_" + template + ".j2"
    else:
        script_path = os.path.dirname(template)

    html_path = os.path.join(path, file_name + ".html")
    js_path = os.path.join(path, file_name + ".js")
    jenv = jinja2.Environment(loader=jinja2.FileSystemLoader(script_path))

    has_legend = False

    for _, value in self.scatters.items():
        if value["has_legend"]:
            has_legend = True
            break

    if not self.show_legend:
        has_legend = False

    # Drop colormaps before passing them to the document, as they are
    # not JSON serializable.
    trees_copy = copy.deepcopy(self.trees)
    scatters_copy = copy.deepcopy(self.scatters)

    for key, _ in trees_copy.items():
        del trees_copy[key]["colormap"]

    for key, _ in scatters_copy.items():
        del scatters_copy[key]["colormap"]

    model = {
        "title": self.title,
        "file_name": file_name + ".js",
        "clear_color": self.clear_color,
        "view": self.view,
        "coords": str(self.coords).lower(),
        "coords_color": self.coords_color,
        "coords_box": str(self.coords_box).lower(),
        "coords_ticks": str(self.coords_ticks).lower(),
        "coords_grid": str(self.coords_grid).lower(),
        "coords_tick_count": self.coords_tick_count,
        "coords_tick_length": self.coords_tick_length,
        "coords_offset": self.coords_offset,
        "x_title": self.x_title,
        "y_title": self.y_title,
        "tree_helpers": list(trees_copy.values()),
        "point_helpers": list(scatters_copy.values()),
        "has_legend": str(has_legend).lower(),
        "legend_title": self.legend_title,
        "legend_orientation": self.legend_orientation,
        "alpha_blending": str(self.alpha_blending).lower(),
        "anti_aliasing": str(self.anti_aliasing).lower(),
        "style": self.style,
        "impress": self.impress,
        "in_notebook": Faerun.in_notebook(),
        "thumbnail_width": self.thumbnail_width,
        "thumbnail_fixed": str(self.thumbnail_fixed).lower(),
    }

    
    model["data"] = self.create_data()
    

    output_text = jenv.get_template(template).render(model)

    with open(html_path, "w") as result_file:
        result_file.write(output_text)


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
plot(f"tmaps/{filename}", template='smiles')

webbrowser.open('file://' + os.path.realpath(f"tmaps/{filename}.html"))