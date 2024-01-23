from loguru import logger
from cmath import log
import pandas as pd
import os

def carrega_parametros():
    logger.info('Verificando login e dias de extração.')
    caminhoArquivo = os.getcwd() + "\\" + 'Parametros.txt'
    try:
        plan = pd.read_table(caminhoArquivo, header=None, sep=":")  # latin-1
        usr = str(plan[1][0]).strip()
        senha = str(plan[1][1]).strip()
        dias = int(plan[1][2])
        return usr,senha,dias
    except:
        pass
        logger.warning('Não foi possivel ler o arquivo')

usr, senha, dias  = carrega_parametros()

print(usr, senha, dias)

