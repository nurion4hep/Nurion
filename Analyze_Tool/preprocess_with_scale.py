import h5py
import numpy as np
import argparse

def get_parser():
	parser = argparse.ArgumentParser(
		description='Run SUSY RPV training',
		formatter_class=argparse.ArgumentDefaultsHelpFormatter
	)
	parser.add_argument('--nb-train-events', action='store', type=int, default=999999999,
		help='Number of events to train on.')

	parser.add_argument('--nb-test-events', action='store', type=int, default=999999999,
		help='Number of events to test on.')
	
	parser.add_argument('--train_out_name', action='store', type=str, default='Preprocessed_Train.h5',
		help='Output name for distributed train set.')
	
	parser.add_argument('--val_out_name', action='store', type=str, default='Preprocessed_Val.h5',
		help='Output name for distributed train set.')
	
	parser.add_argument('--test_out_name', action='store', type=str, default='Preprocessed_Test.h5',
		help='Output name for distributed train set.')

	parser.add_argument('--train_data', action='store', type=str,
		help='path to HDF5 file to train on')

	parser.add_argument('--val_data', action='store', type=str,
		help='path to HDF5 file to validate on')
	
	parser.add_argument('--test_data', action='store', type=str,
		help='path to HDF5 file to test on')

	parser.add_argument('--model', action='store', type=str,
		help='one of: "3ch-CNN", "CNN", "FCN", "BDT"')
	return parser

parser = get_parser()
args = parser.parse_args()



## --Parameter set
nb_train_events =  args.nb_train_events       
nb_test_events = args.nb_test_events		
modelName = args.model					#"3ch-CNN"  

## --Read data


##### Calculate Rescale factors ######
## -----------------------------------------------------##

##### Normed weight factors

print(" ######### Estimate Rescaling ######### ")
print(" #=========================================================# ")
print(" ")

Lumi = 63670
xsecRPV     = 0.013
xsecQCD700  = 6362
xsecQCD1000 = 1094
xsecQCD1500 = 99.16
xsecQCD2000 = 20.25

# Gen evts
GenRPV     = 330599
GenQCD700  = 129223
GenQCD1000 = 103319
GenQCD1500 = 127344
GenQCD2000 = 125664

# weight = xsec * lumi / Gen evts
QCD700  = xsecQCD700 * Lumi / GenQCD700
QCD1000 = xsecQCD1000 * Lumi / GenQCD1000
QCD1500 = xsecQCD1500 * Lumi / GenQCD1500
QCD2000 = xsecQCD2000 * Lumi / GenQCD2000
BKG_weight_sum  = QCD700 + QCD1000 + QCD1500 + QCD2000
print("## BKG weight sum {0}".format(BKG_weight_sum))

## Selected evts ( = # of DNN input )
Signal	   = GenRPV     
QCDsel700  = GenQCD700  
QCDsel1000 = GenQCD1000 
QCDsel1500 = GenQCD1500 
QCDsel2000 = GenQCD2000 

## Renorm target ( signal selected evts )
target = Signal

##### Calculate scalefactor

# 1. Make w_QCD700+w_QCD1000+w_QCD1500+w_QCD2000 = 1
w_QCD700  = QCD700  / BKG_weight_sum
w_QCD1000 = QCD1000 / BKG_weight_sum
w_QCD1500 = QCD1500 / BKG_weight_sum
w_QCD2000 = QCD2000 / BKG_weight_sum

print("####   Normlaize weights to 0 ~ 1 ##")
print("## Normalized weight: ",w_QCD700+w_QCD1000+w_QCD1500+w_QCD2000)
print(" ")

# 2. weight * selected evts
expQCD700  = w_QCD700  *QCDsel700
expQCD1000 = w_QCD1000 *QCDsel1000
expQCD1500 = w_QCD1500 *QCDsel1500
expQCD2000 = w_QCD2000 *QCDsel2000

