import streamlit as st
import folium
from streamlit_folium import folium_static
import geopandas as gpd

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

# Carregando os dados geográficos dos estados do Brasil
# Substitua 'path/to/brazil_geojson.json' pelo caminho do seu arquivo GeoJSON
geo_data = gpd.read_file('./brazil_geo.json')

# Função para gerar o mapa
def generate_map(geo_data):
    # Inicie o mapa centrado no Brasil
    m = folium.Map(location=[-15.788497, -47.879873], zoom_start=4)
    
    folium.GeoJson(
        geo_data,
        name='geojson'
    ).add_to(m)

    return m

# Configurando a página Streamlit
st.title('Mapa dos Estados do Brasil')

# Gerando e mostrando o mapa
br_map = generate_map(geo_data)
folium_static(br_map)

