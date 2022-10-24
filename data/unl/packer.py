import numpy as np
import os
import pandas as pd
from astropy.io import fits
import tqdm
from cv2 import resize, INTER_CUBIC
import multiprocessing
from os.path import exists

csv_name = "raw_fits/unl_small_noise.csv"
fits_folder = "unl_fits"

df = pd.read_csv(csv_name)
ids = df.ID
zps = pd.read_csv("iDR4_zero-points.csv")
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
    
manager = multiprocessing.Manager()
missing = manager.list()
lock = multiprocessing.Lock()

def calibrate(x,id,band):
    ps = 0.55
    zp = float(zps[zps["Field"]==id[7:20]][band_to_zp[band]])
    return (10**(5-0.4*zp)/(ps*ps))*x

def gather_bands(id):
    if exists(f"raw_fits/all_objects/{id}.npy"):
        return 

    mat = []
    for band in bands:
        #print(f'{fits_folder}/{band}/{id}.fits')
        global missing, lock
        fits_file = f'{fits_folder}/{band}/{id}.fits'
        if not exists(fits_file) or os.path.getsize(fits_file)<17000:
            missing.append(id)
            return

        x = fits.open(f'{fits_folder}/{band}/{id}.fits')[1].data
        x = resize(x, dsize=(32, 32), interpolation=INTER_CUBIC)
        x = calibrate(x,id,band)
        mat.append(x)
    np.save(f"raw_fits/all_objects/{id}.npy", np.array(mat))


with multiprocessing.Pool(multiprocessing.cpu_count()) as pool:
    with tqdm.tqdm(total=len(ids)) as pbar:
            for _ in pool.imap_unordered(gather_bands, ids):
                pbar.update(1)

print(len(missing))
df = df[~(df.ID.isin(list(missing)))]
df.to_csv(csv_name)
print(len(df))