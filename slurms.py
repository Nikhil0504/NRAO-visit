

###GENERATE SLURM BATCH SCRIPT TO BE RUN INSIDE NM-6805

def generate_sh_files(name, folders, template):
    for folder in folders:
        last_five_numbers = folder[-5:]
        script_content = template.replace("NAME", name).replace("FOLDER", folder)
        filename = f"runVLA{name}obs{last_five_numbers}.sh"
        with open(filename, 'w') as file:
            file.write(script_content)
        print(f"Generated {filename}")

# Sample batch script template with placeholders NAME and FOLDER
# template = """#!/bin/bash

# #SBATCH --export=ALL                          # Export all environment variables to job.
# #SBATCH --mail-type=BEGIN,END,FAIL            # Send email on begin, end and fail of job.
# #SBATCH --chdir=/lustre/aoc/observers/nm-6805/data/CONICS/NAME/23B-215/FOLDER # Working directory
# #SBATCH --time=30-2:3:4                        # Request 10day, 2hours, 3minutes, and 4seconds.
# #SBATCH --mem=128G                             # Memory needed by the whole job.

# # casa's python requires a DISPLAY for matplot, so create a virtual X server
# module load /home/casa/packages/RHEL7/release/casa-6.5.4-9-pipeline-2023.1.0.125/bin/casa
# xvfb-run -d  --nogui -c /lustre/aoc/observers/nm-6805/data/CONICS/NAME/23B-215/FOLDER/VLAcasa_pipescript_v654_NAME.py
# #xvfb-run -d casa-pipe --nogui -c /lustre/aoc/observers/nm-6805/data/CONICS/NAME/23B-215/FOLDER/VLAcasa_pipescript_v654_NAME.py
# """
template = """#!/bin/sh 

#SBATCH --export ALL # Export all environment variables to the job. 

#SBATCH --mem=128G # Amount of memory needed by the whole job. 

#SBATCH -D /lustre/aoc/observers/nm-6805/data/CONICS/NAME/FOLDER # Working directory set to your Lustre area 

#SBATCH --time=10-2:30:00 # Expected runtime of 10 days 2 hours and 30 minutes 

#SBATCH --mail-type=END,FAIL # Send email when Jobs end or fail 
s
# casa's python requires a DISPLAY for matplot, so create a virtual X server 

xvfb-run -d casa-pipe --nogui -c /lustre/aoc/observers/nm-6805/data/DIRpath/NAME/FOLDER/VLAcasa_pipescript_v654_NAME.py
"""

# Fixed name and list of folders
#<><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>
name = "13296" #13296 GHz;
folders = ["observation.", "", ""]
# Generate the .sh files
generate_sh_files(name, folders, template)