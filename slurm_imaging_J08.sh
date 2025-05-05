#!/bin/sh 

#SBATCH --export ALL # Export all environment variables to the job. 

#SBATCH --mem=128G # Amount of memory needed by the whole job. 

#SBATCH --mem=128G # Amount of memory needed by the whole job

#SBATCH -D /lustre/cv/observers/cv-14744 # Working directory set to your Lustre area 

#SBATCH --time=10-2:30:00 # Expected runtime of 10 days 2 hours and 30 minutes 

#SBATCH --mail-type=END,FAIL # Send email when Jobs end or fail 

# casa's python requires a DISPLAY for matplot, so create a virtual X server 

xvfb-run -d nice mpicasa -n 24 casa-alma --pipeline --nogui -c /lustre/cv/observers/cv-14744/data/NRAO-visit/J08_test.py