print("####  Calculate expected evts ##")
print("#### Calcualte SF ##")
sf = expQCD700 + expQCD1000 + expQCD1500 +expQCD2000
print("--> SF: {0}".format(sf))
print(" ")

expQCD700   = float(expQCD700  /sf)
expQCD1000 = float(expQCD1000  /sf)
expQCD1500  = float(expQCD1500 /sf)
expQCD2000  = float(expQCD2000 /sf)

print("####  Normalize expected evts ##")
print("Normalized expected evts {0}".format(expQCD700+expQCD1000+expQCD1500+expQCD2000))

##### Effective weight
# ----------------------------------------------#

w_QCD700  = w_QCD700  / sf *target
w_QCD1000 = w_QCD1000 / sf *target
w_QCD1500 = w_QCD1500 / sf *target
w_QCD2000 = w_QCD2000 / sf *target


print("### training effective  weight ###")
print("QCD700:  {0}".format(w_QCD700))
print("QCD1000: {0}".format(w_QCD1000))
print("QCD1500: {0}".format(w_QCD1500))
print("QCD2000: {0}".format(w_QCD2000))
print(" ")

print("### Effective events ###")
Eff_QCD700  = w_QCD700  * QCDsel700
Eff_QCD1000 = w_QCD1000 * QCDsel1000
Eff_QCD1500 = w_QCD1500 * QCDsel1500
Eff_QCD2000 = w_QCD2000 * QCDsel2000

print("QCD700:  {0}".format(Eff_QCD700))
print("QCD1000: {0}".format(Eff_QCD1000))
print("QCD1500: {0}".format(Eff_QCD1500))
print("QCD2000: {0}".format(Eff_QCD2000))
print(" ")
print("### Sum of BKG effective evts(=signal selected evts)")
print(Eff_QCD700+Eff_QCD1000+Eff_QCD1500+Eff_QCD2000)
print(" ")
print("### Signal selected evts)")
print(target)
print(" ")





##### Start Rescaling ######
## -----------------------------------------------------##

# Initial weights (Fake)
Norm_sig = 827.71
Norm_QCD700 =  4.05068540e+08
Norm_QCD1000 = 69654980.
Norm_QCD1500 = 6313517.2
Norm_QCD2000 = 1289317.5

	#--Training
if (args.train_data != None):
	print(" ######### Start Rescaling..  ######### ")
	print(" #======================================================# ")
	print(" ")
	
	
	print(" ##### Start --> Training dataset #######" )
	data = h5py.File(args.train_data)
	print(list(data['all_events'].keys())) 
	images     = np.expand_dims(data['all_events']['hist'][:nb_train_events], -1)
	labels     = data['all_events']['y'][:nb_train_events]
	weights    = data['all_events']['weight'][:nb_train_events]
	
	# feature variables
	numJet     = data['all_events']['numJet'][:nb_train_events]
	numbJet    = data['all_events']['numbJet'][:nb_train_events]
	scalarHT   = data['all_events']['scalarHT'][:nb_train_events]
	sumFatJetM = data['all_events']['sumFatJetM'][:nb_train_events]
	
	# Shuffling
	NofData = data['all_events']['y'][:nb_train_events].shape[0]
	inds = np.arange(NofData)
	np.random.RandomState(11).shuffle(inds)
	images     = images[inds]
	labels     = labels[inds]
	weights    = weights[inds]
	numJet     = numJet[inds]
	numbJet    = numbJet[inds]
	scalarHT   = scalarHT[inds]
	sumFatJetM = sumFatJetM[inds]
	
	print('## Signal ##')
	print("Initial_RPV_weight: ",Norm_sig) 
	dim_sig=weights[np.where(weights[:]==Norm_sig)].shape
	weights[np.where(weights[:]==Norm_sig)]=np.ones(dim_sig)
	
	print("## QCD 700-1000 ##")
	print("Initial_QCD700_weight: ",Norm_QCD700) 
	dim_QCD700 = weights[np.where(np.around(weights[:],decimals=1)==Norm_QCD700)].shape
	weights[np.where(np.around(weights[:],decimals=1) == np.around(Norm_QCD700,decimals=1))] = np.ones(dim_QCD700)*w_QCD700
	
	print("## QCD 1000-1500 ##")
	print("Initial_QCD1000_weight: ",Norm_QCD1000) 
	dim_QCD1000 = weights[np.where(np.around(weights[:],decimals=1)==Norm_QCD1000)].shape
	weights[np.where(np.around(weights[:],decimals=1) == np.around(Norm_QCD1000,decimals=1))] = np.ones(dim_QCD1000)*w_QCD1000
	
	print("## QCD 1500-2000 ##")
	print("Initial_QCD_1500_weight: ",Norm_QCD1500) 
	dim_QCD1500 = weights[np.where(np.around(weights[:],decimals=1)==Norm_QCD1500)].shape
	weights[np.where(np.around(weights[:],decimals=1) == np.around(Norm_QCD1500,decimals=1))] = np.ones(dim_QCD1500)*w_QCD1500
	
	print("## QCD 2000-Inf ##")
	print("Initial_QCD_2000_weight: ",Norm_QCD2000) 
	dim_QCD2000 = weights[np.where(np.around(weights[:],decimals=1)==Norm_QCD2000)].shape
	weights[np.where(np.around(weights[:],decimals=3) == np.around(Norm_QCD2000,decimals=3))] = np.ones(dim_QCD2000)*w_QCD2000




	#--Validation
