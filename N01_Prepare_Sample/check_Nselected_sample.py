import h5py
import glob



## 32PU 224x224
#RPV_dir_path = glob.glob('/xrootd_user/hknam/xrootd2/sample4Nurion/2018DAS/Delphes/presel/hdf5_32PU_224x224/RPV/Gluino1400GeV/0000/*.h5')
#QCD1000_dir_path = glob.glob('/xrootd_user/hknam/xrootd2/sample4Nurion/2018DAS/Delphes/presel/hdf5_32PU_224x224/QCDBkg/HT1000to1500/*/*.h5')
#QCD1500_dir_path = glob.glob('/xrootd_user/hknam/xrootd2/sample4Nurion/2018DAS/Delphes/presel/hdf5_32PU_224x224/QCDBkg/HT1500to2000/*/*.h5')
#QCD2000_dir_path = glob.glob('/xrootd_user/hknam/xrootd2/sample4Nurion/2018DAS/Delphes/presel/hdf5_32PU_224x224/QCDBkg/HT2000toInf/*/*.h5')


## noPU 224x224
#RPV_dir_path = glob.glob('/xrootd_user/hknam/xrootd2/sample4Nurion/2018DAS/Delphes/presel/hdf5_noPU_224x224/RPV/Gluino1400GeV/0000/*.h5')
#QCD1000_dir_path = glob.glob('/xrootd_user/hknam/xrootd2/sample4Nurion/2018DAS/Delphes/presel/hdf5_noPU_224x224/QCDBkg/HT1000to1500/*/*.h5')
#QCD1500_dir_path = glob.glob('/xrootd_user/hknam/xrootd2/sample4Nurion/2018DAS/Delphes/presel/hdf5_noPU_224x224/QCDBkg/HT1500to2000/*/*.h5')
#QCD2000_dir_path = glob.glob('/xrootd_user/hknam/xrootd2/sample4Nurion/2018DAS/Delphes/presel/hdf5_noPU_224x224/QCDBkg/HT2000toInf/*/*.h5')

## 32PU 64x64
#RPV_dir_path = glob.glob('/xrootd_user/hknam/xrootd2/sample4Nurion/2018DAS/Delphes/presel/hdf5_32PU/RPV/Gluino1400GeV/0000/*.h5')
#QCD1000_dir_path = glob.glob('/xrootd_user/hknam/xrootd2/sample4Nurion/2018DAS/Delphes/presel/hdf5_32PU/QCDBkg/HT1000to1500/*/*.h5')
#QCD1500_dir_path = glob.glob('/xrootd_user/hknam/xrootd2/sample4Nurion/2018DAS/Delphes/presel/hdf5_32PU/QCDBkg/HT1500to2000/*/*.h5')
#QCD2000_dir_path = glob.glob('/xrootd_user/hknam/xrootd2/sample4Nurion/2018DAS/Delphes/presel/hdf5_32PU/QCDBkg/HT2000toInf/*/*.h5')


## noPU 64x64
RPV_dir_path = glob.glob('/xrootd_user/hknam/xrootd2/sample4Nurion/2018DAS/Delphes/presel/hdf5_noPU/RPV/Gluino1400GeV/0000/*.h5')
QCD1000_dir_path = glob.glob('/xrootd_user/hknam/xrootd2/sample4Nurion/2018DAS/Delphes/presel/hdf5_noPU/QCDBkg/HT1000to1500/*/*.h5')
QCD1500_dir_path = glob.glob('/xrootd_user/hknam/xrootd2/sample4Nurion/2018DAS/Delphes/presel/hdf5_noPU/QCDBkg/HT1500to2000/*/*.h5')
QCD2000_dir_path = glob.glob('/xrootd_user/hknam/xrootd2/sample4Nurion/2018DAS/Delphes/presel/hdf5_noPU/QCDBkg/HT2000toInf/*/*.h5')



print(" -- Start .. scanning RPV events..! ")
print(" ")
sum_RPV_selected =0
for f in RPV_dir_path:
	dat = h5py.File(f,'r')
	sum_RPV_selected += dat['all_events']['hist'].shape[0]
dat.close()


print(" -- Start .. scanning QCD1000-1500  events..! ")
print(" ")
sum_QCD1000_selected =0
for f in QCD1000_dir_path:
	dat = h5py.File(f,'r')
	sum_QCD1000_selected += dat['all_events']['hist'].shape[0]
dat.close()

print(" -- Start .. scanning QCD1500-2000  events..! ")
print(" ")
sum_QCD1500_selected =0
for f in QCD1500_dir_path:
	dat = h5py.File(f,'r')
	sum_QCD1500_selected += dat['all_events']['hist'].shape[0]
dat.close()

print(" -- Start .. scanning QCD2000-Inf  events..! ")
print(" ")
sum_QCD2000_selected =0
for f in QCD2000_dir_path:
	dat = h5py.File(f,'r')
	sum_QCD2000_selected += dat['all_events']['hist'].shape[0]
dat.close()

print(" ############ Summary #############")
print("RPV Selected evts: {0}".format(sum_RPV_selected))
print("QCD1000 Selected evts: {0}".format(sum_QCD1000_selected))
print("QCD1500 Selected evts: {0}".format(sum_QCD1500_selected))
print("QCD2000 Selected evts: {0}".format(sum_QCD2000_selected))



