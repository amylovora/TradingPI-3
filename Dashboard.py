
import os
import streamlit as st
from datetime import datetime, timedelta
import numpy as np
import pandas as pd
import cufflinks as cf
import plotly.graph_objects as px
from plotly.subplots import make_subplots
import time

from DataTrading import *

st.set_page_config(
    page_title="PI-3 CryptoCoin Easy",
    page_icon="✅",
    layout="wide",
)

st.title("CryptoCoin Info")

### Seleccion crypto:
add_selectbox = st.selectbox(
    'Criptomoneda',
    ('BTC', 'ETH', 'BNB', 'XRP', 'DOGE', 'SHIB', 'ATOM', 'LUNC', 'FTT', 'SOL')
)


### Seleccion intervalo tiempo:

add_selecttime = st.sidebar.selectbox(
    'Intervalo de tiempo',
    ('1 minuto', '5 minutos', '15 minutos', '1 hora', '1 dia', '1 semana', '1 mes')
)

if add_selecttime == '1 minuto':
    interval = 60
elif add_selecttime == '5 minutos':
    interval = 60*5
elif add_selecttime == '15 minutos':
    interval = 60*15
elif add_selecttime == '1 hora':
    interval = 60*60
elif add_selecttime == '1 dia':
    interval = 60*60*24
elif add_selecttime == '1 semana':
    interval = 60*60*24*7
elif add_selecttime == '1 mes':
    interval = 60*60*24*30

### Calendario
yesterday = datetime.now() - timedelta(1)

d = st.sidebar.date_input(
    "Fecha inicio",
    yesterday)

fecha = datetime.strptime(str(d), '%Y-%m-%d')
y = fecha.year
dia = fecha.day
mes = fecha.month

### USD Observado hoy

dolarData = getUSD()
dolarObservado = pd.DataFrame(dolarData['serie'])
dolarObservado = dolarObservado['valor']
print(dolarObservado.to_string(index=False))

### Data
crypto = getData(add_selectbox, str(interval), y, mes, dia)
crypto['average_high'] = crypto['high'].rolling(5).mean()
crypto['average_low'] = crypto['low'].rolling(5).mean()
crypto['global mean'] = crypto[['open', 'high', 'low', 'close']].mean(axis=1)

### Variance

variance = round(crypto['global mean'].var(), 2)

# create three columns
kpi1, kpi2, kpi3, kpi4 = st.columns(4)

# fill in those three columns with respective metrics or KPIs
kpi1.metric(
    label="Fecha de hoy",
    value=str(datetime.utcnow().date())
)

kpi2.metric(
    label="Cypto a USD",
    value=str(datetime.utcnow().date())
)

kpi3.metric(
    label="1 USD",
    value=(dolarObservado.to_string(index=False) + 'CLP hoy')
)

kpi4.metric(
    label="Varianza del periodo",
    value=str(variance) + 'USD'
)



### Plot: variabilidad cripto y volumen
#fig = px.Figure()
titulo_sub = ("Variación " + add_selectbox)
fig = make_subplots(rows=2, cols=1, shared_xaxes=True, 
               vertical_spacing=0.08, subplot_titles=(add_selectbox, 'Volume'), 
               row_width=[0.4, 1.2])

fig.add_trace(px.Candlestick(x=crypto["date"], open=crypto["open"], high=crypto["high"],
                low=crypto["low"], close=crypto["close"], name=titulo_sub),
                row=1, col=1)

fig.add_trace(px.Scatter(x=crypto["date"], y=crypto["average_high"], name= 'Media movil alta', line=dict(color='blue', width=2)), row=1, col=1)
fig.add_trace(px.Scatter(x=crypto["date"], y=crypto["average_low"], name= 'Media movil baja', line=dict(color='orange', width=2)), row=1, col=1)


# Bar trace for volumes on 2nd row without legend
fig.add_trace(px.Bar(x=crypto['date'], y=crypto['volume'], showlegend=False), row=2, col=1)

# Do not show OHLC's rangeslider plot 
fig.update(layout_xaxis_rangeslider_visible=False)
fig

### calculadora de USD to Crypto
calculator1 = st.number_input('Inserta USD')
if st.button('Calcular USD'):
    precio1 = getCurrency(add_selectbox)
    conversion1 = calculator1/precio1
    st.write('Equivale a: ' + str(conversion1) + " " + str(add_selectbox))
    
calculator2 = st.number_input('Inserta ' + str(add_selectbox))
if st.button('Calcular Crypto'):
    precio2 = getCurrency(add_selectbox)
    conversion2 = calculator2*precio2
    st.write('Equivale a: ' + str(conversion2) + " " + "USD")


### Tabla datos
st.dataframe(crypto.style.highlight_max(axis=0))