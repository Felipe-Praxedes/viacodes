
from datetime import datetime
import sys
from loguru import logger
from pymsgbox import *
import pandas as pd
import random
import time
import os
from glob import iglob
from os.path import getmtime

class Auxiliar:

    def __init__(self) -> None:
        pass

    def digitar(self,texto,campo):
        for letra in texto:
            campo.send_keys(letra)
            time.sleep(random.randint(1,5)/30)


    # def consolida_base(self,caminhoOrigem,caminhoDestino, nomeArqDestino) -> str:
    #         df = pd.DataFrame()
    #         # for f in os.listdir(caminhoOrigem):
    #         #     if str(nome_Arq) in f:
    #         #         arq_excel = os.path.join(caminhoOrigem,f)
    #         #         plan = pd.read_csv(arq_excel,sep=';',encoding='latin-1')
    #         #         df = df.append(plan,ignore_index=True)

    #         # data_hora = datetime.now()
    #         # data_format = data_hora.strftime('%d%m%Y_%H%M%S')

    #         # direFinal: str = caminhoDestino + '\\' + nomeArqDestino +"_"+ data_format + '.xlsx'
    #         direFinal: str = caminhoDestino + '\\' + nomeArqDestino + '.xlsx'
    #         df.to_csv(direFinal, index=False, encoding='latin-1')
        
    #         return direFinal

    def consolida_base_retorno_rgtp(self, caminhoOrigem,caminhoDestino, nome_Arq, nomeArqDestino):

            qtd_arquivos = 0
            df = pd.DataFrame()
            for f in os.listdir(caminhoOrigem):
                if str(nome_Arq) in f:
                    qtd_arquivos += 1
                    arq_csv = os.path.join(caminhoOrigem,f)
                    plan = pd.read_excel(arq_csv,skiprows=[0])
                    df = df.append(plan,ignore_index=True)
                    

            if qtd_arquivos > 0:
                data_hora = datetime.now()
                data_format = data_hora.strftime('%d%m%Y_%H%M%S')

                writer = pd.ExcelWriter(caminhoDestino + '\\' + nomeArqDestino + data_format + '.xlsx', engine = 'xlsxwriter')
                df.to_excel(writer, sheet_name = 'Base',header=True,index=False)
                writer.save()
                writer.close()
                dirFinal = caminhoDestino + '\\' + nomeArqDestino + data_format + '.xlsx'
                return dirFinal
            else:
                return ''

    def limpa_pasta(self, caminho, nomeArquivo):
        for f in os.listdir(caminho):
            if nomeArquivo in f or '.tmp' in f:
                os.remove(os.path.join(caminho,f))

    def transforma_dict(self,lista:list,numKey:int,numValue:int) -> dict:
        if len(lista)>0:
            dct:dict = {}
            for item in lista:
                dct[item[numKey]] = item[numValue]
            return(dct)
        else:
            print('Nenhum dado dentro da lista')
            time.sleep(3)


    def localiza_arquivo(self, caminho, nomeArq) -> str:
            files = iglob(caminho + "\\*")
            sorted_files = sorted(files, key=getmtime, reverse=True)
            arquivo:str =''
            for f in sorted_files:
                if str(nomeArq) in f:
                    arquivo = f
                    return arquivo       
            print(f'Nenhum arquivo com o nome de "{nomeArq}" foi localizado')
            arquivo = 'Arquivo não localizado'
            return arquivo
    
    def exporta_arquivo_saida_csv(self,dataFrame: pd.DataFrame, caminhoSaida, nomeSaida, colunas:list = [], encodingVar:str ='utf-8'):
        if len(colunas)> 0:

            dataFrame.to_csv(os.path.join(caminhoSaida, '\\' + nomeSaida + '.csv') ,index=False ,encoding=encodingVar,columns=colunas)
        else:
            print(os.path.join(caminhoSaida, '\\' + nomeSaida + '.csv'))
            dataFrame.to_csv(os.path.join(caminhoSaida, '\\' + nomeSaida + '.csv'),index=False ,encoding=encodingVar)


    def exporta_arquivo_saida_excel_openPy(self,dataFrame, caminhoSaida, nome_aba, encodingVar:str ='utf-8'):

        with pd.ExcelWriter(caminhoSaida, engine = 'openpyxl',mode='a') as writer:  
            dataFrame.to_excel(writer, sheet_name = nome_aba ,header=True,index=False)

    def exporta_arquivo_saida_excel_xlsx(self,dataFrame: pd.DataFrame, caminhoSaida, nomeArq, colunas:list = [], encodingVar:str ='utf-8'):
            data_hora = datetime.now()
            data_format = data_hora.strftime('%d%m%Y_%H%M%S')

            writer = pd.ExcelWriter(os.path.join(caminhoSaida,'\\' + nomeArq + data_format + '.xlsx'), engine = 'xlsxwriter')
            if len(colunas)> 0:
                dataFrame.to_excel(writer, sheet_name = 'Base',header=True,index=False, columns=colunas)
            else:
                dataFrame.to_excel(writer, sheet_name = 'Base',header=True,index=False)
            writer.save()
            writer.close()


    def transforma_dict(self, lista: list, numKey: int, numValue: int) -> dict:
        if len(lista) > 0:
            dct: dict = {}
            for item in lista:
                dct[item[numKey]] = item[numValue]
            return(dct)
        else:
            print('Nenhum dado dentro da lista')
            time.sleep(3)

    def saida_arquivo_excel(self,dataFrame: pd.DataFrame, caminhoDestino: str, nomeArquivo: str):
        data_hora = datetime.now()
        data_format = data_hora.strftime('%d%m%Y_%H%M%S')
        caminho_arquivo = caminhoDestino + '\\' + nomeArquivo + data_format + '.xlsx'
        
        writer = pd.ExcelWriter(caminhoDestino + '\\' + nomeArquivo + data_format + '.xlsx', engine='xlsxwriter')
        dataFrame.to_excel(writer, sheet_name='Base',header=True, index=False)
        writer.save()
        writer.close()

        return caminho_arquivo

    def saida_arquivo_csv_rgtp(self,dataFrame: pd.DataFrame, caminhoDestino: str, nomeArquivo: str):
        data_hora = datetime.now()
        data_format = data_hora.strftime('%d%m%Y_%H%M%S')

        direFinal: str = caminhoDestino + '\\' + nomeArquivo +"_"+ data_format + '.csv'
        dataFrame.to_csv(direFinal,sep=';', index=False, encoding='latin-1',header=False)


    def saida_arquivo_csv(self,caminhoOrigem,caminhoDestino, nome_Arq, nomeArqDestino):
            df = pd.DataFrame()
            for f in os.listdir(caminhoOrigem):
                if str(nome_Arq) in f:
                    arq_excel = os.path.join(caminhoOrigem,f)
                    plan = pd.read_csv(arq_excel,sep=';',encoding='latin-1')
                    df = df.append(plan,ignore_index=True)

            data_hora = datetime.now()
            data_format = data_hora.strftime('%d%m%Y_%H%M%S')

            direFinal: str = caminhoDestino + '\\' + nomeArqDestino +"_"+ data_format + '.csv'
            df.to_csv(direFinal, index=False, encoding='latin-1')
        
            return direFinal

    def cria_pasta(self, diretorio: str, novaPasta: str):

        novoDiretorio = diretorio + '\\' + novaPasta

        if os.path.isdir(novoDiretorio):
            return novoDiretorio
        else:
            os.mkdir(novoDiretorio)
            return novoDiretorio


    def arquivo_recente(self, caminho):
        path = caminho
        os.chdir(path)
        files = sorted(os.listdir(os.getcwd()), key=os.path.getmtime)
        newest = files[-1]
        return newest

    def aguarda_download(self,caminho):
        fileends = "crdownload"
        print('Downloading em andamento aguarde...')
        while "crdownload" == fileends:
            time.sleep(1)
            newest_file = self.arquivo_recente(caminho)
            if "crdownload" in newest_file:
                fileends = "crdownload"
            else:
                fileends = "none"
                print('Downloading Completo...')

    def verifica_pasta(self, diretorio):
        if os.path.isdir(diretorio):
            print('O caminho {} existe'.format(diretorio))
            return False
        else:
            print('Pasta não localizada')
            return True
    
    def arquivo_atual(self, nomeArquivo, diretorio, indice: int = 1):
        l_arquivos = os.listdir(diretorio)
        l_datas = []

        for arquivo in l_arquivos:
            if nomeArquivo in arquivo:
                data = os.path.getmtime(os.path.join(os.path.realpath(diretorio), arquivo))
                l_datas.append((data, arquivo))
        try:
            l_datas.sort(reverse=True)
            # for i in l_datas:
            #     print(i)
            ult_arquivo = l_datas[0]
            nome_arquivo = ult_arquivo[1]
            data_arquivo = ult_arquivo[0]
            arq = os.path.join(os.path.realpath(diretorio), nome_arquivo)
            data_mod = self.data_modificacao(arq)
            # return nome_arquivo, data_arquivo
            return nome_arquivo, data_mod
        except:
            return 'Nenhum arquivo Localizado.',''
    
    
    def data_modificacao(self, arquivo):

            ti_m = os.path.getmtime(arquivo) 
            
            m_ti = time.ctime(ti_m) 
            t_obj = time.strptime(m_ti) 
            T_stamp = time.strftime("%d/%m/%Y %H:%M:%S", t_obj) 
            
            # print(f"The file located at the path {arquivo} was last modified at {T_stamp}")
            return T_stamp
        

    def logger(self):
        logger.remove()
        logger.add(
                    'out.txt',
                    sys.stdout,
                    colorize=True,
                    mode='a',
                    format='<g>{time}</g> | <level>{level}</level> |  {message} {file} linha: {line}')
        

if __name__ == "__main__":
    executa = Auxiliar()
    executa.localiza_arquivo(r'F:\Padronização e Controle\09 - Outros\Diversos\LUIZ EDUARDO\BACKUP\CRL\VVLOG', 'apelidoTransportadora')
