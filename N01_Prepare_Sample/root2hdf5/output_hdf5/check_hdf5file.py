import h5py
import numpy as np
import sys
import argparse
parser = argparse.ArgumentParser()

parser.add_argument('path', type=str,
            help="import filepath")

args = parser.parse_args()
data=h5py.File(args.path)

print(list(data["all_events"].keys()))


hist          = data['all_events']['hist'][:]
histEM        = data['all_events']['histEM'][:]
histhisttrack = data['all_events']['histtrack'][:]
numJet        = data['all_events']['numJet'][:]
numbJet       = data['all_events']['numbJet'][:]
passSRJ       = data['all_events']['passSRJ'][:]
scalarHT      = data['all_events']['scalarHT'][:]
sumFatJetM    = data['all_events']['sumFatJetM'][:]
weight        = data['all_events']['weight'][:]


print("HCAL:  {0}".format(hist.shape))
print("ECAL:  {0}".format(histEM.shape))
print("Track: {0}".format(histhisttrack.shape))
print("numJet: {0}".format(numJet.shape))
print("numbJet: {0}".format(numbJet.shape))
print("passSRJ: {0}".format(passSRJ.shape))
print(passSRJ)
print("ScalarHT: {0}".format(scalarHT.shape))
print(scalarHT)
print("SumFatJetM: {0}".format(sumFatJetM.shape))
print("weight: {0}".format(weight.shape))

