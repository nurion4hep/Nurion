import h5py
from tqdm import tqdm
import numpy as np
import glob 


print("## >> Grep All images \n")

### ---Parameters
isQCD=True
isNorm=False
nEvent = 3

Lumi= 138 * 1000

xsecRPV = 0.0252977
genRPV = 330599

xsecQCD1000 = 1207
genQCD1000 = 15466225.


if isNorm:
	weightQCD1000 = xsecQCD1000 * Lumi / genQCD1000
	weightRPV = xsecRPV * Lumi / genRPV
else:
	weightRPV,weightRPV = 1,1


weight_dict ={
'weightQCD1000_key':weightQCD1000,
}
 


### ---File input
if isQCD:
	QCD1000_path = glob.glob("") ## Type path here
	QCD_Full_path = QCD1000_path 
	outname='QCD'
else:
	Full_path = glob.glob("RPV/RPV*.h5")[:nEvent]
	outname='RPV'

### ---Read and concat images
print("## >> Start Processing theses files...")
for p in Full_path:
	print(p)	



print(" ")
arr_HCAL=[]
arr_ECAL=[]
arr_TRACK=[]


if isQCD:
	for f in tqdm(QCD_Full_path):
		data = h5py.File(f,'r')
		weight_arr = np.ones(data['all_events']['HCAL'].shape) * weight_dict['weightQCD1000_key']
		arr_HCAL.append(data['all_events']['HCAL'][:]*weight_arr)
		arr_ECAL.append(data['all_events']['ECAL'][:]*weight_arr)
		arr_TRACK.append(data['all_events']['TRACK'][:]*weight_arr)
		data.close()
		
else:
	for f in tqdm(Full_path):
		data = h5py.File(f,'r')
		weight_arr = np.ones(data['all_events']['HCAL'].shape) * weightRPV
		arr_HCAL.append(data['all_events']['HCAL'][:]*weight_arr)
		arr_ECAL.append(data['all_events']['ECAL'][:]*weight_arr)
		arr_TRACK.append(data['all_events']['TRACK'][:]*weight_arr)
		data.close()
	
images_HCAL  = np.concatenate(tuple(arr_HCAL),axis=0)
images_ECAL  = np.concatenate(tuple(arr_ECAL),axis=0)
images_TRACK = np.concatenate(tuple(arr_TRACK),axis=0)



HCAL  = np.expand_dims(images_HCAL,-1)
ECAL  = np.expand_dims(images_ECAL,-1)
TRACK = np.expand_dims(images_TRACK,-1)
images = np.concatenate([HCAL,ECAL,TRACK],axis=-1)

print(images_HCAL.shape)
print(images_ECAL.shape)
print(images_TRACK.shape)
print(images.shape)


### ---- M A K E   P L O T -------------------
print("## >> Make plots...")

import matplotlib
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm

matplotlib.rcParams.update({'font.size': 20})


def plot_image(image,name="RPV.png"):
	

	fig = plt.figure(figsize=(10,10))
	im = plt.imshow(image,
	interpolation='nearest',
	)
	cbar = plt.colorbar(fraction=0.0455)
	cbar.set_label(r'Energy (MeV)', y=0.83)
	cbar.ax.tick_params()   
	plt.ylabel(r'$\eta$ Cell ID')
	plt.xlabel(r'$\phi$ Cell ID')
	plt.tight_layout()
	plt.savefig(name)
	return im

HCAL_name  = outname + "_HCAL.png"
ECAL_name  = outname + "_ECAL.png"
TRACK_name = outname + "_TRACK.png"


plot_image(images_HCAL.mean(axis=0),HCAL_name)
plot_image(images_ECAL.mean(axis=0),ECAL_name)
plot_image(images_TRACK.mean(axis=0),TRACK_name)
