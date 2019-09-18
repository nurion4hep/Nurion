import h5py
import numpy as np
import pandas as pd


filenames=["train.h5","val.h5","test.h5"]


for filename in filenames:
	path = "normdata/"+filename
	data=h5py.File(filename)
	
	print(list(data['all_events'].keys()))
	weights= data['all_events']['weight'][:]
	
	
	weight_df = pd.DataFrame(weights)
	print("####Data Frame summary####")
	pd.set_option('display.max_rows', 10000)
	print(weight_df)
	print("########################")
	#print("event: " ,len(weights), type(weights[0]))
	
	
	## check ok
	print("#### weight list ####") 
	print(weights[:100])
	
	
	print("## RPV_SUSY ##")
	Norm_sig = 36000 * 0.013  / 330599.
	print(weights[np.where(np.around(weights[:],decimals=1) == np.around(Norm_sig,decimals=1))][:10])
	
	print("## QCD 700-1000 ##")
	Norm_QCD700 = 36000 * 6295 / 218007.
	print(weights[np.where(np.around(weights[:],decimals=1) == np.around(Norm_QCD700,decimals=1))][:10])
	
	print("## QCD 1000-1500 ##")
	Norm_QCD1000 = 36000 * 1093 / 1016136.
	print(weights[np.where(np.around(weights[:],decimals=1) == np.around(Norm_QCD1000,decimals=1))][:10])
	
	print("## QCD 1500-2000 ##")
	Norm_QCD1500 = 36000 * 99.35 / 425202.
	print(weights[np.where(np.around(weights[:],decimals=1) == np.around(Norm_QCD1500,decimals=1))][:10])
	
	print("## QCD 2000-Inf ##")
	Norm_QCD2000 = 36000 * 20.24 / 340101.
	print(weights[np.where(np.around(weights[:],decimals=1) == np.around(Norm_QCD2000,decimals=1))][:10])
	
	
	break	


