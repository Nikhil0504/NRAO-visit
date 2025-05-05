import glob
import numpy as np

import sys
sys.path.append("/users/thunter/AIV/science/analysis_scripts")

import analysisUtils as au

# image PJ132217, PJ231356, PJ132934 and PJ132935


# IF RUN WITH MPI SET TRUE:
parallel=True

# get all MSs from directory


targets = ['PJ132217', 'PJ132934', 'PJ231356']

bands = ['B6', 'B7']



def image_high_and_lo_res(targ, band, hi_lo_res_switch):

    # hires ordered first
    vis_arr = [glob.glob(targ+'/'+band+"/hires/MOUS/calibrated/working/*targets.ms"), glob.glob(targ+'/'+band+"/lores/MOUS/calibrated/working/*targets.ms")]
    ext_arr = ['.hires', '.lores']


    # High- and low- res


    for ind, vis in enumerate(vis_arr):

        if hi_lo_res_switch[ind]:

            preext = ext_arr[ind]

            # get properties from first vis
            # field
            msmd.open(vis[0])
            field=str(msmd.fieldsforintent("OBSERVE_TARGET#ON_SOURCE", True)[0])
            msmd.close()


            direc = targ+'/'+band+'/'+preext[1:]+'/MOUS/calibrated/working/'


            # MFS
            imagename=direc+field+'.'+band+preext+".all.mfs"
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
                            pblimit=0.2)


            # dirty run
            if 1:
                tclean(niter=0, imsize=[2048,2048],cell=["0.02arcsec","0.02arcsec"],savemodel='none',**commonpars)

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

                tclean(calcres=False, calcpsf=False, savemodel='modelcolumn', imsize=[2048,2048],cell=["0.02arcsec","0.02arcsec"], niter=100_000,threshold=str(2*rms)+'Jy',pbcor=True, **commonpars)
                for ext in [".image", ".image.pbcor",".residual",".model"]: exportfits(imagename=imagename+ext,fitsimage=imagename+ext+'.clean.fits', overwrite=True) #[".psf", ".pb"]
                 



def image_combined_res(targ, band):


    # hires ordered first
    vis_arr = [glob.glob(targ+'/'+band+"/hires/MOUS/calibrated/working/*targets.ms"), glob.glob(targ+'/'+band+"/lores/MOUS/calibrated/working/*targets.ms")]


    preext = '.combined'


    vis = vis_arr[0]

    vises_nested = [vis_arr[i][:] for i in range(len(vis_arr))]

    vises = np.concatenate(vises_nested)



    # get properties from first vis
    # field
    msmd.open(vis[0])
    field=str(msmd.fieldsforintent("OBSERVE_TARGET#ON_SOURCE", True)[0])
    msmd.close()


    direc = targ+'/'+band+'/'


    # MFS
    imagename=direc+field+'.'+band+preext+".all.mfs"

    spws=au.getScienceSpws(vis[0], intent='OBSERVE_TARGET#ON_SOURCE', returnString=False)
    spws=','.join(map(str, spws)) # need string later

    commonpars=dict(vis=vises,
                    selectdata=True,
                    field=field,  # this is the source
                    imagename=imagename,
                    specmode="mfs",
                    parallel=parallel,
                    deconvolver="hogbom",
                    interpolation="nearest",
                    spw=spws,
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
                    pblimit=0.2)


    # dirty run
    if 1:
        tclean(niter=0, imsize=[2048,2048],cell=["0.02arcsec","0.02arcsec"],savemodel='none',**commonpars)

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

        tclean(calcres=False, calcpsf=False, savemodel='modelcolumn', imsize=[2048,2048],cell=["0.02arcsec","0.02arcsec"], niter=100_000,threshold=str(2*rms)+'Jy',pbcor=True, **commonpars)
        for ext in [".image", ".image.pbcor",".residual",".model"]: exportfits(imagename=imagename+ext,fitsimage=imagename+ext+'.clean.fits', overwrite=True) #[".psf", ".pb"]
         




#image_high_and_lo_res(targ='PJ132217', band='B6', hi_lo_res_switch = [1,1])
#image_high_and_lo_res(targ='PJ132217', band='B7', hi_lo_res_switch = [1,1])
#
#image_combined_res(targ='PJ132217', band='B6')
#image_combined_res(targ='PJ132217', band='B7')


image_high_and_lo_res(targ='PJ231356', band='B6', hi_lo_res_switch = [1,1])
image_high_and_lo_res(targ='PJ231356', band='B7', hi_lo_res_switch = [1,1])

image_combined_res(targ='PJ231356', band='B6')
image_combined_res(targ='PJ231356', band='B7')