if (args.val_data != None):
	print(" ##### Start --> Validation dataset #######" )
	val = h5py.File(args.val_data)
	

	images_val = np.expand_dims(val['all_events']['hist'][:nb_test_events], -1)
	labels_val = val['all_events']['y'][:nb_test_events]
	weights_val = val['all_events']['weight'][:nb_test_events] 
	

	# feature variables
	numJet_val     = val['all_events']['numJet'][:nb_test_events]
	numbJet_val    = val['all_events']['numbJet'][:nb_test_events]
	scalarHT_val   = val['all_events']['scalarHT'][:nb_test_events]
	sumFatJetM_val = val['all_events']['sumFatJetM'][:nb_test_events]
	
	# Shuffling
	NofData = val['all_events']['y'][:nb_test_events].shape[0]
	inds = np.arange(NofData)
	np.random.RandomState(11).shuffle(inds)
	images_val     = images_val[inds]
	labels_val     = labels_val[inds]
	weights_val    = weights_val[inds]
	numJet_val     = numJet_val[inds]
	numbJet_val	   = numbJet_val[inds]
	scalarHT_val   = scalarHT_val[inds]
	sumFatJetM_val = sumFatJetM_val[inds]




	print('## Signal ##')
	print("Norm: ",Norm_sig) 
	dim_sig=weights_val[np.where(weights_val[:]==Norm_sig)].shape
	weights_val[np.where(weights_val[:]==Norm_sig)]=np.ones(dim_sig)
	
	print("## QCD 700-1000 ##")
	print("Norm: ",Norm_QCD700) 
	dim_QCD700 = weights_val[np.where(np.around(weights_val[:],decimals=1)==Norm_QCD700)].shape
	weights_val[np.where(np.around(weights_val[:],decimals=1) == np.around(Norm_QCD700,decimals=1))] = np.ones(dim_QCD700)*w_QCD700
	
	print("## QCD 1000-1500 ##")
	print("Norm: ",Norm_QCD1000) 
	dim_QCD1000 = weights_val[np.where(np.around(weights_val[:],decimals=1)==Norm_QCD1000)].shape
	weights_val[np.where(np.around(weights_val[:],decimals=1) == np.around(Norm_QCD1000,decimals=1))] = np.ones(dim_QCD1000)*w_QCD1000
	
	print("## QCD 1500-2000 ##")
	print("Norm: ",Norm_QCD1500) 
	dim_QCD1500 = weights_val[np.where(np.around(weights_val[:],decimals=1)==Norm_QCD1500)].shape
	weights_val[np.where(np.around(weights_val[:],decimals=1) == np.around(Norm_QCD1500,decimals=1))] = np.ones(dim_QCD1500)*w_QCD1500
	
	print("## QCD 2000-Inf ##")
	print("Norm: ",Norm_QCD2000) 
	dim_QCD2000 = weights_val[np.where(np.around(weights_val[:],decimals=1)==Norm_QCD2000)].shape
	weights_val[np.where(np.around(weights_val[:],decimals=3) == np.around(Norm_QCD2000,decimals=3))] = np.ones(dim_QCD2000)*w_QCD2000


	#--Test
