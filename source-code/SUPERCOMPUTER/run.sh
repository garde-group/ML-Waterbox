#!/bin/sh
#SBATCH -t 355
#SBATCH --job-name=OWEN_TEST
#SBATCH --partition dcs
#SBATCH --nodes 1
#SBATCH --gres=gpu:4

path_binary=/gpfs/u/home/MMBS/MMBSwnlc/scratch/conv

module load xl_r mpich cuda

srun --gres=gpu:4 -n 4 ./bindProcessToGpu.sh python $path_binary/3dconv_dcs.py 

set +x

# -t in the srun for time, n 4? use dos2unix to fix /r error
