#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 23 01:36:46 2022

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

bands = ['U', 'F378', 'F395', 'F410', 'F430', 'G',
            'F515', 'R', 'F660', 'I', 'F861', 'Z']



with tqdm(total=len(total)) as pbar:
    for index,row in total.iterrows():
        if os.path.exists('data/clf_crops/{}.npy'.format( row['file_name'])):
            pbar.update(1)
            continue
        size = np.ceil(np.maximum(32, 3 * row['FWHM_n'])).astype(np.int)
        im = np.zeros((32,32,12))
        with tqdm(total=12,leave=False) as ind:
            for i in range(len(bands)):
                # Não posso confiar no size da função do splusdata.
                b = conn.get_cut(row['RA_1'], row['DEC_1'], size, bands[i])[1].data
                if b.shape[0] != 32 or b.shape[1] != 32:
                    b = resize(b, dsize=(32, 32), interpolation=INTER_CUBIC)
                im[:,:,i] = b
                ind.update(1)
        #Aqui, pode haver uma transformação asinh, mas vou pular por enquanto
        with open('data/clf_crops/{}.npy'.format( row['file_name']), 'wb') as f:
            np.save(f, im)
        pbar.update(1)
    
#Otimizar?
    
        
