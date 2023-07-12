#!/usr/bin/env python3

from rdkit import Chem 
import random
import re
import itertools
import datetime
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import string
root = Tk()
root.withdraw()

bb = list()
shorts = list()

# Set default file path
default_file_path = "aminoacids.txt"

# Open the file dialog
file_path = askopenfilename(initialdir=default_file_path, title="choose building block file", filetypes=[("Text files", "*.txt")])
#get buildin blocks
if not file_path:
    file_path = default_file_path

    

with open(file_path, 'r') as file:
    file_lines = file.readlines()
    for line in file_lines:
        line = line.strip("\n").split(": ")
        mol = Chem.MolFromSmiles(line[1])
        if mol != None:
            bb.append(line[1])
            shorts.append(line[0])




#declare calculation-methods
original = str()
sequences = set()


#choose sequence type
t = "linear" #"linear" and "cyclic" are the two options
original = "NQCGPRHKDE" #enter ID sequence

def split_string_at_capitals(string):
    # Use regular expression to split the string at each capital letter
    split_string = re.findall('[A-Z][^A-Z]*', string)
    return split_string

# Example usage

original = split_string_at_capitals(original)


#calculate smiles
sequence = ""
for ind in original:

    index = shorts.index(ind)
    sequence += bb[index]

if t == "cyclic":

    sequence = sequence[:1] + "9" + sequence[1:-4] + "9" + sequence[-4:]

else:
    sequence += "O"

sequences.add(sequence)

#create sequences with 1 difference
for x in itertools.product(shorts, repeat=1):
    for y in itertools.combinations(range(len(original)), 1):
        count = sum(1 for a, b in zip(list(x), [original[y[0]]]) if a != b) 
        if count == 1:
            temp_len = len(sequences)
            mutation = original[:y[0]] + [x[0]] + original[y[0] + 1:]
            sequence = ""

            for ind in mutation:

                index = shorts.index(ind)
                sequence += bb[index]

            if t == "cyclic":

                sequence = sequence[:1] + "9" + sequence[1:-4] + "9" + sequence[-4:]

            else:
                sequence += "O"

            sequences.add(sequence)
            
            
#create sequences with 2 differences
for x in itertools.product(shorts, repeat=2):
    for y in itertools.combinations(range(len(original)), 2):
        if list(x) != [original[y[0]], original[y[1]]]:
            temp_len = len(sequences)
            mutation = original[:y[0]] + [x[0]] + original[y[0] + 1:y[1]] + [x[1]] + original[y[1] + 1:]
            sequence = ""

            for ind in mutation:

                index = shorts.index(ind)
                sequence += bb[index]

            if t == "cyclic":

                sequence = sequence[:1] + "9" + sequence[1:-4] + "9" + sequence[-4:]

            else:
                sequence += "O"
            
            sequences.add(sequence)

            
y = datetime.datetime.now()
date = str(y.year) + str(y.strftime("%m")) + str(y.strftime("%d"))

def generate_random_id():
    letters = string.ascii_lowercase
    random_id = ''.join(random.choice(letters) for _ in range(5))
    return random_id

# Generate a random ID
random_id = generate_random_id()

#create textfile
with open(f'samples/{date}_close_sample_{t}_{len(original)}_{random_id}.txt', 'w') as file:
    for line in sequences:
        file.write(str(line) + "\n")
    file.close()