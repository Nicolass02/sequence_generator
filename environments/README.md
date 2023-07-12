# Conda installation
Because the files need somne specifik installations it is recommended to use conda to set up the right environments without affecting the other systems on your computer. 

Please install Conda from the official websites and makes sure to install a version that's compatible with your device (the linux version wont work for windows). 

After that you can simply use the following comand code to install the environment: 
```
conda env create -f environment_1.yml
```

After the environment is completely set up you can activate the conda environment with following comand: 

```
conda activate pyenv
```

After that you should be able to use the python files in the other directory without problems.