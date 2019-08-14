#!/bin/sh
#SBATCH -t 300
#SBATCH --partition dcs
#SBATCH --nodes 1
#SBATCH --gres=gpu:4

path_binary=/gpfs/u/home/MMBS/MMBSwnlc/scratch/conv

module load xl_r mpich cuda


for batch in 256 #128 256 32 64 #128 256
do

rm -rf 3dconv_dcs.py
# sed "s/xxx/$batch/g" batch-var.py > batch-var-run.py

srun --gres=gpu:4 -n 4 ./bindProcessToGpu.sh python $path_binary/3dconv_dcs.py 

set +x
done

# USE dos2unix command to get rid of /r errors
