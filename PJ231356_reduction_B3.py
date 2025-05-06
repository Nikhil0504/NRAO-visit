import os
from glob import glob

def runAutoCleanCube(vn=['/root/path/to/v1.ms','/root/path/to/v2.ms'],
                     specwindow='',
                     linestring='CO',
                     redfreq=100.1,
                     startendvel=[-2000,2000],
                     velres=50.0,
                     thresh='1.0mJy',
                     niter=100000,
                     cycleniter = 100,
                     fieldname = '',
                     synbeam_estimate=0.3,
                     imsize_pix=256,
                     usemask='user',
                     weighting='natural',
                     deconvolver='hogbom',
                     gridder='standard',
                     tag='taginfo',
                     outfolder = 'root/sourcename/weightinginfo/',
                     deletefiles=True,
                     **kwargs,
                     ):



        #roughly the median value between the major/minor axes:
        cellsperbeam = 5.0 #at least less than 1/3 restoring beam
        cellsizeestimate= synbeam_estimate/cellsperbeam
        cellsize = str(cellsizeestimate)+'arcsec' #e.g.# cellsize = '0.04arcsec'

        if deletefiles:
                os.system('rm -rf '+outfolder+'*'+'_cube_'+tag+'*')

        # Imaging parameters
        imagename = outfolder+'_'+linestring+'_cube_'+tag # Output images

        restfreq = str(redfreq)+'GHz' #Rest frequency of line of interest.
        interactive = False
        # Number of iterations before stopping deconvolution (global stopping criterion).
        niter = niter
        #Pixel size of image in arcsec.
        # Needs to be a small fraction (<1/3) of expected beam size (few arcsec in this case).
        cell = cellsize
        # Typically about the size of the primary beam (55" for SMA at 1.3mm), measured in
        # number of pixels. Better if it is a power of 2, as it makes the FFT algorithm more efficient.
        imsize = imsize_pix
        #Weighting of the visibilities before imaging. Natural gives larger beam, lowest noise (hence max SNR).
        # Uniform gives smallest beam, highest noise. Briggs is something in between depending on robust parameter.
        # Only needed if choosing 'briggs' weighting. Balances between natural (+2) and uniform (-2)
        # in increments of 0.5.
        # robust = ''
        # robust = 0.5 #not used in natural or uniform
        #---------------------------------
        # Line parameters
        # Note that this is a lot different than the continuum case!
        # This is where recording the velocity range above is useful! Choose the start, width and nchan to cover
        # this velocity range.
        specmode = 'cube' #For line imaging, use cube mode.
        # Channel width chosen for output cube. CLEAN will carry out interpolation to resample the visibility data
        # before imaging. '' for native (see listobs spw channel width). Use deltanu/nu_line = deltav/c to figure
        # out velocity widths from frequency widths.
        width = str(velres)+'km/s' # ***
        # width = '60.0km/s' # ***
        # NOTE: this will depend on your target!!
        # start = '-3000km/s' # velocity of starting channel of cube. Make sure to cover whole line!
        start = str(startendvel[0])+'km/s' # velocity of starting channel of cube. Make sure to cover whole line!
        numberchans=(startendvel[1]-startendvel[0])/velres
        nchan = int(numberchans) # number of channels in cube. Make sure to cover whole line!
        outframe = 'LSRK' #output reference frame for velocities This is local-standard-of-rest kinematic
        # Gridding and CLEAN algorithm choice. All of these, to begin with, are standard inputs,
        # so we do not actually need to input them, but we will here for completeness.

        # If emission is extended, use the multi-scale deconvolution algorithm.
        # The standard clean methods assume the emission is a collection of point-sources,
        # which is a poor approximation when we have extended emission.
        #>
        # deconvolver = 'hogbom'
        #>
        # deconvolver = 'multiscale'
        # scales = [0,5,15,20]

        #Auto-multithresh:
        # sidelobethreshold = 3.0 # (double=3.0) - sidelobethreshold * the max sidelobe level * peak residual
        # noisethreshold = 3.0 # (double=5.0) - noisethreshold * rms in residual image + location(median)
        # lownoisethreshold = 1.5 # (double=1.5) - lownoisethreshold * rms in residual image + location(median)
        # negativethreshold (double=0.0) - negativethreshold * rms in residual image + location(median)
        # smoothfactor = 1.0 #(double=1.0) - smoothing factor in a unit of the beam
        # minbeamfrac (double=0.3) - minimum beam fraction for pruning
        # cutthreshold (double=0.01) - threshold to cut the smoothed mask to create a final mask
        # growiterations (int=75) - number of binary dilation iterations for growing the mask
        # dogrowprune (bool=True) - Do pruning on the grow mask
        # minpercentchange (double=-1.0) - minimum percentage change in mask size (per channel plane) to trigger updating of mask by automask
        usemask=usemask
        fastnoise=True

        #PRIMARY BEAM CORRECTION
        # primbeamcorr = True
        # pblimit = 0.2
        # The primary beam size is set by the antenna size (7 m for SMA antennas / ACA).
        # Roughly speaking, the noise level goes as 1 / pb decreasing radially outward.


        # Set global threshold for the residual image max in nsigma*rms to stop iterations
        # nsigma = 1.5
        # or:
        # threshold='1.0mJy'

        # Max number of minor cycle (keep changing model) iterations per major cycle (fixed model determines residual checks etc).
        # Set to -1 initially to iteratively in interactive mode. Smaller number = longer time.
        # Used to determine minor cycle threshold. Factor multiplied by the maximum dirty beam
        # sidelobe level to calculate when to trigger major cycle.
        # cyclefactor = 1.0 #Default
        # # Used to determine minor cycle threshold. If max dirty beam sidelobe level is less than
        # # this, use 5% as a threshold to trigger major cycle. Lower boundary for major cycle trigger.
        # minpsffraction = 0.05 #Default
        # # Used to determine minor cycle threshold. If max dirty beam sidelobe level is more than this,
        # # use 80% as a threshold to trigger major cycle. Upper boundary for major cycle trigger.
        # maxpsffraction = 0.8 #Default

        calcres=True
        calcpsf=True # These save some time to avoid recalculating saved products
        ##-----<><><><><><><><><><><><><><><><><><><><><><><><>

        tclean(vis=vn,
            field=fieldname,
            spw=specwindow,
            imagename=imagename,
            imsize=imsize,
            niter=niter,
            cycleniter=cycleniter,
            interactive=False,
            verbose=True,
            usemask=usemask,
            fastnoise=fastnoise,
            threshold=thresh,
            cell=cell,
            weighting=weighting,
            gridder=gridder,
            deconvolver=deconvolver,
            specmode=specmode,
            width=width,
            start=start,
            nchan=nchan,
            restfreq=restfreq,
            outframe=outframe,
            calcres=calcres,
            calcpsf=calcpsf,
            **kwargs
        )

        exportfits(imagename=imagename+'.image',fitsimage=imagename+'.fits')
        # exportfits(imagename=imagename+'.image.pbcor',fitsimage=imagename+'pbcor.fits')

        return



root = '/lustre/cv/observers/cv-15260/data/PJ231356/'

# Using: 29.) casapy-6.6.5
''' All Observations for PJ231356 Band 3
'''

sourcenames = ['PJ231356',]
fieldnames = ['PJ231356.6']

#For two calibrated MSes 
cal_ms = [root + 'calibrated_final_highres.ms',  root + 'calibrated_final_lowres.ms']

spwstring = ['23']
imtag = ['autoclean_v5_briggs_robust0_5']          #0

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
    weighting='briggs',
    robust=0.5,
    deconvolver='multiscale',
    scales=[0, 5, 15, 45],
    tag=imtag[0],
    outfolder=root,
    deletefiles=True,
    parallel=True
)


#========================================================================================================================================
#========================================================================================================================================
#========================================================================================================================================
#========================================================================================================================================
#========================================================================================================================================

### CONTINUUM: 
#NOTE: specwindow='' takes ALL spectral windows

#runAutoCleanCont(vn=cal_ms,specwindow='', im=0, fieldname = fieldnames[0], sourcename=sourcenames[0], synbeam=0.3,imsize_pix=256, tag='_ALLSPWS_robust2',outfolder = root+sourcenames[0]+'/natty/', deletefiles=True)


