import h5py
import pandas as pd
import numpy as np


## Train data
print("###### train data #######")
train_data=h5py.File("train.h5")
print(list(train_data.keys()))
images = train_data['all_events']['hist'][:]
labels = train_data['all_events']['y'][:]

print("N bkg: ",images[labels==0].shape[0])
print("N signal: ",images[labels==1].shape[0])
print(" ")
print(" ")


## Validation data
print("###### validation data #######")
val_data=h5py.File("val.h5")
print(list(train_data.keys()))
images = val_data['all_events']['hist'][:]
labels = val_data['all_events']['y'][:]

print("N bkg: ",images[labels==0].shape[0])
print("N signal: ",images[labels==1].shape[0])


