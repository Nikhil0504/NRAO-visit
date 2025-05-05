#!/bin/sh

# Set SBATCH Directives
# Lines starting with "#SBATCH", before any shell commands are
# interpreted as command line arguments to sbatch.
# Don't put any commands before the #SBATCH directives or they will not work.
#
#SBATCH --export=ALL                          # Export all environment variables to job.
#SBATCH --mail-type=BEGIN,END,FAIL            # Send email on begin, end and fail of job.
#SBATCH --chdir=/lustre/cv/observers/cv-7429/data/
#SBATCH --time=0-2:0:0                        # Expected runtime of 2 hours
#SBATCH --mem=16G                             # Memory needed by the whole job.

# casa's python requires a DISPLAY for matplot, so create a virtual X server
xvfb-run -d casa --nogui -c /lustre/cv/observers/cv-7429/data/image_hires_lores_and_combined_PSK.py
