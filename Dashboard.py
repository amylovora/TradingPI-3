
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

# create three columns
kpi1, kpi2, kpi3 = st.columns(3)

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
    label="USD a CLP Observado",
    value=dolarObservado.to_string(index=False)
)

### Data
crypto = getData(add_selectbox, str(interval), y, mes, dia)
crypto['average_high'] = crypto['high'].rolling(5).mean()
crypto['average_low'] = crypto['low'].rolling(5).mean()



### Plot: variabilidad cripto y volumen
#fig = px.Figure()
titulo_sub = ("Variación " + add_selectbox)
fig = make_subplots(rows=2, cols=1, shared_xaxes=True, 
               vertical_spacing=0.03, subplot_titles=(add_selectbox, 'Volume'), 
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



### Tabla datos
st.dataframe(crypto.style.highlight_max(axis=0))