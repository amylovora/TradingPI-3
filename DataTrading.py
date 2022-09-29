from datetime import datetime
from operator import index
import os
import json
from pickle import FALSE
import pandas as pd
import requests
import time



def getData(crypto, interval, y, mes, dia):   
    endpoint_url = 'https://ftx.com/api/markets'

    base_currency = crypto
    quote_currency = 'USD'
    request_url = f'{endpoint_url}/{base_currency}/{quote_currency}'
    daily=interval
    start_date = datetime(y, mes, dia).timestamp()
    historical = requests.get(
        f'{request_url}/candles?resolution={daily}&start_time={start_date}'
    ).json()
    df = pd.DataFrame(historical['result'])
    df['date'] = pd.to_datetime(
        df['time']/1000, unit='s', origin='unix'
    ) 
    df.drop(['startTime', 'time'], axis=1, inplace=True)
    dataTrading = df
    return dataTrading

def getUSD():  
    d = pd.to_datetime('today').strftime('%d-%m-%Y')
    url = f'https://mindicador.cl/api/dolar/{d}'
    response = requests.get(url)
    data = json.loads(response.text.encode("utf-8"))
    # Para que el json se vea ordenado, retornar pretty_json
    pretty_json = json.dumps(data, indent=2)
    return data


def getCurrency(crypto):   
    print(crypto)
    endpoint_url = 'https://ftx.com/api/markets'

    # Get all market data as JSON
    all_markets = requests.get(endpoint_url).json()

    # Convert JSON to Pandas DataFrame
    df = pd.DataFrame(all_markets['result'])
    df.set_index('name', inplace = True)
    base_currency = crypto
    quote_currency = 'USD'

    # Specify the base and quote currencies to get single market data
    request_url = f'{endpoint_url}/{base_currency}/{quote_currency}'

    df = pd.DataFrame(requests.get(request_url).json())
    precio=df['result']['price']
    return precio

