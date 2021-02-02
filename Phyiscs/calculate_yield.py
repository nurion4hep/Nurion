Lumi         = 63.67 * 1000
xsecSignal   = 0.0252977
xsecQCDHT1000   = 1207
xsecQCDHT1500   = 119.9
xsecQCDHT2000   = 25.24

gensig = 330599
genQCDHT1000 = 15424272
genQCDHT1500 = 3241825
genQCDHT2000 = 3250016





signal_sel = 97437 + 13217

QCD_HT1000_sel = 121
QCD_HT1500_sel = 401
QCD_HT2000_sel = 1707


signal_Y	=  signal_sel * Lumi * xsecSignal / gensig
QCDHT1000_Y =  QCD_HT1000_sel * Lumi * xsecQCDHT1000 / genQCDHT1000
QCDHT1500_Y =  QCD_HT1500_sel* Lumi * xsecQCDHT1500 / genQCDHT1500
QCDHT2000_Y =  QCD_HT2000_sel* Lumi * xsecQCDHT2000 / genQCDHT2000






print("numsig :" ,signal_Y)
print("num bkg: ",QCDHT1000_Y+QCDHT1500_Y+QCDHT2000_Y)
