import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib

def DATAFRAME_generator(datacsvfile, datacsvfile_second, csvfile):
    config = pd.read_csv(csvfile)
    config['Zenith']=config['Dec']-19
    if 'Name' in config.columns:
        config.sort_values(by='Name', inplace=True)
    else:
        raise KeyError(f"[ERROR] La columna 'Name' no está en {csvfile}. Columnas disponibles: {config.columns.tolist()}")

    config.reset_index(drop=True, inplace=True)

    columns = ['Spectrum', 'TS', 'sqrt(TS)', 'flux', 'lowerErr', 'upperErr', 'lowerBound', 'upperBound']
    columns_second = ['Name'] + [item + '_2ndT' for item in columns]

    data1 = pd.read_csv(datacsvfile, sep='\s+', names=columns_second)
    data2 = pd.read_csv(datacsvfile_second, sep='\s+', names=['Name'] + columns)

    data1.drop_duplicates(inplace=True)
    data2.drop_duplicates(inplace=True)

    data1.sort_values(by='Name', inplace=True)
    data2.sort_values(by='Name', inplace=True)

    data = pd.merge(data1, data2, on='Name')
    data.sort_values(by='Name', inplace=True)

    alldf = pd.concat([data, config], axis=1)
    alldf = alldf.loc[:, ~alldf.columns.duplicated()]

    # zenith = pd.read_csv(path_zenith, sep='\s+')
    # zenith = zenith.drop_duplicates(subset='Name')

    alldf = alldf.drop_duplicates(subset='Name')
    # alldf_zenith = pd.merge(alldf on='Name', how='outer')

    return alldf
