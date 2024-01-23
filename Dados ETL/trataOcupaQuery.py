import pandas as pd
import os
from tkinter import Tk
from tkinter.filedialog import *
import timeit

Tk().withdraw()
caminho = os.getcwd() + '\\support_files'
arquivo = os.path.basename(os.getcwd() + '\\support_files\\DeparaOcp.xlsx')
inicio = timeit.default_timer()

def removeColunas(df):
    df.drop(['Cd    Comp  Item', 'Comp', 'loc', 'Valor'], axis=1, inplace=True)

def reordenarColunas(dataframe):
    dataframe = df.reindex(
        columns=['Cd', 'Item', 'Desc', 'Aisl', 'Bloc', 'Nv', 'Qqp', 'Qtd', 'eq', 'END', 'Sts', 'Setor',
                 'Desc_setor', 'Cub', 'Cub Eqp', 'Cub Qtd', '% Ocupação Local', '%Ocupação Palet'])
    return dataframe

deparaFrame = pd.read_excel(open(os.path.join(caminho, arquivo), 'rb'))
dirOrigem = askopenfilename(filetypes=("Arquivos de Excel", "*.xlsx"))
baseName = os.path.basename(dirOrigem)
fileName = os.path.splitext(baseName)[0]
dirDestino = r'C:/Users/2102555972/Documents/Desktop/GESTAO_CD_318/Dev/Python/Python/datajoin/bases'
df = pd.read_fwf(dirOrigem, encoding='cp1252', errors='ignore', header=1)
df.drop(columns='Unnamed: 13', inplace=True)

df_remove = df.loc[(df['Cd    Comp  Item'].str.startswith('-')) | (df['Cd    Comp  Item'].str.contains('/')) |
                   (df['eq'].str.contains('Pecas')) | (df['Cd    Comp  Item'].str.startswith('Cd')) |
                   (df['Cd    Comp  Item'].str.startswith(''))]

rename_dict = {'Cd': 'Filial', 'Item': 'SKU', 'Desc': 'Descrição', 'Aisl': 'Rua', 'Bloc': 'Blocagem', 'Nv': 'Nivel',
               'Qqp': 'Equip', 'eq': 'Qtd Max', 'Sts': 'Status', 'Cub': 'Cub Uni', 'Cub Qtd': 'Cub total',
               'END': 'Eqp/End', 'Cub Eqp': 'Cub Palet', '%Ocupação Palet': '% Ocupação Palet'}

df.drop(df_remove.index, axis=0, inplace=True)
df[['Cd', 'Comp', 'Item']] = df['Cd    Comp  Item'].str.split('  ', expand=True)
df[['Desc']] = ['--']
df[['Cub Qtd', 'Cub Eqp']] = ['-', '-']
df = df.astype({'Setor': int}, errors='ignore')
df = pd.merge(df, deparaFrame, how='left', on='Setor')
removeColunas(df)
df = reordenarColunas(df)

df['Item'].fillna('-', inplace=True)
df['Aisl'].fillna('-', inplace=True)
df['Bloc'].fillna('-', inplace=True)
df['Nv'].fillna('-', inplace=True)

empty_sku_remove = df.loc[(df['Item'].str.startswith('-'))]
remove_filiais = df.loc[
    (df['Cd'].str.startswith(('0125', '1088', '1445', '1475', '1522', '1668', '1760', '1850', '1876',
                              '1888', '3200')))]

df.drop(empty_sku_remove.index, axis=0, inplace=True, errors='ignore')
df.drop(remove_filiais.index, axis=0, inplace=True, errors='ignore')
df.replace({'Cd': {'0014': '1401'}}, inplace=True)

altera_coluna = {'Cub': float, 'Cub Qtd': float, 'Cub Eqp': float, 'Cd': int, 'Item': int, 'Aisl': str, 'Bloc': str,
                 'Nv': str, 'Qtd': int, 'eq': int, 'END': int}

df = df.astype(altera_coluna, errors='ignore')
df.sort_values(by=['Cd'], inplace=True)
df.rename(columns=rename_dict, inplace=True, errors='ignore')
filtro_boa = df.loc[(df['Status'].str.startswith('QEB')) | (df['Status'].str.startswith('SLD'))]
df.drop(filtro_boa.index, axis=0, inplace=True, errors='ignore')
df['Cub Palet'] = df['Cub Uni'] * df['Eqp/End'] * df['Qtd Max']
df['Cub total'] = df['Cub Uni'] * df['Qtd']
df['% Ocupação Palet'] = df['Cub total'] / df['Cub Palet']


df.to_excel(dirDestino + '/' + 'OcupaTratado.xlsx', index=False, engine='xlsxwriter')

fim = timeit.default_timer()
print(fim - inicio)
