# merging_RIMFAX
Repository with code and data for merging RIMFAX data (mars2020 mission)

- Abstract

The integration of GPR data at various frequencies, collected with different antennas or with the use of swept-frequency radars opens up interesting perspectives in the study of the subsurface at different resolutions. The proposed methodology is a semi-supervised DL algorithm based on Bi-Directional Long-Short Term Memory to automatically merge varying numbers of data sets at different frequencies. Neural Network training is done directly on the inference data by minimizing a custom loss function based on the L2 norm of all the input data, weighted on the custom merging area and the single output trace. The inference of the trained Neural Network is applied to the same data. The proposed algorithm is tested on synthetic data simulating the Mars conditions and on RIMFAX radar data collected in the Jezero crater during the Mars 2020 mission of Perseverance rover, showing successful performances and robustness. 
