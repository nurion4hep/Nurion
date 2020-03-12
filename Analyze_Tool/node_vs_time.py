import matplotlib
#matplotlib.use('Agg')
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


## 32K default
time = [2223.3251526355743, 1451.9124898910522, 1137.9917290210724, 1140.3619375228882, 1166.649931192398,1014.0974791049957,1353.4979276657104]

#log scl 32K
#time = [2117.8648080825806,1450.6409270763397,1160.1696314811707,1022.107349872589,878.6063137054443,840.2194459438324]

#log scl 16K
#time = [2440.980729341507, 1764.3287065029144, 1551.672635793686, 1397.4543027877808, 1392.6179225444794,1300.065186738968]
node=[64,128,256,512,1024,2048,4096]



text = ['64node','128','256','512','1024','2048','4096']


title='Training elapsed time'
plt.rc('xtick',labelsize=20)
plt.rc('ytick',labelsize=20)

fig,axs = plt.subplots(1,figsize=(12,7))
axs.plot(node,time,'--bo',color='royalblue',markersize=12)


i=0
for x,y in zip(node,time):
	
	if(i!=3):
		plt.text(x+7,y-8,text[i],fontsize=18)
	i+=1
plt.text(node[3]+40,time[3]-8,text[3],fontsize=18)


axs.set_title(title,fontsize=25)
axs.set_xlabel('Node',fontsize=25)
axs.set_ylabel('Time',fontsize=25)
axs.grid()

plt.tight_layout()
plt.show()
plt.savefig('node_vs_time.png')

