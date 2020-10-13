import matplotlib
matplotlib.use('Agg')
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


## 32K old 50 epoch default
#time = [2223.3251526355743, 1451.9124898910522, 1137.9917290210724, 1140.3619375228882, 1166.649931192398,1014.0974791049957,1353.4979276657104]

## 32K new 100 epoch default
#time = [3694.408791065216, 2829.7513008117676, 2580.9733810424805, 2276.055812358856, 2361.5011258125305,2221.3792428970337,2680.1628584861755]
#time_large=[2935.0999977588654,1908.1206185817719,1401.791358947754,1142.4294373989105,1132.5579342842102,1470.9383869171143]


## 8Kfix for speedup
#time=[258567.16841275874,160685.8866262436,85292.47870731354,25507.26446390152,15490.927917003632,8999.204348564148,5223.29126906395,2850.1766772270203,1731.3487522602081,1353.4979276657104]


#log scl 32K
#time = [2117.8648080825806,1450.6409270763397,1160.1696314811707,1022.107349872589,878.6063137054443,840.2194459438324]

#log scl 16K
#time = [2440.980729341507, 1764.3287065029144, 1551.672635793686, 1397.4543027877808, 1392.6179225444794,1300.065186738968]

#node=[64,128,256,512,1024,2048,4096]
#node_large=[128,256,512,1024,2048,4096]


## 32K 224x224 CP Large Kenel adam LR = 2e-03 Effective batch = 32K


time=[166.9000259399414 ,102.55070827960968 ,70.60527248859405 ,56.91568506240845]
node = [128,256,512,1024]
text = ['128nodes','256','512','1024']

## 32K 224x224 CP Large Kenel adam LR = 2e-03 Batch = 8K
#time = [17308.84763431549 ,10376.94586956501 ,5391.960455553873 ,1655.170814064833 ,842.9652311944961 ,438.2046036052704 ,229.2290646457672 ,134.4215600824356] 
#node = [4,8,16,64,128,256,512,1024] 
#text = ['4nodes','8','16','64','128','256','512','1024'] 




title='Training elapsed time'
plt.rc('xtick',labelsize=20)
plt.rc('ytick',labelsize=20)

fig,axs = plt.subplots(1,figsize=(12,7))
#axs.plot(node,time,'--bo',color='royalblue',markersize=12,label='64x64')
#axs.plot(node_large,time_large,'--bo',color='darkorange',markersize=12,label='224x224')
axs.plot(node,time,'--bo',color='royalblue',markersize=12,label='Training time / epoch')

i=0
for x,y in zip(node,time):
	print(i, text[i])
	plt.text(x-7,y-7,text[i],fontsize=20)
	i+=1

print( '1024 nodes are',1600.95 / 56.91568506240845,'times faster than GPU' )

plt.text(800,130, 'GPU: 1660.95', fontsize=25,color='maroon',alpha=0.6)
axs.set_title(title,fontsize=25)
axs.set_xlabel('Node',fontsize=25)
axs.set_ylabel('Time',fontsize=25)
axs.set_xticks([0,120,250,500,1000,1200])
axs.grid()
plt.legend(prop={'size':15})
plt.tight_layout()
#plt.show()
plt.savefig('time_per_epoch.png')

