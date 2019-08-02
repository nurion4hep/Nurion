import h5py
import numpy as np
import pandas as pd

path_="/xrootd/store/user/hnam/sample4Nurion/RPV/"


# N_sig=96914

N_signal = 10000
N_BKG=10000


Sig_data=h5py.File(path_+"data.h5")
BKG_data=h5py.File('QCD.h5')


print(list(Sig_data['all_events'].keys()))
#['hist', 'histEM', 'histtrack', 'passSR', 'passSR4J', 'passSR5J', 'weight']


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


Nall = N_signal + N_BKG
arr=np.arange(Nall)
arr=arr.reshape(-1,1)


isSig = np.ones([N_siganl,1])
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


shuffled_indices = np.random.permutation(Nall)
val_size		= int(Nall*0.3)
val_indices		= shuffled_indices[:val_size]
train_indices	= shuffled_indices[val_szie:]







print(df)
print(df.shape)



#print(hist.shape)
#print(histEM.shape)
#print(histtrack.shape)



#column=["hist","histEM","histtrack","passSR","passSR4J","weight"]
#row=[arr,arr,arr,passSR,passSR4J,weights]
#df = pd.Dataframe(






#weights = data['all_events']['weight'][:nb_train_events]
#weights = np.log(weights+1)




#print(images.shape)
#print(weights.shape)

