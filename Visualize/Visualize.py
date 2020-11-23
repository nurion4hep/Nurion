import h5py
from tqdm import tqdm
import numpy as np
import glob 


print("## >> Grep All images \n")

### ---Parameters
isQCD=False
isNorm=True
nEvent = 6

Lumi= 138 * 1000

xsecRPV = 0.0252977
genRPV = 330599

xsecQCD1000 = 1207
genQCD1000 = 15466225.

xsecQCD1500 = 119.9
genQCD1500 = 3368613.

xsecQCD2000 = 25.24
genQCD2000 = 3250016.

if isNorm:
	weightQCD1000 = xsecQCD1000 * Lumi / genQCD1000
	weightQCD1500 = xsecQCD1500 * Lumi / genQCD1500
	weightQCD2000 = xsecQCD2000 * Lumi / genQCD2000
	weightRPV = xsecRPV * Lumi / genRPV
else:
	weightQCD1000,weightQCD1500,weightQCD2000,weightRPV = 1,1,1,1


weight_dict ={
'weightQCD1000_key':weightQCD1000,
'weightQCD1500_key':weightQCD1500,
'weightQCD2000_key':weightQCD2000
}
 


### ---File input
if isQCD:
	QCD_list=['QCD_HT1000','QCD_HT1500','QCD_HT2000']
	QCD_Full_path_arr=[]
	for qcd in QCD_list:
		path_name = qcd + "/*.h5"
		QCD_Full_path_arr.append(glob.glob(path_name))

	nEvent = int(nEvent / 3)
	QCD1000_path,QCD1500_path,QCD2000_path = QCD_Full_path_arr[0][:nEvent],QCD_Full_path_arr[1][:nEvent],QCD_Full_path_arr[2][:nEvent]
	Full_path = QCD1000_path + QCD1500_path +QCD2000_path
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
	for path,weight_key in zip([QCD1000_path,QCD1500_path,QCD2000_path],['weightQCD1000_key','weightQCD1500_key','weightQCD2000_key']):
		for f in tqdm(path):
			data = h5py.File(f,'r')
			weight_arr = np.ones(data['all_events']['HCAL'].shape) * weight_dict[weight_key]
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

print(images_HCAL.shape)
print(images_ECAL.shape)
print(images_TRACK.shape)


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
#plot_image((weights.reshape(-1, 1, 1)*images_track_pt)[labels==1].mean(axis=0),"noPU_TrackPT_SIG.png")
