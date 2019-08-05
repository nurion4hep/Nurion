import h5py
import numpy as np
import argparse

def get_parser():
	parser = argparse.ArgumentParser(
		description='Run SUSY RPV training',
		formatter_class=argparse.ArgumentDefaultsHelpFormatter
	)
	parser.add_argument('--nb-train-events', action='store', type=int, default=1000,
		help='Number of events to train on.')

	parser.add_argument('--nb-test-events', action='store', type=int, default=999999999,
		help='Number of events to test on.')

	parser.add_argument('train_data', action='store', type=str,
		help='path to HDF5 file to train on')

	parser.add_argument('val_data', action='store', type=str,
		help='path to HDF5 file to validate on')

	parser.add_argument('model', action='store', type=str,
		help='one of: "3ch-CNN", "CNN", "FCN", "BDT"')
	return parser

parser = get_parser()
args = parser.parse_args()



## --Parameter set
nb_train_events =  args.nb_train_events       #20000
nb_test_events = args.nb_test_events		#1000
modelName = args.model					#"3ch-CNN"  

## --Read data
	#--Training
data = h5py.File(args.train_data)
print(list(data['all_events'].keys())) 
images = np.expand_dims(data['all_events']['hist'][:nb_train_events], -1)
labels = data['all_events']['y'][:nb_train_events]
weights = data['all_events']['weight'][:nb_train_events]
weights = np.log(weights+1) ## --Log weighted
	#--Validation
val = h5py.File(args.val_data)
images_val = np.expand_dims(val['all_events']['hist'][:nb_test_events], -1)
labels_val = val['all_events']['y'][:nb_test_events]
weights_val = val['all_events']['weight'][:nb_test_events] 

print("### images ###")
print(images.shape)
print(images_val.shape)

print("### Labels ###")
print(labels.shape)
print(labels_val.shape)

print("### Weight ###")
print(weights.shape)
print(weights_val.shape)

## -- 3ch-CNN case Merging
if modelName == '3ch-CNN':
	def add_channels(_images, _data, nb_events):
		layer_em = np.expand_dims(_data['all_events']['histEM'][:nb_events], -1)
		layer_track = np.expand_dims(_data['all_events']['histtrack'][:nb_events], -1)
		layer_em = layer_em / layer_em.max()
		layer_track = layer_track / layer_track.max()
		return np.concatenate((np.concatenate((_images,layer_em),axis=-1),layer_track),axis=-1)
	print("### 3ch merging")
	
	images = add_channels(images, data, nb_train_events)
  	images_val = add_channels(images_val, val, nb_test_events)
  	
	print("### images ###")
  	print(images.shape)
  	print(images_val.shape)

  	print("### Labels ###")
  	print(labels.shape)
  	print(labels_val.shape)

  	print("### Weight ###")
  	print(weights.shape)
  	print(weights_val.shape)

## -- Save the preprocessed data
with h5py.File("Preprocessed_Train.h5","w") as f:
	g=f.create_group("all_events")
	g.create_dataset("images", data=images,chunks=True,compression='gzip', compression_opts=9) ## Minimize output file size
	g.create_dataset("labels",data=labels,chunks=True)
	g.create_dataset("weights",data=weights,chunks=True)

with h5py.File("Preprocessed_Val.h5","w") as f:
	g=f.create_group("all_events")
	g.create_dataset("images_val", data=images_val,chunks=True,compression='gzip', compression_opts=9)
	g.create_dataset("labels_val",data=labels_val,chunks=True)
	g.create_dataset("weights_val",data=weights_val,chunks=True)
## -- Check

print("### Check the saved data ###")
hh = h5py.File("Preprocessed_Train.h5")
print("## Preprocessed_Train.h5 open ##")
print(list(hh.keys()))
print(hh["all_events"]["images"].shape)
hh.close()

hh = h5py.File("Preprocessed_Val.h5")
print("## Preprocessed_Val.h5 open ##")
print(list(hh.keys()))
print(hh["all_events"]["images_val"].shape)
hh.close()





