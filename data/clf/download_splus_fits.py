from pathlib import Path
from data.clf.spluslib import SplusService, ImageType

bands = [
  'R', 'I', 'F861', 'Z', 'G', 'F515', 'F660',
  'U', 'F378', 'F395', 'F410', 'F430'
]
ra = [
  160.6341186279781,
  154.0405672404658,
  155.2492264880602,
  175.3182735145332,
  174.6470790167906,
  199.5333321197139,
  351.8919442206255,
  171.9187286476994,
  171.6356941638497,
  330.6821217657193
]
dec = [
  -17.71785960080812,
  -23.63134532606354,
  -29.61571410527581,
  -2.819608003025175,
  -2.805312346592792,
  -11.96523171547243,
  -1.327986392473735,
  -22.21082058266925,
  -22.43693838875754,
  -2.101900566247009
]
ids = [
  'iDR3.SPLUS-n14s08.025197',
  'iDR3.HYDRA-0013.051915',
  'iDR3.HYDRA-0052.035088',
  'iDR3.SPLUS-n03s19.022564',
  'iDR3.SPLUS-n03s19.022691',
  'iDR3.SPLUS-n10s36.042389',
  'iDR3.SPLUS-s02s21.028706',
  'iDR3.SPLUS-n18s15.045604',
  'iDR3.SPLUS-n18s15.053314',
  'iDR3.SPLUS-s03s05.047712'
]


def main():
  # MUDAR AQUI PARA O SEU USUÁRIO E SENHA NO SPLUS.CLOUD:
  service = SplusService('gabrieljp', 'gubi4824')

  for band in bands:
    print(f'\nDonwloading images of band {band}')

    paths = [Path('download') / band / f'{_id}.fits' for _id in ids]

    service.batch_image_download(
      ra=ra,
      dec=dec,
      save_path=paths,
      img_type=ImageType.fits,
      workers=8,
      size=128,
      band=band,
      replace=False
    )


if __name__ == '__main__':
  main()