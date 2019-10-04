import matplotlib
matplotlib.use('Agg')
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from IPython.display import display

data_df = pd.read_csv('train_log.csv')
#display(data_df)

epoch_arr    = data_df['epoch'].values
loss_arr     = data_df['loss'].values
val_loss_arr = data_df['val_loss'].values
acc_arr      = data_df['acc'].values
val_acc_arr  = data_df['val_acc'].values


plt.rc('xtick',labelsize=20)
plt.rc('ytick',labelsize=20)

## ---Select Loss or Acc
#target ='loss'
target ='acc'

train_label_name = "Train-set "+target
val_label_name   = "Validation-set "+target
title ="epoch vs "+target
val_title='epoch vs val_'+target
filename='epoch_'+target+'.png'

x = np.arange(len(data_df['epoch']))


fig,axs = plt.subplots(2,1,figsize=(20,20))
axs[0].plot(x+1,data_df[target],'--bo',color='darkorange',label=train_label_name)
#axs[0].set_yscale('log')
axs[0].set_title(title,fontsize=30)
axs[0].set_xlabel('epoch',fontsize=25)
axs[0].set_ylabel(target,fontsize=25)

axs[1].get_xaxis().get_major_formatter().set_useOffset(False)
axs[1].get_yaxis().get_major_formatter().set_useOffset(False)
axs[1].plot(x+1,data_df['val_'+target],'--bo',color='royalblue',label=val_label_name)
#axs[1].set_yscale('log')
axs[1].set_title(val_title,fontsize=30)
axs[1].set_xlabel('epoch',fontsize=25)
axs[1].set_ylabel(target,fontsize=25)

axs[0].grid()
axs[1].grid()

#axs[0].set_xticks(x)
#axs[1].set_xticks(x)
plt.savefig(filename)

