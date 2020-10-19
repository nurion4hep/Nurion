import pandas as pd
import numpy as np



dir_4    = '../../hepcnn_CPlargekernelnorm0_32PU_224x224_speedup_fixed8batch/SELECT_4_BATCH_8/history_0.csv'
dir_8    = '../../hepcnn_CPlargekernelnorm0_32PU_224x224_speedup_fixed8batch/SELECT_8_BATCH_8/history_0.csv'
dir_16   = '../../hepcnn_CPlargekernelnorm0_32PU_224x224_speedup_fixed8batch/SELECT_16_BATCH_8/history_0.csv'
dir_64   = '../../hepcnn_CPlargekernelnorm0_32PU_224x224_speedup_fixed8batch/SELECT_64_BATCH_8/history_0.csv'
dir_128  = '../../hepcnn_CPlargekernelnorm0_32PU_224x224_speedup_fixed8batch/SELECT_128_BATCH_8/history_0.csv'
dir_256  = '../../hepcnn_CPlargekernelnorm0_32PU_224x224_speedup_fixed8batch/SELECT_256_BATCH_8/history_0.csv'
dir_512  = '../../hepcnn_CPlargekernelnorm0_32PU_224x224_speedup_fixed8batch/SELECT_512_BATCH_8/history_0.csv'
dir_1024 = '../../hepcnn_CPlargekernelnorm0_32PU_224x224_speedup_fixed8batch/SELECT_1024_BATCH_8/history_0.csv'
dir_gpu='/scratch/hpc22a03/HEP-CNN-results/training/224x224_trackpt/model_CPlargekernelnorm0/run__lr_2e-3__batch_64x512__optm_adam/history_0.csv'
EPOCH =50



data4_df    = pd.read_csv(dir_4)
data8_df    = pd.read_csv(dir_8)
data16_df   = pd.read_csv(dir_16)
data64_df   = pd.read_csv(dir_64)
data128_df  = pd.read_csv(dir_128)
data256_df  = pd.read_csv(dir_256)
data512_df  = pd.read_csv(dir_512)
data1024_df = pd.read_csv(dir_1024)
datagpu_df  = pd.read_csv(dir_gpu)



time=[]
time.append(data4_df['time'][:].mean(axis=0))
time.append(data8_df['time'][:].mean(axis=0))
time.append(data16_df['time'][:].mean(axis=0))
time.append(data64_df['time'][:].mean(axis=0))
time.append(data128_df['time'][:].mean(axis=0))
time.append(data256_df['time'][:].mean(axis=0))
time.append(data512_df['time'][:].mean(axis=0))
time.append(data1024_df['time'][:].mean(axis=0))
time.append(datagpu_df['time'][:].mean(axis=0))

print("Elapsed time ####")
for t in time:
	print(t)



accum_time4  = []
accum_time8  = []
accum_time16  = []
accum_time64  = []
accum_time128  = []
accum_time256  = []
accum_time512  = []
accum_time1024  = []
accum_timegpu  = []

accume_timelist = [accum_time4 ,accum_time8 ,accum_time16 ,accum_time64 ,accum_time128,accum_time256,accum_time512,accum_time1024,accum_timegpu]
accume_dir = [data4_df,data8_df,data16_df,data64_df,data128_df,data256_df,data512_df,data1024_df,datagpu_df]





cnt=0
for dir_,time_list in zip(accume_dir,accume_timelist):
	accum_target = dir_

	if cnt < 4:
		for i in range(accum_target.shape[0]+1):
			if i==0:
				continue
			else:
				time_list.append(accum_target['time'][:i].sum())
	
	else:
		for i in range(EPOCH+1):
			if i==0:
				continue
			else:
				time_list.append(accum_target['time'][:i].sum())
	cnt+=1
	


print("START TEST ############# " )
for i in accume_timelist:
	print(len(i))
print("END TEST ############# " )


