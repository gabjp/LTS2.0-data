from pathlib import Path
from spluslib import SplusService, ImageType
import pandas as pd

df = pd.read_csv('unl_small_noise.csv')
df = df[df.ID == 'iDR4_3_STRIPE82-0004_0013352']
bands = [
  'R', 'I', 'F861', 'Z', 'G', 'F515', 'F660',
  'U', 'F378', 'F395', 'F410', 'F430'
]
print(df)

"""
Ordem correta:  [u_iso,
             J0378_iso,
             J0395_iso,
             J0410_iso,
             J0430_iso,
             g_iso,
             J0515_iso,
             r_iso,
             J0660_iso,
             i_iso,
             J0861_iso,
             z_iso]
"""

ra = list(df.RA)
dec = list(df.DEC)
ids = df.ID
sizes = [max(32, 3*(df['FWHM_n'].iloc[i])) for i in range(len(df))]


def main():
  # MUDAR AQUI PARA O SEU USUÁRIO E SENHA NO SPLUS.CLOUD:
  service = SplusService('gabrieljp', 'gubi4824')

  for band in bands:
    print(f'\nDonwloading images of band {band}')

    paths = [Path('./unl_fits') / band / f'{_id}.fits' for _id in ids]

    print(len(paths))

    service.batch_image_download_ms(
      ra=ra,
      dec=dec,
      save_path=paths,
      img_type=ImageType.fits,
      workers=8,
      sizes=sizes,
      band=band,
      replace=False
    )


if __name__ == '__main__':
  main()