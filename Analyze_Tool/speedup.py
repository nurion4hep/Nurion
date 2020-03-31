import matplotlib
matplotlib.use('Agg')
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# 16K results
#time=[36670.725098371506, 9921.49017047882, 2970.891015291214, 1718.982388496399, 1106.7916436195374, 640.1377544403076, 425.4936149120331,303.94]
#Single_time=36670.725098371506
#node=[4,16,64,128,256,512,1024,2048]

# 32K results
time = [85292.47870731354,25507.26446390152,15490.927917003632,8999.204348564148,5223.29126906395,2680.1628584861755]
Single_time=85292.47870731354
node=[16,64,128,256,512,4096]
#node=[16,64,128,256,512,1024,2048,4096]

speedup =[]
for i in time:
	#speedup.append(4 * Single_time / i)
	speedup.append(16 * Single_time / i)
print(speedup)


plt.rc('xtick',labelsize=15)
plt.rc('ytick',labelsize=15)

#x = np.linspace(0,2100,21000)
x = np.linspace(16,4000,21000)
y = x
fig,axs = plt.subplots(1,figsize=(10,10))
axs.plot(node,speedup,'--*',color='midnightblue',markersize=10)
axs.plot(x,y,'--',color='maroon',alpha=0.5)


xmin=10
xmax=5000
ymin=10
ymax=5000
axs.set_yscale('log')
axs.set_xscale('log')
axs.set_xlabel('Node',fontsize=20)
axs.set_ylabel('Speedp-up',fontsize=20)
axs.set_xlim([xmin,xmax])
axs.set_ylim([ymin,ymax])

#minor_ticks = np.arange(4, 5000, 10)
minor_ticks = np.arange(16, 5000, 10)

#axs.set_xticks([4,5,6,7,10,20,30,100,200,1000,2000,3000,4000])
axs.set_xticks([16,60,100,200,1000,2000,4000])
axs.set_xticks(minor_ticks, minor=True)
axs.set_yticks([16,60,100,200,300,1000,2000,4000])
axs.set_yticks(minor_ticks, minor=True)


axs.get_xaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
axs.get_yaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
plt.text(1000,1450, 'Ideal', fontsize=32,
               rotation=45, rotation_mode='anchor',color='maroon',alpha=0.6)
plt.title("speedup",fontsize=25)
plt.minorticks_on()
plt.grid(which='major', linestyle='-')

#plt.show()
plt.savefig('speedup.png')
