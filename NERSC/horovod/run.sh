#!/bin/bash
#PBS -V
#PBS -N tf_mnist
#PBS -q normal
#PBS -W sandbox=PRIVATE
#PBS -A etc
#PBS -l select=4:ncpus=68:mpiprocs=1:ompthreads=68
#PBS -l walltime=02:00:00

export HDF5_USE_FILE_LOCKING='FALSE'
module load gcc/7.2.0 openmpi/3.1.0 craype-mic-knl tensorflow/1.12.0

cd $PBS_O_WORKDIR

beginTime=$(date +%s%N)
mpirun python train_only.py --nb-epochs 12 --nb-train-events 100000 --nb-test-events 10000 --batch-size 512 data/Preprocessed_Train.h5 data/Preprocessed_Val.h5 3ch-CNN 

endTime=$(date +%s%N)
elapsed=`echo "($endTime - $beginTime) / 1000000" | bc`
elapsedSec=`echo "scale=6;$elapsed / 1000" | bc | awk '{printf "%.6f", $1}'`
echo TOTAL: $elapsedSec sec