import argparse
import matplotlib
import matplotlib.pyplot as plt



parser = argparse.ArgumentParser()
parser.add_argument('target', type=str,
            help="python epoch.py acc(loss)")
parser.add_argument('--xtime', type=bool,default=False,
            help="python epoch.py acc(loss) --xtime True/False")
args = parser.parse_args()



target = args.target
x = np.arange(len(data128_df['time']))
x_gpu  = np.arange(len(datagpu_df['time']))

train_label_name = "Train-set "+target
val_label_name   = "Validation-set "+target
title ="epoch vs "+target
val_title='epoch vs val_'+target
filename=target+'.png'


plt.rc('xtick',labelsize=30)
plt.rc('ytick',labelsize=30)

if not args.xtime:

	fig,axs = plt.subplots(2,1,figsize=(20,20))
	axs[0].plot(x+1,data4_df[target],'--bo',color='r',label=train_label_name)
	axs[0].plot(x+1,data8_df[target],'--bo',color='g',label=train_label_name)
	axs[0].plot(x+1,data16_df[target],'--bo',color='b',label=train_label_name)
	axs[0].plot(x+1,data64_df[target],'--bo',color='orange',label=train_label_name)
	axs[0].plot(x+1,data128_df[target],'--bo',color='yellow',label=train_label_name)
	axs[0].plot(x+1,data256_df[target],'--bo',color='lime',label=train_label_name)
	axs[0].plot(x+1,data512_df[target],'--bo',color='teal',label=train_label_name)
	axs[0].plot(x+1,data1024_df[target],'--bo',color='cyan',label=train_label_name)
	axs[0].plot(x_gpu+1,datagpu_df[target],'--bo',color='magenta',label=train_label_name)
	axs[0].legend(['4nodes','8nodes','16nodes','64nodes','128nodes','256nodes','512nodes','1024nodes','gpu'],prop={'size' :30})
	
	############################## Log
	if(target == "loss"):
		axs[0].set_yscale('log')
	
	axs[0].set_title(title,fontsize=50)
	axs[0].set_xlabel('epoch',fontsize=45)
	axs[0].set_ylabel(target,fontsize=45)
	
	axs[1].get_xaxis().get_major_formatter().set_useOffset(False)
	axs[1].get_yaxis().get_major_formatter().set_useOffset(False)
	axs[1].plot(x+1,data4_df['val_'+target],'--bo',color='r',label=val_label_name)
	axs[1].plot(x+1,data8_df['val_'+target],'--bo',color='g',label=val_label_name)
	axs[1].plot(x+1,data16_df['val_'+target],'--bo',color='b',label=val_label_name)
	axs[1].plot(x+1,data64_df['val_'+target],'--bo',color='orange',label=val_label_name)
	axs[1].plot(x+1,data128_df['val_'+target],'--bo',color='yellow',label=val_label_name)
	axs[1].plot(x+1,data256_df['val_'+target],'--bo',color='lime',label=val_label_name)
	axs[1].plot(x+1,data512_df['val_'+target],'--bo',color='teal',label=val_label_name)
	axs[1].plot(x+1,data1024_df['val_'+target],'--bo',color='cyan',label=val_label_name)
	axs[1].plot(x_gpu+1,datagpu_df['val_'+target],'--bo',color='magenta',label=val_label_name)
	
	############################## Log
	
	if(target == "loss"):
		axs[1].set_yscale('log')
	
	axs[1].set_title(val_title,fontsize=50)
	axs[1].set_xlabel('epoch',fontsize=45)
	axs[1].set_ylabel(target,fontsize=45)
	
	axs[0].grid()
	axs[1].grid()

