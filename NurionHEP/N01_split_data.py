import h5py
import numpy as np
import pandas as pd

#for 2016 data
#path="/xrootd/store/user/hnam/sample4Nurion/Sample_0814/raw/"

#for more 2018 data
#path="/xrootd/store/user/hnam/sample4Nurion/2018DAS/Delphes/h5/"

# original path
path_="/xrootd_user/hknam/xrootd/sample4Nurion/2018DAS/Delphes/h5/"

# more evts
path="/xrootd_user/hknam/xrootd/sample4Nurion/2018DAS/Delphes/h5_v2/"


data_700HT  = "QCD700to1000.h5"
data_1000HT = "QCD1000to1500.h5"
data_1500HT = "QCD1500to2000.h5"
data_2000HT = "QCD2000toInf.h5"

BKG700HT_data = h5py.File(path_+data_700HT)
BKG1000HT_data = h5py.File(path+data_1000HT)
BKG1500HT_data = h5py.File(path+data_1500HT)
BKG2000HT_data = h5py.File(path+data_2000HT)
Sig_data=h5py.File(path_+"RPV1400.h5")


N_sig=-1


print(list(Sig_data['all_events'].keys()))
#['hist', 'histEM', 'histtrack', 'passSR', 'passSR4J', 'passSR5J', 'weight']


sig_hist			= Sig_data['all_events']['hist'][:N_sig]
sig_histEM			= Sig_data['all_events']['histEM'][:N_sig]
sig_histtrack		= Sig_data['all_events']['histtrack'][:N_sig]
sig_passSR			= Sig_data['all_events']['passSR'][:N_sig]
sig_passSR4J		= Sig_data['all_events']['passSR4J'][:N_sig]
sig_passSR5J		= Sig_data['all_events']['passSR5J'][:N_sig]
sig_weight			= Sig_data['all_events']['weight'][:N_sig]
print(" ")
print("Signal number: ",sig_hist.shape[0])
print("Signal weight: ",sig_weight[0])

bkg700HT_hist			= BKG700HT_data['all_events']['hist'][:]
bkg700HT_histEM			= BKG700HT_data['all_events']['histEM'][:]
bkg700HT_histtrack		= BKG700HT_data['all_events']['histtrack'][:]
bkg700HT_passSR			= BKG700HT_data['all_events']['passSR'][:]
bkg700HT_passSR4J		= BKG700HT_data['all_events']['passSR4J'][:]
bkg700HT_passSR5J		= BKG700HT_data['all_events']['passSR5J'][:]
bkg700HT_weight			= BKG700HT_data['all_events']['weight'][:]
print(" ")
print("bkg 700-1000HT number: ",bkg700HT_hist.shape[0])
print("bkg 700-1000HT weight: ",bkg700HT_weight[0])

bkg1000HT_hist				= BKG1000HT_data['all_events']['hist'][:]
bkg1000HT_histEM			= BKG1000HT_data['all_events']['histEM'][:]
bkg1000HT_histtrack			= BKG1000HT_data['all_events']['histtrack'][:]
bkg1000HT_passSR			= BKG1000HT_data['all_events']['passSR'][:]
bkg1000HT_passSR4J			= BKG1000HT_data['all_events']['passSR4J'][:]
bkg1000HT_passSR5J			= BKG1000HT_data['all_events']['passSR5J'][:]
bkg1000HT_weight			= BKG1000HT_data['all_events']['weight'][:]
print(" ")
print("bkg 1000-1500HT number: ",bkg1000HT_hist.shape[0])
print("bkg 1000-1500HT weight: ",bkg1000HT_weight[0])

bkg1500HT_hist				= BKG1500HT_data['all_events']['hist'][:]
bkg1500HT_histEM			= BKG1500HT_data['all_events']['histEM'][:]
bkg1500HT_histtrack			= BKG1500HT_data['all_events']['histtrack'][:]
bkg1500HT_passSR			= BKG1500HT_data['all_events']['passSR'][:]
bkg1500HT_passSR4J			= BKG1500HT_data['all_events']['passSR4J'][:]
bkg1500HT_passSR5J			= BKG1500HT_data['all_events']['passSR5J'][:]
bkg1500HT_weight			= BKG1500HT_data['all_events']['weight'][:]
print(" ")
print("bkg 1500-2000HT number: ",bkg1500HT_hist.shape[0])
print("bkg 1500-2000HT weight: ",bkg1500HT_weight[0])

bkg2000HT_hist				= BKG2000HT_data['all_events']['hist'][:]
bkg2000HT_histEM			= BKG2000HT_data['all_events']['histEM'][:]
bkg2000HT_histtrack			= BKG2000HT_data['all_events']['histtrack'][:]
bkg2000HT_passSR			= BKG2000HT_data['all_events']['passSR'][:]
bkg2000HT_passSR4J			= BKG2000HT_data['all_events']['passSR4J'][:]
bkg2000HT_passSR5J			= BKG2000HT_data['all_events']['passSR5J'][:]
bkg2000HT_weight			= BKG2000HT_data['all_events']['weight'][:]

N_signal = sig_hist.shape[0]
N_bkg	 = bkg700HT_hist.shape[0]+bkg1000HT_hist.shape[0]+bkg1500HT_hist.shape[0]+bkg2000HT_hist.shape[0]
Nall	 = N_signal + N_bkg
print(" ")
print("bkg 2000-infHT number: ",bkg2000HT_hist.shape[0])
print("bkg 2000-infHT weight: ",bkg2000HT_weight[0])
print(" ")
print(" ### Num Summary ### ")
print("Signal: ", N_signal)
print("BKG: ", N_bkg)

