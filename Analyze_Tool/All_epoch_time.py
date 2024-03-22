import pandas as pd
import numpy as np


dir_64   = '/scratch/x1797a07/Lastrun/HEP-CNN/run/AfterPM/KMPBLOCKTIME_1__SELECT_64__MPIPROC_64__THREADS_64__BATCH_512/history_0.csv'
dir_128  = '/scratch/x1797a07/Lastrun/HEP-CNN/run/AfterPM/KMPBLOCKTIME_1__SELECT_128__MPIPROC_128__THREADS_64__BATCH_256/history_0.csv'
dir_256  = '/scratch/x1797a07/Lastrun/HEP-CNN/run/AfterPM/KMPBLOCKTIME_1__SELECT_256__MPIPROC_256__THREADS_64__BATCH_128/history_0.csv'
dir_512  = '/scratch/x1797a07/Lastrun/HEP-CNN/run/AfterPM/KMPBLOCKTIME_1__SELECT_512__MPIPROC_512__THREADS_64__BATCH_64/history_0.csv'
dir_1024 = '/scratch/x1797a07/Lastrun/HEP-CNN/run/AfterPM/KMPBLOCKTIME_1__SELECT_1024__MPIPROC_1024__THREADS_64__BATCH_32/history_0.csv'
dir_2048 = '/scratch/x1797a07/Lastrun/HEP-CNN/run/AfterPM/KMPBLOCKTIME_1__SELECT_2048__MPIPROC_2048__THREADS_64__BATCH_16/history_0.csv'
dir_4096 = '/scratch/x1797a07/Lastrun/HEP-CNN/run/perf_nurion_KNL_torch_4096/KMPBLOCKTIME_1__SELECT_4096__MPIPROC_4096__THREADS_64__BATCH_8/history_0.csv'

data64_df   = pd.read_csv(dir_64)
data128_df  = pd.read_csv(dir_128)
data256_df  = pd.read_csv(dir_256)
data512_df  = pd.read_csv(dir_512)
data1024_df = pd.read_csv(dir_1024)
data2048_df = pd.read_csv(dir_2048)
data4096_df = pd.read_csv(dir_4096)



time=[]
time.append(data64_df['time'][:].sum(axis=0))
time.append(data128_df['time'][:].sum(axis=0))
time.append(data256_df['time'][:].sum(axis=0))
time.append(data512_df['time'][:].sum(axis=0))
time.append(data1024_df['time'][:].sum(axis=0))
time.append(data2048_df['time'][:].sum(axis=0))
time.append(data4096_df['time'][:].sum(axis=0))

print(data64_df['time'][:].shape[0])
print(data128_df['time'][:].shape[0])
print(data256_df['time'][:].shape[0])
print(data512_df['time'][:].shape[0])
print(data1024_df['time'][:].shape[0])
print(data2048_df['time'][:].shape[0])
print(data4096_df['time'][:].shape[0])

print("Elapsed time ####")
for t in time:
	print(t)
import argparse
import matplotlib
import matplotlib.pyplot as plt



parser = argparse.ArgumentParser()
parser.add_argument('target', type=str,
            help="python epoch.py acc(loss)")
args = parser.parse_args()



target = args.target
x = np.arange(len(data512_df['time']))
x_4096 = np.arange(len(data4096_df['time']))

train_label_name = "Train-set "+target
val_label_name   = "Validation-set "+target
title ="epoch vs "+target
val_title='epoch vs val_'+target
filename=target+'.png'


plt.rc('xtick',labelsize=30)
plt.rc('ytick',labelsize=30)



fig,axs = plt.subplots(2,1,figsize=(20,20))
axs[0].plot(x+1,data64_df[target],'--bo',color='r',label=train_label_name)
axs[0].plot(x+1,data128_df[target],'--bo',color='g',label=train_label_name)
axs[0].plot(x+1,data256_df[target],'--bo',color='b',label=train_label_name)
axs[0].plot(x+1,data512_df[target],'--bo',color='darkorange',label=train_label_name)
axs[0].plot(x+1,data1024_df[target],'--bo',color='gold',label=train_label_name)
axs[0].plot(x+1,data2048_df[target],'--bo',color='purple',label=train_label_name)
axs[0].plot(x_4096+1,data4096_df[target],'--bo',color='cyan',label=train_label_name)
axs[0].legend(['64node','128node','256node','512node','1024node','2048node','4096node'],prop={'size' :30})
#axs[0].legend(['64node','1024node','2048node','4096node'],prop={'size' :30})

############################## Log
if(target == "loss"):
	axs[0].set_yscale('log')

axs[0].set_title(title,fontsize=50)
axs[0].set_xlabel('epoch',fontsize=45)
axs[0].set_ylabel(target,fontsize=45)

axs[1].get_xaxis().get_major_formatter().set_useOffset(False)
axs[1].get_yaxis().get_major_formatter().set_useOffset(False)
axs[1].plot(x+1,data64_df['val_'+target],'--bo',color='r',label=val_label_name)
axs[1].plot(x+1,data128_df['val_'+target],'--bo',color='g',label=val_label_name)
axs[1].plot(x+1,data256_df['val_'+target],'--bo',color='b',label=val_label_name)
axs[1].plot(x+1,data512_df['val_'+target],'--bo',color='darkorange',label=val_label_name)
axs[1].plot(x+1,data1024_df['val_'+target],'--bo',color='gold',label=val_label_name)
axs[1].plot(x+1,data2048_df['val_'+target],'--bo',color='purple',label=val_label_name)
axs[1].plot(x_4096+1,data4096_df['val_'+target],'--bo',color='cyan',label=val_label_name)

############################## Log

if(target == "loss"):
	axs[1].set_yscale('log')

axs[1].set_title(val_title,fontsize=50)
axs[1].set_xlabel('epoch',fontsize=45)
axs[1].set_ylabel(target,fontsize=45)

axs[0].grid()
axs[1].grid()

fig.tight_layout()
plt.savefig(filename)
plt.show()
