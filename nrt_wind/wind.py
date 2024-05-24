from ai import cdas
import pandas as pd
from datetime import datetime
import numpy as np
# This function returns a dataframe containing Wind/MFI data. Unit of B fields are nT. Unit of `date_time` is UTC

def read_wind_mag(start, end):
    dataset = 'WI_H0_MFI'
    vlist = ['BGSE', 'BF1']
    data = cdas.get_data('sp_phys', dataset, datetime.strptime(str(start)[0:19], "%Y-%m-%d %H:%M:%S"), 
                         datetime.strptime(str(end)[0:19], "%Y-%m-%d %H:%M:%S"), variables=vlist)
    df = pd.DataFrame(data={'date_time':data['EPOCH'],
            'Bx':data['BX_(GSE)'],
            'By':data['BY_(GSE)'],
            'Bz':data['BZ_(GSE)']})
    df['B'] = np.sqrt(data['BX_(GSE)']**2 + data['BY_(GSE)']**2 + data['BZ_(GSE)']**2)
    df.set_index('date_time', inplace=True)
    df.where(df > -1.0e+29, np.nan, inplace=True)
    df.where(df < 1.0e+29, np.nan, inplace=True)
    return df
def read_wind_mag_GSM(start, end):
    dataset = 'WI_H0_MFI'
    vlist = ['BGSM', 'BF1']
    data = cdas.get_data('sp_phys', dataset, datetime.strptime(str(start)[0:19], "%Y-%m-%d %H:%M:%S"), 
                         datetime.strptime(str(end)[0:19], "%Y-%m-%d %H:%M:%S"), variables=vlist)
    df = pd.DataFrame(data={'date_time':data['EPOCH'],
            'Bx':data['BX_(GSM)'],
            'By':data['BY_(GSM)'],
            'Bz':data['BZ_(GSM)']})
    df['B'] = np.sqrt(data['BX_(GSM)']**2 + data['BY_(GSM)']**2 + data['BZ_(GSM)']**2)
    df.set_index('date_time', inplace=True)
    df.where(df > -1.0e+29, np.nan, inplace=True)
    df.where(df < 1.0e+29, np.nan, inplace=True)
    return df
