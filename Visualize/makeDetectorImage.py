#!/usr/bin/env python3
import argparse
import h5py
import numpy as np
import sys
import uproot
from glob import glob
from math import ceil
import numba
import numpy, numba, awkward, awkward.numba

if sys.version_info[0] < 3: sys.exit()

parser = argparse.ArgumentParser()
parser.add_argument('input', nargs='+', action='store', type=str, help='input file names')
parser.add_argument('-o', '--output', action='store', type=str, help='output file name', required=True)
parser.add_argument('-n', '--nevent', action='store', type=int, default=-1, help='number of events to preprocess')
parser.add_argument('--width', action='store', type=int, default=224, help='image width, along eta')
parser.add_argument('--height', action='store', type=int, default=224, help='image height, along phi')
parser.add_argument('--format', action='store', choices=('NHWC', 'NCHW'), default='NCHW', help='image format for output (NHWC for TF default, NCHW for pytorch default)')
parser.add_argument('-c', '--chunk', action='store', type=int, default=1, help='chunk size')
parser.add_argument('--compress', action='store', choices=('gzip', 'lzf', 'none'), default='none', help='compression algorithm')
parser.add_argument('-d', '--debug', action='store_true', default=False, help='debugging')
parser.add_argument('--precision', action='store', type=int, choices=(8,16,32,64), default=32, help='Precision')
parser.add_argument('--dotrackcount', action='store_true', default=False, help='Choose track count for the 3rd channel, rather than the track pt')
parser.add_argument('--mc', action='store_true', default=True, help='flag to set MC sample')
args = parser.parse_args()

###################################################################################################

@numba.njit(nogil=True, fastmath=True, parallel=True)
def selectBaselineCuts(src_fjets_pt, src_fjets_eta, src_fjets_mass,
					   src_jets_pt, src_jets_eta, src_jets_btag):
	nEvent = int(len(src_fjets_pt))
	selEvents = []

	prange = numba.prange
	for ievt in prange(nEvent):
		selJets = (src_jets_pt[ievt] > 30) & (np.fabs(src_jets_eta[ievt]) < 2.4)
		if selJets.sum() < 4: continue ## require nJets >= 4
		ht = (src_jets_pt[ievt][selJets]).sum()
		if ht < 1500: continue ## require HT >= 1500

		selBJets = (src_jets_btag[ievt][selJets] > 0.5)
		if selBJets.sum() < 1: continue ## require nBJets >= 1

		selFjets = (src_fjets_pt[ievt] > 30)
		sumFjetsMass = (src_fjets_mass[ievt][selFjets]).sum()
		if sumFjetsMass < 500: continue ## require sum(FatJetMass) >= 500

		selEvents.append(ievt)

	return np.array(selEvents, dtype=np.dtype('int64'))

###################################################################################################

#@numba.njit(nogil=True, fastmath=True, parallel=True)
## note: numba does not support np.histogram2d. sad...
def getImage(pts, etas, phis, bins):
	xlim = [-2.5, 2.5]
	ylim = [-3.141593, 3.141593]

	hs = []
	for i in range(len(etas)):
		h = np.histogram2d(etas[i], phis[i], weights=pts[i], bins=bins, range=[xlim, ylim])
		hs.append(h[0])

	return np.stack(hs)

###################################################################################################

