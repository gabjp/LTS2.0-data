import numpy as np
import os
import pandas as pd
from astropy.io import fits
import tqdm
from cv2 import resize, INTER_CUBIC
import multiprocessing
from os.path import exists

ids = pd.read_csv("unl_small.csv").ID
zps = pd.read_csv("iDR4_zero-points.csv")
fits_folder = "/media/gjperin/64gb"
bands = ["U",
             "F378",
             "F395",
             "F410",
             "F430",
             "G",
             "F515",
             "R",
             "F660",
             "I",
             "F861",
             "Z"]
band_to_zp = {"U":"ZP_u",
            "F378":"ZP_J0378",
            "F395":"ZP_J0395",
            "F410":"ZP_J0410",
            "F430":"ZP_J0430",
            "G":"ZP_g",
            "F515":"ZP_J0515",
            "R":"ZP_r",
            "F660":"ZP_J0660",
            "I":"ZP_i",
            "F861":"ZP_J0861",
            "Z":"ZP_z"
        }
    
def calibrate(x,id,band):
    ps = 0.55
    zp = float(zps[zps["Field"]==id[7:20]][band_to_zp[band]])
    return (10**(5-0.4*zp)/(ps*ps))*x

def gather_bands(id):
    if exists(f"all_objects/{id}.npy"):
        return 

    mat = []
    for band in bands:
        #print(f'{fits_folder}/{band}/{id}.fits')
        x = fits.open(f'{fits_folder}/{band}/{id}.fits')[1].data
        x = resize(x, dsize=(32, 32), interpolation=INTER_CUBIC)
        x = calibrate(x,id,band)
        mat.append(x)
    np.save(f"all_objects/{id}.npy", np.array(mat))


with multiprocessing.Pool(multiprocessing.cpu_count()) as pool:
    with tqdm.tqdm(total=len(ids)) as pbar:
            for _ in pool.imap_unordered(gather_bands, ids):
                pbar.update(1)