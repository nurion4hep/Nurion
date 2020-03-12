#!/bin/bash


source /apps/applications/miniconda3/etc/profile.d/conda.sh
source /apps/compiler/intel/19.0.5/impi/2019.5.281/intel64/bin/mpivars.sh release_mt
module load git craype-mic-knl
module load gcc/8.3.0
conda activate /scratch/$USER/conda/nurion_torch