if (args.test_data != None):
	print(" ##### Start --> Test dataset #######" )
	test = h5py.File(args.test_data)
	images_test  = np.expand_dims(test['all_events']['hist'][:nb_test_events], -1)
	labels_test  = test['all_events']['y'][:nb_test_events]
	weights_test = test['all_events']['weight'][:nb_test_events] 
	passSRJ =  test['all_events']['passSRJ'][:nb_test_events]
	
	# feature variables
	numJet_test     = test['all_events']['numJet'][:nb_test_events]
	numbJet_test    = test['all_events']['numbJet'][:nb_test_events]
	scalarHT_test   = test['all_events']['scalarHT'][:nb_test_events]
	sumFatJetM_test = test['all_events']['sumFatJetM'][:nb_test_events]
	
	# Shuffling
	NofData = test['all_events']['y'][:nb_test_events].shape[0]
	inds = np.arange(NofData)
	np.random.RandomState(11).shuffle(inds)
	images_test     = images_test[inds]
	labels_test     = labels_test[inds]
	weights_test    = weights_test[inds]
	numJet_test     = numJet_test[inds]
	numbJet_test	= numbJet_test[inds]
	scalarHT_test   = scalarHT_test[inds]
	sumFatJetM_test = sumFatJetM_test[inds]
	passSRJ = passSRJ[inds]
	
	print('## Signal ##')
	print("Norm: ",Norm_sig) 
	dim_sig=weights_test[np.where(weights_test[:]==Norm_sig)].shape
	weights_test[np.where(weights_test[:]==Norm_sig)]=np.ones(dim_sig)
	
	print("## QCD 700-1000 ##")
	print("Norm: ",Norm_QCD700) 
	dim_QCD700 = weights_test[np.where(np.around(weights_test[:],decimals=1)==Norm_QCD700)].shape
	weights_test[np.where(np.around(weights_test[:],decimals=1) == np.around(Norm_QCD700,decimals=1))] = np.ones(dim_QCD700)*w_QCD700
	
	print("## QCD 1000-1500 ##")
	print("Norm: ",Norm_QCD1000) 
	dim_QCD1000 = weights_test[np.where(np.around(weights_test[:],decimals=1)==Norm_QCD1000)].shape
	weights_test[np.where(np.around(weights_test[:],decimals=1) == np.around(Norm_QCD1000,decimals=1))] = np.ones(dim_QCD1000)*w_QCD1000
	
	print("## QCD 1500-2000 ##")
	print("Norm: ",Norm_QCD1500) 
	dim_QCD1500 = weights_test[np.where(np.around(weights_test[:],decimals=1)==Norm_QCD1500)].shape
	weights_test[np.where(np.around(weights_test[:],decimals=1) == np.around(Norm_QCD1500,decimals=1))] = np.ones(dim_QCD1500)*w_QCD1500
	
	print("## QCD 2000-Inf ##")
	print("Norm: ",Norm_QCD2000) 
	dim_QCD2000 = weights_test[np.where(np.around(weights_test[:],decimals=1)==Norm_QCD2000)].shape
	weights_test[np.where(np.around(weights_test[:],decimals=3) == np.around(Norm_QCD2000,decimals=3))] = np.ones(dim_QCD2000)*w_QCD2000
	



