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

##################################################################################################################################################
import streamlit as st
import numpy as np
import plotly.express as px
from streamlit_plotly_events import plotly_events

st.set_page_config(layout="wide")
with st.spinner('Carregando Dados...'):
    


########################################################################################################################################

    conn = psycopg2.connect(database="postgres", user = "postgres", password = "alan7474", host = "127.0.0.1", port = "5433")

    cur = conn.cursor()

    # Consulta SQL para selecionar tudo da tabela 'pni'
    query = "SELECT * FROM pni;"

    # Usando Pandas para executar a consulta e armazenar o resultado em um DataFrame
    dados = pd.read_sql_query(query, conn)

    cur.close()


########################################################################################################################################

    @st.cache_data
    def load_data():
        #dados = pd.read_csv('dfpni.csv', sep='.', decimal='.', thousands='.')
        dados['20 a 24 ANOS'] = dados['20 a 24 ANOS'].astype(int)
        dados['25 a 29 ANOS'] = dados['25 a 29 ANOS'].astype(int)
        dados['30 a 34 ANOS'] = dados['30 a 34 ANOS'].astype(int)
        dados['35 a 39 ANOS'] = dados['35 a 39 ANOS'].astype(int)
        dados['40 a 44 ANOS'] = dados['40 a 44 ANOS'].astype(int)
        dados['45 a 49 ANOS'] = dados['45 a 49 ANOS'].astype(int)
        return dados


    data_load_state = st.text('Loading data...')
    dados = load_data()
    data_load_state.text("Done!")


    from selenium import webdriver
    from selenium.webdriver.firefox.options import Options

    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Firefox(options=options)

    from selenium.webdriver.firefox.options import Options
    options = Options()
    options.headless = True
    driver = webdriver.Firefox(options=options)


    from selenium import webdriver
    from selenium.webdriver.firefox.options import Options
    from selenium.webdriver.firefox.service import Service

    options = Options()
    service = Service(log_path='geckodriver.log')
    driver = webdriver.Firefox(service=service, options=options)




    ##################################################################################################################################################

    st.title('API DATASCIENCE VACINAS')    
        
    
    st.subheader('Campanha Nacional de Vacinação contra o Sarampo - 2020')      

    # Inicializa o estado da sessão
    if 'df' not in st.session_state:
        # Carrega os dados uma única vez e armazena no estado da sessão
        st.session_state.df = dados

    # Utiliza os dados armazenados no estado da sessão
    df = st.session_state.df

    def tabela():

        # Sidebar - Filter Options
        st.sidebar.header("Filter Options")

        # Region Filter - Multiple Selections
        selected_regions = st.sidebar.multiselect('Select Regions', df['Região'].unique(), default=df['Região'].unique())

        # Imunobiológico Filter - Multiple Selections
        selected_imunobiologicos = st.sidebar.multiselect('Select Immunobiological Types', df['Imunobiologico'].unique(), default=df['Imunobiologico'].unique())

        # Age Group Filter
        age_groups = ['20 a 24 ANOS', '25 a 29 ANOS', '30 a 34 ANOS', '35 a 39 ANOS', '40 a 44 ANOS', '45 a 49 ANOS']
        selected_age_groups = st.sidebar.multiselect('Select Age Groups', age_groups, default=age_groups)

        # Filter DataFrame based on selected filters
        filtered_df = df[df['Região'].isin(selected_regions) & df['Imunobiologico'].isin(selected_imunobiologicos)]
        filtered_df = filtered_df[['Região', 'Imunobiologico', 'Dose'] + selected_age_groups]

        # Display the filtered DataFrame
        st.write(filtered_df)


    tabela()

    ###############################################################################################################################################
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


    from PIL import Image
    import requests
    from io import BytesIO
    # Carregar uma imagem do sistema de arquivos local ou de uma URL
    def load_image(image_path_or_url):
        if image_path_or_url.startswith('http'):
            response = requests.get(image_path_or_url)
            image = Image.open(BytesIO(response.content))
        else:
            image = Image.open(image_path_or_url)
        return image

    # Exemplo de imagem
    image_url = "./zegota.png"
    image = load_image(image_url)

    # Adicionando a imagem na barra lateral
    st.sidebar.title("Se vacinar e importante !")
    st.sidebar.image(image, caption='Ze Gotinha')


    preparando()

    ####################################################################################################################################################

    import streamlit as st
    import pandas as pd
    import matplotlib.pyplot as plt
    import seaborn as sns

    
   
    st.title("Análise de Dados de Vacinação")

    # Análise por Região
    st.subheader("Número Total de Vacinas por Região")
    total_por_regiao = df.groupby('Região')['total'].sum()
    st.bar_chart(total_por_regiao)

    # Diferença entre Vacinas
    # Diferença entre Vacinas - Gráfico de Barras Empilhadas
    st.subheader("Distribuição de Vacinas por Tipo")
    # Preparando os dados
    df_grouped = df.groupby(['Região', 'Imunobiologico'])['total'].sum().unstack()
    df_grouped.plot(kind='bar', stacked=True, figsize=(15, 10))
    plt.title('Distribuição de Vacinas por Tipo e Região')
    plt.xlabel('Região')
    plt.ylabel('Número Total de Vacinas')
    st.pyplot(plt.gcf())
    

    # Cobertura Vacinal por Faixa Etária - Gráfico de Barras Agrupadas
    st.subheader("Cobertura Vacinal por Faixa Etária")
    faixas_etarias = ['20 a 24 ANOS', '25 a 29 ANOS', '30 a 34 ANOS', 
                    '35 a 39 ANOS', '40 a 44 ANOS', '45 a 49 ANOS']
    df_faixas = df.melt(id_vars=['Região', 'Imunobiologico'], value_vars=faixas_etarias, 
                        var_name='Faixa Etária', value_name='Número de Vacinas')

    # Criando o gráfico de barras agrupadas
    plt.figure(figsize=(15, 10))  # Aumentando o tamanho da figura
    sns.barplot(data=df_faixas, x='Região', y='Número de Vacinas', hue='Faixa Etária')
    plt.xticks(rotation=45)
    plt.legend(title='Faixa Etária', bbox_to_anchor=(1.05, 1), loc='upper left')
    st.pyplot(plt.gcf())


    # Footer
    st.info("Dashboard de Análise de Vacinação")

    st.divider()

    ######################################################################################################################################################

        
    import streamlit as st
    import pandas as pd
    from sklearn.model_selection import train_test_split
    from sklearn.linear_model import LinearRegression
    from sklearn.metrics import mean_squared_error
    import numpy as np

    # Função para carregar e limpar dados de sarampo
    def load_clean_sarampo_data():
        df_sarampo = pd.read_csv('Sarampoteste.csv', delimiter=';', encoding='utf-8')
        df_sarampo.drop(['RegiÃ£o e UF'], axis=1, inplace=True)
        df_sarampo = df_sarampo.sum()
        return df_sarampo

    # Função para carregar e limpar dados de vacinação
    def load_clean_vacinacao_data():
        df_vacinacao = dados
        faixas_etarias = ['20 a 24 ANOS', '25 a 29 ANOS', '30 a 34 ANOS', '35 a 39 ANOS', '40 a 44 ANOS', '45 a 49 ANOS']
        df_vacinacao = df_vacinacao[faixas_etarias].mean()
        return df_vacinacao

    # Função para preparar dados
    def prepare_data(df_sarampo, df_vacinacao):
        combined_df = pd.DataFrame({
            'Ano': df_sarampo.index,
            'Total Casos Sarampo': df_sarampo.values
        })
        for faixa in df_vacinacao.index:
            combined_df[faixa] = df_vacinacao[faixa]
        return combined_df

    # Função para construir e treinar o modelo
    def train_model(combined_df, df_vacinacao):
        X = combined_df[df_vacinacao.index]
        y = combined_df['Total Casos Sarampo']
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
        model = LinearRegression()
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        mse = mean_squared_error(y_test, y_pred)
        rmse = np.sqrt(mse)
        return model, rmse

    # Função para previsões futuras
    def make_predictions(model, mean_features):
        predictions = {}
        for year in range(2024, 2027):
            predicted_cases = model.predict([mean_features])
            predictions[year] = int(predicted_cases[0]) if predicted_cases[0] > 0 else 0
        return predictions

    # Função principal para executar o app Streamlit
    def gerar():
        st.title("Análise e Previsão de Casos de Sarampo no Brasil")

        df_sarampo = load_clean_sarampo_data()
        df_vacinacao = load_clean_vacinacao_data()
        combined_df = prepare_data(df_sarampo, df_vacinacao)
        model, rmse = train_model(combined_df, df_vacinacao)
        mean_features = combined_df[df_vacinacao.index].mean().values
        predictions = make_predictions(model, mean_features)

       
        for year, prediction in predictions.items():
            st.markdown(f"**{year}:** {prediction} casos estimados", unsafe_allow_html=True)
        st.write(f"RMSE do modelo: {rmse}")

        




    def down():
        
        st.title("Análise e Previsão de Casos de Sarampo no Brasil")

        # Restante do código...

        # Adicionando o dropdown (expander) com informações sobre o modelo de ML
        with st.expander("Saiba Mais Sobre o Modelo de Machine Learning Utilizado"):
            st.write("""
                ### Modelo de Regressão Linear
                O modelo de regressão linear utilizado neste projeto tenta prever o número 
                de casos de sarampo com base na média das doses de vacinação aplicadas em diferentes faixas etárias.
                
                - **Características (Features):** Médias de doses de vacinação para diferentes faixas etárias.
                - **Variável Alvo (Target):** Total de casos de sarampo reportados anualmente.
                - **Método de Treinamento:** O modelo é treinado usando uma parte dos dados (treino) e validado com outra parte (teste).
                
                A regressão linear tenta traçar uma linha que melhor se ajusta aos dados, minimizando a diferença (erro) entre os valores previstos e os valores reais.
            """)
            
            st.markdown("![Alt Text](https://miro.medium.com/v2/resize:fit:4800/format:webp/1*wsBakfF2Geh1zgY4HJbwFQ.gif)")









    gerar()
    down()

    
    # Footer
    st.info("Previsão de Casos de Sarampo com Machine Learning")


##################################################################################################################################################

st.stop()

