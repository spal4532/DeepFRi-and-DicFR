import numpy as np
import pandas as pd
import os
from matplotlib import pyplot
import matplotlib.pyplot as plt
import pickle
import glob
import shutil
from PIL import Image
from datetime import datetime
from nrt_wind.wind import read_wind_mag
from pandas.errors import EmptyDataError

def createPlot(fig, ax, x, y, z, index, outFile):

    if (index == 0):
        ax.plot(x, y, 'k') # 'k' is color abbreviation for black
        ax.scatter(x[0], y[0], s=20, c='black')
    elif (index == 1):
        ax.plot(x, z, 'k') # 'k' is color abbreviation for black
        ax.scatter(x[0], z[0], s=20, c='black')
    else:
        ax.plot(z, y, 'k') # 'k' is color abbreviation for black
        ax.scatter(z[0], y[0], s=20, c='black')
    
    fig.savefig(outFile)
    ax.cla()
    ax.set_ylim(-1.25,1.25)
    ax.set_xlim(-1.25,1.25)
    ax.set_axis_off()


def combine(imgp):
    """
    Take a list of 3, n x n images and combine into one image n x 3n x 1
    """
    shape1 = imgp[0].shape
    shape2 = imgp[1].shape
    shape3 = imgp[2].shape
    if ((shape1 != shape2) or (shape1 != shape3) or (shape1[0] != shape1[1])):
        print("Image Shapes must match and be square")
        return None
    else:
        img = np.concatenate(imgp, axis=1)
        return img
    

def create_hodogram_realFR_t_minus_24hr(st,et,imgPath):
    t_s=datetime.strptime(str(st)[0:19], "%Y-%m-%d %H:%M:%S")
    t_ef=datetime.strptime(str(et)[0:19], "%Y-%m-%d %H:%M:%S")
    
    tts=(t_s-datetime(1970, 1, 1, 0, 0)).total_seconds()
    npoint=256
    l=int(np.round(24*60./npoint)) #window size=8hrs
    tts_p=tts-l*npoint*60.
    t_sp=pd.to_datetime(tts_p,unit='s')
    cin=0
    while tts<=(t_ef-datetime(1970, 1, 1, 0, 0)).total_seconds()+l*npoint*60.:
        
        try:
            df= read_wind_mag( t_sp,t_s)
        except EmptyDataError:
            df= pd.DataFrame()
        df= read_wind_mag( t_sp,t_s)
        if df['Bx'].isna().sum()/len(df.Bx)<=0.1 and df['By'].isna().sum()/len(df.By)<=0.1 and df['Bz'].isna().sum()/len(df.Bz)<=0.1:
            df=df.interpolate()
            bxn=df.Bx.rolling(window=l,step=l).mean()
            byn=df.By.rolling(window=l,step=l).mean()
            bzn=df.Bz.rolling(window=l,step=l).mean()
            mag = np.sqrt( bxn*bxn + byn*byn + bzn*bzn )
            bx=(bxn/ mag)
            by=(byn/ mag)
            bz=(bzn/ mag)
            fig = plt.figure(figsize=(0.54,0.54))
            ax = fig.add_axes([0.,0.,1.,1.])
            ax.set_ylim(-1.25,1.25)
            ax.set_xlim(-1.25,1.25)
            ax.set_axis_off()
            
            count=0

            outname = 'wind' + str(cin) +' '+str(t_sp)+'.jpg'
            
            createPlot(fig,ax,bx,by,bz,0, imgPath + 'bx_by/' +outname)
            createPlot(fig,ax,bx,by,bz,1, imgPath + 'bx_bz/' +outname)
            createPlot(fig,ax,bx,by,bz,2, imgPath + 'bz_by/' +outname)

            count+=1
           
            bxyPath = imgPath+'bx_by/'
            bxzPath = imgPath+'bx_bz/'
            bzyPath = imgPath+'bz_by/'

            bxyFiles = glob.glob(bxyPath+'*.jpg')
            bxzFiles = glob.glob(bxzPath+'*.jpg')
            bzyFiles = glob.glob(bzyPath+'*.jpg')


            bxyFiles
            ix=0
            for bxyfile in bxyFiles:
                filename = bxyFiles[ix].split('/')[-1]
                bxzfile = bxzPath + filename
                bzyfile = bzyPath + filename

                bxyarr = np.array(Image.open(bxyfile).convert('L'))
                bxzarr = np.array(Image.open(bxzfile).convert('L'))
                bzyarr = np.array(Image.open(bzyfile).convert('L'))
                im = (Image.fromarray(combine([bxyarr, bxzarr, bzyarr])))
                path = imgPath+'concat/' + filename
                im.save(path)
                ix+=1 
            cin=cin+1
        tts=tts+npoint*0.04*l*60. #(the window is shifted with 4% of npoint=61 min)
        t_s=pd.to_datetime(tts,unit='s')
        tts_p=tts-l*npoint*60.
        t_sp=pd.to_datetime(tts_p,unit='s')
        
    return