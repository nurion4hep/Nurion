import h5py

import numpy as np
import sys
import argparse
parser = argparse.ArgumentParser()

parser.add_argument('path', type=str,
            help="import filepath")

args = parser.parse_args()




data = h5py.File(args.path)
print(data['all_events'].keys())
weights = data['all_events']['weight'][:]
print(weights)


images = data['all_events']['hist'][:]
images_em = data['all_events']['histEM'][:]
images_track = data['all_events']['histtrack'][:]
images_track_pt = data['all_events']['histtrackPt'][:]
labels = data['all_events']['y'][:]
labels=labels.flatten()


# Initial weights (Fake)
Norm_sig = 827.71
Norm_QCD700 =  4.05068540e+08
Norm_QCD1000 = 69654980.
Norm_QCD1500 = 6313517.2
Norm_QCD2000 = 1289317.5

Lumi = 63670
xsecRPV     = 0.013
xsecQCD700  = 6362
xsecQCD1000 = 1094
xsecQCD1500 = 99.16
xsecQCD2000 = 20.25

# Gen evts
GenRPV     = 330599
GenQCD700  = 129223
GenQCD1000 = 103319
GenQCD1500 = 127344
GenQCD2000 = 125664

# weight = xsec * lumi / Gen evts
w_Signal  = xsecRPV * Lumi / GenQCD700
w_QCD700  = xsecQCD700 * Lumi / GenQCD700
w_QCD1000 = xsecQCD1000 * Lumi / GenQCD1000
w_QCD1500 = xsecQCD1500 * Lumi / GenQCD1500
w_QCD2000 = xsecQCD2000 * Lumi / GenQCD2000

print('## Signal ##')
print("Initial_RPV_weight: ",Norm_sig)
dim_sig=weights[np.where(weights[:]==Norm_sig)].shape
weights[np.where(weights[:]==Norm_sig)]=np.ones(dim_sig)*w_Signal
print(weights[weights==w_Signal].shape)

print("## QCD 700-1000 ##")
print("Initial_QCD700_weight: ",Norm_QCD700)
dim_QCD700 = weights[np.where(np.around(weights[:],decimals=1)==Norm_QCD700)].shape
weights[np.where(np.around(weights[:],decimals=1) == np.around(Norm_QCD700,decimals=1))] = np.ones(dim_QCD700)*w_QCD700
print(weights[weights==w_QCD700].shape)

print("## QCD 1000-1500 ##")
print("Initial_QCD1000_weight: ",Norm_QCD1000)
dim_QCD1000 = weights[np.where(np.around(weights[:],decimals=1)==Norm_QCD1000)].shape
weights[np.where(np.around(weights[:],decimals=1) == np.around(Norm_QCD1000,decimals=1))] = np.ones(dim_QCD1000)*w_QCD1000
print(weights[weights==w_QCD1000].shape)

print("## QCD 1500-2000 ##")
print("Initial_QCD_1500_weight: ",Norm_QCD1500)
dim_QCD1500 = weights[np.where(np.around(weights[:],decimals=1)==Norm_QCD1500)].shape
weights[np.where(np.around(weights[:],decimals=1) == np.around(Norm_QCD1500,decimals=1))] = np.ones(dim_QCD1500)*w_QCD1500
print(weights[weights==w_QCD1500].shape)

print("## QCD 2000-Inf ##")
print("Initial_QCD_2000_weight: ",Norm_QCD2000)
dim_QCD2000 = weights[np.where(np.around(weights[:],decimals=1)==Norm_QCD2000)].shape
weights[np.where(np.around(weights[:],decimals=3) == np.around(Norm_QCD2000,decimals=3))] = np.ones(dim_QCD2000)*w_QCD2000
print(weights[weights==w_QCD2000].shape)

print(" ############# END Normnalize ################## " )
print(" ############# Validate Normnalize ################## " )
print(weights.shape[0])
print(weights[weights==w_Signal].shape[0] + weights[weights==w_QCD700].shape[0] + weights[weights==w_QCD1000].shape[0] + weights[weights==w_QCD1500].shape[0] + weights[weights==w_QCD2000].shape[0] )


print('BKG number: ',images[labels==0].shape)
print('SIG number: ',images[labels==1].shape)

### ---- M A K E   P L O T -------------------

import matplotlib
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm

matplotlib.rcParams.update({'font.size': 20})


def plot_image(image,name="BKG.png"):
	'''
	Args:
	-----
	    image: ndarray with energies collected by each calo cell
	    vmin: float, min energy to clip at
	    vmax: float, max energy to clip at
	'''
	fig = plt.figure(figsize=(10,10))
	im = plt.imshow(image,
	           interpolation='nearest',
	           #norm=LogNorm(vmin, vmax)
	)
	cbar = plt.colorbar(fraction=0.0455)
	cbar.set_label(r'Energy (MeV)', y=0.83)
	cbar.ax.tick_params()   
	plt.ylabel(r'$\eta$ Cell ID')
	plt.xlabel(r'$\phi$ Cell ID')
	plt.tight_layout()
	plt.savefig(name)
	return im


plot_image((weights.reshape(-1, 1, 1)*images)[labels==0].mean(axis=0),"noPU_HCAL_BKG.png")
plot_image((weights.reshape(-1, 1, 1)*images)[labels==1].mean(axis=0),"noPU_HCAL_SIG.png")
plot_image((weights.reshape(-1, 1, 1)*images_em)[labels==0].mean(axis=0),"noPU_ECAL_BKG.png")
plot_image((weights.reshape(-1, 1, 1)*images_em)[labels==1].mean(axis=0),"noPU_ECAL_SIG.png")
plot_image((weights.reshape(-1, 1, 1)*images_track)[labels==0].mean(axis=0),"noPU_Track_BKG.png")
plot_image((weights.reshape(-1, 1, 1)*images_track)[labels==1].mean(axis=0),"noPU_Track_SIG.png")
plot_image((weights.reshape(-1, 1, 1)*images_track_pt)[labels==0].mean(axis=0),"noPU_TrackPT_BKG.png")
plot_image((weights.reshape(-1, 1, 1)*images_track_pt)[labels==1].mean(axis=0),"noPU_TrackPT_SIG.png")








