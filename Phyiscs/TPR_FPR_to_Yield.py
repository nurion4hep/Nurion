TPR = 0.0035026281059025704
FPR = 0.3745928891301398


Lumi  = 63.67 * 1000



N_sig = 294762 * 0.0252977 * Lumi / 330599.
N_HT1000 = 37091 * 1207 * Lumi / 15466225.
N_HT1500 = 137805 * 119.9 * Lumi / 3368613.
N_HT2000 = 280279 * 25.24 * Lumi / 3250016.

N_bkg = N_HT1000 + N_HT1500 + N_HT2000
N_all = N_sig + N_bkg


TP = TPR * N_sig
FP = FPR * N_bkg

Signal_region = TP + FP
BKG_region = N_all -  Signal_region


print("N_sig",N_sig)
print("N_bkg",N_bkg)
print("N_all",N_all)
print("TP",TP)
print("FP",FP)
print("# of Signal_region ",Signal_region)
print("# of BKG_region ",BKG_region)
