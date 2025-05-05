import os
from glob import glob

from Imfuncs import runAutoCleanCube

root = '/lustre/cv/observers/cv-15260/data/PJ231356/'

# Using: 29.) casapy-6.6.5
''' All Observations for PJ231356 Band 3
'''

sourcenames = ['PJ231356',]
fieldnames = ['PJ231356.6']

#For two calibrated MSes 
cal_ms = [root + 'calibrated_final_highres.ms',  root + 'calibrated_final_lowres.ms']

spwstring = ['23']
imtag = ['autoclean_v4_bigger_scales_low_threshold']          #0

#If spectral lines: redshifted frequency of expected line to center the cube.
linestring = ['CO3']
redfreq = [107.5664]  #

runAutoCleanCube(
    vn=cal_ms,
    specwindow=spwstring[0],
    linestring=linestring[0],
    redfreq=redfreq[0],
    startendvel=[-1000, 1000],
    velres=100.0,
    thresh='0.13mJy',
    fieldname=fieldnames[0],
    synbeam_estimate=0.3,
    imsize_pix=2048,
    usemask='auto-multithresh',
    noisethreshold=1.5,
    lownoisethreshold=1.0,
    smoothfactor=2.0,
    minbeamfrac=0.2,
    pbcor=True,
    weighting='natural',
    deconvolver='multiscale',
    scales=[0, 5, 15, 20, 40, 60, 80],
    tag=imtag[0],
    outfolder=root,
    deletefiles=True
)


#========================================================================================================================================
#========================================================================================================================================
#========================================================================================================================================
#========================================================================================================================================
#========================================================================================================================================

### CONTINUUM: 
#NOTE: specwindow='' takes ALL spectral windows

#runAutoCleanCont(vn=cal_ms,specwindow='', im=0, fieldname = fieldnames[0], sourcename=sourcenames[0], synbeam=0.3,imsize_pix=256, tag='_ALLSPWS_robust2',outfolder = root+sourcenames[0]+'/natty/', deletefiles=True)


