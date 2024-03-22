import glob
import subprocess
import argparse


##################################################################
#  * Purpose: run excute.py code with input files			    
#  * There are many input files								
#  * You want to run like this:							    
#																
#  - Suppose the number of total input files = 11				
#  - You wan to input maxium 4 input files for each run															 
#    >python excute.py input0 input1 input2 input3				 
#    >python excute.py input4 input5 input6 input7				 
#    >python excute.py input8 input9 input10					 
#																 
#  You can choose maxfile ( max input file number )			     
#  The number of ouput files are automatically calculated		 
##################################################################


################################################
# Set path

# 1. excute following command to make output directories
#$ mkdir -p temp_sample_directory/QCD_HT1000 temp_sample_directory/QCD_HT1500 temp_sample_directory/QCD_HT2000 temp_sample_directory/RPV

out_RPV="temp_sample_directory/RPV/RPV.h5"
out_HT1000="temp_sample_directory/QCD_HT1000/QCD_HT1000.h5"
out_HT1500="temp_sample_directory/QCD_HT1500/QCD_HT1500.h5"
out_HT2000="temp_sample_directory/QCD_HT2000/QCD_HT2000.h5"


in_RPV="/xrootd/store/user/hnam/sample4Nurion/2018DAS/Delphes/Jetcorrec_32PU/RPV/Gluino1400GeV/0000/*.root"
in_HT1000="/xrootd/store/user/hnam/sample4Nurion/2018DAS/Delphes/Jetcorrec_32PU/QCDBkg/HT1000to1500/*/*.root"
in_HT1500="/xrootd/store/user/hnam/sample4Nurion/2018DAS/Delphes/Jetcorrec_32PU/QCDBkg/HT1500to2000/*/*.root"
in_HT2000="/xrootd/store/user/hnam/sample4Nurion/2018DAS/Delphes/Jetcorrec_32PU/QCDBkg/HT2000toInf/*/*.root"

infile_path  = [in_RPV,in_HT1000,in_HT1500,in_HT2000]
outfile_path = [out_RPV,out_HT1000,out_HT1500,out_HT2000]
basedirs	 = ["temp_sample_directory/RPV/","temp_sample_directory/QCD_HT1000/","temp_sample_directory/QCD_HT1500/","temp_sample_directory/QCD_HT2000/"]


parser = argparse.ArgumentParser()
parser.add_argument('--maxfile',action='store', type=int, help='Maxfile in one process')
args = parser.parse_args()



### 2. Select sample name 
# RPV:	  0
# HT1000: 1
# HT1500: 2
# HT2000: 3
file_list  = glob.glob(infile_path[0])
outfile_name = outfile_path[0]
basedir = basedirs[0]















### 3. Run
# do not forget --maxfile option! 
####################################################

def calc_Nout(maxfile,nfile):
	nfile = maxfile + nfile - 1
	nout = int(nfile / maxfile)
	return(nout)

maxfile=args.maxfile # Max number of input files for each run ( argumnet )
nfile=len(file_list) #  Number of total input files
nout  = calc_Nout(maxfile,nfile) # Number of output files


print("Total files: ",nfile)

for i in range(nout):
	start = i*maxfile 
	end = start + maxfile 
	
	infiles = (' '.join(file_list[start:end]))

	fn = outfile_name.split('/')[2] 
	fn = fn.split('.')[0]
	fn_out = basedir + fn + '_' + str(i) + ".h5"
	fn_out_log = basedir + fn + '_' + str(i) + ".log"
	

	print(" ###### start",i," th loop")
	print(infiles)
	print( " " )
	print(fn_out)
	
	args = 'python' + ' '+ 'makeDetectorImage.py' + ' ' + '--format' + ' ' + 'NCHW' + ' '+ '--nevent' + ' ' + '$((1024*16))' + ' ' + '-o' + ' ' + fn_out + ' ' + infiles + ' ' + ' 2>&1' + ' ' + 'tee' + ' ' + fn_out_log
	subprocess.call(args,shell=True)
