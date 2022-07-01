from os import listdir
from tqdm import tqdm
import numpy as np
import pds4_tools
import sys
import os
# deactivate warning
import warnings
warnings.filterwarnings("ignore")
####

##### works only if pds4_tools.__version__=='0.71'
####
data_path = 'data/'
data_save = 'data_ok/'
npy_fmt   = True

# run the program in the folder before folder data. Need to mkdir data in that folder
try:
    os.stat(data_save)
except:
    os.mkdir(data_save)

data_surface = np.zeros((0, 16384))
data_shallow = np.zeros((0, 16384))
data_deep    = np.zeros((0, 16384))
lat = np.zeros((0))
lon = np.zeros((0))
elev = np.zeros((0))

# check if pds4_tools.__version__=='0.71'
if pds4_tools.__version__== '0.71':
	print('Correct pds4_tools version: it should work!')
	# find all the files in current folder with 'L' at the end --> only files with header infos
	onlyfiles = ['data/' + f for f in listdir('data/') if f[-4: ] == '.xml']
	day = np.zeros((len(onlyfiles), 2))
	# for each a [tqdm is just for progress bar]
	k = 0
	for name in tqdm(onlyfiles):
		# if filename has the correct number and is the LPR-2B version of the data
		if name[:-4] != '.xml':
			# read data structure with pds4_tools [no print]
			struct_2B = pds4_tools.pds4_read(name)
			la  = struct_2B.structures[0][27]
			lo  = struct_2B.structures[0][28]
			el  = struct_2B.structures[0][29]
			data_2B  = struct_2B.structures[0][90]
			data_2B = data_2B/np.max(np.abs(data_2B))
			idx_surf = np.where((struct_2B.structures[0][55] == "Surface")  & (struct_2B.structures[0][57]==0) & (struct_2B.structures[0][2]==0) & (struct_2B.structures[0][58]==0))[0]
			idx_shal = np.where((struct_2B.structures[0][55] == "Shallow") & (struct_2B.structures[0][57]==0) & (struct_2B.structures[0][2]==0) & (struct_2B.structures[0][58]==0))[0]
			idx_deep = np.where((struct_2B.structures[0][55] == "Deep")     & (struct_2B.structures[0][57]==0) & (struct_2B.structures[0][2]==0) & (struct_2B.structures[0][58]==0))[0]
			day[k, 0] =  int(name[-9:-4]) 
			day[k, 1] =  idx_surf.shape[0]
			lat = np.append(lat, la[idx_surf])
			lon = np.append(lon, lo[idx_surf])
			elev = np.append(elev, el[idx_surf])
			data_surface = np.append(data_surface, data_2B[idx_surf, :], axis=0)
			data_shallow = np.append(data_shallow, data_2B[idx_shal, :], axis=0)
			data_deep = np.append(data_deep, data_2B[idx_deep, :], axis=0)
			k += 1
else:
	sys.exit('Wrong pds4_tools version installed!\nExpected: 0.71, but found: ' + pds4_tools.__version__)

np.save(data_save + 'day',        day)					
np.save(data_save + 'longitude',  lon)					
np.save(data_save + 'latitude',   lat)					
np.save(data_save + 'elevation', elev)					

# normalazi to 1. 
data_surface = data_surface/np.max(np.abs(data_surface))
data_shallow = data_shallow/np.max(np.abs(data_shallow))
data_deep = data_deep/np.max(np.abs(data_deep))


if npy_fmt == False:
    np.save(data_save + 'data_surface', data_surface)
    np.save(data_save + 'data_shallow', data_shallow)
    np.save(data_save + 'data_deep', data_deep)
else: 
    data_surface.astype('float32').tofile(data_save + 'data_surface' + '_float32')
    data_shallow.astype('float32').tofile(data_save + 'data_shallow' + '_float32')
    data_deep.astype('float32').tofile(data_save + 'data_deep' + '_float32')
