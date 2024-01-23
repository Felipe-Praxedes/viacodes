from selenium.webdriver.support import expected_conditions as ce
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from dateutil.relativedelta import relativedelta
from selenium.webdriver.support.ui import Select
from Tratamento_dados_1200 import Tratar_Base_Labor
from Events_1200 import Aprovacao
from EmployeeTracking_1400 import employee_1400
from EmployeeTracking_1500 import employee_1500
from selenium.webdriver.common.by import By
from datetime import datetime, timedelta
from selenium import webdriver
from loguru import logger
import shutil
import time 
import glob
import os
import sys

class employee:
    def __init__(self) -> None:
        self.usuario = "customeradmin@system.com"
        self.senha = "Vz3KK!F&zV5Q"
        self.url = "https://viavp-sci.sce.manh.com/bi/?perspective=authoring&id=i9B8D13F7BE474072BEF9F7ED75F8EEAC&objRef=i9B8D13F7BE474072BEF9F7ED75F8EEAC&action=run&format=CSV&cmPropStr=%7B%22id%22%3A%22i9B8D13F7BE474072BEF9F7ED75F8EEAC%22%2C%22type%22%3A%22report%22%2C%22defaultName%22%3A%2210.01%20-%20Employee%20Tracking%20-%20GAP%20Time%22%2C%22permissions%22%3A%5B%22execute%22%2C%22read%22%2C%22traverse%22%2C%22write%22%5D%7D"
        self.pastaDownloads = os.path.expanduser("~") + "\\Downloads"
        self.date = datetime.today()
        self.month = self.date.month
        self.year = self.date.year
        self.yesterday = self.date - relativedelta(days=1)
        self.data_inicio = '01/' + f'{self.month}/' + f'{self.year}'
        self.data_final = '04/' + f'{self.month}/' + f'{self.year}'
        self.listaArqvs = glob.glob(os.path.join(self.pastaDownloads, "*.csv"))
        self.listaArqvs = [arquivo for arquivo in self.listaArqvs if os.path.basename(arquivo).startswith('10.01 - Employee Tracking')]
        self.pastaBase = os.getcwd() + '\\Base'
        self.folderResult = os.getcwd() + '\\Resultado' 

    def comecar(self):
        self.carrega_pagina_web()
        self.login()

    def sair(self):
        logger.critical('Encerrando...')
        self.driver.quit()
        sys.exit()

    def carrega_pagina_web(self) -> None:
        options = Options()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        options.add_experimental_option('prefs', {"safebrowsing.enabled": True})

        try:    
            self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
            self.wait = WebDriverWait(self.driver, 10)
            self.wait2 = WebDriverWait(self.driver, 5000)
            self.driver.get(self.url)
            self.driver.minimize_window()
            logger.success('Abrindo navegador')
        except:
            logger.critical('Não foi possível abrir a página web')
            time.sleep(4)
            self.sair()

    def login(self):
        lSci: str = '//*[@name="CAMNamespace"]'
        luser: str = '//*[@name="CAMUsername"]'
        lsenha: str = '//*[@name="CAMPassword"]'
        lSFrame: str = '//*[@id="rsIFrameManager_1"]'
        lconnect: str = '//*[@type="button"]'
        listFilial: str = '//*[@id="dv33_ValueComboBox"]'
        ldt_incial: str = '(//input)[1]'
        ldt_final: str = '(//input)[2]'
        lbt_submit: str = '(//div[34]//button)[4]'
        lCarregamento: str = '//*[@id="idDownloadViewer"]/div[1]/div/div[1]/span'

        try:
            op_sci = self.wait2.until(
                ce.presence_of_element_located((By.XPATH, lSci)))
            lista_sci = Select(op_sci)
            lista_sci.select_by_value('SCI')

            logger.info('Efetuando login.')

            l_user = self.wait2.until(
                ce.presence_of_element_located((By.XPATH, luser)))
            l_user.send_keys(self.usuario)

            l_senha = self.wait2.until(
                ce.presence_of_element_located((By.XPATH, lsenha)))
            l_senha.send_keys(self.senha)

            bt_connect = self.wait2.until(
                ce.presence_of_element_located((By.XPATH, lconnect)))
            bt_connect.click()
            logger.success('Login efetuado com sucesso')
        except:
            logger.error("Falha ao tentar realizar o login" )
            self.sair()

        time.sleep(1)

        try:
            s_frame = self.wait2.until(
                ce.presence_of_element_located((By.XPATH, lSFrame)))
            self.driver.switch_to.frame(s_frame)

            logger.info('Selecionando filial')
            l_filial = self.wait2.until(
                ce.presence_of_element_located((By.XPATH, listFilial)))
            s_1200 = Select(l_filial)
            s_1200.select_by_value('1200')

            dtInicial = self.wait2.until(
                ce.presence_of_element_located((By.XPATH, ldt_incial)))
            dtInicial.click()
            dtInicial.clear()
            dtInicial.send_keys(self.data_inicio)

            dtFinal = self.wait2.until(
                ce.presence_of_element_located((By.XPATH, ldt_final)))
            dtFinal.click()
            dtFinal.clear()
            dtFinal.send_keys(self.data_final)

            bt_submit = self.wait2.until(
                ce.presence_of_element_located((By.XPATH, lbt_submit)))
            bt_submit.click()
        except Exception as e:
            logger.error(f'Não foi possível realizar o download do relatorio. Favor tentar novamente. Erro: {e}')
            self.sair()

        try:
            self.wait2.until(ce.visibility_of_element_located((By.XPATH, lCarregamento)))
            logger.info('Download em andamento...')
        except Exception as e:
            logger.error(f'Falha ao iniciar download. Erro: {e}')
            self.sair()

        try: 
            if len(self.listaArqvs) > 0:
                logger.info(f'Removendo {len(self.listaArqvs)} arquivos')
                for arquivo in self.listaArqvs:
                    os.remove(arquivo)
                logger.info(f'arquivos removidos: {len(self.listaArqvs)}')
            else:
                logger.success('Diretório limpo.')
        except Exception as e:
            logger.info(f'Erro: {e}')

        try:
            self.wait2.until(ce.invisibility_of_element_located((By.XPATH, lCarregamento)))
            logger.success('Download concluído')
        except Exception as e:
            logger.error(f'Falha ao baixar arquivo. Erro: {e}')
            self.sair()

    def download_data(self):
        while self.data_inicio is not None and self.data_final is not None:
            self.comecar()
            
            dta_formatada = "%d/%m/%Y"
            dta_inicio = datetime.strptime(self.data_inicio, dta_formatada)
            self.dta_final = datetime.strptime(self.data_final, dta_formatada)
            nova_dt_inicial = self.dta_final + timedelta(days=1)
            nova_dt_final = self.dta_final + timedelta(days=4)

            if nova_dt_inicial >= self.date:
                nova_dt_inicial = self.yesterday.strftime(dta_formatada)
                nova_dt_final = self.yesterday.strftime(dta_formatada)
                print(self.date)
            else:
                nova_dt_inicial

            if nova_dt_final.day >= self.date.day: 
                nova_dt_final = self.yesterday
            else: 
                nova_dt_final

            self.data_inicio = nova_dt_inicial.strftime(dta_formatada)
            self.data_final = nova_dt_final.strftime(dta_formatada)

            try:
                time.sleep(1.5)
                while any(arquivo.endswith('.crdownload') for arquivo in os.listdir(self.pastaDownloads)):
                    time.sleep(1)
                self.rename()

            except Exception as e:
                logger.error(f'Falha ao renomear o arquivo. Erro: {e}')
                self.sair()

    def rename(self):
        self.pastaBase = os.getcwd() + '\\Base'
        if not os.path.exists(self.pastaBase):
            print("A pasta base não existe, criando...")
            os.makedirs(self.pastaBase)

        newNameFile = f"10.01 - Employee Tracking - GAP Time_" + self.dta_final.strftime("%m_%d") + ".csv"
        baseFolderFile = os.path.join(self.pastaBase, newNameFile)
        downloadFolderFile = os.path.join(self.pastaDownloads, newNameFile)
        FileName = f"10.01 - Employee Tracking - GAP Time_" + self.yesterday.strftime("%m_%d") + ".csv"
        name: str = '10.01 - Employee Tracking - GAP Time.csv'
        nameFile = os.path.join(self.pastaDownloads, name)
        
        fileYesterday = os.path.join(self.pastaBase, FileName)

        logger.success('Arquivo baixado com sucesso')
 
        try:
            time.sleep(1.5)
            os.rename(nameFile, downloadFolderFile)
            logger.success(f'Arquivo renomeado para {newNameFile}')
        except Exception as e:
            logger.error(f'Ocorreu um erro ao renomear o arquivo. Erro {e}')

        if os.path.isfile(baseFolderFile):
            logger.warning('Arquivo existente na pasta de destino. Apagando...')
            os.remove(baseFolderFile)
            if os.path.isfile(baseFolderFile):
                logger.error('Não foi possível apagar arquivo.')
            else:
                logger.success('Arquivo apagado com sucesso')
                logger.warning('Movendo arquivo...')
                shutil.move(downloadFolderFile, self.pastaBase)
        else:
            logger.warning('Movendo arquivo...')
            shutil.move(downloadFolderFile, self.pastaBase)

        if os.path.isfile(baseFolderFile):
            logger.success('Arquivo movido com sucesso.')
        else:
            logger.error('Falha ao mover arquivo')

        if os.path.isfile(fileYesterday):
            qtdeArquivos = len(os.listdir(self.pastaBase))
            logger.success(f'{qtdeArquivos} arquivos baixados com sucesso.')
            self.driver.quit()
            if not os.path.exists(self.folderResult):
                print("A pasta resultado não existe, criando...")
                os.makedirs(self.folderResult)
            tratamento = Tratar_Base_Labor()
            tratamento.start()
            self.shareFile()

    def shareFile(self):
        listaArqvsBase = glob.glob(os.path.join(self.pastaBase, "*.csv"))
        name = '1200_Labor_' + f'{self.year}_' + f'{self.month}.csv' 
        resultName = os.path.join(self.folderResult, name)
        sharepointFolder = os.path.expanduser('~') + "\\Via Varejo S.A\\Capacity - 01_1200 (1)"
        sharepointFile = os.path.join(sharepointFolder, name)
        nameFile = 'Base_Resultado.csv'
        result = os.path.join(self.folderResult, nameFile)

        try:
            os.rename(result, resultName)
            logger.success(f'Arquivo renomeado para {name}')
        except Exception as e:
            logger.error(f'Erro ao renomear arquivo. Erro: {e}')

        try:
            if os.path.isfile(sharepointFile):
                logger.info('Arquivo já existe na pasta. Apagando...')
                os.remove(sharepointFile)
                if not os.path.isfile(sharepointFile):
                    logger.success('Arquivo apagado com sucesso.')
                else:
                    logger.error('Falha ao apagar arquivo.')
            else:
                logger.info(f'Arquivo {sharepointFile} não encontrado na pasta {sharepointFolder}. Adicionando novo mês aos dados.'  )
        except Exception as e:
            logger.error(f'falha ao remover arquivo do mesmo mês baixado {e}')

        try:
            logger.info('Movendo arquivo...')
            shutil.move(resultName, sharepointFolder)
        except Exception as e:
            logger.error(f'Falha ao mover arquivo. {e}')

        try:
            if os.path.isfile(sharepointFile):
                logger.success(f'Arquivo movido para {sharepointFolder} com sucesso')
        except Exception as e:
            logger.error(f'Erro ao mover arquivo {e}')

        try:
          for arquivo in listaArqvsBase:
              logger.info('Limpando pasta base...')
              os.remove(arquivo)
        except Exception as e:
            logger.error(f'Erro ao remover arquivos. Erro {e}')
       
        try:
            events = Aprovacao()
            events.start()
        except Exception as e:
            logger.error(f'Falha ao baixar relatorio de Eventos sem aprovação.')
        
        try:
            logger.info('Começando atualização da filial 1400')
            events = employee_1400()
            events.download_data()
        except Exception as e:
            logger.error(f'Falha ao atualizar filial 1400.')

        try:
            logger.info('Começando atualização da filial 1500')
            events = employee_1500()
            events.download_data()
        except Exception as e:
            logger.error(f'Falha ao atualizar filial 1500')
        


        sys.exit()

if __name__ == '__main__':
    executa = employee()
    executa.download_data()