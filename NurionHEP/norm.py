import h5py
import numpy as np
import pandas as pd


filenames=["train.h5","val.h5","test.h5"]


for filename in filenames:
	path = "normdata/"+filename
	data=h5py.File(filename)
	
	print(list(data['all_events'].keys()))
	hist            = data['all_events']['hist'][:]
	histEM          = data['all_events']['histEM'][:]
	histtrack       = data['all_events']['histtrack'][:]
	passSR          = data['all_events']['passSR'][:]
	passSR4J        = data['all_events']['passSR4J'][:]
	passSR5J        = data['all_events']['passSR45'][:]
	weights         = data['all_events']['weight'][:]
	Y               = data['all_events']['y'][:]
	print("number: ",hist.shape[0])
	print(" ")
	
	
	
	#weight_df = pd.DataFrame(weights)
	#print("####Data Frame summary####")
	#pd.set_option('display.max_rows', 10000)
	#print(weight_df)
	#print("########################")
	#print("event: " ,len(weights), type(weights[0]))
	
	
	## check ok
	#print("#### weight list ####") 
	#print(weights[-20:-1])
	
	'''
	print("#### Normalized weight ####")
	print("## RPV_SUSY ##")
	Norm_sig = weights[np.where(np.around(weights[:],decimals=1) == 468.0)] * 311924. / 330599
	print(Norm_sig)
	weights[np.where(np.around(weights[:],decimals=1) == 468.0)] = Norm_sig
	
	print("## QCD 700-1000 ##")
	Norm_QCD700 = weights[np.where(np.around(weights[:],decimals=1) == 245844000.0)] * 1088. / 218007
	print(Norm_QCD700)
	weights[np.where(np.around(weights[:],decimals=1) == 245844000.0)] = Norm_QCD700
	
	print("## QCD 1000-1500 ##")
	Norm_QCD1000 = weights[np.where(np.around(weights[:],decimals=1) == 43092000.0)] * 134774. / 1016136
	print(Norm_QCD1000)
	weights[np.where(np.around(weights[:],decimals=1) == 43092000.0)] = Norm_QCD1000
	
	print("## QCD 1500-2000 ##")
	Norm_QCD1500 = weights[np.where(np.around(weights[:],decimals=1) == 4338000.0)] * 133963. / 425202
	print(Norm_QCD1500)
	weights[np.where(np.around(weights[:],decimals=1) == 4338000.0)] = Norm_QCD1500
	
	
	print("## QCD 2000-Inf ##")
	Norm_QCD2000 = weights[np.where(np.around(weights[:],decimals=1) == 912960.0)] * 127669. / 340101
	print(Norm_QCD2000)
	weights[np.where(np.around(weights[:],decimals=1) == 912960.0)] = Norm_QCD2000
	
	'''
	
	
	print("successfully read!, now normalize!")
	#print("#### Normalized weight ####")
	#print("## RPV_SUSY ##")
	Norm_sig = 36000 * 0.013  / 330599.
	#print(Norm_sig)
	dim_sig = weights[np.where(np.around(weights[:],decimals=1) == 468.0)].shape
	weights[np.where(np.around(weights[:],decimals=1) == 468.0)] = np.ones(dim_sig)*Norm_sig
	#print(weights[np.where(np.around(weights[:],decimals=1) == np.around(Norm_sig,decimals=1))][:10])
	
	#print("## QCD 700-1000 ##")
	Norm_QCD700 = 36000 * 6295 / 218007.
	#print(Norm_QCD700)
	dim_QCD700 = weights[np.where(np.around(weights[:],decimals=1) == 245844000.0)].shape
	weights[np.where(np.around(weights[:],decimals=1) == 245844000.0)] = np.ones(dim_QCD700)*Norm_QCD700
	#print(weights[np.where(np.around(weights[:],decimals=1) == np.around(Norm_QCD700,decimals=1))][:10])
	
	#print("## QCD 1000-1500 ##")
	Norm_QCD1000 = 36000 * 1093 / 1016136.
	#print(Norm_QCD1000)
	dim_QCD1000 = weights[np.where(np.around(weights[:],decimals=1) == 43092000.0)].shape
	weights[np.where(np.around(weights[:],decimals=1) == 43092000.0)] = np.ones(dim_QCD1000)*Norm_QCD1000
	#print(weights[np.where(np.around(weights[:],decimals=1) == np.around(Norm_QCD1000,decimals=1))][:10])
	
	#print("## QCD 1500-2000 ##")
	Norm_QCD1500 = 36000 * 99.35 / 425202.
	#print(Norm_QCD1500)
	dim_QCD1500 = weights[np.where(np.around(weights[:],decimals=1) == 4338000.0)].shape
	weights[np.where(np.around(weights[:],decimals=1) == 4338000.0)] = np.ones(dim_QCD1500)*Norm_QCD1500
	#print(weights[np.where(np.around(weights[:],decimals=1) == np.around(Norm_QCD1500,decimals=1))][:10])
	
	#print("## QCD 2000-Inf ##")
	Norm_QCD2000 = 36000 * 20.24 / 340101.
	#print(Norm_QCD2000)
	dim_QCD2000 = weights[np.where(np.around(weights[:],decimals=1) == 912960.0)].shape
	weights[np.where(np.around(weights[:],decimals=1) == 912960.0)] = np.ones(dim_QCD2000)*Norm_QCD2000
	#print(weights[np.where(np.around(weights[:],decimals=1) == np.around(Norm_QCD2000,decimals=1))][:10])
	
	
	## check ok
	#print("#### changed weight list ####") 
	#print(weights[-20:-1])
	
	print("Now compress and writing!")
	with h5py.File(path,"w") as f:
		g=f.create_group("all_events")
		g.create_dataset("hist",      data=hist,chunks=True,compression='gzip', compression_opts=9) 
		g.create_dataset("histEM",    data=histEM,chunks=True,compression='gzip', compression_opts=9) 
		g.create_dataset("histtrack", data=histtrack,chunks=True,compression='gzip', compression_opts=9) 
		g.create_dataset("passSR",	  data=passSR,chunks=True,compression='gzip', compression_opts=9) 
		g.create_dataset("passSR4J",  data=passSR4J,chunks=True,compression='gzip', compression_opts=9) 
		g.create_dataset("passSR5j",  data=passSR5J,chunks=True,compression='gzip', compression_opts=9) 
		g.create_dataset("weight",    data=weights,chunks=True)
		g.create_dataset("y", data=Y,chunks=True)


