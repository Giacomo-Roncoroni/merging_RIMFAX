# Data generation program

Activate the environment, you will need: 

  1. pds4_tools
  2. numpy
  3. tqdm
  
Set the current data path where you have saved data, the path where you want to save the data and npy_fmt variable at the beginning of 2B_stacked.py and run: 

      python 2B_stacked.py

If npy_fmt==True, it will save data_surface, data_shallow, data_deep in npy format, if npy_fmt==False it will same as binary float32.
