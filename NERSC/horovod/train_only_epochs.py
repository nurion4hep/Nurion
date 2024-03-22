import h5py
import argparse
import numpy as np
import os
import errno
import tensorflow as tf
import numpy as np
from tensorflow import keras
import math
from tensorflow.keras import layers
import sys
sys.modules['keras'] = keras
import horovod.tensorflow.keras as hvd



def get_parser():
	parser = argparse.ArgumentParser(
		description='Run SUSY RPV training',
		formatter_class=argparse.ArgumentDefaultsHelpFormatter
	)
	parser.add_argument('--nb-epochs', action='store', type=int, default=50,
						help='Number of epochs to train for.')

	parser.add_argument('--nb-train-events', action='store', type=int, default=1000,
						help='Number of events to train on.')
	
	parser.add_argument('--nb-test-events', action='store', type=int, default=999999999,
						help='Number of events to test on.')

	parser.add_argument('--batch-size', action='store', type=int, default=256,
						help='batch size per update')

	parser.add_argument('train_data', action='store', type=str,
						help='path to HDF5 file to train on')

	parser.add_argument('val_data', action='store', type=str,
						help='path to HDF5 file to validate on')

	parser.add_argument('model', action='store', type=str,
						help='one of: "3ch-CNN", "CNN", "FCN", "BDT"')

	return parser

if __name__ == '__main__':
	parser = get_parser()
	args = parser.parse_args()

	# -- check that model makes sense:
	if args.model not in ['3ch-CNN', 'CNN', 'FCN', 'BDT']:
		raise ValueError("The model type needs to be one of '3ch-CNN', 'CNN', 'FCN', 'BDT'.")
	
	### Horovod:  init
	hvd.init()
	
	# Horovod: pin GPU to be used to process local rank (one GPU per process)
	config = tf.ConfigProto()
	config.gpu_options.allow_growth = True
	config.gpu_options.visible_device_list = str(hvd.local_rank())
	config.intra_op_parallelism_threads = 64
	config.inter_op_parallelism_threads = 1
	keras.backend.set_session(tf.Session(config=config))

	print("horovod: hvdsize: ",hvd.size())

	# -- load data:
	print("############## LOAD DATA ###################")
	data 	= h5py.File(args.train_data)
	images 	= data['all_events']['images'][:args.nb_train_events]
	labels 	= data['all_events']['labels'][:args.nb_train_events]
	weights	= data['all_events']['weights'][:args.nb_train_events]
	val 		= h5py.File(args.val_data)
	images_val 	= val['all_events']['images_val'][:args.nb_test_events]
	labels_val 	= val['all_events']['labels_val'][:args.nb_test_events]
	weights_val = val['all_events']['weights_val'][:args.nb_test_events]  

	
	
	# -- output file names
	model_weights = 'model_weights_log_' + args.model + '.h5'
	predictions_file = 'prediction_nn_log_' + args.model + '.pyc'

	if args.model == 'BDT':
		from sklearn.ensemble import GradientBoostingClassifier
		from sklearn.model_selection import GridSearchCV
		base_clf = GradientBoostingClassifier(verbose=2)
		parameters = {
			'n_estimators': [50, 100],
			'max_depth':[3, 5]
		}
		clf = GridSearchCV(base_clf, parameters, n_jobs=4, fit_params={'sample_weight': weights})
		clf.fit(images.reshape(images.shape[0], -1), labels)
		yhat = clf.predict_proba(images_val.reshape(images_val.shape[0], -1))
		np.save(predictions_file, yhat)

	elif 'CNN' in args.model:
		
			
		x = layers.Input(shape=(images.shape[1], images.shape[2], images.shape[3]))
		h = layers.Conv2D(64, kernel_size=(3, 3), activation='relu', strides=1, padding='same')(x)
		h = layers.BatchNormalization()(h)																																					 
		h = layers.MaxPooling2D(pool_size=(2, 2))(h)																																		   
		h = layers.Dropout(0.5)(h)				  
		h = layers.Conv2D(128, kernel_size=(3, 3), activation='relu', strides=2, padding='same')(h)
		h = layers.BatchNormalization()(h)																																					 
		h = layers.MaxPooling2D(pool_size=(2, 2))(h)																																		   
		h = layers.Dropout(0.5)(h)				  
		h = layers.Conv2D(256, kernel_size=(3, 3), activation='relu', strides=1, padding='same')(h)
		h = layers.BatchNormalization()(h)																																					 
		h = layers.MaxPooling2D(pool_size=(2, 2))(h)
		h = layers.Conv2D(256, kernel_size=(3, 3), activation='relu', strides=2, padding='same')(h)
		h = layers.BatchNormalization()(h)		  
		h = layers.Flatten()(h)
		h = layers.Dense(512, activation='relu')(h)
		h = layers.Dropout(0.5)(h)
		y = layers.Dense(1, activation='sigmoid')(h)
		model = tf.keras.Model(
			inputs = x,
			outputs = y
		)
		model.summary()
		
		

		# Horovod: Set epoch and distributed optimizer
		nb_epochs = int(math.ceil(args.nb_epochs / hvd.size()))
		opt = tf.keras.optimizers.Adam(0.001 * hvd.size())
		opt = hvd.DistributedOptimizer(opt)
		batch_size=args.batch_size
	



		model.compile(
			optimizer=opt,
			loss='binary_crossentropy',
			metrics=['accuracy']
		)

		from keras.callbacks import CSVLogger
		csv_logger = CSVLogger('train_log.csv', append=True, separator=',')
		tb_hist = keras.callbacks.TensorBoard(log_dir='./graph', histogram_freq=0, write_graph=True, write_images=True)
		
		callbacks=[
		hvd.callbacks.BroadcastGlobalVariablesCallback(0),
		tf.keras.callbacks.EarlyStopping(verbose=True, patience=20, monitor='val_loss'),
		keras.callbacks.LambdaCallback(on_epoch_begin=None, on_epoch_end=None, on_batch_begin=None, on_batch_end=None, on_train_begin=None, on_train_end=None)
		]
		
		if hvd.rank()==0:
			callbacks.append(tf.keras.callbacks.ModelCheckpoint('./checkpoint-{epoch}.h5'))
			callbacks.append(tf.keras.callbacks.ModelCheckpoint(model_weights,monitor='val_loss', verbose=True, save_best_only=True))
			callbacks.append(csv_logger)
			callbacks.append(tb_hist)

			#callbacks.append(tb_hist)
		
		
	
		try:
			model.load_weights(model_weights)
			print('Weights loaded from ' + model_weights)
		except IOError:
			print('No pre-trained weights found')
		try:
			model.fit(images, labels,
					  batch_size=batch_size,
					  sample_weight=weights,
					  epochs=nb_epochs,
					  verbose=1,
					  callbacks = callbacks,
					  validation_data=(images_val, labels_val, weights_val)
			)
		except KeyboardInterrupt:
			print('Training finished early')

		model.load_weights(model_weights)
		yhat = model.predict(images_val, verbose=1, batch_size=args.batch_size)
	   # score = model.evaluate(images_val, labels_val, sample_weight=weights_val, verbose=1)
	   # print 'Validation loss:', score[0]
	   # print 'Validation accuracy:', score[1]
		np.save(predictions_file, yhat)

