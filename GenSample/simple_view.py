import h5py
import numpy as np
import sys
import argparse
parser = argparse.ArgumentParser()

parser.add_argument('path', type=str,
            help="import filepath")

args = parser.parse_args()

#data=h5py.File("test_output.h5")


data=h5py.File(args.path)

#print("#### all_event branches #####")
#print(list(data["all_events"].keys()))

np.set_printoptions(threshold=sys.maxsize)

hist		  = data['all_events']['hist'][:]
histEM		  = data['all_events']['histEM'][:]
histhisttrack = data['all_events']['histtrack'][:]
numJet		  = data['all_events']['numJet'][:]
numbJet		  = data['all_events']['numbJet'][:]
passSRJ		  = data['all_events']['passSRJ'][:]
scalarHT	  = data['all_events']['scalarHT'][:]
sumFatJetM	  = data['all_events']['sumFatJetM'][:]
weight		  = data['all_events']['weight'][:]


print(hist.shape)
#print(histEM.shape) 		 
#print(histhisttrack.shape)
#print(numJet.shape) 		 
#print(numbJet.shape) 		 
#print(passSRJ.shape) 		 
#print(scalarHT.shape)	 
#print(sumFatJetM.shape)	 
#print(weight.shape)		 
