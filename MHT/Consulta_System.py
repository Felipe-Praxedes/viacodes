from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support import expected_conditions as condicaoEsperada
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
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

class Mht_System:

    def __init__(self) -> None:
        logger.success('Bot iniciado com sucesso.')
        self.usuario = 'monitoria_arm'
        self.senha = 'Vi@!1234'
        self.loginMht = 'https://viavp-auth.sce.manh.com/discover_user'
        self.loginMhtSys = 'https://viavp.sce.manh.com/'
        self.tranlog = 'https://viavp.sce.manh.com/cfw/screen/xint/tranlogdetails'

    def start(self):
        self.carrega_pagina_web()
        self.login()
        self.entrar_system()
        self.entrar_tranlog()
        self.consulta_tranlog()

        time.sleep(1)
        self.driver.quit()
        logger.success('Consulta finalizada com sucesso.')

    def carrega_pagina_web(self) -> None:
        options = Options()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        options.add_argument("--start-maximized")
        logger.info('Iniciando Browser')
        try:
            self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
            self.wait = WebDriverWait(self.driver, 1)
            self.wait2 = WebDriverWait(self.driver, 120)
            self.driver.get(self.loginMht)
        except:
            logger.critical('Não foi possivel abrir a pagina web.')
            time.sleep(4)

    def login(self) -> None:
        logger.info('Realizando login')
        lLogin: str = '//*[@id="login-username"]'
        lProximo: str = '//*[@id="discover-user-submit"]'
        lSenha: str = '//*[@id="login-password"]'
        lEntrar: str = '//*[@id="login-submit"]'
        lTitulo: str = '//*[@id="home-page-navbar"]/profile-summary/div/div[1]/div'
        lEsperar: str = '//*[@id="ion-overlay-1"]/div'

        try:
            login = self.wait2.until(
                condicaoEsperada.presence_of_element_located((By.XPATH, lLogin)))
            login.send_keys(self.usuario)
        except:
            logger.critical('Campo login não encontrado.')
        
        try:
            bt_entrar = self.wait2.until(
                condicaoEsperada.presence_of_element_located((By.XPATH, lProximo)))
            bt_entrar.click()
        except:
            logger.critical('Botão entrar não encontrado.')

        try:
            senha = self.wait2.until(
                condicaoEsperada.presence_of_element_located((By.XPATH, lSenha)))
            senha.send_keys(self.senha)
        except:
            logger.critical('Campo senha não encontrado.')

        try:
            bt_entrar = self.wait2.until(
                condicaoEsperada.presence_of_element_located((By.XPATH, lEntrar)))
            bt_entrar.click()
        except:
            logger.critical('Botão entrar não encontrado.')
        
        time.sleep(1)

        self.driver.get(self.loginMhtSys)

        while self.valida_elemento(By.XPATH, lEsperar):
            pass

        try:
            self.wait2.until(
                condicaoEsperada.presence_of_element_located((By.XPATH, lTitulo)))
        except TimeoutException as e:
            logger.warning('Tempo de Login atingido.\nVerifique sua conexão e tente novamente.')
            alert(
                'Tempo de Login atingido.\nVerifique sua conexão e tente novamente.', "Tempo de Login")
            self.driver.quit()

        while self.valida_elemento(By.XPATH, lEsperar):
            pass

    def entrar_system(self) -> None:
        lSelecionaMenu: str = '//*[@data-component-id="menu-toggle-button"]'
        lSelecionaProcura: str = '//*[@id="menu-search"]/input'
        lSelecionaSystem: str = '//*[@id="cfwApp"]'
        lEsperar: str = '//*[@class="loading-content sc-ion-loading-md"]'

        try:
            bt_menu = self.wait2.until(
                condicaoEsperada.presence_of_element_located((By.XPATH, lSelecionaMenu)))
            bt_menu.click()
        except:
            logger.critical('Botão menu não encontrado.')
        
        try:
            bt_procura = self.wait2.until(
                condicaoEsperada.presence_of_element_located((By.XPATH, lSelecionaProcura)))
            bt_procura.send_keys("System Management")
        except:
            logger.critical('Botão procura não encontrado.')
        
        try:
            bt_system = self.wait2.until(
                condicaoEsperada.presence_of_element_located((By.XPATH, lSelecionaSystem)))
            bt_system.click()
        except:
            logger.critical('Botão menu não encontrado.')
        
        while self.valida_elemento(By.XPATH, lEsperar):
            pass
        
        time.sleep(2)

    def entrar_tranlog(self) -> None:
        lSelecionaMenu: str = '//*[@data-component-id="menu-toggle-button"]'
        lSelecionaProcura: str = '//*[@id="menu-search"]/input'
        lSelecionaTranslog: str = '//*[@id="tranlogdetails"]'
        lEsperar: str = '//*[@class="loading-content sc-ion-loading-md"]'
        lTitulo: str = '//*[@data-component-id="ManhattanProActive"]'

        self.fecha_aba()

        try:
            self.wait2.until(
                condicaoEsperada.presence_of_element_located((By.XPATH, lTitulo)))
        except TimeoutException as e:
            logger.warning('Tempo de Login atingido.\nVerifique sua conexão e tente novamente.')
            alert(
                'Tempo de Login atingido.\nVerifique sua conexão e tente novamente.', "Tempo de Login")
            self.driver.quit()

        while self.valida_elemento(By.XPATH, lEsperar):
            pass

        try:
            bt_menu = self.wait2.until(
                condicaoEsperada.presence_of_element_located((By.XPATH, lSelecionaMenu)))
            bt_menu.click()
        except:
            logger.critical('Botão menu não encontrado.')
        
        try:
            bt_procura = self.wait2.until(
                condicaoEsperada.presence_of_element_located((By.XPATH, lSelecionaProcura)))
            bt_procura.send_keys("Tranlog")
        except:
            logger.critical('Botão procura não encontrado.')
        
        try:
            bt_menu = self.wait2.until(
                condicaoEsperada.presence_of_element_located((By.XPATH, lSelecionaTranslog)))
            bt_menu.click()
        except:
            logger.critical('Botão details não encontrado.')

        time.sleep(1)

        while self.valida_elemento(By.XPATH, lEsperar):
            pass

    def consulta_tranlog(self) -> None:
        lSelecionaExpandir: str = '//*[@data-component-id="expand-button"]'
        lTipoMessage: str = 'SHC_ANY_ShipConfirm_Custom'
        lEsperar: str = '//*[@class="loading-content sc-ion-loading-md"]'
        lPesquisas: str = '//*[@class="native-input sc-ion-input-md"]'
        lCheck: str = '//*[@type="checkbox"]'
        lPayload: str = '//*[@data-component-id="ViewPayload"]'
        lFrame: str = '//*[@class="ace_layer ace_text-layer"]'
        # lFrame: str = '//*[@class="ace_layer ace_text-layer"]'

        while self.valida_elemento(By.XPATH, lEsperar):
            pass

        try:
            lListaExpandir= self.driver.find_elements(By.XPATH, lSelecionaExpandir)
        except:
            logger.critical('Lista não encontrada.')

        x = 1
        for i in lListaExpandir:
            try:
                i.click
            except:
                logger.critical('Botão não encontrado.')
            x += 1
            if x == 2: break
        
        while self.valida_elemento(By.XPATH, lEsperar):
            pass
        
        try:
            lListaPesquisas= self.driver.find_elements(By.XPATH, lPesquisas)
        except:
            logger.critical('Lista não encontrada.')
        
        while True:
            i = 1
            for pesquisa in lListaPesquisas:
                try:
                    if i == 2: 
                        pesquisa.send_keys("605155590")
                    if i == 3: 
                        pesquisa.send_keys(lTipoMessage)
                    if i == 4:
                        pesquisa.send_keys(Keys.ENTER)
                        break
                except:
                    logger.critical('Pesquisa não encontrada.')
                i += 1
            
            while self.valida_elemento(By.XPATH, lEsperar):
                pass
            
            try:
                bt_check = self.wait2.until(
                    condicaoEsperada.presence_of_element_located((By.XPATH, lCheck)))
                bt_check.click()
            except:
                logger.critical('Botão menu não encontrado.')
            
            while self.valida_elemento(By.XPATH, lEsperar):
                pass
            
            try:
                bt_payload = self.wait2.until(
                    condicaoEsperada.presence_of_element_located((By.XPATH, lPayload)))
                bt_payload.click()
            except:
                logger.critical('Botão menu não encontrado.')

            try:
                payload = self.wait2.until(
                    condicaoEsperada.presence_of_element_located((By.XPATH, lFrame)))
                textPayload = payload.text
            except:
                logger.critical('Botão menu não encontrado.')

    def fecha_aba(self):
        self.pagina_principal = self.driver.current_window_handle
        for window_handle in self.driver.window_handles:
            if window_handle == self.pagina_principal:
                self.driver.close()
            elif window_handle != self.pagina_principal:
                self.driver.switch_to.window(window_handle)

    def navega_entre_aba(self):
        for window_handle in self.driver.window_handles:
            if window_handle != self.pagina_principal:
                self.driver.switch_to.window(window_handle)
                time.sleep(1)
            
    def valida_elemento(self, tipo, path) -> bool:
        # logger.info('Aguardando processamento...')
        try:
            lVisibilidade = self.wait.until(
                condicaoEsperada.visibility_of_element_located((tipo, path)))
        except:
            return False
        return True
    
    # self.wait_for_element(By.XPATH, checkbox_xpath).click()
    # self.wait_for_element(By.XPATH, view_payload_button_xpath).click()

    # try:
    #     payload_frame = self.wait_for_element(By.XPATH, payload_frame_xpath)
    #     text_payload = payload_frame.text
    # except NoSuchElementException:
    #     logger.critical('Payload frame not found.')

    def wait_for_element(self, by, locator, timeout=10):
        return WebDriverWait(self.driver, timeout).until(
            condicaoEsperada.presence_of_element_located((by, locator)))

    def wait_for_element_to_disappear(self, by, locator, timeout=10):
        return WebDriverWait(self.driver, timeout).until_not(
        condicaoEsperada.presence_of_element_located((by, locator)))

if __name__ == '__main__':
    executa = Mht_System()
    executa.start()
