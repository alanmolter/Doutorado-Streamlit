import psycopg2
from psycopg2 import sql
from string import Template
import psycopg2.extras
import psycopg2.extensions
import json
from psycopg2 import sql, extras
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
import base64
import queue


result_queue = queue.Queue()

##################################################################################################################################################

url = 'https://sipni.datasus.gov.br/si-pni-web/faces/relatorio/consolidado/dosesAplicadasCampanhaPolioSarampo.jsf'


option = Options()
option.headless = False
driver = webdriver.Firefox(options=option)

driver.get(url)

time.sleep(5)

driver.find_element(By.ID, "pesquisar").click()

time.sleep(5)

for handle in driver.window_handles:
        driver.switch_to.window(handle)


element = driver.find_element(By.XPATH, '/html/body/div[5]/div/table[2]/tbody/tr/td/form/div[4]/div[2]/div[1]/table')
html_content = element.get_attribute('outerHTML')
print(html_content)

# Parseando o conteudo do HTML com o  beautifulsoup

soup = BeautifulSoup(html_content, 'html.parser')
table = soup.find(name='table')


    # Estruturar o conteudo em um DataFrame do Pandas

df_full = pd.read_html(str(table))[0]
df = df_full
df.columns = ['Região','Imunobiologico','Dose','20 a 24 ANOS','25 a 29 ANOS','30 a 34 ANOS','35 a 39 ANOS','40 a 44 ANOS','45 a 49 ANOS','Total','Data/Hora']


df.drop('Data/Hora',axis='columns',inplace=True)
    #df.drop('seila',axis='columns',inplace=True)


for col in df.columns:
        df[col] = df[col].apply(str)
        

df.replace('nan', '-',inplace=True)


print(df)  
        
driver.quit()      


df.to_csv('dfpni.csv', index=False, sep=',')

############################################################################################################################



def inserir_db():
    conn = psycopg2.connect(database="postgres", user = "postgres", password = "alan7474", host = "127.0.0.1", port = "5433")

    cur = conn.cursor()

    csv_file_path = 'dfpni.csv'

    # Abrir o arquivo CSV e importar os dados
    with open(csv_file_path, 'r', encoding='utf-8') as f:
        # Pular o cabeçalho
        next(f)
        # Copiar dados do CSV para a tabela
        cur.copy_from(f, 'pni', sep=',',columns=('Região', 'Imunobiologico', 'Dose', '20 a 24 ANOS', '25 a 29 ANOS', '30 a 34 ANOS', '35 a 39 ANOS', '40 a 44 ANOS', '45 a 49 ANOS','total')
)
        
        conn.commit()
        cur.close()


inserir_db()



print("Opened database successfully(1)")



##############################################################################################################################

#################################################################################################################################################
### pagina heatmap #################################


import select
import streamlit as st
import folium
from folium.plugins import HeatMap
from streamlit_folium import folium_static
import pandas as pd
import geopandas as gpd
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
import pydeck as pdk
import numpy as np
import threading
import queue



st.set_page_config(page_title="Dashboard de monitoramento de Surtos", layout='wide')

import json



