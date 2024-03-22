import pandas as pd
import numpy as np
import matplotlib.pyplot as plt



## ------------------- 1. Set var, list 
## 64x64
#df_64 = pd.read_csv('KPS_default_norm_64x64/SELECT_64_BATCH_512_LR_8e-3/prediction.csv')
#df_128  = pd.read_csv('KPS_default_norm_64x64/SELECT_1024_BATCH_32_LR_8e-3/prediction.csv')
#df_256  = pd.read_csv('KPS_default_norm_64x64/SELECT_128_BATCH_256_LR_8e-3/prediction.csv')
#df_512  = pd.read_csv('KPS_default_norm_64x64/SELECT_256_BATCH_128_LR_8e-3/prediction.csv')
#df_1024 = pd.read_csv('KPS_default_norm_64x64/SELECT_512_BATCH_64_LR_8e-3/prediction.csv')


## 224x224
df_128  = pd.read_csv('CPLK_DFTnorm0_KSC_128node/prediction.csv')
df_256  = pd.read_csv('CPLK_DFTnorm0_KSC_256node/prediction.csv')
df_512  = pd.read_csv('CPLK_DFTnorm0_KSC_512node/prediction.csv')
df_1024 = pd.read_csv('CPLK_DFTnorm0_KSC_1024node/prediction.csv')


#224x224
#df_list = [df_64,df_128,df_256,df_512,df_1024]
df_list = [df_128,df_256,df_512,df_1024]
lumiVal = 63.67



## ------------------- 2. Make DNN score Plot
color_map_SIG = {'df_64':'pink','df_128':'maroon','df_256':'red','df_512':'tomato','df_1024':'lightsalmon'}
color_map_QCD = {'df_64':'slateblue','df_128':'midnightblue','df_256':'b','df_512':'royalblue','df_1024':'skyblue'}


plt.rc('legend', fontsize=12)
hsig_arr = []
hbkg_arr = []



for df,df_str in zip(df_list,['df_128']): # for 64x64
	df_bkg = df[df.label==0]
	
	label_name = 'N' + df_str.split('_')[1]
	hbkg1 = plt.hist(df_bkg['prediction'], histtype='step', stacked=True,weights=1000*lumiVal*df_bkg['weight'], bins=100, alpha=0.7, color=color_map_QCD[df_str], label='QCD_%s' %(label_name))
	plt.yscale('log')
	plt.ylabel('Events/(%.3f)/(fb-1)' % lumiVal,fontsize=13)
	plt.xlabel('DNN score',fontsize=13)
	hbkg_arr.append(hbkg1)

for df,df_str in zip(df_list,['df_128']): #for 64x64
	df_sig = df[df.label==1]
	
	label_name = 'N' + df_str.split('_')[1]
	hsig1 = plt.hist(df_sig['prediction'], histtype='step', stacked=True,weights=1000*lumiVal*df_sig['weight'], bins=100, alpha=0.7, color=color_map_SIG[df_str], label='RPV_%s' %(label_name))



	label_bkg = 'QCD_%s' %(label_name)
	label_sig = 'RPV_%s' %(label_name)

#	plt.hist((df_bkg['prediction'],df_sig['prediction']),histtype='step',stacked=True,weights=(1000*lumiVal*df_bkg['weight'],1000*lumiVal*df_sig['weight']),linewidth=1,bins=100,label=(label_bkg,label_sig))


	plt.yscale('log')
	plt.ylabel('Events/(%.3f)/(fb-1)' % lumiVal)
	plt.xlabel('DNN score',fontsize=13)
	hsig_arr.append(hsig1)


#plt.yticks([100,500,1000,3000,5000,10000,30000,50000,70000,90000,100000])
#minor_ticks = [100,500,1000,3000,5000,10000,30000,50000,70000,90000,100000]
#plt.minorticks_on()
#plt.yticks(minor_ticks)

#plt.ylim(0,500)
plt.legend(['RPV_N128','QCD_N128']) # for 64x64
plt.savefig('DNN_Score_224x224_test_log.png')
plt.close()


## -------------------3. Make Significance Plot
import scipy
import ROOT
from scipy.stats import poisson


def GetPvalue(nbkg,nsigNbkg):
    x = np.arange(nsigNbkg) # H0 prob var array upto H1 mean
    mu = nbkg  # H0 mean
    y1 = poisson(mu).pmf(x) # H0 dist array
    p_value = 1 - y1.sum() 
    return p_value



color_map = {'64node':'purple','128node':'maroon','256node':'red','512node':'tomato','1024node':'lightsalmon'} # 64x64
import math
#name_list=['64node','128node','256node','512node','1024node'] #64x64
name_list=['128node','256node','512node','1024node'] #64x64
cnt=0




for hsig,hbkg in zip(hsig_arr,hbkg_arr):
	
	print("Start {0}".format(name_list[cnt]))
	N_sig = hsig[0]
	N_bkg = hbkg[0]
	
	print(sum(N_sig))
	print(sum(N_bkg))

	print(N_sig)
	print(N_bkg)

	#Score = list([round(i*0.02,2) for i in range(0,50)])
	Score = list([round(i*0.01,2) for i in range(0,100)])
	
	arr_significance = []
	print("cut,Nsig,Nbkg,p-val,Significance")
	#for cut in range(0,len(Score)-1,1):
	for cut in range(0,len(Score),1):
		sig_integral = sum(N_sig[cut:])
		bkg_integral = sum(N_bkg[cut:])
		
		#significance = sig_integral / math.sqrt(sig_integral+bkg_integral)  ## For cut optimized
		
		p_value = GetPvalue(bkg_integral, sig_integral+bkg_integral) ## For official calculation
		significance =  ROOT.Math.gaussian_quantile_c(p_value,1)  ## For official calculation 

		arr_significance.append(significance)
		print("{0},{1},{2},{3},{4}".format(cut,sig_integral,bkg_integral,p_value,significance))

	print(" ")

	print("## * 20")
	print(arr_significance >= 5.0)
	#opti_y = arr_significance[arr_significance >= 5.0][0]
	#opti_x = arr_significance.index(arr_significance[arr_significance >= 5.0][0])
	print("##### 5sigma points ##### ")
	#print(opti_x,opti_y)


	plt.rcParams["legend.loc"] = 'lower left'
	alpha=0.7
	if name_list[cnt] == '64node':
		alpha=1
	elif name_list[cnt] == '128node':
		alpha=0.9
	#plt.plot(list([round(i*0.02,2) for i in range(0,49)]),arr_significance,'-o',color=color_map[name_list[cnt]],alpha=alpha)
	plt.plot(Score,arr_significance,'-*',color=color_map[name_list[cnt]],alpha=alpha)
	plt.xlabel('DNN score',fontsize=13)
	plt.ylabel('Significance',fontsize=13)
	plt.hlines(5,0,1, linestyle='dashed',linewidth=1, alpha=0.5, color='red')
	#plt.vlines(opti_x,0,7.6, linestyle='dashed',linewidth=1, alpha=0.5, color='red')
	#plt.plot(x_dot, y_dot, 'o',color='orange', label='Max significance: 7.8$\sigma$')
	plt.xlim(0,1)
	#plt.ylim(0,8.5)
	plt.grid(which='major', linestyle='-')
	plt.minorticks_on()
	cnt+=1
plt.legend(['128 node']) # 64x64
plt.savefig("Significance_224x224_test.png")
