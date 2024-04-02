import time
import requests
import pandas as pd
from bs4 import BeautifulSoup
import selenium_firefox
import selenium_browser
from selenium import *
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By


import json

url = 'http://tabnet.datasus.gov.br/cgi/tabcgi.exe?sinannet/cnv/hepabr.def'

option = Options()
option.headless = False
driver = webdriver.Firefox(options=option)

driver.get(url)

time.sleep(10)

driver.find_element(By.CLASS_NAME, "mostra").click()

time.sleep(15)

for handle in driver.window_handles:
    driver.switch_to.window(handle)

# resultado = driver.find_element(By.XPATH, '/html/body/div/div/table/tbody/tr[1]/td[2]').text      deu certo!!!
#print(resultado)

element = driver.find_element(By.XPATH, '/html/body/div/div/table')
html_content = element.get_attribute('outerHTML')
#print(html_content)


# Parseando o conteudo do HTML com o  beautifulsoup

soup = BeautifulSoup(html_content, 'html.parser')
table = soup.find(name='table')


# Estruturar o conteudo em um DataFrame do Pandas

df_full = pd.read_html(str(table))[0].head(10)
df = df_full[['HEPATITES VIRAIS - Casos confirmados Notificados no Sistema de Informação de Agravos de Notificação - Brasil Casos confirmados segundo Ano Diag/sintomas Período: 2020']]
df.columns = ['Ano', 'N_de_Casos','seila']

df.drop('seila',axis='columns',inplace=True)

print(df)


# Transformar os dados em um dicionario

hepatitesVirais = {}
hepatitesVirais['hepatitesViraistotal'] = df.to_dict('records')

print(hepatitesVirais['hepatitesViraistotal'])


# Converter e salvar os dados em um arquivo JSON

js = json.dumps(hepatitesVirais)
fp = open('hepatitesVirais.json', 'w')
fp.write(js)
fp.close()


###############

driver.quit()