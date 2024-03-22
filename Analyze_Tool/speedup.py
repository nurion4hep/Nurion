import matplotlib
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

### ---- Batch=128 fix results  64 image 50epoch
#time_B128=[36670.725098371506, 9921.49017047882, 2970.891015291214, 1718.982388496399, 1106.7916436195374, 640.1377544403076, 425.4936149120331,303.94]
#Single_time_B128=36670.725098371506
#node_B128=[4,16,64,128,256,512,1024,2048]


### ----Batch=8 fix results 64 image 100epoch

## -- Node: 4~4096
#time_B8=[258567.16841275874,160685.8866262436,85292.47870731354,25507.26446390152,15490.927917003632,8999.204348564148,5223.29126906395,2850.1766772270203,1731.3487522602081,1353.4979276657104]
#Single_time_B8= 258567.16841275874
#node_B8=[4,8,16,64,128,256,512,1024,2048,4096]

## -- Node: 128~4096
#time_B8=[15490.927917003632,8999.204348564148,5223.29126906395,2850.1766772270203,1731.3487522602081,1353.4979276657104]
#Single_time_B8= 15490.927917003632
#node_B8=[128,256,512,1024,2048,4096]


### ----Batch=8 fix results 224 image 100epoch

## --with fisrt step
#time_B8_large = [8283.649612903595,4303.832903146744,2492.4370584487915,1323.1843650341034,786.8695237636566,768.4916355609894]
#Single_time_B8_large= 8283.649612903595

## --without first step
#time_B8_large = [7517.727783441544 ,3897.3332884311676 ,2249.131636619568 ,1192.2444183826447 ,672.5603361129761 ,634.646270275116]
#Single_time_B8_large= 7517.727783441544
#node_B8_large=[128,256,512,1024,2048,4096]


# Effective Batch= 32K  64image 100epoch
#time_large=[3694.408791065216, 2829.7513008117676, 2580.9733810424805, 2276.055812358856, 2361.5011258125305,2221.3792428970337,2680.1628584861755
#time_32K=[2829.7513008117676, 2580.9733810424805, 2276.055812358856, 2361.5011258125305,2221.3792428970337,2680.1628584861755]
#Single_time_32K= 2829.7513008117676
#node_32K=[128,256,512,1024,2048,4096]

# Effective Batch= 32K  224image 20epoch
#time_large=[2935.0999977588654,1908.1206185817719,1401.791358947754,1142.4294373989105,1132.5579342842102,1470.9383869171143]
#Single_time_large= 2935.0999977588654
#node_large=[128,256,512,1024,2048,4096]

# ---------------------------------------------------------------

# 32K 224x224 CP Large Kernel LR=2e-03
#time = [166.53976332187653 ,101.92912660121918 ,70.34434948921204 ,56.16551579713821 ,58.9195232200622] # with 2048
#time_224 = [166.53976332187653 ,101.92912660121918 ,70.34434948921204 ,56.16551579713821]
#Single_time_224 = time_224[0]
#node_224 = [128,256,512,1024]


# 8batch 224x224 CP Large Kernel LR=2e-03
time_224 = [17308.84763431549 ,10376.94586956501 ,5391.960455553873 ,1655.170814064833 ,842.9652311944961 ,438.2046036052704 ,229.2290646457672 ,134.4215600824356]
Single_time_224 = time_224[0]
node_224=[4,8,16,64,128,256,512,1024]


# 32K 64x64 DefaultNorm0 LR=8e-03
#time_64 = [52.64287549972534 ,34.76981614112854 ,26.27677938938141 ,23.179390041828157 ,26.423430993556977] # with 64
#time_64 = [34.76981614112854 ,26.27677938938141 ,23.179390041828157 ,26.423430993556977] 
#Single_time_64 = time_64[0]
#node_64 = [64,128,256,512,1024]
#node_64 = [128,256,512,1024]

# 8batch 64x64 DefaultNorm0 LR=8e-03
time_64 = [4754.470872561137 ,2544.376339018345 ,1367.4141018159928 ,397.29915613889693 ,287.7252774953842 ,125.58801151514054 ,86.47991998195648 ,52.25830784082413]
Single_time_64 = time_64[0]
node_64=[4,8,16,64,128,256,512,1024]


# strong 224x224 CP Large Kernel LR=2e-03
#speedup_224 = []
#for i in time_224:
#	speedup_224.append(128 * Single_time_224 / i )

# strong 64x64 CP DefaultNorm0  LR=8e-03
#speedup_64 = []
#for i in time_64:
#	speedup_64.append(64 * Single_time_64 / i )


# weak 224x224 CP Large Kernel LR=2e-03
speedup_224 = []
for i in time_224:
	speedup_224.append(4 * Single_time_224 / i )

# weak 64x64 CP DefaultNorm0  LR=8e-03
speedup_64 = []
for i in time_64:
	speedup_64.append(4 * Single_time_64 / i )







plt.rc('xtick',labelsize=15)
plt.rc('ytick',labelsize=15)

# --strong
#x = np.linspace(60,5000,20000)
# --weak
x = np.linspace(3,5000,20000)


y = x
fig,axs = plt.subplots(1,figsize=(10,10))
axs.plot(node_224,speedup_224,'--*',color='crimson',markersize=10,label="224x224")
axs.plot(node_64,speedup_64,'--*',color='royalblue',markersize=10,label="64x64")
axs.plot(x,y,'--',color='gray',alpha=0.5)
plt.legend(prop={'size':15})

xmin=3
xmax=1200
ymin=3
ymax=1200

axs.set_yscale('log')
axs.set_xscale('log')
axs.set_xlabel('Number of nodes',fontsize=20)
axs.set_ylabel('Speedp-up per epoch',fontsize=20)
axs.set_xlim([xmin,xmax])
axs.set_ylim([ymin,ymax])


# --weak
axs.set_xticks([4,16,64,128,200,400,600,1200])
axs.set_yticks([4,16,64,128,200,400,600,1200])
minor_ticks = np.arange(3, 1200, 10)

# -- strong
#axs.set_xticks([64,200,400,600,1200])
#axs.set_yticks([64,200,400,600,1200])
#minor_ticks = np.arange(64, 1200, 10)



axs.set_xticks(minor_ticks, minor=True)

axs.get_xaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
axs.get_yaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
plt.text(600,600, 'Ideal', fontsize=32,
               rotation=45, rotation_mode='anchor',color='maroon',alpha=0.6)
plt.minorticks_on()
plt.grid(which='major', linestyle='-')

#plt.show()
plt.savefig('speedup_per_epoch_weak.png')
