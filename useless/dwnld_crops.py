#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 25 19:37:09 2022

@author: gjperin
"""

import pickle
import pandas as pd
import numpy as np
import splusdata
from cv2 import imread, imwrite, resize, INTER_CUBIC
from tqdm import tqdm
import os

total = pd.read_csv("data/clf_total.csv")
conn = splusdata.connect('gabrieljp', 'gubi4824')

with tqdm(total=len(total)) as pbar:
    for index,row in total.iterrows():
        if os.path.exists('data/clf_crops_comp/{}.tar.gz'.format( row['file_name'])):
            pbar.update(1)
            continue
        size = np.ceil(np.maximum(32, 3 * row['FWHM_n'])).astype(np.int)  
        b = conn.get_cut(row['RA_1'], row['DEC_1'], size, "all", filepath=f"data/clf_crops_comp/{row['file_name']}")
        pbar.update(1)