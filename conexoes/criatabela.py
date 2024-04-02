
import psycopg2
from psycopg2 import sql
from string import Template
import psycopg2.extras
import psycopg2.extensions
import json
from string import Template
from psycopg2 import sql, extras
import pandas as pd


#conn = psycopg2.connect(database="postgres", user = "postgres", password = "alan7474", host = "127.0.0.1", port = "5433")

#print("Opened database successfully")

#cur = conn.cursor()



#cur.execute('''CREATE TABLE journal
 #     (ID SERIAL PRIMARY KEY     NOT NULL,
  #         dados JSONB  
   #   );''')
#print("Table created successfully")



        
#cur.execute('''INSERT INTO journal (dados) 
#VALUES 
 # (
 #   '{"title": "My first day at work", "Feeling": "Mixed                   feeling"}'
 # );''')


#######################################################################################

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

####################################################################################

for col in df.columns:
      df[col] = df[col].apply(str)
    


def inserir_db(sql):
    conn = psycopg2.connect(database="postgres", user = "postgres", password = "alan7474", host = "127.0.0.1", port = "5433")

    cur = conn.cursor()
    
    try:
        cur.execute(sql)
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error: %s" % error)
        conn.rollback()
        cur.close()
        return 1
    cur.close()
    
    
    
# Inserindo cada registro do DataFrame
for i in df.index:
    sql = """
    INSERT into hepatites (ano, n_de_casos) 
    values('%s','%s');
    """ % (df['Ano'][i], df['N_de_Casos'][i])
    inserir_db(sql)










#conn.commit()


#conn.close()
