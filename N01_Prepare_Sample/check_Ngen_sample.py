import glob
import uproot
import os


## 32PU 
#RPV_dir_path	 = glob.glob('/xrootd_user/hknam/xrootd2/sample4Nurion/2018DAS/Delphes/Jetcorrec_32PU/RPV/Gluino1400GeV/0000/*.root')
#QCD1000_dir_path = glob.glob('/xrootd_user/hknam/xrootd2/sample4Nurion/2018DAS/Delphes/Jetcorrec_32PU/QCDBkg/HT1000to1500/*/*.root')
#QCD1500_dir_path = glob.glob('/xrootd_user/hknam/xrootd2/sample4Nurion/2018DAS/Delphes/Jetcorrec_32PU/QCDBkg/HT1500to2000/*/*.root')
#QCD2000_dir_path = glob.glob('/xrootd_user/hknam/xrootd2/sample4Nurion/2018DAS/Delphes/Jetcorrec_32PU/QCDBkg/HT2000toInf/*/*.root')

## noPU 
RPV_dir_path	 = glob.glob('/xrootd_user/hknam/xrootd2/sample4Nurion/2018DAS/Delphes/Jet_correction/RPV/Gluino1400GeV/0000/*.root')
QCD1000_dir_path = glob.glob('/xrootd_user/hknam/xrootd2/sample4Nurion/2018DAS/Delphes/Jet_correction/QCDBkg/HT1000to1500/*/*.root')
QCD1500_dir_path = glob.glob('/xrootd_user/hknam/xrootd2/sample4Nurion/2018DAS/Delphes/Jet_correction/QCDBkg/HT1500to2000/*/*.root')
QCD2000_dir_path = glob.glob('/xrootd_user/hknam/xrootd2/sample4Nurion/2018DAS/Delphes/Jetcorrec_noPU/QCDBkg/HT2000toInf/*/*.root')


print(len(RPV_dir_path))
print(len(QCD1000_dir_path))
print(len(QCD1500_dir_path))
print(len(QCD2000_dir_path))

print(" Scanning... RPV..!")
print(" ")
sum_RPV=0
for f in RPV_dir_path:
	if os.stat(f).st_size != 0:
		print(uproot.tree.numentries(f,'Delphes'))
		sum_RPV+= uproot.tree.numentries(f,'Delphes')
	else:
		 print("{0} file is empty.. pass this file".format(f))



print(" Scanning... QCD1000..!")
print(" ")
sum_QCD1000=0
for f in QCD1000_dir_path:
	if os.stat(f).st_size != 0:
		print(uproot.tree.numentries(f,'Delphes'))
		sum_QCD1000+= uproot.tree.numentries(f,'Delphes')
	else:
		 print("{0} file is empty.. pass this file".format(f))


print(" Scanning... QCD1500..!")
print(" ")
sum_QCD1500=0
for f in QCD1500_dir_path:
	if os.stat(f).st_size != 0:
		print(uproot.tree.numentries(f,'Delphes'))
		sum_QCD1500+= uproot.tree.numentries(f,'Delphes')
	else:
		 print("{0} file is empty.. pass this file".format(f))


print(" Scanning... QCD2000..!")
print(" ")
sum_QCD2000=0
for f in QCD2000_dir_path:
	if os.stat(f).st_size != 0:
		print(uproot.tree.numentries(f,'Delphes'))
		sum_QCD2000+= uproot.tree.numentries(f,'Delphes')
	else:
		 print("{0} file is empty.. pass this file".format(f))

print(" ########### Summary ############# " )
print("Ngen RPV {0}".format(sum_RPV))
print("Ngen QCD1000 {0}".format(sum_QCD1000))
print("Ngen QCD1500 {0}".format(sum_QCD1500))
print("Ngen QCD2000 {0}".format(sum_QCD2000))
