import pandas as pd
from sklearn.metrics import roc_curve, roc_auc_score, accuracy_score
import numpy as np

import h5py

f = h5py.File('../NERSC_work/HEPdata_NEW/Merging_dir_forHT700bin/Preprocessed_Test.h5')
y_true = f['all_events']['labels_val'][:] 
predFile    = 'prediction.csv'
df = pd.read_csv(predFile)
y_pred = df['prediction']


#print(df)

print("Accuracy: ", accuracy_score(y_true,y_pred>=0.5))
tpr, fpr4, thr = roc_curve(df['label'], df['prediction'], pos_label=0)
auc = roc_auc_score(df['label'], df['prediction'])
print("AUC: ", auc)


