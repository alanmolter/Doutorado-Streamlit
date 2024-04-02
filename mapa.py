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
import folium
from streamlit_folium import st_folium
import requests
from folium.plugins import HeatMap
from folium import plugins



df = pd.read_csv('../hepabr.csv', sep=',')

df.dropna(inplace=True)

df['casos'] = df['casos'].astype('int64')



print(df['casos'].dtypes)




mapa = pd.read_csv('../mapabr.csv', sep=',')
mapa = pd.DataFrame(mapa)

#print(mapa)


data = pd.concat([df, mapa], axis=1, join='inner')


print(data)



baseMap = folium.Map(width= '100',height= '100',location= [-15.788497, -47899873],zoom_start= 4)


coordenadas = data[['latitude', 'longitude','casos']].values.tolist()

print(coordenadas)


HeatMap(coordenadas, radius=15).add_to(baseMap)


for i in range(0,len(data)):
    folium.Circle(
    location = [data.iloc[i]['latitude'], data.iloc[i]['longitude']],
    color = '#000000',
    fill = '#00A1B3',
    tooltip = '<li><bold> UF: ' + str(data.iloc[i]['Estado']) + '<li><bold> Casos: ' + str(int(data.iloc[i]['casos'])),
    radius= 10).add_to(baseMap)



st.write(data)

#st_data = st_folium(baseMap)

st.write(
        f'<iframe src=""></iframe>',
        unsafe_allow_html=True,
    )
