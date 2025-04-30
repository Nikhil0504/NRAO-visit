import glob
import numpy as np
import analysisUtils as au

# image 5094
zsource=2.1715


# IF RUN WITH MPI SET TRUE:
parallel=False

# get all MSs from directory
vis=glob.glob("*.ms")

# get properties from first vis
# field
msmd.open(vis[0])
field=str(msmd.fieldsforintent("OBSERVE_TARGET#UNSPECIFIED", True)[0])
msmd.close()


# MFS
imagename=field+".all.mfs"
spws=au.getScienceSpws(vis[0], intent='OBSERVE_TARGET#UNSPECIFIED', returnString=False)
spws=','.join(map(str, spws)) # need string later

commonpars=dict(vis=vis,
                selectdata=True,
                field=field,  # this is the source
                imagename=imagename,
                specmode="mfs",
                parallel=parallel,
                deconvolver="clark",
                interpolation="nearest",
                spw=spws,
                imsize=[512,512],
                cell=["0.6arcsec","0.6arcsec"],
                weighting="natural", #robust=robust,
                uvtaper="",
                pblimit=0.2)

if 0:
    tclean(niter=0,**commonpars)
                                                            

# CUBE
imagename=field+".all.cube"
restfreq=str(115.2712018/(1.+zsource))+"GHz"
print(field, zsource, restfreq)
spws=[4,5,6,7]
spws=','.join(map(str, spws)) # need string later
mask=["circle[["+str(int(256))+"pix,"+str(int(256))+"pix],3arcsec]"] # center of the map

commonpars=dict(vis=vis,
                selectdata=True,
                field=field,  # this is the source
                imagename=imagename,
                specmode="cube",
                nchan=150,
                start="-2500km/s",
                width="40.0km/s",
                restfreq=restfreq,
                parallel=parallel,
                deconvolver="clark",
                interpolation="nearest",
                spw=spws,
                imsize=[512,512],
                cell=["0.6arcsec","0.6arcsec"],
                weighting="natural", #robust=robust,
                uvtaper="",
                pblimit=0.2)

# dirty run
if 1:
    tclean(niter=0, **commonpars)
    
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

    tclean(calcres=False, calcpsf=False, niter=10000,threshold=str(2*rms)+'Jy',pbcor=True, mask=mask, **commonpars)
    for ext in [".image", ".image.pbcor",".residual",".model"]: exportfits(imagename=imagename+ext,fitsimage=imagename+ext+'.clean.fits', overwrite=True) #[".psf", ".pb"]
                                                                                                                                                                                                                                                            
                                  
