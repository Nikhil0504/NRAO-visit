#! /bin/bash

#SBATCH --export=ALL                          # Export all environment variables to job
#SBATCH --mail-type=BEGIN,END,FAIL            # Send email on begin, end and fail of job.
#SBATCH --chdir=/lustre/cv/observers/cv-15260/data/NRAO-visit/ # Working directory
#SBATCH --time=0-3:00:00                        # Request 3 hours
#SBATCH --mem=64G                             # Memory for the whole job
#SBATCH --nodes=1                             # Request 1 node
#SBATCH --ntasks-per-node=8                  # Request 8 cores

echo "Starting job"

CASAPATH=/home/casa/packages/RHEL7/release/current # Use a specific version of CASA
xvfb-run -d ${CASAPATH}/bin/mpicasa ${CASAPATH}/bin/casa --nogui -c PJ231356_reduction.py
