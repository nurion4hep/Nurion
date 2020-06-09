import glob
import h5py

## --- QCDHT1000
target='/HT1000to1500/'
arr_bkg_sub_dir = ['0000','0001','0002','0003','0004']
bkg_dir='/xrootd_user/hknam/xrootd2/sample4Nurion/2018DAS/Delphes/presel/hdf5_noPU_224x224/QCDBkg' + target
bkg_full_path=[]


sum_bkg =0
for bkg_sub_dir in arr_bkg_sub_dir:
	
	print(bkg_dir + bkg_sub_dir + '/*.h5')
	bkg_full_path = glob.glob(bkg_dir + bkg_sub_dir + '/*.h5')
	
	for bkg_path in bkg_full_path:
		dat = h5py.File(bkg_path,'r')
		n_event = dat['all_events']['weight'].shape[0]
		sum_bkg +=n_event
		print("N events for {0} is {1}".format(bkg_path,n_event))


print("Total events: ", sum_bkg)
print(" ")



## --QCDHT1500
target='/HT1500to2000/'
arr_bkg_sub_dir = ['0000','0001']
bkg_dir='/xrootd_user/hknam/xrootd2/sample4Nurion/2018DAS/Delphes/presel/hdf5_noPU_224x224/QCDBkg' + target
bkg_full_path=[]


sum_bkg =0
for bkg_sub_dir in arr_bkg_sub_dir:
	
	print(bkg_dir + bkg_sub_dir + '/*.h5')
	bkg_full_path = glob.glob(bkg_dir + bkg_sub_dir + '/*.h5')
	
	for bkg_path in bkg_full_path:
		dat = h5py.File(bkg_path,'r')
		n_event = dat['all_events']['weight'].shape[0]
		sum_bkg +=n_event
		print("N events for {0} is {1}".format(bkg_path,n_event))


print("Total events: ", sum_bkg)
print(" ")



## --QCDHT1500
target='/HT2000toInf/'
arr_bkg_sub_dir = ['0000']
bkg_dir='/xrootd_user/hknam/xrootd2/sample4Nurion/2018DAS/Delphes/presel/hdf5_noPU_224x224/QCDBkg' + target
bkg_full_path=[]


sum_bkg =0
for bkg_sub_dir in arr_bkg_sub_dir:
	
	print(bkg_dir + bkg_sub_dir + '/*.h5')
	bkg_full_path = glob.glob(bkg_dir + bkg_sub_dir + '/*.h5')
	
	for bkg_path in bkg_full_path:
#		print(bkg_path)
		dat = h5py.File(bkg_path,'r')
		n_event = dat['all_events']['weight'].shape[0]
		sum_bkg +=n_event
		print("N events for {0} is {1}".format(bkg_path,n_event))


print("Total events: ", sum_bkg)
print(" ")



## --RPV
target='/Gluino1400GeV/'
arr_bkg_sub_dir = ['0000']
bkg_dir='/xrootd_user/hknam/xrootd2/sample4Nurion/2018DAS/Delphes/presel/hdf5_noPU_224x224/RPV' + target
bkg_full_path=[]


sum_bkg =0
for bkg_sub_dir in arr_bkg_sub_dir:
	
	print(bkg_dir + bkg_sub_dir + '/*.h5')
	bkg_full_path = glob.glob(bkg_dir + bkg_sub_dir + '/*.h5')
	
	for bkg_path in bkg_full_path:
		#print(bkg_path)
		dat = h5py.File(bkg_path,'r')
		n_event = dat['all_events']['weight'].shape[0]
		sum_bkg +=n_event
		#print("N events for {0} is {1}".format(bkg_path,n_event))


print("Total events: ", sum_bkg)
print(" ")