class FileSplitOut:
	def __init__(self, maxEvent, args):
		self.maxEvent = maxEvent

		self.chunkSize = args.chunk
		self.debug = args.debug

		self.height = args.height
		self.width = args.width
		if args.format == 'NHWC': ## TF default
			self.shape = [self.height, self.width, 3]
			self.each_shape = [self.height, self.width]
			self.chAxis = -1
		else: ## pytorch default
			self.shape = [3, self.height, self.width]
			self.each_shape = [self.height, self.width]
			self.chAxis = 1

		precision = 'f%d' % (args.precision//8)
		self.kwargs = {'dtype':precision}
		if args.compress == 'gzip':
			self.kwargs.update({'compression':'gzip', 'compression_opts':9})
		elif args.compress == 'lzf':
			self.kwargs.update({'compression':'lzf'})

		if not args.output.endswith('.h5'): self.prefix, self.suffix = args.output+'/data', '.h5'
		else: self.prefix, self.suffix = args.output.rsplit('.', 1)

		self.nOutFile = 0
		self.nOutEvent = 0

		self.initOutput()

	def initOutput(self):
		## Build placeholder for the output
		self.weights = np.ones(0)
		self.images = np.ones([0,*self.shape])
		self.HCAL = np.ones([0,*self.each_shape])
		self.ECAL = np.ones([0,*self.each_shape])
		self.TRACK = np.ones([0,*self.each_shape])

	def addEvents(self, src_weights,
				  src_tracks_pt, src_tracks_eta, src_tracks_phi,
				  src_towers_eta, src_towers_phi, src_towers_Eem, src_towers_Ehad):
		nSrcEvent = len(src_weights)
		begin = 0
		while begin < nSrcEvent:
			end = min(nSrcEvent, begin+self.maxEvent-len(self.weights))
			self.nOutEvent += (end-begin)
			print("%d events processed..." % (self.nOutEvent), end='\r')

			self.weights = np.concatenate([self.weights, src_weights[begin:end]])

			images_h = getImage(src_towers_Ehad[begin:end], src_towers_eta[begin:end], src_towers_phi[begin:end], [self.width, self.height])
			images_e = getImage(src_towers_Eem[begin:end], src_towers_eta[begin:end], src_towers_phi[begin:end], [self.width, self.height])
			images_t = getImage(src_tracks_pt[begin:end], src_tracks_eta[begin:end], src_tracks_phi[begin:end], [self.width, self.height])
			
			images_h = 1000 * images_h
			images_e = 1000 * images_e
			if not args.dotrackcount: images_t = 1000 * images_t


			#images_h = np.expand_dims(images_h, self.chAxis)
			#images_e = np.expand_dims(images_e, self.chAxis)
			#images_t = np.expand_dims(images_t, self.chAxis)

	
			self.HCAL    = np.concatenate([self.HCAL, images_h])
			self.ECAL    = np.concatenate([self.ECAL, images_e])
			self.TRACK   = np.concatenate([self.TRACK, images_t])

			if len(self.weights) == self.maxEvent: self.flush()
			begin = end

	def flush(self):
		self.save()
		self.initOutput()

	def save(self):
		fName = "%s_%d.h5" % (self.prefix, self.nOutFile)
		nEventToSave = len(self.weights)
		if nEventToSave == 0: return
		if self.debug: print("Writing output file %s..." % fName, end='')

		chunkSize = min(self.chunkSize, nEventToSave)
		with h5py.File(fName, 'w', libver='latest', swmr=True) as outFile:
			g = outFile.create_group('all_events')
			g.create_dataset('weights', data=self.weights, chunks=(chunkSize,), dtype='f4')
			g.create_dataset('HCAL' , data=self.HCAL , chunks=(chunkSize,*self.each_shape), **self.kwargs)
			g.create_dataset('ECAL' , data=self.ECAL , chunks=(chunkSize,*self.each_shape), **self.kwargs)
			g.create_dataset('TRACK' , data=self.TRACK , chunks=(chunkSize,*self.each_shape), **self.kwargs)
			if self.debug: print("  done")

		self.nOutFile += 1

		if self.debug:
			with h5py.File(fName, 'r', libver='latest', swmr=True) as outFile:
				print("  created %s %dth file" % (fName, self.nOutFile), end='')
				print("  keys=", list(outFile['all_events'].keys()))
				print("  weights=", outFile['all_events/weights'].shape, end='')
				print("  shapeHC=", outFile['all_events/HCAL'].shape)
				print("  shapeEC=", outFile['all_events/ECAL'].shape)
				print("  shapeTR=", outFile['all_events/TRACK'].shape)

###################################################################################################

import os

## Find root files with corresponding trees
print("@@@ Checking input files... (total %d files)" % (len(args.input)))
nEventTotal = 0
nEvent0s = []
srcFileNames = []
for x in args.input:
	for fName in glob(x):
		if not fName.endswith('.root'): continue
		if os.stat(fName).st_size == 0: continue
		f = uproot.open(fName)
		if "Delphes" not in f: continue
		tree = f["Delphes"]
		if tree == None: continue

		if args.debug and nEventTotal == 0:
			print("-"*40)
			print("\t".join([str(key) for key in tree.keys()]))
			print("\t".join([str(key) for key in tree["Jet"].keys()]))
			print("-"*40)

		srcFileNames.append(fName)
		nEvent0 = len(tree)
		nEvent0s.append(nEvent0)
		nEventTotal += nEvent0
nEventOutFile = min(nEventTotal, args.nevent) if args.nevent >= 0 else nEventTotal

fileOuts = FileSplitOut(nEventOutFile, args)

print("@@@ Start processing...")
weightName = None if args.mc else "Weight"
for nEvent0, srcFileName in zip(nEvent0s, srcFileNames):
	if args.debug: print("@@@ Open file", srcFileName)
	## Open data files
	fin = uproot.open(srcFileName)
	tree = fin["Delphes"]

	## Load objects
	src_weights = np.ones(nEvent0) if weightName == None else tree[weightName]
	src_jets_eta = tree["Jet"]["Jet.Eta"].array()
	src_jets_phi = tree["Jet"]["Jet.Phi"].array()

	## Apply event selection in this file
	src_fjets_pt   = tree["FatJet"]["FatJet.PT"].array()
	src_fjets_eta  = tree["FatJet"]["FatJet.Eta"].array()
	src_fjets_mass = tree["FatJet"]["FatJet.Mass"].array()
	src_jets_pt   = tree["Jet"]["Jet.PT"].array()
	src_jets_btag = tree["Jet"]["Jet.BTag"].array()
	selEvent = selectBaselineCuts(src_fjets_pt, src_fjets_eta, src_fjets_mass,
								  src_jets_pt, src_jets_eta, src_jets_btag)

	## Load tracks and calo towers
	src_tracks_pt   = tree["Track"]["Track.PT"].array()
	src_tracks_eta  = tree["Track"]["Track.Eta"].array()
	src_tracks_phi  = tree["Track"]["Track.Phi"].array()
	src_towers_et   = tree["Tower"]["Tower.ET"].array()
	src_towers_eta  = tree["Tower"]["Tower.Eta"].array()
	src_towers_phi  = tree["Tower"]["Tower.Phi"].array()
	src_towers_Eem  = tree["Tower"]["Tower.Eem"].array()
	src_towers_Ehad = tree["Tower"]["Tower.Ehad"].array()

	## Apply event selection
	src_weights	 = src_weights[selEvent]
	src_tracks_pt   = src_tracks_pt[selEvent]
	src_tracks_eta  = src_tracks_eta[selEvent]
	src_tracks_phi  = src_tracks_phi[selEvent]
	#src_towers_et   = src_towers_et[selEvent]
	src_towers_eta  = src_towers_eta[selEvent]
	src_towers_phi  = src_towers_phi[selEvent]
	src_towers_Eem  = src_towers_Eem[selEvent]
	src_towers_Ehad = src_towers_Ehad[selEvent]

	## Save output
	if args.dotrackcount: src_tracks_pt = [None]*len(src_tracks_pt)
	fileOuts.addEvents(src_weights, src_tracks_pt, src_tracks_eta, src_tracks_phi,
					   src_towers_eta, src_towers_phi, src_towers_Eem, src_towers_Ehad)

## save remaining events
fileOuts.flush()

print("@@@ Finished processing")
print("	Number of input files   =", len(srcFileNames))
print("	Number of input events  =", nEventTotal)
print("	Number of output files  =", fileOuts.nOutFile)
print("	Number of output events =", fileOuts.nOutEvent)

###################################################################################################

