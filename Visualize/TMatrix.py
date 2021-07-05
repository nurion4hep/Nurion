from ROOT import TCanvas,TH2F,gStyle
from ROOT import TMatrix
import h5py 
import numpy as np 

infile_QCD = "QCD_HT1000/QCD_HT1000_0.h5"
#infile_RPV = "RPV/RPV_0.h5"
#dat = h5py.File(infile_RPV)
dat = h5py.File(infile_QCD)


#target = 'ECAL'
#target = 'HCAL'
target = 'TRACK'


data = dat['all_events'][target][0]
print(data)





data = data / 1000.
mat = TMatrix(224,224)


for i in range(224):
	for j in range(224):
		mat[i][j] = data[i][j]

#mat.Print()

gStyle.SetOptStat(0)
gStyle.SetTitleFontSize(25)
h2 = TH2F(mat)

h2.GetXaxis().SetNdivisions(8)
h2.GetXaxis().SetTitle('#eta pixel')
h2.GetXaxis().SetTitleOffset(1.5)
h2.GetXaxis().SetTitleSize(0.05)
h2.GetXaxis().SetLabelSize(0.04)


h2.GetYaxis().SetNdivisions(8)
h2.GetYaxis().SetTitle('#phi pixel')
h2.GetYaxis().SetTitleOffset(1.5)
h2.GetYaxis().SetTitleSize(0.05)
h2.GetYaxis().SetLabelSize(0.04)


#h2.GetZaxis().SetTitle('Energy density [GeV]')
h2.GetZaxis().SetTitle('p_{T} density [GeV]')
#h2.GetZaxis().SetTitleOffset(1.5)
h2.GetZaxis().SetTitleSize(0.05)
h2.GetZaxis().SetLabelSize(0.04)



outname = target + '.png'

c1 = TCanvas("c1","c2",600,400)
c1.Update()
#h2.Draw('LEGO2Z')
h2.Draw("LEGO2 0")
c1.SetGrid()
c1.Print(outname)
input('a')



