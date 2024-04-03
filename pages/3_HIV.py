import select
import psycopg2
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

from selenium import webdriver
from selenium.webdriver.firefox.options import Options

options = Options()
options.add_argument("--headless")
driver = webdriver.Firefox(options=options)

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service

options = Options()
service = Service(log_path='geckodriver.log')
driver = webdriver.Firefox(service=service, options=options)



st.set_page_config(page_title="Dashboard de monitoramento de Surtos", layout='wide')

import json

with st.spinner('Carregando Dados...'):

    def preparando():
        msg = st.toast('Preparando...')
        time.sleep(3)
        msg.toast('Organizando tabela...')
        time.sleep(3)
        msg.toast('Pronto!', icon = "🤖")


    def scrape_website_1(result_queue):
  
        conn = psycopg2.connect(database="postgres", user = "postgres", password = "alan7474", host = "127.0.0.1", port = "5433")

        cur = conn.cursor()

        # Consulta SQL para selecionar tudo da tabela 'hiv2023'
        query = "SELECT * FROM hiv2023;"

        # Usando Pandas para executar a consulta e armazenar o resultado em um DataFrame
        dados = pd.read_sql_query(query, conn)

        cur.close()

       
        result = dados
        result_queue.put(("website_1",result))

       

    #################################################################################################################################################

    def scrape_website_2(result_queue):


        conn = psycopg2.connect(database="postgres", user = "postgres", password = "alan7474", host = "127.0.0.1", port = "5433")

        cur = conn.cursor()

        # Consulta SQL para selecionar tudo da tabela 'hiv2023'
        query = "SELECT * FROM dados_hivgeral;"

        # Usando Pandas para executar a consulta e armazenar o resultado em um DataFrame
        dados2 = pd.read_sql_query(query, conn)

        cur.close()

        
        result = dados2
        result_queue.put(("website_2",result))
        
      


    ################################################################################################
        
   
    #####################################################################
    
 # Carregando os dados geográficos dos estados do Brasil
    geo_data = gpd.read_file('./brazil_geo.json')

    # Substitua isto pelos seus dados reais de casos de gripe
    # Exemplo: flu_data = pd.read_csv('path/to/flu_data.csv')


    # Juntando os dados de casos de gripe com os dados geográficos

    def process_data_website_1(data):
        st.title("Dashboard de monitoramento de Surtos")
        st.subheader("Um dashboard interativo para monitoramento de casos")
        st.markdown('Casos de HIV no Brasil em 2023')
        st.write(data)

        
        chart_data = pd.DataFrame({
                    "Uf": data['UF Residência'],
                "casos": data['Frequencia'],
                
                })
        st.line_chart(chart_data, x='Uf', y='casos')

        data = pd.concat([data,geo_data], axis=1, join='inner')
        
         # Função para gerar o mapa
        def generate_heat_map(geo_data):
            m = folium.Map(location=[-15.788497, -47.879873], zoom_start=4)

            # Gerar dados para o Heat Map
            heat_data = [[row['geometry'].centroid.y, row['geometry'].centroid.x] 
                        for index, row in geo_data.iterrows()]

            # Adicionar o Heat Map ao mapa
            HeatMap(heat_data).add_to(m)

            return m



        # Configurando a página Streamlit
        
        st.title('Heat Map de Casos de HIV no Brasil em 2023')
        # Gerando e mostrando o mapa
        heat_map = generate_heat_map(geo_data)
        folium_static(heat_map)


        with st.expander("See explanation"):
            st.write('Numero de casos confirmados informados ao SINAN')
            st.text('''
                HIV: Definição, Transmissão, Prevenção e Tratamento

                O Vírus da Imunodeficiência Humana (HIV) é um retrovírus que ataca o sistema imunológico do corpo humano,
                especificamente as células T CD4, que são cruciais para a resposta imune. Com o tempo,
                e sem tratamento adequado, a ação do HIV pode levar à Síndrome da Imunodeficiência Adquirida (AIDS), 
                um estágio avançado da infecção por HIV caracterizado por uma contagem extremamente 
                baixa de células T CD4 e a ocorrência de doenças oportunistas.

                Transmissão:
                O HIV é transmitido principalmente através do contato com fluidos corporais infectados, incluindo sangue, sêmen, fluidos vaginais e leite materno. As vias de transmissão mais comuns são:
                - Relações sexuais desprotegidas com uma pessoa infectada.
                - Compartilhamento de seringas ou agulhas contaminadas.
                - De mãe para filho durante a gravidez, o parto ou a amamentação.
                - Transfusões de sangue ou transplantes de órgãos com material infectado (menos comum em países com rigorosa triagem de doadores).

                Prevenção:
                A prevenção do HIV envolve várias estratégias:
                - Uso de preservativos em todas as relações sexuais.
                - Terapias de profilaxia pré-exposição (PrEP) e pós-exposição (PEP) para pessoas de alto risco.
                - Educação e conscientização sobre as vias de transmissão e medidas de prevenção.
                - Testagem regular para HIV, especialmente para indivíduos em grupos de risco.
                - Uso de agulhas e seringas esterilizadas.
                - Medidas preventivas em gestantes HIV positivas para reduzir o risco de transmissão para o bebê.

                Tratamento:
                Embora não haja cura para o HIV, o tratamento antirretroviral (TARV) 
                pode controlar eficazmente o vírus, permitindo que as pessoas infectadas mantenham
                uma alta qualidade de vida. O TARV envolve a combinação de diferentes medicamentos 
                antirretrovirais que impedem a replicação do vírus, protegendo assim o sistema imunológico
                e prevenindo a progressão para AIDS. É crucial iniciar o tratamento o mais cedo 
                possível após o diagnóstico e seguir rigorosamente o regime prescrito.

                Além do TARV, o tratamento do HIV também inclui cuidados de suporte, 
                como tratamento de infecções oportunistas e acompanhamento médico regular 
                para monitorar a saúde geral e a eficácia do tratamento.
                    ''')
            st.image('./hiv.jpg')
            
            st.divider()


    st.divider()

    import streamlit as st
    import pandas as pd
    import plotly.express as px

    # Function to load and preprocess the data
    @st.cache_data
    def load_data():
        data = pd.read_csv('./dfHIVtodosanos2.csv', delimiter=';')
       
        return data

    # Loading data
    data = load_data()

    

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

    print(data.columns)


    def process_data_website_2(data): 
        st.title('Casos de HIV no Brasil desde 1980')
            # Adicionar um filtro na sidebar para escolher um ano
        st.sidebar.header("Filtros")
        # Os anos são obtidos diretamente do DataFrame, assumindo que as colunas estão nomeadas pelos anos
        anos = [col for col in data.columns if col.isnumeric()]  # Lista todos os anos presentes no DataFrame
        anos.insert(0, 'Todos os anos')  # Adiciona uma opção para mostrar todos os anos
        ano_escolhido = st.sidebar.selectbox('Escolha um ano', anos, index=0)  # Define "Todos os anos" como o valor padrão

        # Adicionar um filtro na sidebar para escolher uma UF
        ufs = data['uf_residencia'].unique()
        uf_escolhido = st.sidebar.selectbox('Escolha uma UF', ['Todos'] + list(ufs))

        # Aplicar filtros
        if ano_escolhido == 'Todos os anos' and uf_escolhido == 'Todos':
            dados_filtrados = data
        elif ano_escolhido == 'Todos os anos':
            dados_filtrados = data[data['UF Residência'] == uf_escolhido]
        elif uf_escolhido == 'Todos':
            dados_filtrados = data[['UF Residência', ano_escolhido]]
        else:
            dados_filtrados = data[data['UF Residência'] == uf_escolhido][['UF Residência', ano_escolhido]]

        # Mostrar os dados filtrados
        titulo = f"Dados para {uf_escolhido}, ano {ano_escolhido}" if ano_escolhido != 'Todos os anos' else f"Dados para {uf_escolhido}, todos os anos"
        st.write(titulo if uf_escolhido != 'Todos' else titulo.replace(f"para {uf_escolhido}, ", ""))
        st.dataframe(dados_filtrados)


    while not result_queue.empty():
                identifier, result = result_queue.get()

                if identifier == "website_1":
                    # Processa os dados do website 1
                    process_data_website_1(result)
                elif identifier == "website_2":
                    #Processa os dados do website 2
                    process_data_website_2(result)
    


    

    st.divider()


    preparando()

    
   
    ####################################################################################################################################

    
    

    st.divider()

    st.image('./hiv_cases_brazil_1980_2022_improved.png')
    
    st.divider()

    st.image('./hiv_cases_forecast_1980_2027.png')

    st.divider()

    st.image('./hiv_cases_predictions_2023_2027.png')

    st.divider()

