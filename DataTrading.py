from datetime import datetime
import os
import json
import pandas as pd
import requests
import time

    
endpoint_url = 'https://ftx.com/api/markets'

base_currency = 'ETH'
quote_currency = 'USD'
request_url = f'{endpoint_url}/{base_currency}/{quote_currency}'
daily=str(60*60*24)
start_date = datetime(2019, 1, 1).timestamp()
historical = requests.get(
    f'{request_url}/candles?resolution={daily}&start_time={start_date}'
).json()
df = pd.DataFrame(historical['result'])
df['date'] = pd.to_datetime(
    df['time']/1000, unit='s', origin='unix'
) 
df.drop(['startTime', 'time'], axis=1, inplace=True)
dataTrading = df
print(dataTrading)