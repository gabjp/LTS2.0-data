#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 23 04:24:22 2022

@author: gjperin
"""

import pickle
import pandas as pd
import numpy as np

useful = ['ID', 'RA','DEC','A', 'B', 'KRON_RADIUS', 'FWHM_n',
       'u_iso', 'J0378_iso', 'J0395_iso', 'J0410_iso', 'J0430_iso',
       'g_iso', 'J0515_iso', 'r_iso', 'J0660_iso', 'i_iso',
       'J0861_iso', 'z_iso', 'SEX_FLAGS_r' ] 

s82_dr4 = pd.read_csv("data/STRIPE82_iDR4.csv", usecols = useful)

for i in range(7,19):
    s82_dr4 = s82_dr4[s82_dr4[useful[i]] != 99]
    print("feito")
    
s82_dr4 = s82_dr4[s82_dr4["SEX_FLAGS_r"] == 0]

#Arrumar critérios de filtragem