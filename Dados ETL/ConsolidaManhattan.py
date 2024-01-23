import os
import timeit
from tkinter.filedialog import *

import pandas as pd

inicio = timeit.default_timer()

caminho = askdirectory()
arquivos = os.listdir(caminho)
caminhoDepara = os.getcwd()
arquivoDepara = os.path.basename(os.getcwd() + '\\Depara_Setor.xlsx')
dirDestino = r'C:/Users/2102555972/Documents/Desktop/GESTAO_CD_318/Dev/Python/Python/datajoin/bases'

listaArquivos = []
nomeArquivo: str = ""

def defineDataFrame(caminho, arquivo):
    df = pd.read_excel(open(os.path.join(caminho, arquivo), 'rb'))
    return df

def removeColunas(df):
    df.drop(['Data criação inventário', 'Data modificação inventário', 'Local bloqueado',
             'Local bloqueado', 'Tipo dedicação', 'LPN', 'Tipo do local', 'Task Movement',
             'Reabastecimento', 'Local atual', 'Qtde. alocada', 'Qtde. a preencher', 'Qtde. abastecimento',
             'Qtde. Mínima', 'Qtde. Máxima'], axis=1, inplace=True)

def reordenarColunas1(dataframe):
    dataframe = df.reindex(columns=['Filial', 'Item', 'Descrição', 'Rua', 'Blocagem', 'Nivel', 'Tipo embalagem',
                                    'Qtde. no local', 'Qtde. Embalagem', 'Eqp/End', 'Status do item', 'Setor',
                                    'Desc_setor', 'Item Volume', 'Local Volume', 'Cub total',
                                    '% Ocupação Local', '% Ocupação Palet'])
    return dataframe

def reordenarColunas2(dataframe):
    dataframe = df.reindex(columns=['Filial', 'Item', 'Descrição', 'Rua', 'Blocagem', 'Nivel', 'Tipo embalagem',
                                    'Qtde. no local', 'Qtde. embalagem', 'Eqp/End', 'Status do item', 'Setor',
                                    'Desc_setor', 'Item Volume', 'Local Volume', 'Cub total',
                                    '% Ocupação', '% Ocupação Palet'])
    return dataframe

deparaFrame = pd.read_excel(open(os.path.join(caminhoDepara, arquivoDepara), 'rb'))

for arquivo in arquivos:
    if 'Base' in arquivo:
        nomeArquivo = arquivo
        filial: int = nomeArquivo[5:9]
        df = defineDataFrame(caminho, arquivo)
        df['Indicador Inbound/Outbound'].fillna('N/A', inplace=True)

        type_dictionary = {'Filial': int, 'Item': int, 'Descrição': str, 'Rua': str, 'Blocagem': str, 'Nivel': str,
                           'Tipo embalagem': str, 'Qtde. no local': int, 'Qtde. Embalagem': int, 'Status do item': str,
                           'Item Volume': float, 'Local Volume': float, '% Ocupação Local': float}

        type_dictionary2 = {'Filial': int, 'Item': int, 'Descrição': str, 'Rua': int, 'Blocagem': int, 'Nivel': int,
                            'Tipo embalagem': str, 'Qtde. no local': int, 'Qtde. embalagem': int, 'Status do item': str,
                            'Item Volume': float, 'Local Volume': float, '% Ocupação': float}

        map_dictionary = {'Inbound': filial, 'Outbound': filial, 'N/A': filial}
        dicionario = df['Indicador Inbound/Outbound'].map(map_dictionary)
        df['Filial'] = dicionario
        df.rename(columns={'Setor': 'Desc_setor'}, inplace=True, errors='ignore')
        df = pd.merge(df, deparaFrame, how='left', on='Desc_setor')
        listaArquivos.append(df)

        try:
            df[['Rua', 'Blocagem', 'Nivel']] = df['Local atual'].str.split('-', expand=True)
        except BaseException as e:
            df[['Rua', 'Blocagem', 'Nivel']] = ['-', '-', '-']
        try:
            df = df.astype(type_dictionary, errors='ignore')
        except BaseException as e:
            df = df.astype(type_dictionary2, errors='ignore')
        removeColunas(df)
        df = pd.concat(listaArquivos)
        try:
            df = reordenarColunas1(df)
        except BaseException as e:
            df = reordenarColunas2(df)

rename_dict = {'Item': 'SKU', 'Tipo embalagem': 'Equip', 'Qtde. no local': 'Qtd', 'Qtde. Embalagem': 'Qtd Max',
               'Qtde. embalagem': 'Qtd Max', 'Status do item': 'Status', 'Item Volume': 'Cub Uni',
               'Local Volume': 'Cub Palet', '%Ocupação Palet': '% Ocupação Palet'}

df.rename(columns=rename_dict, inplace=True, errors='ignore')
df = df.astype({'Setor': int}, errors='ignore')
filtro_boa = df.loc[(df['Status'].str.startswith('QEB')) | (df['Status'].str.startswith('SLD'))]
df.drop(filtro_boa.index, axis=0, inplace=True, errors='ignore')

df['Cub total'] = (df['Cub Uni'] * df['Qtd'])

df.to_excel(dirDestino + '/' + 'ManhattanConsolidado.xlsx', index=False)

fim = timeit.default_timer()

print(fim - inicio)