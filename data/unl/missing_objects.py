import os
import pandas as pd
import tqdm

directory = "/media/gjperin/64gb/R"
df = pd.read_csv("unl_small.csv")
with tqdm.tqdm(total=len(df)) as pbar:
    for id in df.ID:
        if (f"{id}.fits") not in os.listdir(directory):
            print(id)
        pbar.update(1)

    


