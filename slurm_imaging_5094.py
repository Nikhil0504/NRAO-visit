#!/bin/sh

# Set SBATCH Directives
# Lines starting with "#SBATCH", before any shell commands are
# interpreted as command line arguments to sbatch.
# Don't put any commands before the #SBATCH directives or they will not work.
#
#SBATCH --export=ALL                          # Export all environment variables to job.
#SBATCH --mail-type=BEGIN,END,FAIL            # Send email on begin, end and fail of job.
#SBATCH --chdir=/lustre/aoc/observers/nm-11222/CONICS_IMAGING/S5094/imaging/ # Working directory
#SBATCH --time=4-0:0:0                        # Request 1day, 2hours, 3minutes, and 4seconds.
#SBATCH --mem=128G                             # Memory needed by the whole job.

# casa's python requires a DISPLAY for matplot, so create a virtual X server
xvfb-run -d casa --nogui -c /lustre/aoc/observers/nm-11222/CONICS_IMAGING/S5094/imaging/image_5094.py
