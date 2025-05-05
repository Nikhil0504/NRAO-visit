import os
from glob import glob

def getlistobs(uv_ms='', outfile=''):
      listobs(vis=uv_ms,listfile=outfile)
      return


InspectPLOTMS = False
if InspectPLOTMS:

      plotms(vis='cal.ms',
            xaxis='freq',
            yaxis='amp',
            field=fieldname,
            avgtime='1e8',
            avgscan=True,
            iteraxis='spw')

      plotms(vis='cal.ms',
            # spw='37',
            xaxis='uvwave',
            yaxis='amp',
            field=fieldname,
            avgtime='1e9',avgscan=True,
            avgchannel='1e8',
            coloraxis='observation')







# weighting='briggs',robust = 2.0, 
# weighting = 'natural'
# gridder = 'standard'
# gridder = 'mosaic',  psfphasecenter='',phasecenter=''
# deconvoler='multiscale',scales=[0,5,15,20,25]
# pbcorr=True,pblimit=0.2

def runAutoCleanCube(vn=['/root/path/to/v1.ms','/root/path/to/v2.ms'],
                     specwindow='', 
                     linestring='CO', 
                     redfreq=100.1,startendvel=[-2000,2000],velres=50.0, 
                     thresh='1.0mJy', niter=100000, cycleniter = 100,
                     fieldname = '', 
                     synbeam_estimate=0.3,imsize_pix=256,
                     noisethreshold = 5.0,lownoisethreshold = 1.5, sidelobethreshold=3.0,
                     tag='taginfo',outfolder = 'root/sourcename/weightinginfo/',deletefiles=True, **kwargs):  

       

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
        verbose = True #(bool=False) - True: print more automasking information in the logger
        usemask='auto-multithresh'
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

        DOLINEIMAGING = True
        if DOLINEIMAGING:
                tclean(vis=vn,
                        imagename=imagename,
                        field=fieldname,
                        spw=specwindow,
                        niter=niter, 
                        cycleniter=cycleniter,
                        interactive=False,
                        usemask=usemask,noisethreshold=noisethreshold,verbose=verbose,fastnoise=fastnoise,
                        lownoisethreshold=lownoisethreshold,threshold=thresh,
                        cell=cell,
                        imsize=imsize,
                        weighting=weighting,
                        gridder=gridder,
                        deconvolver=deconvolver,
                        specmode=specmode,
                        width=width,
                        start=start,
                        nchan=nchan,
                        restfreq=restfreq,
                        outframe=outframe,calcres=calcres, calcpsf=calcpsf                        )  

        exportfits(imagename=imagename+'.image',fitsimage=imagename+'.fits')
        # exportfits(imagename=imagename+'.image.pbcor',fitsimage=imagename+'pbcor.fits')

        return 


