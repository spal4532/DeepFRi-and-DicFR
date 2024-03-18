from pathlib import Path
import ssl
import copy 

from ai import cdas
import pandas as pd
import numpy as np



def read_wind_mag(start, end, cache_dir='./cdas-data'):
    """
    Load magnetic field data variables for Wind mission (MFI instrument)
    using the AI.CDAS package

    start/end: datetime objects for start/end time of interest
    cache_dir: (optional) directory for storing downloaded data.  
                Defaults to './cdas-data/'

    -----
    Returns a pandas DataFrame
    """

    ssl._create_default_https_context = ssl._create_unverified_context 

    cache_dir = Path(cache_dir)
    if not cache_dir.exists():
        cache_dir.mkdir(parents=True)
    cdas.set_cache(True, cache_dir)

    dataset = 'WI_H0_MFI'
    vlist = ['BGSE', 'BF1']
    try:
        data = cdas.get_data('sp_phys', dataset, start, end, variables=vlist)
    except:
        print(f"CDAS Error loading {dataset} data for this date range")
        return pd.DataFrame()

    map_mag = {'date_time':data['EPOCH'],
        'Bx':data['BX_(GSE)'],
        'By':data['BY_(GSE)'],
        'Bz':data['BZ_(GSE)']}
    df = pd.DataFrame(data=map_mag)
    df['B'] = np.sqrt(data['BX_(GSE)']**2 + data['BY_(GSE)']**2 + data['BZ_(GSE)']**2)
    df['ddoy'] = df.date_time.dt.day_of_year \
                + (df.date_time.dt.hour + (df.date_time.dt.minute)/60 \
                + (df.date_time.dt.second)/3600)/24
    df.set_index('date_time', inplace=True)

    # Rudimentary quality filter
    df.where(df > -1.0e+29, np.nan, inplace=True)
    df.where(df < 1.0e+29, np.nan, inplace=True)

    # Store metadata
    df.attrs['data_source'] = f'Wind MFI H0 1min dataset [{dataset}]'
    df.attrs['timezone'] = 'UTC'    
    df.attrs['coord_system'] = 'GSE'
    df.Bx.attrs['unit'] = 'nT'
    df.By.attrs['unit'] = 'nT'
    df.Bz.attrs['unit'] = 'nT'
    df.B.attrs['unit'] = 'nT'

    units = {}
    for c in df:
        if 'unit' in df[c].attrs:
            units[c] = df[c].attrs['unit']

    if len(units) > 0:
        df.attrs['units'] = units

    return df

