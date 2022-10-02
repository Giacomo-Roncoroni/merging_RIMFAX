# Merging gated Frequency-Modulated Continuous-Wave Mars2020 RIMFAX GPR data
G. Roncoroni, E. Forte, M. Pipan

Department of Mathematics and Geosciences, University of Trieste, Italy

Submitted

# Abstract

The integration of GPR data at various frequencies, collected with different antennas or with the use of swept-frequency radars opens up interesting perspectives in the study of the subsurface at different resolutions. The proposed methodology is a semi-supervised DL algorithm based on Bi-Directional Long-Short Term Memory to automatically merge varying numbers of data sets at different frequencies. Neural Network training is done directly on the inference data by minimizing a custom loss function based on the L2 norm of all the input data, weighted on the custom merging area and the single output trace. The inference of the trained Neural Network is applied to the same data. The proposed algorithm is tested on synthetic data simulating the Mars conditions and on RIMFAX radar data collected in the Jezero crater during the Mars 2020 mission of Perseverance rover, showing successful performances and robustness. 

# Data download 

Data are open access and can be efficiently downloaded from a Ubuntu terminal with the comand:

     wget -A xml,csv -m -p -E -k -K -np -nc  https://pds-geosciences.wustl.edu/m2020/urn-nasa-pds-mars2020_rimfax/data_calibrated/2021/

# Data reading and Sorting 

Data are read using pds4_tools package by python: python script has been tested only with a version <= 0.71 which can be downloaded from https://pdssbn.astro.umd.edu/toolsrc/readpds_python/0.71/ You can find the zipped version in this repository. 
Python version has to be 3.x < 3.8. If a wrong version of python, i.e. Python > 3.9, it raises the error: 

      AttributeError: 'ElementTree' object has no attribute 'getiterator'

Please downgrade python. 
In 00_data_gen folder you can find the script. 

# Data merging

See the notebook that describes the procedure