def runAutoCleanCont(vn=['v1.ms','v2.ms'],specwindow='', im=0, fieldname = '', sourcename='', synbeam=0.3,imsize_pix=256,weightscheme='briggs',robustfactor = 2.0, tag='taginfo',outfolder = 'root/sourcename/weightinginfo/', deletefiles=True): 


        ##IMPORTANT: PLEASE DEFINE 'IMTAG' ABOVE 

        #roughly the median value between the major/minor axes:
        cellsperbeam = 5.0 #at least less than 1/3 restoring beam 
        cellsizeestimate= synbeam/cellsperbeam
        cellsize = str(cellsizeestimate)+'arcsec' #e.g.# cellsize = '0.04arcsec' 

        if deletefiles:
                # os.system('rm -rf '+outfolder+sourcename+'_'+linestring[lineID]+'*cube_dirty*')
                # os.system('rm -rf '+outfolder+sourcename+'*'+'_cube_'+tag+'*') 
                os.system('rm -rf '+outfolder+'*'+'_cont_'+tag+'*')


        ContInput = True
        if ContInput:
                # Change weighting/robust and imagename accordingly 
                # File names
                imagename = outfolder+sourcename+imtag[im]+'_cont_'+tag # Output images
                # specwin=specwindow #
                # Imaging parameters
                #Shows residual image and waits after every major cycle iteration.
                interactive = False
                # Number of iterations before stopping deconvolution (global stopping criterion).
                niter = 1000000
                #Pixel size of image in arcsec.
                # Needs to be a small fraction (<1/3) of expected beam size (few arcsec in this case).
                cell = cellsize
                # Typically about the size of the primary beam (55" for SMA at 1.3mm), measured in
                # number of pixels. 
                # Better if it is a power of 2, as it makes the FFT algorithm more efficient.
                imsize = imsize_pix
                #Weighting of the visibilities before imaging. Natural gives larger beam, lowest noise (hence max SNR).
                # Uniform gives smallest beam, highest noise. Briggs is something in between depending on robust parameter.
                weighting = weightscheme
                if weightscheme == 'briggs':
                        robust=robustfactor
                elif weightscheme == 'natural' or weightscheme == 'uniform':
                        robust = ''

                specmode = 'mfs'

                gridder = 'standard'
                deconvolver = 'hogbom' 
                # pbmask (double=0.0) - primary beam mask
                # sidelobethreshold (double=3.0) - sidelobethreshold * the max sidelobe level * peak residual
                noisethreshold = 2.0 # (double=5.0) - noisethreshold * rms in residual image + location(median)
                lownoisethreshold = 1.5 # (double=1.5) - lownoisethreshold * rms in residual image + location(median)
                # negativethreshold (double=0.0) - negativethreshold * rms in residual image + location(median)
                smoothfactor = 1.0 #(double=1.0) - smoothing factor in a unit of the beam
                # minbeamfrac (double=0.3) - minimum beam fraction for pruning
                # cutthreshold (double=0.01) - threshold to cut the smoothed mask to create a final mask
                # growiterations (int=75) - number of binary dilation iterations for growing the mask
                # dogrowprune (bool=True) - Do pruning on the grow mask
                # minpercentchange (double=-1.0) - minimum percentage change in mask size (per channel plane) to trigger updating of mask by automask
                verbose = True #(bool=False) - True: print more automasking information in the logger
                usemask='auto-multithresh'
                fastnoise=True
                primbeamcorr = True

                # Set global threshold for the residual image max in nsigma*rms to stop iterations
                nsigma = 2.5
                threshold='1.0mJy'
                # Max number of minor cycle iterations per major cycle.
                #
                cycleniter = 100
                # Used to determine minor cycle threshold. Factor multiplied by the maximum dirty beam
                # sidelobe level to calculate when to trigger major cycle.
                cyclefactor = 1.0 #Default
                # Used to determine minor cycle threshold. If max dirty beam sidelobe level is less than
                # this, use 5% as a threshold to trigger major cycle. Lower boundary for major cycle trigger.
                minpsffraction = 0.05 #Default
                # Used to determine minor cycle threshold. If max dirty beam sidelobe level is more than this,
                # use 80% as a threshold to trigger major cycle. Upper boundary for major cycle trigger.
                maxpsffraction = 0.8 #Default
                # The primary beam size is set by the antenna size (7 m for SMA antennas).
                # Roughly speaking, the noise level goes as 1 / pb decreasing radially outward.
                # pblimit = 0.25
                # mask = '....crtf'
                ##-----<><><><><><><><><><><><><><><><><><><><><><><><>

        DOCONTIMAGING = True
        if DOCONTIMAGING:
                tclean(vis=vn,
                        imagename=imagename,
                        field=fieldname,spw=specwindow,niter=niter, cycleniter=cycleniter,threshold=threshold,
                        interactive=False,
                        usemask=usemask,noisethreshold=noisethreshold,verbose=verbose,fastnoise=fastnoise,
                        lownoisethreshold=lownoisethreshold,smoothfactor=smoothfactor,
                        cell=cell,
                        imsize=imsize,
                        weighting=weighting,
                        robust=robust,
                        gridder=gridder,
                        deconvolver=deconvolver,
                        specmode=specmode,
                        # width=width,
                        # start=start, nsigma=nsigma,
                        # nchan=nchan,
                        # restfreq=restfreq,outframe=outframe,
                        pbcor=primbeamcorr,
                        calcres=True, calcpsf=True  # These save some time to avoid recalculating saved products
                        )

        exportfits(imagename=imagename+'.image.pbcor',fitsimage=imagename+'.fits')

        return 









#========================================================================================================================================
#========================================================================================================================================
#========================================================================================================================================
#========================================================================================================================================
#========================================================================================================================================

# Notes:
#

# LINE IMAGING EXAMPLE:

runAutoCleanCube(vn=cal_ms,specwindow='55,59,63,67', lineID=0, fieldname = fieldnames[0], sourcename=sourcenames[0], synbeam=0.3,imsize_pix=256,robustfactor = 0.5, tag='_nocontsub_rob0p5_v20',startendvel=[-2000,1000],velres=20.0,outfolder = root+sourcenames[0]+'/natty/', deletefiles=True)


#========================================================================================================================================
#========================================================================================================================================
#========================================================================================================================================
#========================================================================================================================================
#========================================================================================================================================

### CONTINUUM: 
#NOTE: specwindow='' takes ALL spectral windows

#runAutoCleanCont(vn=cal_ms,specwindow='', im=0, fieldname = fieldnames[0], sourcename=sourcenames[0], synbeam=0.3,imsize_pix=256, tag='_ALLSPWS_robust2',outfolder = root+sourcenames[0]+'/natty/', deletefiles=True)


