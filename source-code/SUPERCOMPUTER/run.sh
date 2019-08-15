#!/bin/sh
#SBATCH --time=10
#SBATCH --job-name=OWEN_TEST
#SBATCH --partition dcs
#SBATCH --nodes 1
#SBATCH --gres=gpu:4

path_binary=/gpfs/u/home/MMBS/MMBSwnlc/scratch/conv

module load xl_r mpich cuda

srun --gres=gpu:4 -n 4 ./bindProcessToGpu.sh python $path_binary/3dconv_dcs.py 

set +x