def scrape_website_1(result_queue):

        url = 'https://www2.aids.gov.br/cgi/deftohtm.exe?tabnet/br.def'

        option = Options()
        option.headless = False
        driver = webdriver.Firefox(options=option)

        driver.get(url)

        time.sleep(5)


        driver.find_element(By.XPATH, '/html/body/table/tbody/tr/td/center/form/select[1]/option[4]').click()

        driver.find_element(By.XPATH,'/html/body/table/tbody/tr/td/center/form/select[4]/option[1]').click()

        driver.find_element(By.XPATH,'/html/body/table/tbody/tr/td/center/form/select[4]/option[1]').click()

        driver.find_element(By.XPATH,'/html/body/table/tbody/tr/td/center/form/p[3]/table/tbody/tr[1]/td[3]/select/option[45]').click()


        time.sleep(5)

        driver.find_element(By.XPATH, "/html/body/table/tbody/tr/td/center/form/p[3]/table/tbody/tr[22]/td/p[2]/input[1]").click()

        time.sleep(5)

        for handle in driver.window_handles:
            driver.switch_to.window(handle)



        element = driver.find_element(By.XPATH, '/html/body/table/tbody/tr/td/center/p/table')
        html_content = element.get_attribute('outerHTML')
        #print(html_content)


        # Parseando o conteudo do HTML com o  beautifulsoup

        soup = BeautifulSoup(html_content, 'html.parser')
        table = soup.find(name='table')


        # Estruturar o conteudo em um DataFrame do Pandas

        df_full = pd.read_html(str(table))[0]
        df = df_full
        df.columns = ['UF Residência', 'Freqüência']
        df['Freqüência'].astype(int)

        df = df.drop(df.index[0])
        
        df['Freqüência'] = df['Freqüência'].astype(float).astype(int)

        dados1 = df.to_csv('dfHIV.csv', index=False, sep=';')

        
        dados = pd.read_csv('dfHIV.csv', sep=';')


        ##df.drop('seila',axis='columns',inplace=True)


        #dados['Freqüência'] = dados['Freqüência'].astype(int)

        print(dados)

        result_queue = queue.Queue()

        result = dados1
        result_queue.put(("website_1",result))
        driver.quit()


        def inserir_db2():
            conn = psycopg2.connect(database="postgres", user = "postgres", password = "alan7474", host = "127.0.0.1", port = "5433")

            cur = conn.cursor()

            csv_file_path = 'dfHIV.csv'

            # Abrir o arquivo CSV e importar os dados
            with open(csv_file_path, 'r', encoding='utf-8') as f:
                # Pular o cabeçalho
                next(f)
                # Copiar dados do CSV para a tabela
                cur.copy_from(f, 'hiv2023', sep=';',columns=('UF Residência', 'Frequencia')) 
                conn.commit()
                cur.close()
                
        inserir_db2()     



        

print("Opened database successfully(2)")


#################################################################################################################################################



