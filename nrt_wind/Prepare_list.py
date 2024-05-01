import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
from datetime import datetime
from datetime import datetime, timedelta
from nrt_wind.wind import read_wind_mag

def prepare_pre_list(imgPath,inputfile,outputfile):
    sig_th=0.5
    npoint=256
    l=int(np.round(24*60./npoint)) #Window duration 24 hours
    threshold_cons=1. 
    df = pd.read_csv(imgPath+inputfile, names=['fname','y'], header=None)

    df['val'] = 0
    mask = df.y > sig_th
    df.loc[mask, 'val'] = 1

    time = df.fname.str.split('[T.]',expand=False).str.get(-2)
    df["time"]= time.str[0:2]+':'+time.str[2:4]+':'+time.str[4:6]
    date = df.fname.str.split('[T_]',expand=False).str.get(-2)
    df["date"] = date
    df['value_grp'] = (df['val'].diff(1) != 0).astype('int').cumsum()
    grouped = df.groupby('value_grp')
    df_final = pd.DataFrame({'BeginDate': grouped.date.first(),
                             'BeginTime': grouped.time.first(),
                             'EndDate': grouped.date.last(),
                             'EndTime': grouped.time.last(),
                             'Consecutive': grouped.size(),
                             'Value': grouped.val.first()}).reset_index(drop=True)
    # df_final
    c=0
    file= open(imgPath+'List1_prelim.txt', 'w')
    ii=0
    while ii< (len(df_final.Value)):
        
        if df_final.Value[ii] ==1 and df_final.Consecutive[ii]>=threshold_cons:
            
            end_e=(str(df_final.EndDate[ii])+' '+str(df_final.EndTime[ii]))
            ttee = (datetime.strptime(end_e, '%Y-%m-%d %H:%M:%S') - datetime(1970, 1, 1, 0, 0)).total_seconds()
            end_e_new=pd.to_datetime(ttee+np.round(l*npoint*60./3600)*3600.,unit='s')
            c=c+1
            file.writelines(str(df_final.BeginDate[ii])+' '+str(df_final.BeginTime[ii])+' '+str(end_e_new)+'\n')
        ii=ii+1
    file.close()
    print(c)
    c_fin=0
    if os.path.getsize(imgPath+'List1_prelim.txt') == 0:
        print('no FRs')
    
  
    else:
        df_extreme = pd.read_csv(imgPath+'List1_prelim.txt', sep=" ", header=None)
        i=0
        file= open(imgPath+outputfile, 'w')
        if len(df_extreme)>1:
            while i< (len(df_extreme[1])):
                end_e=str(df_extreme[2][i])+' '+str(df_extreme[3][i])
                ttee=(datetime.strptime(str(end_e)[0:19], "%Y-%m-%d %H:%M:%S")-datetime(1970, 1, 1, 0, 0)).total_seconds()
                begin_e=str(df_extreme[0][i+1])+' '+str(df_extreme[1][i+1])
                ttbe=(datetime.strptime(str(begin_e)[0:19], "%Y-%m-%d %H:%M:%S")-datetime(1970, 1, 1, 0, 0)).total_seconds()
                if ttee<ttbe:
                    file.writelines(str(df_extreme[0][i-c_fin])+' '+str(df_extreme[1][i-c_fin])+' '+str(end_e)+'\n')
                    c_fin=0
                else:
                    c_fin=c_fin+1
                i=i+1  
        if len(df_extreme)==1:
            file.writelines(str(df_extreme[0][0])+' '+str(df_extreme[1][0])+' '+str(df_extreme[2][0])+' '+str(df_extreme[3][0])+'\n')
    file.close()
    return


