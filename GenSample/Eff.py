import numpy as np
import h5py

Lumi = 63670
xsecRPV     = 0.013
bkg = 3867.83848132


## CMS cut
GenRPV     = 330599.
SF=124675.506754


## --NERSC cut noPU
SelRPV = 294554
SF = 2560.86981306


## --NERSC cut 32PU
#SelRPV = 297263
#SF = 2958.0861464

#target = GenRPV # for CMS cut
target = SelRPV  # for NERSC cut


infile="Preprocessed_Test.h5"
f = h5py.File(infile)
	
print(" ### -- Start {0} --- ### ".format(infile))
print(" #--------------------------------------#")
print(" ")
#print(f['all_events'].keys())
#print(f['all_events']['labels_val'][:].shape)
#print(f['all_events']['weights_val'][:].shape)

y_true = f['all_events']['labels_val'][:] 
w = f['all_events']['weights_val'][:]

# Re- calculate weight as Lumi * Xsec / target
print(" ## --- Normalized weight --- ##")
print(w)
w[w!=1] = w[w!=1] * bkg * SF / target
w[w==1] = Lumi * xsecRPV / target
print(w)
print(" ")
y_true = y_true.flatten()

# -- Calculate Eff
print(" ## --- N of expected events in SR --- ##")
all_expected_evt = np.sum(w)

#SR_expected_evt  = np.sum(w[(f['all_events']['passSRJ'][:] == 1)])
SR_expected_evt  = np.sum(w[(f['all_events']['passSR'][:] == 1)])


eff = SR_expected_evt / all_expected_evt
print("All expected evts: ",all_expected_evt)
print("SR expected evts: ",SR_expected_evt)
print(" Eff: {0} / {1} = {2}".format(SR_expected_evt,all_expected_evt,eff))
print(" ")


# -- Calculate TPR, FPR
print(" ## --- TPR and FPR  --- ##")
TPR = np.sum(w[(f['all_events']['passSRJ'][:] == 1) & (y_true == 1)]) / np.sum(w[y_true==1])
FPR = np.sum(w[(f['all_events']['passSRJ'][:] == 1) & (y_true == 0)]) / np.sum(w[y_true==0])
	
print("TPR: ",TPR)
print("FPR: ",FPR)
print(" ")



