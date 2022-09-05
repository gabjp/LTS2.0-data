#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 16 10:31:34 2022

@author: gjperin
"""

import os
import subprocess
import numpy as np
from tqdm import tqdm
from astropy.io import fits

t = 0
order = [10,0,1,2,3,7,4,9,5,8,6,11]
path_of_the_directory= './data/clf_crops_comp'
obj_list = os.listdir(path_of_the_directory)

with tqdm(total = len(obj_list)) as pbar:
    for filename in obj_list:
        f = os.path.join(path_of_the_directory,filename)
        
        dir = os.path.join('./data/clf_crops', filename)
        if not os.path.exists(dir):
            os.mkdir(dir)
        
        p = subprocess.run(['tar', '-zxf', f, '--directory', dir ], stderr = subprocess.DEVNULL)
        
        if p.returncode != 0:
            t+=1
            
        else:
            infiles = sorted(os.listdir(dir))
            l = []
            
            for index in order:
                l.append(fits.open(os.path.join(dir,infiles[index]))[1].data)
                
            final = np.array(l)
            savefile = os.path.join('./data/clf_crops', f"{filename}.npy")
            
            with open(savefile, 'xb') as sf:
                np.save(sf,final)
                
        subprocess.run(['rm', '-r', dir])
        pbar.update(1)

print(t)