import numpy as np
import pandas as pd
import h5py

isnorm=0


# 32PU CNT
f = h5py.File('../../../../NERSC_work/HEPdata_NEW/Merging_dir_forHT700bin/2020_CMScut_32PU_v2_full/Distributed/preproc_cnt/Preprocessed_test.h5')
pred_dir   = '32PU_TrackCnt_512_EPOCH_50'

## 32PU PT
#f = h5py.File('../../../../NERSC_work/HEPdata_NEW/Merging_dir_forHT700bin/2020_CMScut_32PU_v2_full/Distributed/preproc_pt/Preprocessed_test.h5')
#pred_dir  = '32PU_TrackPT_512_EPOCH_50'



weight  = f['all_events']['weights_val'][:]
label   = f['all_events']['labels_val'][:]

pred = pred_dir + '/prediction.csv'

df_pred = pd.read_csv(pred)

## -- Re-calculate weight as Xsec*Lumi / Gen
GenRPV     = 147144.
xsecRPV     = 0.013
Lumi = 63670

SF  =37091.0
bkg=14.4609249377

weight[weight!=1] = weight[weight!=1] * bkg * SF / GenRPV
weight[weight==1] = Lumi * xsecRPV / GenRPV

sig_index = df_pred[df_pred['label'] == 1].index
bkg_index = df_pred[df_pred['label'] == 0].index

hist_sig = df_pred[df_pred['label'] == 1]['prediction']
hist_bkg = df_pred[df_pred['label'] == 0]['prediction']

if isnorm:
	print(" Normalized .. ")
	weight_sig = weight[sig_index.tolist()]
	weight_bkg = weight[bkg_index.tolist()]
else:
	weight_sig = 1 * np.ones(hist_sig.shape[0])
	weight_bkg = 1 * np.ones(hist_bkg.shape[0])

import matplotlib.pyplot as plt
import matplotlib

# Draw plot
plt.rc('xtick',labelsize=20)
plt.rc('ytick',labelsize=20)
plt.rcParams["figure.figsize"] = (8,8)


print(hist_bkg.shape)

bins = np.linspace(0,1,100)
normed_hist_sig = plt.hist(hist_sig,bins=bins,color='r',histtype='step',linewidth=1,weights=weight_sig,label='DNN signal')
normed_hist_bkg = plt.hist(hist_bkg,bins=bins,color='b',histtype='step',linewidth=1,weights=weight_bkg,label='DNN background')
plt.xlabel('DNN score',fontsize=25)
plt.ylabel('Nuber of events',fontsize=25)
plt.legend(prop={'size':15})
plt.yscale('log')

minor_ticks = np.arange(1, 70000, 50)
plt.yticks([10,100,1000,10000])

plt.ylim(8,70000)
#plt.ylim(4,70000)
plt.minorticks_on()


#plt.gca().yaxis.set_major_formatter(matplotlib.ticker.ScalarFormatter())

plt.grid(which='major', linestyle='-')
plt.minorticks_on()

plt.tight_layout()
plt.savefig(pred_dir + "/Score.png")
plt.close()

