import matplotlib
matplotlib.use('Agg')
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


## 32K old 50 epoch default
#time = [2223.3251526355743, 1451.9124898910522, 1137.9917290210724, 1140.3619375228882, 1166.649931192398,1014.0974791049957,1353.4979276657104]

## 32K new 100 epoch default
#time = [3694.408791065216, 2829.7513008117676, 2580.9733810424805, 2276.055812358856, 2361.5011258125305,2221.3792428970337,2680.1628584861755]

## 8Kfix for speedup
time=[258567.16841275874,160685.8866262436,85292.47870731354,25507.26446390152,15490.927917003632,8999.204348564148,5223.29126906395,2850.1766772270203,1731.3487522602081,1353.4979276657104]


#log scl 32K
#time = [2117.8648080825806,1450.6409270763397,1160.1696314811707,1022.107349872589,878.6063137054443,840.2194459438324]

#log scl 16K
#time = [2440.980729341507, 1764.3287065029144, 1551.672635793686, 1397.4543027877808, 1392.6179225444794,1300.065186738968]

node=[4,8,16,64,128,256,512,1024,2048,4096]



text = ['4node','8','16','64','128','256','512','1024','2048','4096']


title='Training elapsed time'
plt.rc('xtick',labelsize=20)
plt.rc('ytick',labelsize=20)

fig,axs = plt.subplots(1,figsize=(12,7))
axs.plot(node,time,'--bo',color='royalblue',markersize=12)


i=0
for x,y in zip(node,time):
	if i!=4 or i!=5:
		plt.text(x+9,y-8,text[i],fontsize=15)
		print(i, text[i])
	else:
		plt.text(x-7,y-16,text[i],fontsize=15)
	i+=1

axs.set_title(title,fontsize=25)
axs.set_xlabel('Node',fontsize=25)
axs.set_ylabel('Time',fontsize=25)
axs.grid()

plt.tight_layout()
#plt.show()
plt.savefig('node_vs_time.png')

