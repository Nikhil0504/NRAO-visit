#!/bin/sh

# Set SBATCH Directives
# Lines starting with "#SBATCH", before any shell commands are
# interpreted as command line arguments to sbatch.
# Don't put any commands before the #SBATCH directives or they will not work.
#
#SBATCH --export=ALL                          # Export all environment variables to job.
#SBATCH --mail-type=BEGIN,END,FAIL            # Send email on begin, end and fail of job.
#SBATCH --chdir=/lustre/cv/observers/cv-7429/data/
#SBATCH --time=0-3:0:0                        # Expected runtime of 3 hours
#SBATCH --mem=64G                             # Memory needed by the whole job.
#SBATCH --nodes=1                             # Request 1 node
#SBATCH --ntask-per-node=8					  # Request 8 cores

CASAPATH=/home/casa/packages/RHEL7/release/current # Use a specific version of CASA
xvfb-run -d ${CASAPATH}/bin/mpicasa ${CASAPATH}/bin/casa --nogui -c /lustre/cv/observers/cv-7429/data/NRAO-visit/image_hires_lores_and_combined_PSK.py
