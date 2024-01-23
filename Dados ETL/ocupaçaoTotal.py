import os
import timeit
from tkinter.filedialog import *

import pandas as pd

inicio = timeit.default_timer()

caminho = askdirectory()
arquivos = os.listdir(caminho)
dirDestino = r'C:/Users/2102555972/Documents/Desktop/GESTAO_CD_318/Dev/Python/Python/datajoin'

listaArquivos = []


def defineDataFrame(caminho, arquivo):
    df = pd.read_excel(open(os.path.join(caminho, arquivo), 'rb'))
    return df


for arquivo in arquivos:
    df = defineDataFrame(caminho, arquivo)
    listaArquivos.append(df)
    df = pd.concat(listaArquivos)

df.sort_values(by=['Filial'], inplace=True)
df.to_excel(dirDestino + '/' + 'OcupacaoGeral.xlsx', index=False)

fim = timeit.default_timer()

print(fim - inicio)
