import matplotlib
matplotlib.use('Agg')
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

time=[2332.4771234989166,1718.982388496399,1225.7143347263336,1195.5247712135315,1194.7604217529297,981.2357094287872]
node=[64,128,256,512,1024,2048]

title='Node_vs_Time'




plt.rc('xtick',labelsize=30)
plt.rc('ytick',labelsize=30)

fig,axs = plt.subplots(1,figsize=(20,20))
axs.plot(time,node,'--bo',color='royalblue',markersize=12)

#axs[0].set_yscale('log')
axs.set_title(title,fontsize=30)
axs.set_xlabel('Node',fontsize=30)
axs.set_ylabel('Time',fontsize=30)
axs.grid()

#axs[0].set_xticks(x)
#axs[1].set_xticks(x)
#plt.show()
plt.savefig('node_time.png')