##############################################################################################################################

    import pandas as pd
    import numpy as np
    import itertools
    from statsmodels.tsa.arima.model import ARIMA
    from statsmodels.tsa.stattools import adfuller
    import matplotlib.pyplot as plt
    from statsmodels.graphics.tsaplots import plot_acf, plot_pacf

    # Etapa 1: Carregar o arquivo CSV
    df = pd.read_csv('dfHIVtodosanos3.csv', sep=';')
    df_total_brasil = df[df['UF Residência'] == 'TOTAL'].drop(columns=['UF Residência', 'Total'])

    # Etapa 2: Transformar os dados em uma série temporal
    df_total_brasil_t = df_total_brasil.T
    df_total_brasil_t.columns = ['Casos']
    df_total_brasil_t.index = pd.to_datetime(df_total_brasil_t.index, format='%Y')

    # Etapa 3: Verificar a estacionariedade da série temporal e imprimir o resultado
    adf_result = adfuller(df_total_brasil_t['Casos'])
    print(f"Valor-p do teste de Dickey-Fuller: {adf_result[1]}")
    if adf_result[1] < 0.05:
        print("A série temporal é estacionária.")
        st.write("A série temporal é estacionária.")
    else:
        print("A série temporal não é estacionária.")
        st.write("A série temporal não é estacionária.")

    # Etapa 4: Análise de autocorrelação e autocorrelação parcial
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
    plot_acf(df_total_brasil_t['Casos'], ax=ax1, title="Autocorrelation Function")
    plot_pacf(df_total_brasil_t['Casos'], ax=ax2, title="Partial Autocorrelation Function", method='ywm')
    plt.tight_layout()
    plt.show()

    # Análise de autocorrelação (ACF)
    fig, ax = plt.subplots(figsize=(12, 4))
    plot_acf(df_total_brasil_t['Casos'], ax=ax, title="Autocorrelation Function")
    st.pyplot(fig)

    # Análise de autocorrelação parcial (PACF)
    fig, ax = plt.subplots(figsize=(12, 4))
    plot_pacf(df_total_brasil_t['Casos'], ax=ax, title="Partial Autocorrelation Function", method='ywm')
    st.pyplot(fig)

    # Etapa 5: Escolha de parâmetros iniciais e ajuste do modelo ARIMA
    p = d = q = range(0, 3)
    pdq_combinations = list(itertools.product(p, d, q))
    best_aic = np.inf
    best_pdq = None
    best_model = None

    for combination in pdq_combinations:
        try:
            model = ARIMA(df_total_brasil_t['Casos'], order=combination)
            model_fit = model.fit()
            if model_fit.aic < best_aic:
                best_aic = model_fit.aic
                best_pdq = combination
                best_model = model_fit
        except:
            continue

    # Etapa 6: Realizar previsões para os próximos 5 anos
    forecast_years = 5
    forecast = best_model.get_forecast(steps=forecast_years)
    forecast_conf_int = forecast.conf_int()
    forecast_predicted_mean = forecast.predicted_mean

    
   ################ ETAPA 7
    # Importar as bibliotecas necessárias
    import streamlit as st
    import pandas as pd
    import matplotlib.pyplot as plt
    from pandas.tseries.offsets import DateOffset


    # Gerar o gráfico
    plt.figure(figsize=(10, 6))
    plt.plot(df_total_brasil_t.index, df_total_brasil_t['Casos'], label='Dados Históricos')
    future_dates = [df_total_brasil_t.index[-1] + DateOffset(years=i) for i in range(1, forecast_years+1)]
    plt.plot(future_dates, forecast_predicted_mean, color='red', label='Previsões')
    plt.fill_between(future_dates, forecast_conf_int['lower Casos'], forecast_conf_int['upper Casos'], color='pink', label='Intervalo de Confiança')
    plt.title('ARIMA - Previsão de Casos de HIV no Brasil para os Próximos 5 Anos')
    plt.xlabel('Ano')
    plt.ylabel('Casos de HIV')
    plt.grid(color='gray', linestyle='-', linewidth=0.5)
    plt.legend()

    # Usar st.pyplot() para exibir o gráfico no Streamlit
    st.pyplot(plt)

    # Etapa 8: Exibir os resultados da previsão
    forecast_predicted_mean, forecast_conf_int


    st.divider()




    st.divider()
##############################################################################################################################
    st.video(data='https://youtu.be/m_nvjJ_u7fY?si=15KA-8Qp7t9VVBjF',format="video/mp4", start_time=0)
    st.success('Done!')

st.stop()