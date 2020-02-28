#!/bin/bash


source /apps/applications/miniconda3/etc/profile.d/conda.sh
source /apps/compiler/intel/19.0.5/impi/2019.5.281/intel64/bin/mpivars.sh release_mt
module load git craype-mic-knl
module load gcc/8.3.0
export USE_CUDA=0
export USE_MKLDNN=1
export USE_OPENMP=1
export USE_TBB=0
conda activate /scratch/$USER/conda/nurion_torch

export HDF5_USE_FILE_LOCKING='FALSE'
export TF_XLA_FLAGS=--tf_xla_cpu_global_jit
export KMP_AFFINITY=granularity=fine,compact
export KMP_SETTINGS=1
export CUDA_VISIBLE_DEVICES=""

export OMPI_MCA_btl_openib_allow_ib=1
export OMPI_MCA_btl_openib_if_include="hfi1_0:1"
export LD_LIBRARY_PATH=/opt/pbs/lib:$LD_LIBRARY_PATH

