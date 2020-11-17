import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


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

#64x64
#df_list = [df_64,df_128,df_256,df_512,df_1024]

#224x224
df_list = [df_128,df_256,df_512,df_1024]

lumiVal = 138
color_map_SIG = {'df_64':'pink','df_128':'maroon','df_256':'red','df_512':'tomato','df_1024':'lightsalmon'}
color_map_QCD = {'df_64':'slateblue','df_128':'midnightblue','df_256':'b','df_512':'royalblue','df_1024':'skyblue'}


plt.rc('legend', fontsize=7)


hsig_arr = []
hbkg_arr = []
for df,df_str in zip(df_list,['df_128','df_256','df_512','df_1024']):
#for df,df_str in zip(df_list,['df_64','df_128','df_256','df_512','df_1024']):
	df_sig = df[df.label==1]
	
	label_name = 'N' + df_str.split('_')[1]
	#hsig1 = df_sig['prediction'].plot(kind='hist', histtype='step', weights=1000*lumiVal*df_sig['weight'], bins=50, alpha=0.7, color=color_map_SIG[df_str], label='RPV_%s' %(label_name))
	hsig1 = plt.hist(df_sig['prediction'], histtype='step', weights=1000*lumiVal*df_sig['weight'], bins=50, alpha=0.7, color=color_map_SIG[df_str], label='RPV_%s' %(label_name))
	plt.yscale('log')
	plt.ylabel('Events/(%f)/(fb-1)' % lumiVal)
	hsig_arr.append(hsig1)


for df,df_str in zip(df_list,['df_128','df_256','df_512','df_1024']):
#for df,df_str in zip(df_list,['df_64','df_128','df_256','df_512','df_1024']):
	df_bkg = df[df.label==0]
	
	label_name = 'N' + df_str.split('_')[1]
	#hbkg1 = df_bkg['prediction'].plot(kind='hist', histtype='step', weights=1000*lumiVal*df_bkg['weight'], bins=50, alpha=0.7, color=color_map_QCD[df_str], label='QCD_%s' %(label_name))
	hbkg1 = plt.hist(df_bkg['prediction'], histtype='step', weights=1000*lumiVal*df_bkg['weight'], bins=50, alpha=0.7, color=color_map_QCD[df_str], label='QCD_%s' %(label_name))
	plt.yscale('log')
	plt.ylabel('Events/(%f)/(fb-1)' % lumiVal)
	hbkg_arr.append(hbkg1)

plt.legend(['RPV_N128','RPV_N256','RPV_N512','RPV_N1024','QCD_N128','QCD_N256','QCD_N512','QCD_N1024'])
#plt.legend(['RPV_N64','RPV_N128','RPV_N256','RPV_N512','RPV_N1024','QCD_N64','QCD_N128','QCD_N256','QCD_N512','QCD_N1024'])
#plt.savefig('DNN_Score.png')
plt.close()


#hbkg2 = df_bkg['prediction'].plot(kind='hist', histtype='step', weights=df_bkg['scaledWeight'], bins=50, alpha=0.7, color='red', label='QCD')
#hsig2 = df_sig['prediction'].plot(kind='hist', histtype='step', weights=df_sig['scaledWeight'], bins=50, alpha=0.7, color='blue', label='RPV')
##plt.yscale('log')
#plt.ylabel('Arbitrary Unit')
#plt.legend()
##plt.show()
#plt.savefig(args.input+'/Score_2.png')
#plt.close()



color_map = {'128node':'maroon','256node':'red','512node':'tomato','1024node':'lightsalmon'}
import math
name_list=['128node','256node','512node','1024node']
cnt=0

max_couple=[]
for hsig,hbkg in zip(hsig_arr,hbkg_arr):
	
	print("Start {0}".format(name_list[cnt]))
	N_sig = hsig[0]
	N_bkg = hbkg[0]
	Score = list([round(i*0.02,2) for i in range(0,50)])
	
	
	arr_significance = []
	for cut in range(0,len(Score)-1,1):
		sig_integral = sum(N_sig[cut:])
		bkg_integral = sum(N_bkg[cut:])
		print(cut,sig_integral,bkg_integral)
		#print(sig_integral,bkg_integral)
		significance = sig_integral / math.sqrt(sig_integral+bkg_integral)
		arr_significance.append(significance)

	max_couple.append((arr_significance.index(max(arr_significance))*0.02,max(arr_significance)))
	print(arr_significance.index(max(arr_significance)))
	print(max(arr_significance))


	x_max = arr_significance.index(max(arr_significance))
	plt.rcParams["legend.loc"] = 'lower left'
	plt.plot(list([round(i*0.02,2) for i in range(0,49)]),arr_significance,'-o',color=color_map[name_list[cnt]])
	plt.xlabel('DNN score',fontsize=25)
	plt.ylabel('Significance',fontsize=25)
	plt.vlines(x_max, ymin=0, ymax=10, linestyle='dashed',linewidth=3, alpha=0.5, color='red',label=name_list[cnt])
	#plt.plot(x_dot, y_dot, 'o',color='orange', label='Max significance: 7.8$\sigma$')
	plt.xlim(0,1)
	#plt.ylim(0,8.5)
	plt.grid(which='major', linestyle='-')
	plt.minorticks_on()
	cnt+=1
plt.legend(['128 node','256 node','512 node','1024 node'])
plt.savefig("Significance.png")

for i in max_couple:
	print(i)