def scrape_website_2(result_queue):

        url = 'http://www2.aids.gov.br/cgi/tabcgi.exe?tabnet/br.def'

        option = Options()
        option.headless = False
        driver = webdriver.Firefox(options=option)

        driver.get(url)

        time.sleep(5)

        driver.find_element(By.XPATH, '/html/body/table/tbody/tr/td/center/form/select[1]/option[4]').click()##UF residencia
        driver.find_element(By.XPATH, '/html/body/table/tbody/tr/td/center/form/select[2]/option[2]').click()##Ano diagnostico

        

        driver.find_element(By.XPATH, '/html/body/table/tbody/tr/td/center/form/select[4]');##box periodos disponiveis
        
        driver.find_element(By.XPATH, '/html/body/table/tbody/tr/td/center/form/select[4]/option[1]').click() ##todos os anos 1980 a 2023
        driver.find_element(By.XPATH, '/html/body/table/tbody/tr/td/center/form/select[4]/option[2]').click()
        driver.find_element(By.XPATH, '/html/body/table/tbody/tr/td/center/form/select[4]/option[3]').click()
        driver.find_element(By.XPATH, '/html/body/table/tbody/tr/td/center/form/select[4]/option[4]').click()
        driver.find_element(By.XPATH, '/html/body/table/tbody/tr/td/center/form/select[4]/option[5]').click()
        driver.find_element(By.XPATH, '/html/body/table/tbody/tr/td/center/form/select[4]/option[6]').click()
        driver.find_element(By.XPATH, '/html/body/table/tbody/tr/td/center/form/select[4]/option[7]').click()
        driver.find_element(By.XPATH, '/html/body/table/tbody/tr/td/center/form/select[4]/option[8]').click()
        driver.find_element(By.XPATH, '/html/body/table/tbody/tr/td/center/form/select[4]/option[9]').click()
        driver.find_element(By.XPATH, '/html/body/table/tbody/tr/td/center/form/select[4]/option[10]').click()
        driver.find_element(By.XPATH, '/html/body/table/tbody/tr/td/center/form/select[4]/option[11]').click()
        driver.find_element(By.XPATH, '/html/body/table/tbody/tr/td/center/form/select[4]/option[12]').click()
        driver.find_element(By.XPATH, '/html/body/table/tbody/tr/td/center/form/select[4]/option[13]').click()
        driver.find_element(By.XPATH, '/html/body/table/tbody/tr/td/center/form/select[4]/option[14]').click()
        driver.find_element(By.XPATH, '/html/body/table/tbody/tr/td/center/form/select[4]/option[15]').click()
        driver.find_element(By.XPATH, '/html/body/table/tbody/tr/td/center/form/select[4]/option[16]').click()
        driver.find_element(By.XPATH, '/html/body/table/tbody/tr/td/center/form/select[4]/option[17]').click()
        driver.find_element(By.XPATH, '/html/body/table/tbody/tr/td/center/form/select[4]/option[18]').click()
        driver.find_element(By.XPATH, '/html/body/table/tbody/tr/td/center/form/select[4]/option[19]').click()
        driver.find_element(By.XPATH, '/html/body/table/tbody/tr/td/center/form/select[4]/option[20]').click()
        driver.find_element(By.XPATH, '/html/body/table/tbody/tr/td/center/form/select[4]/option[21]').click()
        driver.find_element(By.XPATH, '/html/body/table/tbody/tr/td/center/form/select[4]/option[22]').click()
        driver.find_element(By.XPATH, '/html/body/table/tbody/tr/td/center/form/select[4]/option[23]').click()
        driver.find_element(By.XPATH, '/html/body/table/tbody/tr/td/center/form/select[4]/option[24]').click()
        driver.find_element(By.XPATH, '/html/body/table/tbody/tr/td/center/form/select[4]/option[25]').click()
        driver.find_element(By.XPATH, '/html/body/table/tbody/tr/td/center/form/select[4]/option[26]').click()
        driver.find_element(By.XPATH, '/html/body/table/tbody/tr/td/center/form/select[4]/option[27]').click()
        driver.find_element(By.XPATH, '/html/body/table/tbody/tr/td/center/form/select[4]/option[28]').click()
        driver.find_element(By.XPATH, '/html/body/table/tbody/tr/td/center/form/select[4]/option[29]').click()
        driver.find_element(By.XPATH, '/html/body/table/tbody/tr/td/center/form/select[4]/option[30]').click()
        driver.find_element(By.XPATH, '/html/body/table/tbody/tr/td/center/form/select[4]/option[31]').click()
        driver.find_element(By.XPATH, '/html/body/table/tbody/tr/td/center/form/select[4]/option[32]').click()
        driver.find_element(By.XPATH, '/html/body/table/tbody/tr/td/center/form/select[4]/option[33]').click()
        driver.find_element(By.XPATH, '/html/body/table/tbody/tr/td/center/form/select[4]/option[34]').click()
        driver.find_element(By.XPATH, '/html/body/table/tbody/tr/td/center/form/select[4]/option[35]').click()
        driver.find_element(By.XPATH, '/html/body/table/tbody/tr/td/center/form/select[4]/option[36]').click()
        driver.find_element(By.XPATH, '/html/body/table/tbody/tr/td/center/form/select[4]/option[37]').click()
        driver.find_element(By.XPATH, '/html/body/table/tbody/tr/td/center/form/select[4]/option[38]').click()
        driver.find_element(By.XPATH, '/html/body/table/tbody/tr/td/center/form/select[4]/option[39]').click()
        driver.find_element(By.XPATH, '/html/body/table/tbody/tr/td/center/form/select[4]/option[40]').click()
        driver.find_element(By.XPATH, '/html/body/table/tbody/tr/td/center/form/select[4]/option[41]').click()
        driver.find_element(By.XPATH, '/html/body/table/tbody/tr/td/center/form/select[4]/option[42]').click()
        driver.find_element(By.XPATH, '/html/body/table/tbody/tr/td/center/form/select[4]/option[43]').click()
        

        
        
        driver.find_element(By.XPATH, "/html/body/table/tbody/tr/td/center/form/p[3]/table/tbody/tr[22]/td/p[2]/input[1]").click()##botao mostra


        time.sleep(7)

        for handle in driver.window_handles:
            driver.switch_to.window(handle)



        element = driver.find_element(By.XPATH, '/html/body/table/tbody/tr/td/center/p/table')
        html_content = element.get_attribute('outerHTML')
        #print(html_content)


        # Parseando o conteudo do HTML com o  beautifulsoup

        soup = BeautifulSoup(html_content, 'html.parser')
        table = soup.find(name='table')


        # Estruturar o conteudo em um DataFrame do Pandas

        df_full = pd.read_html(str(table))[0]
        df2 = df_full

        ### df2.columns = ['UF Residência', 'Freqüência']
    
        df2.to_csv('dfHIVtodosanos.csv', index=False, sep=';')

        dados2 = pd.read_csv('dfHIVtodosanos.csv', sep=';')


        print(dados2)

        dados2['Total'] = dados2['Total']

       
        for coluna in dados2.columns:
            if coluna.startswith('1' or '2'):
                dados2[coluna] = pd.to_numeric(dados2[coluna], errors='coerce').fillna(0).astype(int)

        #pd.to_numeric(dados2['Total'], errors='coerce').fillna(0, downcast='infer')
        dados2['Total'] = pd.to_numeric(dados2['Total'], errors='coerce').fillna(0)

        dados2.to_csv('dfHIVtodosanos2.csv', index=False, sep=';')

        

        driver.quit()

        result_queue = queue.Queue()
        

        result = dados2
        result_queue.put(("website_2",result))

      

        # Carregar o DataFrame novamente
        dados3 = pd.read_csv('dfHIVtodosanos2.csv', sep=';')

        # Limpar os valores e converter para int
        for coluna in dados3.columns:
                    if coluna.startswith('ano_'or '1' or '2'):
                        # Substituir ponto por nada e converter para int
                        dados3[coluna] = pd.to_numeric(dados3[coluna], errors='coerce').fillna(0).astype(int)
                        dados3[coluna] = dados3[coluna].replace({"\.": ""}, regex=True).astype(int)
                        dados3[coluna] = dados3[coluna].astype(str).str.replace('.', '').astype(int)


        # Convert all numeric columns to integers while preserving their original values (thousands without the decimal separator)
        for col in dados3.columns[1:]:  # Skip the first column
            dados3[col] = (dados3[col] * 1000).round(0).astype(int)


        print(dados3.head())

        # Salvar o DataFrame limpo para um novo CSV
        dados3.to_csv('dfHIVtodosanos3.csv', index=False, sep=';')

        def inserir_db3():
            conn = psycopg2.connect(database="postgres", user = "postgres", password = "alan7474", host = "127.0.0.1", port = "5433")

            cur = conn.cursor()

    
            csv_file_path = 'dfHIVtodosanos3.csv'

            # Abrir o arquivo CSV e importar os dados
            with open(csv_file_path, 'r', encoding='utf-8') as f:
                # Pular o cabeçalho
                next(f)
                # Copiar dados do CSV para a tabela
                cur.copy_from(f, 'dados_hivgeral', sep=';',columns=('uf_residencia', 'ano_1980', 'ano_1982', 'ano_1983', 'ano_1984', 'ano_1985', 'ano_1986', 'ano_1987', 'ano_1988', 'ano_1989', 'ano_1990', 'ano_1991', 'ano_1992', 'ano_1993', 'ano_1994', 'ano_1995', 'ano_1996', 'ano_1997', 'ano_1998', 'ano_1999', 'ano_2000', 'ano_2001', 'ano_2002', 'ano_2003', 'ano_2004', 'ano_2005', 'ano_2006', 'ano_2007', 'ano_2008', 'ano_2009', 'ano_2010', 'ano_2011', 'ano_2012', 'ano_2013', 'ano_2014', 'ano_2015', 'ano_2016', 'ano_2017', 'ano_2018', 'ano_2019', 'ano_2020', 'ano_2021', 'ano_2022', 'total')) 
                conn.commit()
                cur.close()
                
        inserir_db3()     



        

print("Opened database successfully(3)")

    
##########################################################################################################################################


    
# Cria uma fila para armazenar os resultados
result_queue = queue.Queue()

# Cria threads para cada tarefa de scraping
thread1 = threading.Thread(target=scrape_website_1, args=(result_queue,))
thread2 = threading.Thread(target=scrape_website_2, args=(result_queue,))

# Inicia as threads
thread1.start()
thread2.start()

# Aguarda a conclusão de ambas as threads
thread1.join()
thread2.join()

while not result_queue.empty():
                identifier, result = result_queue.get()

                if identifier == "website_1":
                    # Processa os dados do website 1
                    scrape_website_1(result)
                elif identifier == "website_2":
                    #Processa os dados do website 2
                    scrape_website_2(result)
        
    

print('SALVAMENTO E CONSULTA REALIZADOS COM SUCESSO!!!!')