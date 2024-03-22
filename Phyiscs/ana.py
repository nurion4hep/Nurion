import uproot # for uproot4



import glob
import awkward as ak
from numba import jit
import numpy as np
from tqdm import tqdm

import time
start_time = time.time()

# using file list
f = open('file_list')
file_list = [line.rstrip() for line in f]

# using glob
#dir_path = "/x4/cms/dylee/Delphes/data/Storage/Second_data/root/signal/condorDelPyOut/*.root"
#file_list = glob.glob(dir_path)



# for uproot4
flist=[]
for f in file_list:
	flist.append(f + ':Delphes')




branches = ["Jet.PT","Jet.Eta","Jet.Phi","Jet.T","Jet.BTag","FatJet.PT","FatJet.Mass","ScalarHT.HT"]




#@jit # for future developer...
def Loop(file_list):

	# define array
	histo={}

	# --Start File Loop
	for arrays in uproot.iterate(flist,branches): #  for Uproot4

		print(len(arrays))
		Jet = ak.zip({
		    "PT"        : arrays["Jet.PT"],
		    "Eta"       : arrays["Jet.Eta"],
		    "Phi"       : arrays["Jet.Phi"],
		    "T"         : arrays["Jet.T"],
		    "BTag"          : arrays["Jet.BTag"],
		})

		FatJet = ak.zip({
		    "PT"        : arrays["FatJet.PT"],
		    "Mass"          : arrays["FatJet.Mass"],
		})


		HT = arrays["ScalarHT.HT"]

		# Jet definition
		Jet_sel_mask = (abs(Jet.Eta)  <=2.4)  & (Jet.PT > 30)
		Jet			 = Jet[Jet_sel_mask]
		Jet_evt_sel_mask = ak.num(Jet) > 0

		Jet          = Jet[Jet_evt_sel_mask]
		HT		     = HT[Jet_evt_sel_mask]
		FatJet       = FatJet[Jet_evt_sel_mask]

		# FatJet definition
		FatJet_sel_mask = FatJet.PT > 30
		FatJet          = FatJet[FatJet_sel_mask]
		FatJet_evt_sel_mask = ak.num(FatJet) > 0

		FatJet = FatJet[FatJet_evt_sel_mask]
		Jet = Jet[FatJet_evt_sel_mask]
		HT = HT[FatJet_evt_sel_mask]

		
		

		# Baseline selection
		njet_mask = ak.num(Jet) >= 4
		HT_mask   = ak.flatten(HT >= 1500)
		btag_mask = ak.sum(Jet.BTag,axis=1) >= 1
		FatJetmass_mask =  ak.sum(FatJet.Mass,axis=-1) >= 500
				
		Baseline_mask = njet_mask & HT_mask & btag_mask & FatJetmass_mask
		
		Jet_sel    = Jet[Baseline_mask]
		HT_sel     = HT[Baseline_mask]
		FatJet_sel = FatJet[Baseline_mask]

		print(Jet_sel.Eta)
		print(Jet_sel.Phi)

		h_jet_eta = ak.to_numpy(ak.flatten(Jet_sel.Eta))
		h_jet_phi = ak.to_numpy(ak.flatten(Jet_sel.Phi))
		
		if len(histo) == 0:
			histo['Jet_eta'] = h_jet_eta
			histo['Jet_phi'] = h_jet_phi
		else:
			 histo['Jet_eta'] = np.concatenate(histo['Jet_eta'],h_jet_eta,axis=0)
			 histo['Jet_phi'] = np.concatenate(histo['Jet_phi'],h_jet_phi,axis=0)
	
		return histo

histo = Loop(file_list)

print(histo)
print("--- %s seconds ---" % (time.time() - start_time))
