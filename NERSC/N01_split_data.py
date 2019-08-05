import h5py
import numpy as np
import pandas as pd

## Set Path data path
path_="/xrootd/store/user/hnam/sample4Nurion/RPV/"
path="/hcp/data/data02/jwkim2/WORK/Nurion/preprocess/"

## Read data
Sig_data=h5py.File(path_+"data.h5")
BKG_data=h5py.File(path+'QCD.h5')

## Set # of  data
N_signal = 10000
N_BKG=10000


print(list(Sig_data['all_events'].keys()))
print
#['hist', 'histEM', 'histtrack', 'passSR', 'passSR4J', 'passSR5J', 'weight']


## Read HDF5 branches as numpy array
sig_hist			= Sig_data['all_events']['hist'][:N_signal]
sig_histEM			= Sig_data['all_events']['histEM'][:N_signal]
sig_histtrack		= Sig_data['all_events']['histtrack'][:N_signal]
sig_passSR			= Sig_data['all_events']['passSR'][:N_signal]
sig_passSR4J		= Sig_data['all_events']['passSR4J'][:N_signal]
sig_weight			= Sig_data['all_events']['weight'][:N_signal]

bkg_hist			= BKG_data['all_events']['hist'][:N_BKG]
bkg_histEM			= BKG_data['all_events']['histEM'][:N_BKG]
bkg_histtrack		= BKG_data['all_events']['histtrack'][:N_BKG]
bkg_passSR			= BKG_data['all_events']['passSR'][:N_BKG]
bkg_passSR4J		= BKG_data['all_events']['passSR4J'][:N_BKG]
bkg_weight			= BKG_data['all_events']['weight'][:N_BKG]

# show results
print("sig hist: ",sig_hist.shape)
print("bkg hist: ",bkg_hist.shape)
print("----------------------------")
print("sig histEM: ",sig_histEM.shape)
print("bkg histEM: ",bkg_histEM.shape)
print("----------------------------")
print("sig histtrak: ",sig_histtrack.shape)
print("bkg histtrak: ",bkg_histtrack.shape)
print("----------------------------")
print("sig passSR: ",sig_passSR.shape)
print("bkg passSR: ",bkg_passSR.shape)
print("----------------------------")
print("sig passSR4J: ",sig_passSR4J.shape)
print("bkg passSR4J: ",bkg_passSR4J.shape)
print("----------------------------")
print("sig weight: ",sig_weight.shape)
print("bkg weight: ",bkg_weight.shape)

# Number of all data
Nall = N_signal + N_BKG

## Make Label(y) array: 0 for background 1 for signal
isSig = np.ones([N_signal,1])
isBKG = np.zeros([N_BKG,1])


#### Virtual table
hist		= np.concatenate([sig_hist,bkg_hist],axis=0)
histEM		= np.concatenate([sig_histEM,bkg_histEM],axis=0)
histtrack	= np.concatenate([sig_histtrack,bkg_histtrack],axis=0)
passSR		= np.concatenate([sig_passSR,bkg_passSR],axis=0)
passSR4J	= np.concatenate([sig_passSR4J,bkg_passSR4J],axis=0)
weights		= np.concatenate([sig_weight,bkg_weight],axis=0)
Y = np.concatenate([isSig,isBKG],axis=0)
####

## Add signal and background and shuffle! 
# Make random indices
shuffled_indices = np.random.permutation(Nall)
val_size		= int(Nall*0.3)
val_indices		= shuffled_indices[:val_size]
train_indices	= shuffled_indices[val_size:]

# Indexing
val_hist		= hist[val_indices]
train_hist		= hist[train_indices]
val_histEM		= histEM[val_indices]
train_histEM	= histEM[train_indices]
val_histtrack		= histtrack[val_indices]
train_histtrack		= histtrack[train_indices]
val_passSR			= passSR[val_indices]
train_passSR		= passSR[train_indices]
val_passSR4J		= passSR4J[val_indices]
train_passSR4J		= passSR4J[train_indices]
val_weights		=  weights[val_indices]
train_weights	=  weights[train_indices]
val_Y	=	Y[val_indices]
train_Y	=	Y[train_indices]


print("### Train and validation split results ###")
print("### hist ###")
print(val_hist.shape)
print(train_hist.shape)
print("### histEM ###")
print(val_histEM.shape)
print(train_histEM.shape)
print("### histtrack ###")
print(val_histtrack.shape) 
print(train_histtrack.shape)
print("### passSR ###")
print(val_passSR.shape)
print(train_passSR.shape)
print("### passSR4J ###")
print(val_passSR4J.shape)
print(train_passSR4J.shape)
print("### weight ###")
print(val_weights.shape)
print(train_weights.shape)
print("### Label ###")
print(val_Y.shape)
print(train_Y.shape)


#['hist', 'histEM', 'histtrack', 'passSR', 'passSR4J', 'passSR5J', 'weight']



print("### Converting HDF5 files...")

with h5py.File("train.h5","w") as f:
	g=f.create_group("all_events")
	g.create_dataset("hist",      data=train_hist,chunks=True,compression='gzip', compression_opts=9) 
	g.create_dataset("histEM",    data=train_histEM,chunks=True,compression='gzip', compression_opts=9) 
	g.create_dataset("histtrack", data=train_histtrack,chunks=True,compression='gzip', compression_opts=9) 
	g.create_dataset("passSR",	  data=train_passSR,chunks=True,compression='gzip', compression_opts=9) 
	g.create_dataset("passSR4J",  data=train_passSR4J,chunks=True,compression='gzip', compression_opts=9) 
	g.create_dataset("weights",   data=train_weights,chunks=True)
	g.create_dataset("y",   data=train_Y,chunks=True)

with h5py.File("val.h5","w") as f:
	g=f.create_group("all_events")
	g.create_dataset("hist",      data=val_hist,chunks=True,compression='gzip', compression_opts=9) 
	g.create_dataset("histEM",    data=val_histEM,chunks=True,compression='gzip', compression_opts=9) 
	g.create_dataset("histtrack", data=val_histtrack,chunks=True,compression='gzip', compression_opts=9) 
	g.create_dataset("passSR",	  data=val_passSR,chunks=True,compression='gzip', compression_opts=9) 
	g.create_dataset("passSR4J",  data=val_passSR4J,chunks=True,compression='gzip', compression_opts=9) 
	g.create_dataset("weights",   data=val_weights,chunks=True)
	g.create_dataset("y",   data=val_Y,chunks=True)



print("### Successfully saved!")


