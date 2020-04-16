import pandas as pd
from sklearn.metrics import roc_curve, roc_auc_score
import numpy as np
import h5py


# -- Read file
f = h5py.File('../../../NERSC_work/HEPdata_NEW/Merging_dir_forHT700bin/2020_sample/Merged_samples/Preprocessed_test.h5')
w = f['all_events']['weights_val'][:]
y_true = f['all_events']['labels_val'][:]

## -- Re-calculate weight as Xsec*Lumi / Gen
SF=124675.506754
GenRPV     = 330599.
bkg = 3867.83848132
Lumi = 63670
xsecRPV     = 0.013
GenRPV     = 330599

print(w)
w[w!=1] = w[w!=1] * bkg * SF / GenRPV
w[w==1] = Lumi * xsecRPV / GenRPV
print(w)


## -- Calculate ACU
predFile   = 'Merged_BATCH_512_EPOCH_50/prediction.csv'
df = pd.read_csv(predFile)
tpr, fpr, thr = roc_curve(df['label'], df['prediction'], pos_label=0)
auc = roc_auc_score(df['label'], df['prediction'])
print("##### --auc: ",auc)
## 0.997187612586373

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Cut based  TPR FPR
x_dot = np.sum(w[(f['all_events']['passSRJ'][:] == 1) & (y_true == 0)]) / np.sum(w[y_true==0])
y_dot = np.sum(w[(f['all_events']['passSRJ'][:] == 1) & (y_true == 1)]) / np.sum(w[y_true==1])


plt.plot(x_dot, y_dot, 'o', label='physics selection')
plt.plot(fpr, tpr, color='darkred')
plt.legend(['physics selection]'],prop={'size' :20})
plt.vlines(x_dot, ymin=0, ymax=1, linestyle='dashed', alpha=0.5, color='black')
plt.xlabel('1 - Background rejection')
plt.ylabel('Signal efficiency')
plt.xlim(0, 0.01)
plt.ylim(0, 1.01)
plt.legend()
plt.savefig('ROC_all.png')
