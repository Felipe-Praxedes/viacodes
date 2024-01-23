import numpy as np
import pandas as pd
import os

dos_caminho = os.path.join(os.path.realpath(os.getcwd()), "Dos.txt")
df_dos = pd.read_csv(dos_caminho, sep=",",header=None, encoding='latin-1', dtype=str)

for index, do in df_dos.iterrows():
    print(do)