import matplotlib.pyplot as plt 
import numpy as np
import pandas as pd

df = pd.read_csv("clf.csv")
num = 1
print(df[df.target==2 & (df.r_iso<14)].iloc[num])
x = np.load(f"./all_objects/{df[(df.target==2) & (df.r_iso<14)].iloc[num].ID}.npy")
for i in x:
    print(f"max: {np.max(i)}")
    print(f"min: {np.min(i)}")
    plt.matshow(i)
plt.show()