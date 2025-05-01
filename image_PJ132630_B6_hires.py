import glob
import numpy as np

import sys
sys.path.append("/users/thunter/AIV/science/analysis_scripts")

import analysisUtils as au

# image PJ132630
zsource=2.9507


# IF RUN WITH MPI SET TRUE:
parallel=False

# get all MSs from directory
vis=glob.glob("../*.ms.split.cal")

# get properties from first vis
# field
msmd.open(vis[0])
field=str(msmd.fieldsforintent("OBSERVE_TARGET#ON_SOURCE", True)[0])
msmd.close()


# MFS
imagename=field+".all.mfs"
spws=au.getScienceSpws(vis[0], intent='OBSERVE_TARGET#ON_SOURCE', returnString=False)
spws=','.join(map(str, spws)) # need string later

commonpars=dict(vis=vis,
                selectdata=True,
                field=field,  # this is the source
                imagename=imagename,
                specmode="mfs",
                parallel=parallel,
                deconvolver="hogbom",
                interpolation="nearest",
                spw=spws,
                imsize=[2048,2048],
                cell=["0.02arcsec","0.02arcsec"],
                restoringbeam='common',
                weighting="briggs", #robust=robust,
                robust=0.5,
                usemask='auto-multithresh', 
                sidelobethreshold=2.5, 
                noisethreshold=5.0, 
                lownoisethreshold=1.5, 
                negativethreshold=0.0, 
                minbeamfrac=0.3, 
                growiterations=75, 
                dogrowprune=True, 
                minpercentchange=1.0, 
                fastnoise=True,
                uvtaper="",
                pblimit=0.2,
                savemodel='none')


# dirty run
if 1:
    tclean(niter=0,**commonpars)

    for ext in [".psf", ".pb"]: exportfits(imagename=imagename+ext,fitsimage=imagename+ext+'.fits', overwrite=True)
    for ext in [".image"]: exportfits(imagename=imagename+ext,fitsimage=imagename+ext+'.dirty.fits', overwrite=True)
      


                                                                                                      
# clean run
if 1:
    ia.open(imagename+".image")
    stat=ia.statistics(axes=[0,1],algorithm="chauvenet", zscore=3, maxiter=20)
    ia.close()
    rmses=stat["rms"]
    print("rms per ch", rmses)
    rms=np.nanmedian(rmses[rmses>0])
    print("med rms", rms)
    rms=np.min(rmses[rmses>0])
    print("min rms (use)", rms)

    tclean(calcres=False, calcpsf=False, niter=10000,threshold=str(2*rms)+'Jy',pbcor=True, **commonpars)
    for ext in [".image", ".image.pbcor",".residual",".model"]: exportfits(imagename=imagename+ext,fitsimage=imagename+ext+'.clean.fits', overwrite=True) #[".psf", ".pb"]
         


