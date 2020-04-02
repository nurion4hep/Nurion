

##### Normed weight factors
# ----------------------------------------------#

# weight = xsec * lumi / Gen evts
QCD700  = 8.57213705
QCD1000 = 38.7232
QCD1500 = 8.4115
QCD2000 = 2.1424
BKG = QCD700 + QCD1000 + QCD1500 + QCD2000
print("## BKG weight sum {0}".format(BKG))

## Selected evts ( = # of DNN input )
Signal = 311924
QCDsel700  = 127081
QCDsel1000 = 134774
QCDsel1500 = 133963
QCDsel2000 = 127669 

## Renorm target ( signal selected evts )
target = Signal


##### Calculate scalefactor
# ----------------------------------------------#

# 1. Make w_QCD700+w_QCD1000+w_QCD1500+w_QCD2000 = 1
w_QCD700  = QCD700  / BKG  
w_QCD1000 = QCD1000 / BKG  
w_QCD1500 = QCD1500 / BKG  
w_QCD2000 = QCD2000 / BKG  

print("####   Normlaize weights to 0 ~ 1 ##")
print("## Normalized weight: ",w_QCD700+w_QCD1000+w_QCD1500+w_QCD2000)
print(" ")

# 2. weight * selected evts 
expQCD700  = w_QCD700  *QCDsel700 
expQCD1000 = w_QCD1000 *QCDsel1000
expQCD1500 = w_QCD1500 *QCDsel1500
expQCD2000 = w_QCD2000 *QCDsel2000

print("####  Calculate expected evts ##")
print("#### Calcualte SF ##")
sf = expQCD700 + expQCD1000 + expQCD1500 +expQCD2000
print("--> SF: {0}".format(sf))  
print(" ")

expQCD700   = float(expQCD700  /sf)
expQCD1000 = float(expQCD1000  /sf)
expQCD1500  = float(expQCD1500 /sf) 
expQCD2000  = float(expQCD2000 /sf)

print("####  Normalize expected evts ##")
print("Normalized expected evts {0}".format(expQCD700+expQCD1000+expQCD1500+expQCD2000))
print(" ")
# SF: 133252.99586385902


##### Show results: effective weight, events
# ----------------------------------------------#

w_QCD700  = w_QCD700   / sf *target
w_QCD1000 = w_QCD1000  / sf *target
w_QCD1500 = w_QCD1500  / sf *target
w_QCD2000 = w_QCD2000  / sf *target


print("### training effective  weight ###")
print("QCD700:  {0}".format(w_QCD700))
print("QCD1000: {0}".format(w_QCD1000))
print("QCD1500: {0}".format(w_QCD1500))
print("QCD2000: {0}".format(w_QCD2000))
print(" ")

print("### Effective events ###")
Eff_QCD700  = w_QCD700  * QCDsel700
Eff_QCD1000 = w_QCD1000 * QCDsel1000
Eff_QCD1500 = w_QCD1500 * QCDsel1500
Eff_QCD2000 = w_QCD2000 * QCDsel2000

print("QCD700:  {0}".format(Eff_QCD700))
print("QCD1000: {0}".format(Eff_QCD1000))
print("QCD1500: {0}".format(Eff_QCD1500))
print("QCD2000: {0}".format(Eff_QCD2000))
print(" ")
print("### Sum of BKG effective evts(=signal selected evts)")
print(Eff_QCD700+Eff_QCD1000+Eff_QCD1500+Eff_QCD2000)
print(" ")
print("### Signal selected evts)")
print(target)

