import numpy as np
import h5py
from sklearn.metrics import roc_auc_score, roc_curve, confusion_matrix, precision_recall_curve

f = h5py.File('val.h5')
print(f.keys())
y_true = f['all_events']['y'][:]
y_pred = np.load('prediction_nn_log_3ch-CNN.pyc.npy')
w = f['all_events']['weight'][:] 

print(" ")
print(" ###########")
print("AUC: ",roc_auc_score(y_true, y_pred, sample_weight=w))
print(confusion_matrix(y_true, y_pred>=0.5, sample_weight=w))


fpr, tpr, _ = roc_curve(y_true, y_pred, sample_weight=w)


x_dot = np.sum(w[(f['all_events']['passSR'][:] == 1) & (y_true == 0)]) / np.sum(w[y_true==0])
y_dot = np.sum(w[(f['all_events']['passSR'][:] == 1) & (y_true == 1)]) / np.sum(w[y_true==1])

import matplotlib
#%matplotlib inline
#matplotlib.use('Agg')
import matplotlib.pyplot as plt
from IPython.display import display


matplotlib.rcParams.update({'font.size': 20})

fig = plt.figure(figsize=(8,8))
plt.vlines(x_dot, ymin=0, ymax=1, linestyle='dashed', alpha=0.5, color='black')
plt.plot(x_dot, y_dot, 'o', label='cuts')
_ = plt.plot(fpr, tpr, label='CNN 3 Channel')
plt.xlim(0, 0.0004)
plt.xlabel('False Positive Ratio')
plt.ylabel('True Positive Ratio')
plt.ylim(0, 1)
plt.legend(loc='lower right')
plt.show()
plt.savefig('ROC.png')
