

##### Normed weight factors
# ----------------------------------------------#
#Lumi = 1
Lumi = 63670

xsecRPV     = 0.013
xsecQCD1000 = 1094.
xsecQCD1500 = 99.16
xsecQCD2000 = 20.25

## --Gen evts no baseline selection
#GenRPV     = 330599
#GenQCD700  = 129223
#GenQCD1000 = 103319
#GenQCD1500 = 127344
#GenQCD2000 = 125664

## --Gen evts baseline selection
GenRPV     = 330599
GenQCD1000 = 15466225
GenQCD1500 = 3199737
GenQCD2000 = 1520178


# weight = xsec * lumi / Gen evts
QCD1000 = xsecQCD1000 *Lumi / GenQCD1000
QCD1500 = xsecQCD1500 *Lumi / GenQCD1500
QCD2000 = xsecQCD2000 *Lumi / GenQCD2000
BKG = QCD1000 + QCD1500 + QCD2000
print("## BKG weight sum {0}".format(BKG))

## Selected evts ( = # of DNN input )

## ---NERSC cut noPU
#Signal	   = 294554  
#QCDsel700  = 350 
#QCDsel1000 = 10266
#QCDsel1500 = 30633
#QCDsel2000 = 36073

## ---NERSC cut 32PU
#Signal	   = 297263
#QCDsel700  = 555
#QCDsel1000 = 11514
#QCDsel1500 = 31527
#QCDsel2000 = 36894

## ---CMS cut noPU & 32PU
#Signal	   = GenRPV    
#QCDsel700  = GenQCD700 
#QCDsel1000 = GenQCD1000
#QCDsel1500 = GenQCD1500
#QCDsel2000 = GenQCD2000

## ---CMS cut 32PU pre-selection baseline selection
Signal	   = 294762
QCDsel1000 = 37091
QCDsel1500 = 130952
QCDsel2000 = 130802


## Renorm target ( signal selected evts )
target = Signal


##### Calculate scalefactor
# ----------------------------------------------#

# 1. Make w_QCD700+w_QCD1000+w_QCD1500+w_QCD2000 = 1
w_QCD1000 = QCD1000 / BKG  
w_QCD1500 = QCD1500 / BKG  
w_QCD2000 = QCD2000 / BKG  



print("####   Normlaize weights to 0 ~ 1 ##")
print("## Normalized weight: ",w_QCD1000 + w_QCD1500 + w_QCD2000)
print(" ")

# 2. weight * selected evts 
expQCD1000 = w_QCD1000 *QCDsel1000
expQCD1500 = w_QCD1500 *QCDsel1500
expQCD2000 = w_QCD2000 *QCDsel2000

print("####  Calculate expected evts ##")
print("#### Calcualte SF ##")
sf = expQCD1000 + expQCD1500 + expQCD2000
print("--> SF: {0}".format(sf))  
print(" ")

expQCD1000  = float(expQCD1000 /sf) 
expQCD1500  = float(expQCD1500 /sf) 
expQCD2000  = float(expQCD2000 /sf)

print("####  Normalize expected evts ##")
print("Normalized expected evts {0}".format(expQCD1000 + expQCD1500 + expQCD2000))
print(" ")
# SF: 133252.99586385902


##### Show results: effective weight, events
# ----------------------------------------------#

w_QCD1000 = w_QCD1000  / sf *target
w_QCD1500 = w_QCD1500  / sf *target
w_QCD2000 = w_QCD2000  / sf *target


print("### training effective  weight ###")
print("QCD1000: {0}".format(w_QCD1000))
print("QCD1500: {0}".format(w_QCD1500))
print("QCD2000: {0}".format(w_QCD2000))
print(" ")

print("### Effective events ###")
Eff_QCD1000 = w_QCD1000 * QCDsel1000
Eff_QCD1500 = w_QCD1500 * QCDsel1500
Eff_QCD2000 = w_QCD2000 * QCDsel2000

print("QCD1000: {0}".format(Eff_QCD1000))
print("QCD1500: {0}".format(Eff_QCD1500))
print("QCD2000: {0}".format(Eff_QCD2000))
print(" ")
print("### Sum of BKG effective evts(=signal selected evts)")
print(Eff_QCD1000 + Eff_QCD1500 + Eff_QCD2000)
print(" ")
print("### Signal selected evts)")
print(target)