def boundary_finding(imgPath,inputfile,tstart,tend,outfile): 
    npoint=256
    sig_th = 0.5
    l=int(np.round(24*60./npoint))
    shift=np.round(l*npoint*60*0.04/60)
    dfr = pd.read_csv(imgPath+inputfile, names=['fname', 'y'], header=None)
    time = dfr.fname.str.split('[T.]',expand=False).str.get(-2)
    dfr["time"]= time.str[0:2]+':'+time.str[2:4]+':'+time.str[4:6]
    date = dfr.fname.str.split('[T_]',expand=False).str.get(-2)
    dfr["date"] = date

    dfr['val'] = 0
    mask = dfr.y > sig_th
    dfr.loc[mask, 'val'] = 1

    dfr_ = dfr[(dfr['date']+' '+dfr['time'] >= tstart) & (dfr['date']+' '+dfr['time'] < tend)]
    dfr = dfr_.reset_index(drop=True)

    tstart=(datetime.strptime(str(tstart)[0:19], "%Y-%m-%d %H:%M:%S")-datetime(1970, 1, 1, 0, 0)).total_seconds()
    tend=(datetime.strptime(str(tend)[0:19], "%Y-%m-%d %H:%M:%S")-datetime(1970, 1, 1, 0, 0)).total_seconds()

    tt=[]
    if dfr.empty!=True:
        for i in dfr.index:
            tt.append(dfr['date'][i]+' '+dfr['time'][i])
            
        ti=pd.to_datetime(tt)
        tend=pd.to_datetime((pd.to_datetime(ti[-1])-pd.to_datetime('1970-01-01 00:00:00')).total_seconds()+np.round(l*npoint*60./3600)*3600.,unit='s')

        v = dfr['val']
        plt.figure(figsize=(15, 5))
        plt.bar(pd.to_datetime(tt),dfr['val'],width=0.002)
        for i in  dfr.index:
            if v[i]==1:
                
                t_ss=(datetime.strptime(str(ti[i]), "%Y-%m-%d %H:%M:%S")-datetime(1970, 1, 1, 0, 0)).total_seconds()
                t_ei=pd.to_datetime(t_ss+l*npoint*60.,unit='s')
            
                plt.axvspan(ti[i],t_ei, ymin=0, ymax=1, alpha=0.08, color='red')
    
            else:
                t_ss=(datetime.strptime(str(ti[i]), "%Y-%m-%d %H:%M:%S")-datetime(1970, 1, 1, 0, 0)).total_seconds()
                t_ei=pd.to_datetime(t_ss+l*npoint*60.,unit='s')
                plt.axvspan(ti[i],t_ei, ymin=0, ymax=1, alpha=0.08, color='none')
        t_s=datetime.strptime(str(ti[0])[0:19], "%Y-%m-%d %H:%M:%S")
    

        df= read_wind_mag( t_s,t_ei)
        

        bxn=df.Bx.rolling(window=l,step=l).mean()
        byn=df.By.rolling(window=l,step=l).mean()
        bzn=df.Bz.rolling(window=l,step=l).mean()

        plt.plot(np.sqrt(bxn*bxn+byn*byn+bzn*bzn),label='|B|')
        plt.plot(bxn,label='Bx')
        plt.plot(byn,label='By')
        plt.plot(bzn,label='Bz')
        plt.legend()
        def datetime_range(start, end, delta):
            current = start
            while current < end:
                yield current
                current += delta


        dts = [pd.to_datetime(dt.strftime('%Y-%m-%d %H:%M:%S') )for dt in 
            datetime_range(datetime.strptime(str(ti[0]), "%Y-%m-%d %H:%M:%S"), t_ei, 
            timedelta(minutes=shift))]
        
        vn=[0 for k in range(len(dfr)+int(np.round(l*npoint*60/3600)))]
        for gg in range(len(ti)):
            if v[gg]==1:
                for j in range(gg,gg+int(np.round(l*npoint*60/3600))):
                    vn[j]=vn[j]+1
            else:
                for j in range(gg,gg+int(np.round(l*npoint*60/3600))):
                    vn[j]=vn[j]+0



        q=[]
        if np.max(vn)>1:
            
            for kkk in range(len(vn)):
                if vn[kkk]>=0.5*max(vn): #FWHM
                    q.append(kkk)
            start_boundary=dts[q[0]]
            end_boundary=dts[q[-1]]
            plt.plot(dts,vn[0:len(dts)],color='k',linestyle='--',label='$V_{cumsum}$')
            plt.axvline(start_boundary, color='k', linestyle='-', lw=2)
            plt.axvline(end_boundary, color='k', linestyle='-', lw=2)

            df_mini=read_wind_mag(datetime.strptime(str(start_boundary), "%Y-%m-%d %H:%M:%S"),datetime.strptime(str(end_boundary), "%Y-%m-%d %H:%M:%S"))
            if df_mini.empty!=True:
                df_mini=df_mini.dropna()
                bxnmini=df_mini.Bx
                bynmini=df_mini.By
                bznmini=df_mini.Bz
                btotmini=np.sqrt(bxnmini*bxnmini+bynmini*bynmini+bznmini*bznmini)

            if np.mean(btotmini)>=5:#b_th = 5 nT:
                print(start_boundary,end_boundary)
                outfile.writelines(str(start_boundary)+' '+str(end_boundary)+'\n')
                return  start_boundary,end_boundary