else:
	fig,axs = plt.subplots(2,1,figsize=(20,20))
	axs[0].plot(accume_timelist[0],data4_df[target][:],'--bo',color='brown',label=train_label_name)
	axs[0].plot(accume_timelist[1],data8_df[target][:],'--bo',color='saddlebrown',label=train_label_name)
	axs[0].plot(accume_timelist[2],data16_df[target][:],'--bo',color='gold',label=train_label_name)
	axs[0].plot(accume_timelist[3],data64_df[target][:],'--bo',color='orange',label=train_label_name)
	axs[0].plot(accume_timelist[4],data128_df[target][:EPOCH],'--bo',color='indigo',label=train_label_name)
	axs[0].plot(accume_timelist[5],data256_df[target][:EPOCH],'--bo',color='g',label=train_label_name)
	axs[0].plot(accume_timelist[6],data512_df[target][:EPOCH],'--bo',color='b',label=train_label_name)
	axs[0].plot(accume_timelist[7],data1024_df[target][:EPOCH],'--bo',color='cyan',label=train_label_name)
	axs[0].plot(accume_timelist[8],datagpu_df[target][:EPOCH],'--bo',color='lime',label=train_label_name)
	axs[0].legend(['4nodes (2 EPOCH)','8 (4 EPOCH)','16 (7 EPOCH)','64 (27 EPOCH)','128','256','512','1024','gpu'],prop={'size' :20})
	#axs[0].set_xscale('log')	

	############################## Log
	if(target == "loss"):
		axs[0].set_yscale('log')
		minor_ticks = np.array([0.1,0.2,0.4,0.6,1.0,2,6,10,20])
		axs[0].set_yticks([0.1,0.2,0.4,0.6,1.0,2,6,10,20])
		axs[0].set_yticks(minor_ticks,minor=True)
		axs[0].get_yaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
	
	axs[0].set_title(title,fontsize=50)
	axs[0].set_xlabel('Training time',fontsize=45)
	axs[0].set_ylabel(target,fontsize=45)

	axs[1].get_xaxis().get_major_formatter().set_useOffset(False)
	axs[1].get_yaxis().get_major_formatter().set_useOffset(False)
	axs[1].plot(accume_timelist[0],data4_df['val_'+target][:],'--bo',color='brown',label=val_label_name)
	axs[1].plot(accume_timelist[1],data8_df['val_'+target][:],'--bo',color='saddlebrown',label=val_label_name)
	axs[1].plot(accume_timelist[2],data16_df['val_'+target][:],'--bo',color='gold',label=val_label_name)
	axs[1].plot(accume_timelist[3],data64_df['val_'+target][:],'--bo',color='orange',label=val_label_name)
	axs[1].plot(accume_timelist[4],data128_df['val_'+target][:EPOCH],'--bo',color='indigo',label=val_label_name)
	axs[1].plot(accume_timelist[5],data256_df['val_'+target][:EPOCH],'--bo',color='g',label=val_label_name)
	axs[1].plot(accume_timelist[6],data512_df['val_'+target][:EPOCH],'--bo',color='b',label=val_label_name)
	axs[1].plot(accume_timelist[7],data1024_df['val_'+target][:EPOCH],'--bo',color='cyan',label=val_label_name)
	axs[1].plot(accume_timelist[8],datagpu_df['val_'+target][:EPOCH],'--bo',color='lime',label=val_label_name)
	#axs[1].set_xscale('log')	
	
	############################## Log
	
	if(target == "loss"):
		axs[1].set_yscale('log')
		minor_ticks = np.array([0.1,0.2,0.4,0.6,1.0,2,6,10,20,50,100])
		axs[1].set_yticks([0.1,0.2,0.4,0.6,1.0,2,6,10,20,50,100])
		axs[1].set_yticks(minor_ticks,minor=True)
		axs[1].get_yaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
	
	axs[1].set_title(val_title,fontsize=50)
	axs[1].set_xlabel('Training time',fontsize=45)
	axs[1].set_ylabel(target,fontsize=45)
	

	axs[0].grid()
	axs[1].grid()
	
	

fig.tight_layout()
plt.savefig(filename)
plt.show()
