import h5py
import argparse
import numpy as np
from time import time
from tensorflow import keras
import matplotlib
matplotlib.use('Agg')
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from IPython.display import display









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


	if 'CNN' in args.model:
		from keras.layers import (Input, Conv2D, LeakyReLU,
			BatchNormalization, MaxPooling2D, Dropout, Dense, Flatten)
		from keras.models import Model
		from keras.callbacks import EarlyStopping, ModelCheckpoint

		x = Input(shape=(images.shape[1], images.shape[2], images.shape[3]))
		h = Conv2D(64, kernel_size=(3, 3), activation='relu', strides=1, padding='same')(x)
		h = BatchNormalization()(h)																																					 
		h = MaxPooling2D(pool_size=(2, 2))(h)																																		   
		h = Dropout(0.5)(h)				  
		h = Conv2D(128, kernel_size=(3, 3), activation='relu', strides=2, padding='same')(h)
		h = BatchNormalization()(h)																																					 
		h = MaxPooling2D(pool_size=(2, 2))(h)																																		   
		h = Dropout(0.5)(h)				  
		h = Conv2D(256, kernel_size=(3, 3), activation='relu', strides=1, padding='same')(h)
		h = BatchNormalization()(h)																																					 
		h = MaxPooling2D(pool_size=(2, 2))(h)
		h = Conv2D(256, kernel_size=(3, 3), activation='relu', strides=2, padding='same')(h)
		h = BatchNormalization()(h)		  
		h = Flatten()(h)
		h = Dense(512, activation='relu')(h)
		h = Dropout(0.5)(h)
		y = Dense(1, activation='sigmoid')(h)
		model = Model(
			inputs = x,
			outputs = y
		)
		model.summary()

		model.compile(
			optimizer='adam',
			loss='binary_crossentropy',
			metrics=['accuracy']
		)
	
		# ---Training monitering

		from keras.callbacks import LambdaCallback
		from keras.callbacks import CSVLogger
		csv_logger = CSVLogger('train_log.csv', append=True, separator=',')
		tb_hist = keras.callbacks.TensorBoard(log_dir='./graph', histogram_freq=0, write_graph=True, write_images=True)
		lambda_hist = keras.callbacks.LambdaCallback(on_epoch_begin=None, on_epoch_end=None, on_batch_begin=None, on_batch_end=None, on_train_begin=None, on_train_end=None)
	
	
		try:
			model.load_weights(model_weights)
			print 'Weights loaded from ' + model_weights
		except IOError:
			print 'No pre-trained weights found'
		try:
				model.fit(images, labels,
				batch_size = args.batch_size,
				sample_weight=weights,
				epochs=args.nb_epochs,
				verbose=1,
				callbacks = [
					EarlyStopping(verbose=True, patience=50, monitor='val_loss'),
					ModelCheckpoint(model_weights,
					monitor='val_loss', verbose=True, save_best_only=True),
					lambda_hist,
					tb_hist,
					csv_logger
					],
					validation_data=(images_val, labels_val, weights_val)
					#validation_data=(images_val, labels_val)
			)
		except KeyboardInterrupt:
			print 'Training finished early'

		model.load_weights(model_weights)
		yhat = model.predict(images_val, verbose=1, batch_size=args.batch_size)
	   # score = model.evaluate(images_val, labels_val, sample_weight=weights_val, verbose=1)
	   # print 'Validation loss:', score[0]
	   # print 'Validation accuracy:', score[1]
		np.save(predictions_file, yhat)


