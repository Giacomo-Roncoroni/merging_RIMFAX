from os import listdir
from tqdm import tqdm
import numpy as np
import pds4_tools
import sys
import os
# deactivate warning
import warnings
warnings.filterwarnings("ignore")

#################################################
############### User input ######################
#################################################
# define path
# path with raw data
data_path = 'pds-geosciences.wustl.edu/m2020/urn-nasa-pds-mars2020_rimfax/data_calibrated/2022/'
# path to save data
data_save = 'data_ok/'
# True if save format is numpy, False for binary
npy_fmt   = True
#################################################
#################################################
#################################################

#################################################
# Need to mkdir data_save in that folder, just a check
try:
    os.stat(data_save)
except:
    os.mkdir(data_save)
#################################################

#################################################
#init matrix variable for three modes
data_surface = np.zeros((0, 16384))
data_shallow = np.zeros((0, 16384))
data_deep    = np.zeros((0, 16384))
#save also lat, lon and elevation of the rover
lat = np.zeros((0))
lon = np.zeros((0))
elev = np.zeros((0))

#################################################


#################################################
####
##### works only if pds4_tools.__version__=='0.71'
####
# check if pds4_tools.__version__=='0.71'
if pds4_tools.__version__== '0.71':
	print('Correct pds4_tools version: it should work!')
	# find all the files in current folder with '.xml' extension --> only files with header infos
	onlyfiles = [data_path + f for f in listdir(data_path) if f[-4: ] == '.xml']
	# init days according to number of files
	day = np.zeros((len(onlyfiles), 2))
	#k is just for days index
	k = 0
	# for each a [tqdm is just for progress bar]
	for name in tqdm(onlyfiles):
		# if filename has the correct extension
		if name[:-4] != '.xml':
			# read data structure with pds4_tools [no print]
			struct_2B = pds4_tools.pds4_read(name)
			# latitude
			la  = struct_2B.structures[0][27]
			# longitude
			lo  = struct_2B.structures[0][28]
			# elevation
			el  = struct_2B.structures[0][29]
			# data matrix
			data_2B  = struct_2B.structures[0][90]
			# check where the header is:
			## struct_2B.structures[0][55] == Identifier of RIMFAX configuration mode: [Surface, Shallow or Deep]
			## struct_2B.structures[0][57] == Indicates measured signal is: 0 = from the Antenna, 1 = from the Calibration Cable, 2 = alternating between Antenna and Calibration Cable (
			## struct_2B.structures[0][2] == Type of table record: 0 = Active Sounding Measurement, 1 = Passive Radiometry Measurement, 5 = Housekeeping Measurement, 8 = Calibration Array
			## struct_2B.structures[0][58] == Indicates measurement is part of a: 0 = Traverse/Mobile set, 1 = Stationary set
			idx_surf = np.where((struct_2B.structures[0][55] == "Surface")  & (struct_2B.structures[0][57]==0) & (struct_2B.structures[0][2]==0) & (struct_2B.structures[0][58]==0))[0]
			idx_shal = np.where((struct_2B.structures[0][55] == "Shallow") & (struct_2B.structures[0][57]==0) & (struct_2B.structures[0][2]==0) & (struct_2B.structures[0][58]==0))[0]
			idx_deep = np.where((struct_2B.structures[0][55] == "Deep")     & (struct_2B.structures[0][57]==0) & (struct_2B.structures[0][2]==0) & (struct_2B.structures[0][58]==0))[0]
			# save day number, i.e. SOL and length in the merged profile. 
			day[k, 0] =  int(name[-9:-4]) 
			day[k, 1] =  idx_surf.shape[0]
			# append and create matrix
			if idx_surf.shape == idx_shal.shape and idx_surf.shape == idx_deep.shape:
				lat = np.append(lat, la[idx_surf])
				lon = np.append(lon, lo[idx_surf])
				elev = np.append(elev, el[idx_surf])
				data_surface = np.append(data_surface, data_2B[idx_surf, :], axis=0)
				data_shallow = np.append(data_shallow, data_2B[idx_shal, :], axis=0)
				data_deep = np.append(data_deep, data_2B[idx_deep, :], axis=0)
				k += 1
else:
	sys.exit('Wrong pds4_tools version installed!\nExpected: 0.71, but found: ' + pds4_tools.__version__)

#################################################
# save day, elevation and coordinates
np.save(data_save + 'day',        day)					
np.save(data_save + 'longitude',  lon)					
np.save(data_save + 'latitude',   lat)					
np.save(data_save + 'elevation', elev)
#################################################


#################################################
# normalize to 1. 
data_surface = data_surface/np.max(np.abs(data_surface))
data_shallow = data_shallow/np.max(np.abs(data_shallow))
data_deep = data_deep/np.max(np.abs(data_deep))
#################################################


#################################################
# save data
if npy_fmt == False:
    np.save(data_save + 'data_surface', data_surface)
    np.save(data_save + 'data_shallow', data_shallow)
    np.save(data_save + 'data_deep', data_deep)
else: 
    data_surface.astype('float32').tofile(data_save + 'data_surface' + '_float32')
    data_shallow.astype('float32').tofile(data_save + 'data_shallow' + '_float32')
    data_deep.astype('float32').tofile(data_save + 'data_deep' + '_float32')