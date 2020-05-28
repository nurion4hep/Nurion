#!/bin/bash

#infiles_QCDHT1000=("../../Data_directory/32PU_fulldata/unmerged/HT1000to1500/*.h5")
infiles_RPV=("../../Data_directory/32PU_fulldata/unmerged/RPV/*.h5")

# -- For Track Cnt
#outfile_QCDHT1000="../../Data_directory/32PU_fulldata/preprocessed_cnt/QCDHT1000/QCDHT1000.h5"
#outfile_RPV="../../Data_directory/32PU_fulldata/preprocessed_cnt/RPV/RPV.h5"

# -- For Track Pt
#outfile_QCDHT1000="../../Data_directory/32PU_fulldata/preprocessed_pt/QCDHT1000.h5"
outfile_RPV="../../Data_directory/32PU_fulldata/preprocessed_pt/RPV/RPV.h5"

#python preprocess.py -o $outfile_QCDHT1000 $infiles_QCDHT1000
python preprocess.py -o $outfile_RPV $infiles_RPV


