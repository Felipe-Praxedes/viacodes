from pickle import TRUE
import pandas as pd
import numpy as np
import os

dePara = os.getcwd() + '\\DePara_Loja_CD.csv'
vendaAprovada = os.getcwd() + "\\BASE\\VENDA_ON_E_OFF_-_APPROVED_20220617192407.csv"
saidaVendaAprovada = os.getcwd() + "\\BASE\\VENDA_APPROVED.csv"

baseDePara = pd.read_csv(dePara, sep=';')
baseVenda = pd.read_csv(vendaAprovada, sep=';')

baseDePara= baseVenda.apply(str) 

baseVenda['QUANTIDADE_VENDA'] = baseVenda['QUANTIDADE_VENDA'].str.replace(".", "").str.replace(",",".")
baseVenda[['QUANTIDADE_VENDA']] = baseVenda[['QUANTIDADE_VENDA']].apply(pd.to_numeric) 

baseConsolidada = pd.merge(baseVenda, baseDePara, how= 'left', on= 'FILIAL')
baseConsolidadaTable = pd.pivot_table(baseConsolidada, values=["QUANTIDADE_VENDA"], 
    index=["CANAL", "CD ATENDE", "SETOR", "ITEM", "DESCRICAO", "DIRETORIA", "ESPECIE", "MARCA"], aggfunc=np.sum, fill_value=0)

baseConsolidadaTable.to_csv(saidaVendaAprovada)

print(baseConsolidadaTable)