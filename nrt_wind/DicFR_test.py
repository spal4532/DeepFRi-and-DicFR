import pickle
import numpy as np
import matplotlib.pyplot as plt 
from nrt_wind.wind import read_wind_mag
from nrt_wind.wind import read_wind_mag_GSM
from datetime import datetime
import scipy
import pickle
import pandas as pd
import glob
from PIL import Image
import os
import shutil
from nrt_wind.wind import read_wind_mag

###########################################################################################################
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




##########################################################################################################

def create_hodogram(st,et,c,file):
  
    l=5
    st=datetime.strptime(str(st)[0:19], "%Y-%m-%d %H:%M:%S")
    et=datetime.strptime(str(et)[0:19], "%Y-%m-%d %H:%M:%S")
    df= read_wind_mag_GSM(st,et)
    if df.empty!=True:
        if df['Bx'].isna().sum()/len(df.Bx)<=0.1 and df['By'].isna().sum()/len(df.By)<=0.1 and df['Bz'].isna().sum()/len(df.Bz)<=0.1:
          
            df=df.interpolate()
         
            bxn=df.Bx.rolling(window=l,step=l).mean()
            byn=df.By.rolling(window=l,step=l).mean()
            bzn=df.Bz.rolling(window=l,step=l).mean()
            
            
            mag = np.sqrt( bxn*bxn + byn*byn + bzn*bzn )
            bx=(bxn/ mag)
            by=(byn/ mag)
            bz=(bzn/ mag)
            # imgPath='./dstfr_wind_'+'2008-2014'+'_30_30/'
            imgPath=file
            
            
            fig = plt.figure(figsize=(0.54,0.54))
            ax = fig.add_axes([0.,0.,1.,1.])
            ax.set_ylim(-1.25,1.25)
            ax.set_xlim(-1.25,1.25)
            # ax.set_axis_off()
            
        

            outname = 'dstfr_wind'+ str(c)+'.jpg'
    
            createPlot(fig,ax,bx,by,bz,0, imgPath + 'bx_by/' +outname)
            createPlot(fig,ax,bx,by,bz,1, imgPath + 'bx_bz/' +outname)
            createPlot(fig,ax,bx,by,bz,2, imgPath + 'bz_by/' +outname)   
    return

def DicFR(imgPath,list2,finallist):
    l=5
    load_model = pickle.load(open('./nrt_wind/difr_gsm.pkl', 'rb')) 
    # load_model  

    dstPath=imgPath+'dstfr_wind/'
    path = os.path.join(dstPath, 'bx_by')
    isFile = os.path.isdir(path)
    if isFile==True:
        shutil.rmtree(path)
    os.makedirs(path)
    path = os.path.join(dstPath, 'bx_bz')
    isFile = os.path.isdir(path)
    if isFile==True:
        shutil.rmtree(path)
    os.makedirs(path)
    path = os.path.join(dstPath, 'bz_by')
    isFile = os.path.isdir(path)
    if isFile==True:
        shutil.rmtree(path)
    os.makedirs(path)

    if os.path.getsize(imgPath+list2) == 0:
        return 'no FRs'
    else:

        df_extreme_m = pd.read_csv(imgPath+list2, sep=" ", header=None)
        file= open(imgPath+finallist, 'w')
        for oq in df_extreme_m.index:
            begin=df_extreme_m[0][oq]+' '+df_extreme_m[1][oq]
            end=df_extreme_m[2][oq]+' '+df_extreme_m[3][oq]
            create_hodogram(begin,end,oq,dstPath) # create hodogram and we will use bz_by
            files =dstPath+'bz_by/dstfr_wind'+str(oq)+'.jpg'
            img=Image.open(files).convert('L')
            bl_count = np.sum(np.array(img) == 0)
            
            c_bp = 0
            for y in range(0,int(np.round(img.height))):
                for x in range(0,int(np.round(img.width/2))):
                    pixel = img.getpixel((x, y))
                    if pixel ==0:
                        c_bp += 1
            
            df_mini=read_wind_mag_GSM(datetime.strptime(begin, "%Y-%m-%d %H:%M:%S"),datetime.strptime(end, "%Y-%m-%d %H:%M:%S"))
            
            if df_mini.empty!=True:
                
                bznmini=df_mini.Bz.rolling(window=l,step=l).mean()
                
                xtt=[[np.min(bznmini),  c_bp/bl_count]]
                # ypp= clf.predict(xtt)
                ypp = load_model.predict(xtt) 

                file.writelines(begin+' '+end+' '+ypp+' \n')
            

        file. close()  
        return      
      
      
     
    
