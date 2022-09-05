#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 23 00:36:55 2022

@author: gjperin
"""

import pickle
import pandas as pd
import numpy as np
from astropy.stats import sigma_clip, mad_std
from astropy.table import Table

def apply_sigma_clip(data, mag_splus, mag_sdss, sigma_value=4):
    '''
    Apply n-sigma clipping on the S-PLUS and SDSS magnitude difference per 
    magnitude (from S-PLUS) bin of size 0.5 
    
    Keywords arguments:
    data -- full dataset
    mag_splus -- magnitude from S-PLUS
    mag_sdss -- magnitude from SDSS
    sigma_value -- value of n (default: 4)
    create_plot -- determine if plot of mag_sdss - mag_splus x mag_splus is created
    
    returns a subset from data that pass through n-sigma clipping
    '''
    aux2 = data
    final_data = pd.DataFrame([])
    for i in np.arange(np.floor(np.min(data.query(mag_splus+'!=99 and '+mag_splus+'!=-99')[mag_splus])), np.ceil(np.max(data.query(mag_splus+'!=99 and '+mag_splus+'!=-99')[mag_splus])), 0.5):
        aux = aux2[(aux2[mag_splus] > i) & (aux2[mag_splus] <= i+0.5)].query(mag_sdss+'< 90 and '+mag_sdss+"> -90 and "+mag_splus+" <90")
        filtered_data = sigma_clip(
            aux[mag_sdss]-aux[mag_splus], sigma=sigma_value, maxiters=5, stdfunc=mad_std, return_bounds=True)
        if len(filtered_data) != 0:
            final_data = pd.concat(
                [final_data, aux[filtered_data[0].mask == False]], axis=0)

    return final_data


#Carrega os objetos classificados

QSO = Table.read("data/QSO_S82_iDR4.fits", format='fits')
QSO = QSO.to_pandas().assign(target=0).rename(columns={"r":"modelmag_r"})

STAR = Table.read("data/STAR_S82_iDR4.fits", format='fits')
STAR = STAR.to_pandas().assign(target=1)

GAL = Table.read("data/GALAXY_S82_iDR4.fits", format='fits')
GAL = GAL.to_pandas().assign(target=2)
    
QSO = QSO[(QSO['SEX_FLAGS_r'] == 0) & (QSO['r_iso']<=22)]
STAR = STAR[(STAR['SEX_FLAGS_r'] == 0) & (STAR['r_iso']<=22) & (STAR['r_iso']>13)]
GAL = GAL[(GAL['SEX_FLAGS_r'] == 0) & (GAL['r_iso']<=22) & (GAL['zWarning']==0)]

useful = ['ID', 'RA_1','DEC_1','A', 'B', 'KRON_RADIUS', 'FWHM_n',
       'u_iso', 'J0378_iso', 'J0395_iso', 'J0410_iso', 'J0430_iso',
       'g_iso', 'J0515_iso', 'r_iso', 'J0660_iso', 'i_iso',
       'J0861_iso', 'z_iso', 'w1mpro', 'w2mpro', 'target' ] 

total = pd.concat([QSO,STAR,GAL]).reset_index()
total = apply_sigma_clip(total, 'r_iso', 'modelmag_r',)
total = total[useful]

# Filtra valores faltantes
for i in range(7,19):
    total = total[total[useful[i]] != 99]
    
total["file_name"] = total["ID"].str[2:30]
#Filtrar photoflag: SEX_FLAGS_r é equivalente?
    
total.to_csv("./data/clf_total.csv", index=False)

#Arrumar critérios de filtragem

