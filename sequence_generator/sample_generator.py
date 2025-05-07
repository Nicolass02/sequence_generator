
#!/usr/bin/env python3
import random
from rdkit import Chem 
import datetime
import string
from tkinter import Tk
from tkinter.filedialog import askopenfilename
# Create the Tkinter root window
root = Tk()
root.withdraw()

bb = list()

# Create the Tkinter root window
root = Tk()
root.withdraw()

# Set default file path
default_file_path = "bb.txt"

# Open the file dialog
file_path = askopenfilename(initialdir=default_file_path, title="choose building block file (SMILES format)", filetypes=[("Text files", "*.txt")])
#get buildin blocks
if not file_path:
    file_path = default_file_path

#load building blocks
with open(file_path, 'r') as file: 
    file_lines = file.readlines()
    for line in file_lines:
        mol = Chem.MolFromSmiles(line)
        if mol != None:
            bb.append(line.strip())
    file.close()



sample = set()


# Generate sample with size and length of choice
list_size = 1000 #recommended not to go over 50'000
seq_len = 10 #never smaller than 2
type = "linear" #"linear" and "cyclic" are the two options

#create samples
while len(sample) < list_size:

    #create sequence
    sequence = ""
    for x in range(seq_len):
        sequence += str(random.choice(bb))

    #alter sequence depending which type is set
    if type == 'linear':
        sample.add(sequence + 'O')
    elif type == 'cyclic':
        sample.add(sequence[:1] + '9' + sequence[1:-4] + '9' + sequence[-4:])

sample = list(sample)

#get date
y = datetime.datetime.now()
date = str(y.year) + str(y.strftime("%m")) + str(y.strftime("%d"))

def generate_random_id():
    letters = string.ascii_lowercase
    random_id = ''.join(random.choice(letters) for _ in range(5))
    return random_id

# Generate a random ID
random_id = generate_random_id()

#create textfile
with open(f'samples/{date}_sample_{type}_{seq_len}_{random_id}.txt', 'w') as file:
    for line in sample:
        file.write(str(line) + "\n")
    file.close()


