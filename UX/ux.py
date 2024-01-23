from functools import partial
from tokenize import String
from typing import List
from webbrowser import get
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, WebDriverException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as condicaoEsperada
from datetime import datetime
from time import sleep
from mimetypes import init
import os
import sys
import pathlib
import shutil

login= 'thiago.acacio'
password = 'miguel2014'

urlUx = 'http://vvlog.uxdelivery.com.br/'
urlUXConsulta = 'http://vvlog.uxdelivery.com.br/Listas/listaconsulta'
urlEntrega = 'http://vvlog.uxdelivery.com.br/Entregas/EntregaConsulta'

dirBaixados = os.getcwd()

class Dados:

    def loginUX(self):

        options = Options()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        options.add_experimental_option(
            'prefs', {
            "download.default_directory": dirBaixados,
            "download.Prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True
        })
        options.add_argument("--start-maximized")

        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        sleep(0.5)
        self.driver.get(urlUx)
        sleep(0.5)
        self.driver.get(urlUx)
        self.wdw = WebDriverWait(self.driver, 30)

        op = True
        while op:
            userEmail = self.driver.find_element(By.ID, 'rcmloginuser')
            userPassword = self.driver.find_element(By.ID, 'rcmloginpwd')
            btn_login = self.driver.find_element(By.ID, 'rcmloginsubmit')
            userEmail.send_keys(login)
            print(f'Email {login} utilizado')
            userPassword.send_keys(password)
            btn_login.click()
            op = False

        else:
            sleep(2)

        self.baixarXml(self.driver)

        self.lista_arquivos_upload(dirBaixados)

        if len(self.listaUpload) == 0:
            self.driver.quit()
            pass
        else:

            self.driver.get(urlJw)
            sleep(2)

            op = True
            while op:
                userJw = self.wdw.until(condicaoEsperada.element_to_be_clickable((By.ID, 'user_email')))
                userPassword = self.wdw.until(condicaoEsperada.element_to_be_clickable((By.ID, 'user_password')))
                btn_login = self.driver.find_element(By.XPATH, '//*[@id="new_user"]/div[2]/div/div[1]/input')
                userJw.send_keys(loginJw)
                print(f'Email {loginJw} utilizado')
                userPassword.send_keys(passwordJw)
                btn_login.click()
                op = False

            else:
                sleep(2)
            espera_btn = self.wdw.until(condicaoEsperada.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div/div/div[1]/ul[2]/li[7]/a')))
            espera_btn.click()
            self.uploadXml(self.driver)
            self.driver.quit()

    def baixarXml(self, driver):
        menu = self.wdw.until(condicaoEsperada.element_to_be_clickable((By.XPATH, '//*[@id="mailsearchform"]')))
        mostrarMsg = self.wdw.until(condicaoEsperada.element_to_be_clickable((By.XPATH, '//a[@title="Mostrar mensagens não lidas"]')))
        mostrarMsg.click()
        menu.send_keys('cteseara')
        menu.send_keys(Keys.ENTER)
        wdwToEmail = WebDriverWait(self.driver, 5)
        try:
            esperarEmail = wdwToEmail.until(condicaoEsperada.element_to_be_clickable((By.CLASS_NAME, 'rcmContactAddress')))
        except:
            pass
        sleep(0.5)

        tx = 0
        while len(self.driver.find_elements(By.CLASS_NAME,'rcmContactAddress')) > 0: 
            email = self.wdw.until(condicaoEsperada.element_to_be_clickable((By.XPATH, "//table[@id='messagelist']/tbody/tr[1]/td[2]/span[@class ='subject']/a")))
            webdriver.ActionChains(self.driver).double_click(email).perform()
            sleep(0.5)

            totalAtch = self.wdw.until(condicaoEsperada.element_to_be_clickable((By.XPATH, "//ul[@id='attachment-list']")))
            lengthAtch = len(self.driver.find_elements(By.XPATH,"//*[@id='attachment-list']/li"))
            atch = 1    
            while atch <= lengthAtch:
                xml_email = self.wdw.until(condicaoEsperada.element_to_be_clickable((By.XPATH, f"//ul[@id='attachment-list']/li[{atch}]/a")))
                nome = xml_email.accessible_name
                if ".xml" in nome:
                    xml_email.click()
                atch = atch + 1
            self.driver.back()
            mostrarMsg = self.wdw.until(condicaoEsperada.element_to_be_clickable((By.XPATH, '//a[@title="Mostrar mensagens não lidas"]')))
            menu = self.wdw.until(condicaoEsperada.element_to_be_clickable((By.XPATH, '//*[@id="mailsearchform"]')))
            menu.send_keys('cteseara')
            menu.send_keys(Keys.ENTER)
            try:
                esperarEmail = wdwToEmail.until(condicaoEsperada.element_to_be_clickable((By.CLASS_NAME, 'rcmContactAddress')))
            except:
                pass
            sleep(0.5)
            tx = tx +1

        if tx != 0 and tx > 1:
            print(f'{tx} Arquivos baixados com sucesso')
        elif tx == 1:
            print(f'{tx} Arquivo baixado com sucesso')

    def uploadXml(self, driver):
        mostrar = self.wdw.until(condicaoEsperada.element_to_be_clickable((By.XPATH, '//*[@id="rcmliSU5CT1guVHJhc2g"]/a')))
        mostrarMenu = self.wdw.until(condicaoEsperada.element_to_be_clickable((By.XPATH, '//*[@id="import"]/a')))
        mostrarMenu.click()
        importacaoMenu = self.wdw.until(condicaoEsperada.element_to_be_clickable((By.XPATH, '//*[@id="integration/import/freight"]/a/span')))
        importacaoMenu.click()
        novaImportacao = self.wdw.until(condicaoEsperada.element_to_be_clickable((By.XPATH, '/html/body/div[6]/div/div[1]/div/div/div/div[2]/div/a/span')))
        novaImportacao.click()
        sleep(1)

        tituloXML = self.wdw.until(condicaoEsperada.element_to_be_clickable((By.XPATH, '//*[@id="upload-modal"]/div/div/div/h4')))
        procurarXML = self.driver.find_element(By.ID, 'integration_import_freight_documents')

        self.lista_arquivos_upload(dirBaixados)

        hList = len(self.listaUpload)

        if hList == 0:
            pass
        else:
            for xml in self.listaUpload:
                procurarXML = self.driver.find_element(By.ID, 'integration_import_freight_documents')
                procurarXML.send_keys(str(xml))
                salvarXML = self.driver.find_element(By.ID, 'submit')
                salvarXML.click()
                sleep(1)
                confirm_btn = self.wdw.until(condicaoEsperada.element_to_be_clickable((By.XPATH, '/html/body/div[13]/div/div[3]/button[1]')))
                confirm_btn.click()
                print(f'{xml} importado com sucesso')
                sleep(0.5)
                novaImportacaoLoop = self.wdw.until(condicaoEsperada.element_to_be_clickable((By.XPATH, '/html/body/div[6]/div/div[1]/div/div/div/div[2]/div/a/span')))
                novaImportacaoLoop.click()
                sleep(1)
                tituloXMLLoop = self.wdw.until(condicaoEsperada.element_to_be_clickable((By.XPATH, '//*[@id="upload-modal"]/div/div/div/h4')))

        if hList != 0 and hList > 1:
            print(f'{hList} Arquivos importados com sucesso')
        elif hList == 1:
            print(f'{hList} Arquivo importado com sucesso')

class TransferenciaArquivos:

    def iniciar(self, old_dir, new_dir):
        new_list_file = self.lista_arquivos_inicial(old_dir)
        self.copia_arquivos(new_dir, new_list_file)

    def lista_arquivos_inicial(self, dirBaixados):
        lista = []
        for root, dirs, files in os.walk(dirBaixados):
            for file in files:
                lista.append(os.path.join(root, file))
        return lista

    def copia_arquivos(self, dirBaixados, lista):
        if len(lista) == 0:
            pass
        else:
            for file in lista:
                name_arq = pathlib.Path(file).name
                new_dir = os.path.join(dirBaixados, name_arq)
                list_file.append(file)
                try:
                    shutil.move(file, new_dir)
                    print(f'O arquivo {file} foi transferido com sucesso')
                except Exception as e:
                    print(f'Não foi possível copiar o arquivo {name_arq}')
                    continue
        if len(lista) == 1:
            print(f'{len(lista)} Transferido para a pasta Enviados') 
        else:
            print(f'{len(lista)} Transferidos para a pasta Enviados')    

try:
    origem = dirBaixados
    var = valida_dir(origem)
    if var == False:
        sys.exit()
    destino = dirEnviados
    var = valida_dir(destino)
    if var == False:
        sys.exit()

except KeyboardInterrupt:
    print()
    print('O Programa foi finalizado')
    sys.exit()

extrair_dados = Dados()
extrair_dados.login_ux()

program = TransferenciaArquivos()
program.iniciar(origem, destino)

sys.exit()