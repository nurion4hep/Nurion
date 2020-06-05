import glob
import subprocess


RPV	    = glob.glob("/xrootd_user/jwkim2/xrootd2/HEP_CNN_Large_Image/32PU/RPV/*.h5")
QCD1000 = glob.glob("/xrootd_user/jwkim2/xrootd2/HEP_CNN_Large_Image/32PU/QCD1000/*.h5")
QCD1500 = glob.glob("/xrootd_user/jwkim2/xrootd2/HEP_CNN_Large_Image/32PU/QCD1500/*.h5")
QCD2000 = glob.glob("/xrootd_user/jwkim2/xrootd2/HEP_CNN_Large_Image/32PU/QCD2000/*.h5")

# Tracker Cnt
#outfile_RPV="/xrootd_user/jwkim2/xrootd2/HEP_CNN_Large_Image/32PU/preprocessed_cnt/RPV/RPV.h5"
#outfile_QCD1000="/xrootd_user/jwkim2/xrootd2/HEP_CNN_Large_Image/32PU/preprocessed_cnt/QCD1000/QCD1000.h5"
#outfile_QCD1500="/xrootd_user/jwkim2/xrootd2/HEP_CNN_Large_Image/32PU/preprocessed_cnt/QCD1500/QCD1500.h5"
#outfile_QCD2000="/xrootd_user/jwkim2/xrootd2/HEP_CNN_Large_Image/32PU/preprocessed_cnt/QCD2000/QCD2000.h5"

# Tracker Pt
outfile_RPV="/xrootd_user/jwkim2/xrootd2/HEP_CNN_Large_Image/32PU/preprocessed_pt/RPV/RPV.h5"
outfile_QCD1000="/xrootd_user/jwkim2/xrootd2/HEP_CNN_Large_Image/32PU/preprocessed_pt/QCD1000/QCD1000.h5"
outfile_QCD1500="/xrootd_user/jwkim2/xrootd2/HEP_CNN_Large_Image/32PU/preprocessed_pt/QCD1500/QCD1500.h5"
outfile_QCD2000="/xrootd_user/jwkim2/xrootd2/HEP_CNN_Large_Image/32PU/preprocessed_pt/QCD2000/QCD2000.h5"


def calc_nout(maxfile,nfile):
	nfile = maxfile + nfile - 1
	nout = int(nfile / maxfile)
	return(nout)

print(" ###### Start RPV ########" )
maxfile=4
nfile=len(RPV)
nout  = calc_nout(maxfile,nfile)

print("Total file number: ", nfile)
print("Merge file number: ", maxfile)
print("Expected output files: ",nout)
print(" ")


for i in range(nout):
	start = i*maxfile 
	end = start + maxfile 
	
	infiles_RPV= (' '.join(RPV[start:end]))
	print("Processing..")
	print(infiles_RPV)

	fn = outfile_RPV.split('.')[0] 
	fn_RPV = fn + '_' + str(i) + ".h5"

	print(fn_RPV)
	args = 'python' + ' '+ 'preprocess.py' + ' ' + '-o' + ' ' + fn_RPV + ' '+  infiles_RPV
	subprocess.call(args,shell=True)
print(" ")


print(" ###### Start QCD1000 ########" )
maxfile=20
nfile=len(QCD1000)
nout  = calc_nout(maxfile,nfile)

print("Total file number: ", nfile)
print("Merge file number: ", maxfile)
print("Expected output files: ",nout)
print(" ")

for i in range(nout):
	start = i*maxfile 
	end = start + maxfile 
	
	infiles_QCD1000= (' '.join(QCD1000[start:end]))
	print("Processing..")
	print(infiles_QCD1000)


	fn = outfile_QCD1000.split('.')[0]
	fn_QCD1000 = fn + '_' + str(i) + ".h5"

	print(fn_QCD1000)
	args = 'python' + ' '+ 'preprocess.py' + ' ' + '-o' + ' ' + fn_QCD1000 + ' '+  infiles_QCD1000
	subprocess.call(args,shell=True)

print(" ")


print(" ###### Start QCD1500 ########" )
maxfile=10
nfile=len(QCD1500)
nout  = calc_nout(maxfile,nfile)

print("Total file number: ", nfile)
print("Merge file number: ", maxfile)
print("Expected output files: ",nout)
print(" ")

for i in range(nout):
	start = i*maxfile 
	end = start + maxfile 
	
	infiles_QCD1500= (' '.join(QCD1500[start:end]))
	print("Processing..")
	print(infiles_QCD1500)
	
	fn = outfile_QCD1500.split('.')[0]
	fn_QCD1500 = fn + '_' + str(i) + ".h5"
	
	print(fn_QCD1500)
	args = 'python' + ' '+ 'preprocess.py' + ' ' + '-o' + ' ' + fn_QCD1500 + ' '+  infiles_QCD1500
	subprocess.call(args,shell=True)
print(" ")



print(" ###### Start QCD2000 ########" )
maxfile=10
nfile=len(QCD2000)
nout  = calc_nout(maxfile,nfile)

print("Total file number: ", nfile)
print("Merge file number: ", maxfile)
print("Expected output files: ",nout)
print(" ")

for i in range(nout):
	start = i*maxfile 
	end = start + maxfile 
	
	infiles_QCD2000= (' '.join(QCD2000[start:end]))

	print("Processing..")
	print(infiles_QCD2000)

	fn = outfile_QCD2000.split('.')[0]
	fn_QCD2000 = fn + '_'+ str(i) + ".h5"

	print(fn_QCD2000)
	args = 'python' + ' '+ 'preprocess.py' + ' ' + '-o' + ' ' + fn_QCD2000 + ' '+  infiles_QCD2000
	subprocess.call(args,shell=True)
print(" ")

