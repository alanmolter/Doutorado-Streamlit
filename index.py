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


##################################################################################################################################################
import streamlit as st
import numpy as np
import plotly.express as px
from streamlit_plotly_events import plotly_events
from selenium.webdriver.firefox.options import Options
options = Options()
options.headless = True
driver = webdriver.Firefox(options=options)



url = 'http://tabnet.datasus.gov.br/cgi/tabcgi.exe?sinannet/cnv/hepabr.def'

option = Options()
option.headless = True
driver = webdriver.Firefox(options=option)

driver.get(url)

time.sleep(5)

driver.find_element(By.CLASS_NAME, "mostra").click()

time.sleep(5)

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

df_full = pd.read_html(str(table))[0]
df = df_full[['HEPATITES VIRAIS - Casos confirmados Notificados no Sistema de Informação de Agravos de Notificação - Brasil Casos confirmados segundo Ano Diag/sintomas Período: 2020']]
df.columns = ['Ano', 'N_de_Casos','seila']

df.drop('seila',axis='columns',inplace=True)


for col in df.columns:
      df[col] = df[col].apply(str)
      
print(df)  
      
driver.quit()      
################################################################################     
df.drop(df.head(1).index,inplace=True) 
df.drop(df.tail(1).index,inplace=True) 


df.to_csv('df.csv', index=False, sep='.')


@st.cache_data
def load_data():
    dados = pd.read_csv('df.csv', sep='.', decimal='.', thousands='.')
    dados['N_de_Casos'] = dados['N_de_Casos'].astype(int)
    return dados


data_load_state = st.text('Loading data...')
dados = load_data()
data_load_state.text("Done! (using st.cache_data)")






################################################################################################################################################
      
st.title('API DATASCIENCE VACINAS')    
      
  
      
      
st.subheader('Hepatites virais - Casos Confirmados')      


st.data_editor(dados)



st.bar_chart(data=dados, x='Ano', y='N_de_Casos', use_container_width=True)

      
@st.cache_data
def converte_csv(df):
    return df.to_csv(index = False).encode('utf-8')



def mensagem_sucesso():
    sucesso = st.success('Arquivo baixado com sucesso', icon = "✅") 
    time.sleep(6)
    sucesso.empty()


def preparando():
    msg = st.toast('Preparando...')
    time.sleep(3)
    msg.toast('Organizando tabela...')
    time.sleep(3)
    msg.toast('Pronto!', icon = "🤖")


st.markdown('Escreva um nome para o arquivo')
coluna1 , coluna2 = st.columns(2)
with coluna1:
    nome_arquivo = st.text_input('', label_visibility='collapsed', value='dados')
    nome_arquivo += '.csv'
    
    
with coluna2:
    contador = 0
    if st.download_button('Fazer o download da tabela em csv', data= converte_csv(df), file_name= nome_arquivo, mime= 'text/csv', on_click= mensagem_sucesso):
        preparando()
        contador+=1
        st.stop()
    elif contador != 0:
            st.stop()


st.divider()

st.image('./hepatitis_cases_trends_150dpi.png')


st.stop()


     
      
      
      
      
      
      
      

