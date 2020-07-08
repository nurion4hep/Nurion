import matplotlib
matplotlib.use('Agg')
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Batch=128 fix results  64 image 50epoch
#time_B128=[36670.725098371506, 9921.49017047882, 2970.891015291214, 1718.982388496399, 1106.7916436195374, 640.1377544403076, 425.4936149120331,303.94]
#Single_time_B128=36670.725098371506
#node_B128=[4,16,64,128,256,512,1024,2048]
#
## Batch=8 fix results 64 image 100epoch
#time_B8=[258567.16841275874,160685.8866262436,85292.47870731354,25507.26446390152,15490.927917003632,8999.204348564148,5223.29126906395,2850.1766772270203,1731.3487522602081,1353.4979276657104]
#Single_time_B8= 258567.16841275874
#node_B8=[4,8,16,64,128,256,512,1024,2048,4096]

# Effective Batch= 32K  64image 100epoch
#time_large=[3694.408791065216, 2829.7513008117676, 2580.9733810424805, 2276.055812358856, 2361.5011258125305,2221.3792428970337,2680.1628584861755
time_32K=[2829.7513008117676, 2580.9733810424805, 2276.055812358856, 2361.5011258125305,2221.3792428970337,2680.1628584861755]
Single_time_32K= 2829.7513008117676
node_32K=[128,256,512,1024,2048,4096]

# Effective Batch= 32K  224image 20epoch
time_large=[2935.0999977588654,1908.1206185817719,1401.791358947754,1142.4294373989105,1132.5579342842102,1470.9383869171143]
Single_time_large= 2935.0999977588654
node_large=[128,256,512,1024,2048,4096]


#speedup_B128 =[]
#for i in time_B128:
#	speedup_B128.append(4 * Single_time_B128 / i)
#	#speedup.append(16 * Single_time / i)
#
#speedup_B8 =[]
#for i in time_B8:
#	speedup_B8.append(4 * Single_time_B8 / i)
#	#speedup.append(16 * Single_time / i)

speedup_large =[]
for i in time_large:
	speedup_large.append(128 * Single_time_large / i)
	#speedup.append(16 * Single_time / i)

speedup_32K =[]
for i in time_32K:
	speedup_32K.append(128 * Single_time_32K / i)
	#speedup.append(16 * Single_time / i)




plt.rc('xtick',labelsize=15)
plt.rc('ytick',labelsize=15)

#x = np.linspace(0,2100,21000)
x = np.linspace(128,5000,20000)
y = x
fig,axs = plt.subplots(1,figsize=(10,10))
#axs.plot(node_B8,speedup_B8,'--*',color='midnightblue',markersize=10,label="2020 Summer(Batch=8 Fixed)")
#axs.plot(node_B128,speedup_B128,'--*',color='green',markersize=10,alpha=0.6,label="2019 Fall(Batch=128 fixed)")
axs.plot(node_32K,speedup_32K,'--*',color='midnightblue',markersize=10,alpha=0.6,label="64x64 EffectiveBatch=32K")
axs.plot(node_large,speedup_large,'--o',color='crimson',markersize=10,alpha=1,label="224x224 EffectiveBatch=32K fixed")
axs.plot(x,y,'--',color='gray',alpha=0.5)
plt.legend(prop={'size':15})

xmin=128
xmax=5000
ymin=128
ymax=1000
axs.set_yscale('log')
axs.set_xscale('log')
axs.set_xlabel('Node',fontsize=20)
axs.set_ylabel('Speedp-up',fontsize=20)
axs.set_xlim([xmin,xmax])
axs.set_ylim([ymin,ymax])

#minor_ticks = np.arange(4, 5000, 10)
#axs.set_xticks([4,5,6,7,10,20,30,100,200,1000,2000,3000,4000])
#axs.set_xticks([4,16,60,100,200,1000,2000,4000])
#axs.set_xticks(minor_ticks, minor=True)
#axs.set_yticks([4,16,60,100,200,300,1000,2000,4000])
#axs.set_yticks(minor_ticks, minor=True)

minor_ticks = np.arange(128, 5000, 10)
#axs.set_xticks([128,200,1000,2000,3000,4000])
axs.set_xticks([128,200,400,600,800,1000,2000,4000])
axs.set_xticks(minor_ticks, minor=True)
axs.set_yticks([128,200,400,600,800,1000,2000,4000])
axs.set_yticks(minor_ticks, minor=True)

axs.get_xaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
axs.get_yaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
plt.text(1000,1450, 'Ideal', fontsize=32,
               rotation=45, rotation_mode='anchor',color='maroon',alpha=0.6)
plt.minorticks_on()
plt.grid(which='major', linestyle='-')

#plt.show()
plt.savefig('speedup_32Kcompare.png')
