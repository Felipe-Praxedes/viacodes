from numpy import array
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support import expected_conditions as condicaoEsperada
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium import webdriver
from datetime import datetime
from datetime import timedelta
from pymsgbox import *
from loguru import logger
import pandas as pd
import pyperclip as pc
import time
import os

class Parametros():
        
    def paramURL():
        urlManhattan: str = 'https://viavp-sci.sce.manh.com/bi/?perspective=home' 
        return urlManhattan
    
    def paramDiretorio():
        diretorioDownload:str = os.getcwd() 
        arquivoUpload: str = os.getcwd() + "\\bd_entregas.csv"
        arquivos: list = ['entrega']
        nomeArquivoSaida: list = ['bd_entregas.csv']
        return diretorioDownload, arquivoUpload, arquivos, nomeArquivoSaida
        
    def paramCredencial():
        # usuarioTms = usuario[0]
        # senhaTms = senha[0]
        # usuarioSP = usuario[1]
        # senhaSP = senha[1]
        # listaUnidade = unidades
        arquivoParametros = os.getcwd() + "\\" + 'Parametros.txt'
        usuario, senha, dias, unidades = Manhattan_Extract.carrega_parametros(arquivoParametros)
        return usuario, senha, dias, unidades
    
    def paramDate():
        dias: int = Parametros.paramCredencial[2]
        lDataInicial = (datetime.now() - timedelta(days=dias)).strftime('%d-%m-%Y')
        lDataFinal = datetime.today().strftime('%d-%m-%Y')
        return lDataInicial, lDataFinal
        
class Manhattan_Extract():
    
    def start(self):
        self.diretorio_download:str = Parametros.paramDiretorio()[0]
        # arquivos:str = Parametros.paramDiretorio()[2][0]
        # nome_arquivo_saida = Parametros.paramDiretorio()[3]
        # lista_unidades:list = Parametros.paramCredencial()[3]
        
        # self.limpa_pasta(diretorio_download, arquivos)
        self.carrega_pagina_web()
        self.login()
        # self.consulta_entrega(self.listaUnidade)
        self.aguarda_download(self.diretorio_download)
        # self.renomear_arquivo(diretorio_download, arquivos, nome_arquivo_saida,lista_unidades)
        # self.uploadSharePoint()

        time.sleep(1)
        self.driver.quit()
        logger.success('Consulta finalizada com sucesso.')
        
    def carrega_parametros(caminhoArquivo):
        
        logger.info('Verificando login e dias de extração.')
        try:
            plan = pd.read_table(caminhoArquivo, header=None, sep=":")  # latin-1
            usr = str(plan[1][0]).split(", ")
            senha = str(plan[1][1]).split(", ")
            dias = int(plan[1][2])
            unidades = str(plan[1][3]).split(", ")
            logger.info(f'Usuário: {usr}\nExtração de: {dias} dias')
            return usr, senha, dias, unidades
        except:
            pass
            logger.warning('Não foi possivel ler o arquivo')
        
    def carrega_pagina_web(self) -> None:

        options = Options()
        # if not self.proxy == '':
        #     options.add_argument(f'--proxy-server={self.proxy}')
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        options.add_experimental_option('prefs', {
            "download.default_directory":self.diretorio_download,
            "download.Prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True
        })
        options.add_argument("--start-maximized")
        logger.info('Iniciando Browser')
        # try:
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        self.wait = WebDriverWait(self.driver, 2)
        self.wait2 = WebDriverWait(self.driver, 120)
        # except:
        #     logger.critical('Não foi possivel abrir a pagina web.')
        #     time.sleep(2)
            
    def login(self) -> None:
        logger.info('Realizando login')
        lLogin: str = "//*[@type='email']"
        lSenha: str = "//input[@name='passwd']"
        lEntrar: str = '//*[@type="submit"]'
        lAlerta: str = '//div[@class="alert alert-error"]'
        lCampoVazio: str = '//span[@class="field-validation-error"]'
        lTitulo: str = '/html/body/div[2]/div/section[1]/h1'
        lSelecionaTipo: str = '//*[@name="CAMNamespace"]'
        lButtonExemple: str = ''

        self.driver.get(Parametros.paramURL())

        try:
            selecaoTipo = self.wait2.until(
                condicaoEsperada.presence_of_element_located((By.XPATH, lSelecionaTipo)))
            selecao_object = Select(selecaoTipo)
            selecao_object.select_by_value('AzureAD')
        except:
            pass
            logger.warning('elemento selecaoTipo não encontrado.')

        try:
            bt_entrar = self.wait2.until(
                condicaoEsperada.presence_of_element_located((By.XPATH, lButtonExemple)))
            bt_entrar.click()
        except:
            pass
            logger.critical('Botão entrar não encontrado.')

        try:
            login = self.wait2.until(
                condicaoEsperada.presence_of_element_located((By.XPATH, lLogin)))
            login.send_keys("ronaldo.luis@viavarejo.com.br")
        except:
            pass
            logger.critical('Campo login não encontrado.')

        try:
            senha = self.wait2.until(
                condicaoEsperada.presence_of_element_located((By.XPATH, lSenha)))
            senha.send_keys("250309@Rio")
        except:
            pass
            logger.critical('Campo senha não encontrado.')

        try:
            bt_entrar = self.wait2.until(
                condicaoEsperada.presence_of_element_located((By.XPATH, lEntrar)))
            bt_entrar.click()
        except:
            pass
            logger.critical('Botão entrar não encontrado.')

        time.sleep(5)
        if self.valida_elemento(By.XPATH, lAlerta):
            tipo_erro = self.wait.until(
                condicaoEsperada.presence_of_element_located((By.XPATH, lAlerta))).text
            logger.warning('Login não efetuado')
            alert(tipo_erro, "Erro de Login")
            self.driver.quit()
        elif self.valida_elemento(By.XPATH, lCampoVazio):
            erro_campo = self.wait.until(
                condicaoEsperada.presence_of_element_located((By.XPATH, lCampoVazio)))
            str_erro: str = ''
            for erro in erro_campo:
                str_erro + erro.text + '\n'

            logger.warning('Campos Vazios')
            alert(str_erro, "Campos Vazios")
            self.driver.quit()

        try:
            self.wait2.until(
                condicaoEsperada.presence_of_element_located((By.XPATH, lTitulo)))
        except TimeoutException as e:
            logger.warning('Tempo de Login atingido.\nVerifique sua conexão e tente novamente.')
            alert(
                'Tempo de Login atingido.\nVerifique sua conexão e tente novamente.', "Tempo de Login")
            self.driver.quit()
            
    def aguarda_download(self, caminho):
        fileends = "crdownload"
        logger.info('Downloading em andamento, aguarde...')
        while "crdownload" == fileends:
            time.sleep(2)
            newest_file = self.arquivo_recente(caminho)
            if "crdownload" in newest_file:
                fileends = "crdownload"
            else:
                fileends = "none"
                logger.info('Downloading Completo...')
            
if __name__ == '__main__':
    runnable = Manhattan_Extract()
    runnable.start()