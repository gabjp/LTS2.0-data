import pandas as pd
import sys
import requests
import tarfile
import os
import multiprocessing
import tqdm

WISE_FOLDER = "./wise_fits"
W1_FOLDER = "./wise_fits/w1"
W2_FOLDER = "./wise_fits/w2"

#CSV column names:
RA = "RA_1"
DEC = "DEC_1"
ID = "ID"

def wise_url(ra, dec, size):
    return f"http://unwise.me/cutout_fits?version=allwise&ra={ra}&dec={dec}&size={size}&bands=12&file_img_m=on"

def download(link, filelocation):
    # from https://stackoverflow.com/questions/33541956/how-to-download-a-file-over-http-with-multi-thread-asynchronous-download-using
    r = requests.get(link, stream=True)

    with open(filelocation, 'wb') as f:
        f.write(r.content)

    tar = tarfile.open(filelocation)
    names = tar.getnames()
    tar.extract(names[0], W1_FOLDER)
    tar.extract(names[1], W2_FOLDER)

    os.remove(filelocation)
    return 

def get_fits(ra_dec_size_id):
    (ra, dec, size, id) = ra_dec_size_id
    url = wise_url(ra,dec,size)
    download(url, WISE_FOLDER + f"/{id}.tar.gz")


def main():
    csv_path = sys.argv[1] + ".csv"

    csv = pd.read_csv(csv_path)

    RAs = list(csv[RA])
    DECs = list(csv[DEC])
    SIZEs = [max(32, 3*(csv['FWHM_n'].iloc[i])) for i in range(len(csv))]
    IDs = list(csv[ID])

    ra_dec_size_id = [(RAs[i], DECs[i], SIZEs[i], IDs[i]) for i in range(len(csv))][2:4]

    with multiprocessing.Pool(multiprocessing.cpu_count()) as pool:
        with tqdm.tqdm(total=len(ra_dec_size_id)) as pbar:
                for _ in pool.imap_unordered(get_fits, ra_dec_size_id):
                    pbar.update(1)

    return 

if __name__ == "__main__":
    main()



# NOTAS:

"""
O problema atual é que os arquivos dentro do tar possuem nomes repetidos. Criar pastas -> extrair arquivos dentro dela -> Mover e renomear -> excluir pasta e tar.

"""