# -- 3ch-CNN case Merging
print(" ##### Start 3ch mergning #####" )
if modelName == '3ch-CNN':
	def add_channels(_images, _data, nb_events):
		layer_em = np.expand_dims(_data['all_events']['histEM'][:nb_events], -1)
		layer_track = np.expand_dims(_data['all_events']['histtrack'][:nb_events], -1)
		layer_em = layer_em / layer_em.max()
		layer_track = layer_track / layer_track.max()
		return np.concatenate((np.concatenate((_images,layer_em),axis=-1),layer_track),axis=-1)
	print("### 3ch merging")
	
	if (args.train_data != None):
		images 	  	= add_channels(images, data, nb_train_events)
	if (args.val_data != None):
		images_val  = add_channels(images_val, val, nb_test_events)
	if (args.test_data != None):
		images_test = add_channels(images_test, test, nb_test_events)
  	



print(" ##### Create hdf5 piles  #####" )
## -- Save the preprocessed data
if (args.train_data != None):
	print(" ## Create train.hdf5 ##" )
	with h5py.File("HEPdata_NEW/Merging_dir_forHT700bin/2020_sample/"+args.train_out_name,"w") as f:
		g=f.create_group("all_events")
		g.create_dataset("images", data=images,chunks=True,compression='gzip', compression_opts=9) ## Minimize output file size
		g.create_dataset("labels",data=labels,chunks=True)
		g.create_dataset("weights",data=weights,chunks=True)
		
		# Feature variables
		g.create_dataset("numJet" ,data=numJet ,chunks=True)
		g.create_dataset("numbJet" ,data=numbJet ,chunks=True)
		g.create_dataset("scalarHT" ,data=scalarHT ,chunks=True)
		g.create_dataset("sumFatJetM" ,data=sumFatJetM ,chunks=True)

if (args.val_data != None):
	print(" ## Create val.hdf5 ##" )
	with h5py.File("HEPdata_NEW/Merging_dir_forHT700bin/2020_sample/"+args.val_out_name,"w") as f:
		g=f.create_group("all_events")
		g.create_dataset("images_val", data=images_val,chunks=True,compression='gzip', compression_opts=9)
		g.create_dataset("labels_val",data=labels_val,chunks=True)
		g.create_dataset("weights_val",data=weights_val,chunks=True)
	
		# Feature variables
		g.create_dataset("numJet_val" ,data=numJet_val ,chunks=True)
		g.create_dataset("numbJet_val" ,data=numbJet_val ,chunks=True)
		g.create_dataset("scalarHT_val" ,data=scalarHT_val ,chunks=True)
		g.create_dataset("sumFatJetM_val" ,data=sumFatJetM_val ,chunks=True)

if (args.test_data != None):
	print(" ## Create test.hdf5 ##" )
	with h5py.File("HEPdata_NEW/Merging_dir_forHT700bin/2020_sample/"+args.test_out_name,"w") as f:
		g=f.create_group("all_events")
		g.create_dataset("images_val", data=images_test,chunks=True,compression='gzip', compression_opts=9)
		g.create_dataset("labels_val",data=labels_test,chunks=True)
		g.create_dataset("weights_val",data=weights_test,chunks=True)
		g.create_dataset("passSRJ",data=passSRJ,chunks=True)
		
		# Feature variables
		g.create_dataset("numJet_val" ,data=numJet_test ,chunks=True)
		g.create_dataset("numbJet_val" ,data=numbJet_test ,chunks=True)
		g.create_dataset("scalarHT_val" ,data=scalarHT_test ,chunks=True)
		g.create_dataset("sumFatJetM_val" ,data=sumFatJetM_test ,chunks=True)
