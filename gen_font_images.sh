#!/bin/bash

#SBATCH --time=3:00:00   # walltime
#SBATCH --ntasks=1   # number of processor cores (i.e. tasks)
#SBATCH --nodes=1   # number of nodes
##SBATCH --exclusive   # number of nodes
#SBATCH --mem-per-cpu=8000M   # memory per CPU core
##SBATCH --gres=gpu:4
#SBATCH --output="./gen_font_images.slurm"
#SBATCH --constraint rhel7

# Set the max number of threads to use for programs using OpenMP. Should be <= ppn. Does nothing if the program doesn't use OpenMP.
export OMP_NUM_THREADS=$SLURM_CPUS_ON_NODE

# LOAD MODULES, INSERT CODE, AND RUN YOUR PROGRAMS HERE
#%Module

cat /etc/os-release
cat /etc/redhat-release

module purge
#source /fslhome/tarch/.bashrc
#module load anaconda
#export PATH="/fslhome/tarch/anaconda3/bin:$PATH"
export PATH="/fslhome/tarch/anaconda3/envs/munit/bin:$PATH"
#conda activate main
#source activate main
#source activate /fslhome/tarch/anaconda3/envs/main

which python

#/zhome/tarch/compute/handwriting
cd "/fslhome/tarch/compute/research/handwriting/text_generation/gen_text_images"

python -u create_font_images.py

# To run:
#sbatch ./run.sh
#squeue -u tarch