''' 



print(" ")
print("### Branch summary ###")
print("sig hist: ",sig_hist.shape)
print("bkg hist: ",bkg700HT_hist.shape)
print("----------------------------")
print("sig histEM: ",sig_histEM.shape)
print("bkg histEM: ",bkg700HT_histEM.shape)
print("----------------------------")
print("sig histtrak: ",sig_histtrack.shape)
print("bkg histtrak: ",bkg700HT_histtrack.shape)
print("----------------------------")
print("sig passSR: ",sig_passSR.shape)
print("bkg passSR: ",bkg700HT_passSR.shape)
print("----------------------------")
print("sig passSR4J: ",sig_passSR4J.shape)
print("bkg passSR4J: ",bkg700HT_passSR4J.shape)
print("----------------------------")
print("sig passSR5J: ",sig_passSR5J.shape)
print("bkg passSR5J: ",bkg700HT_passSR5J.shape)
print("----------------------------")
print("sig weight: ",sig_weight.shape)
print("bkg weight: ",bkg700HT_weight.shape)


isSig = np.ones([N_signal,1])
isBKG = np.zeros([N_bkg,1])

print(" ")
print(" ### Merging data..")
#### Virtual table
hist		= np.concatenate([sig_hist,bkg700HT_hist,bkg1000HT_hist,bkg1500HT_hist,bkg2000HT_hist],axis=0)
histEM		= np.concatenate([sig_histEM,bkg700HT_histEM,bkg1000HT_histEM,bkg1500HT_histEM,bkg2000HT_histEM],axis=0)
histtrack	= np.concatenate([sig_histtrack,bkg700HT_histtrack,bkg1000HT_histtrack,bkg1500HT_histtrack,bkg2000HT_histtrack],axis=0)
passSR		= np.concatenate([sig_passSR,bkg700HT_passSR,bkg1000HT_passSR,bkg1500HT_passSR,bkg2000HT_passSR],axis=0)
passSR4J	= np.concatenate([sig_passSR4J,bkg700HT_passSR4J,bkg1000HT_passSR4J,bkg1500HT_passSR4J,bkg2000HT_passSR4J],axis=0)
passSR5J	= np.concatenate([sig_passSR5J,bkg700HT_passSR5J,bkg1000HT_passSR5J,bkg1500HT_passSR5J,bkg2000HT_passSR5J],axis=0)
weights		= np.concatenate([sig_weight,bkg700HT_weight,bkg1000HT_weight,bkg1500HT_weight,bkg2000HT_weight],axis=0)
Y = np.concatenate([isSig,isBKG],axis=0)
####

print(" ")
print(" ### Spliting data..")
shuffled_indices = np.random.permutation(Nall)
val_size		= int(Nall*0.3)
val_indices		= shuffled_indices[:val_size]
train_indices	= shuffled_indices[val_size:]

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

val_passSR5J		= passSR5J[val_indices]
train_passSR5J		= passSR5J[train_indices]

val_weights		=  weights[val_indices]
train_weights	=  weights[train_indices]

val_Y	=	Y[val_indices]
train_Y	=	Y[train_indices]


print(" ")
print("### Train and validation split results ###")
print("### hist ###")
print(train_hist.shape)
print(val_hist.shape)
print("### histEM ###")
print(train_histEM.shape)
print(val_histEM.shape)
print("### histtrack ###")
print(train_histtrack.shape)
print(val_histtrack.shape) 
print("### passSR ###")
print(train_passSR.shape)
print(val_passSR.shape)
print("### passSR4J ###")
print(train_passSR4J.shape)
print(val_passSR4J.shape)
print("### passSR5J ###")
print(train_passSR5J.shape)
print(val_passSR5J.shape)
print("### weight ###")
print(train_weights.shape)
print(val_weights.shape)
print("### Label ###")
print(train_Y.shape)
print(val_Y.shape)


print("### Converting HDF5 files...")

with h5py.File("train.h5","w") as f:
	g=f.create_group("all_events")
	g.create_dataset("hist",      data=train_hist,chunks=True,compression='gzip', compression_opts=9) 
	g.create_dataset("histEM",    data=train_histEM,chunks=True,compression='gzip', compression_opts=9) 
	g.create_dataset("histtrack", data=train_histtrack,chunks=True,compression='gzip', compression_opts=9) 
	g.create_dataset("passSR",	  data=train_passSR,chunks=True,compression='gzip', compression_opts=9) 
	g.create_dataset("passSR4J",  data=train_passSR4J,chunks=True,compression='gzip', compression_opts=9) 
	g.create_dataset("passSR45",  data=train_passSR5J,chunks=True,compression='gzip', compression_opts=9) 
	g.create_dataset("weight",   data=train_weights,chunks=True)
	g.create_dataset("y",   data=train_Y,chunks=True)

with h5py.File("val.h5","w") as f:
	g=f.create_group("all_events")
	g.create_dataset("hist",      data=val_hist,chunks=True,compression='gzip', compression_opts=9) 
	g.create_dataset("histEM",    data=val_histEM,chunks=True,compression='gzip', compression_opts=9) 
	g.create_dataset("histtrack", data=val_histtrack,chunks=True,compression='gzip', compression_opts=9) 
	g.create_dataset("passSR",	  data=val_passSR,chunks=True,compression='gzip', compression_opts=9) 
	g.create_dataset("passSR4J",  data=val_passSR4J,chunks=True,compression='gzip', compression_opts=9) 
	g.create_dataset("passSR5J",  data=val_passSR5J,chunks=True,compression='gzip', compression_opts=9) 
	g.create_dataset("weight",   data=val_weights,chunks=True)
	g.create_dataset("y",   data=val_Y,chunks=True)



print("### Successfully saved!")

'''

