import numpy as np
import h5py


SF=124675.506754
GenRPV     = 330599.
bkg = 3867.83848132
Lumi = 63670
xsecRPV     = 0.013
GenRPV     = 330599



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

# Re- calculate weight as Lumi * Xsec / Gen 
print(" ## --- Normalized weight --- ##")
print(w)
w[w!=1] = w[w!=1] * bkg * SF / GenRPV
w[w==1] = Lumi * xsecRPV / GenRPV
print(w)
print(" ")
y_true = y_true.flatten()

# -- Calculate Eff
print(" ## --- N of expected events in SR --- ##")
all_expected_evt = np.sum(w)
SR_expected_evt  = np.sum(w[(f['all_events']['passSRJ'][:] == 1)])


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



