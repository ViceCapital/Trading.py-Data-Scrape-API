
#Equity Scraper

from keys import ameritrade
import requests, time, re, os
import pandas as pd
import pickle as pkl

url = 'https://api.tdameritrade.com/v1/instruments'

df = pd.read_excel('company_list.xlsx')
symbols = df['Symbol'].values.tolist()


start = 0
end = 500
files = []


#Creating loop for 500 tickers per pull request
while start < len(symbols):

    tickers = symbols[start:end]

    payload = {'apikey': ameritrade,
               'symbol': tickers,
               'projection': 'fundamental'}
    
    results = requests.get(url,params=payload)
    data = results.json()
    file = time.asctime() + '.pkL'
    file = re.sub('[ :]','_',file)
    files.append(file)
    with open(file, 'wb') as file:
        pkl.dump(data,file)
    start = end
    end += 500
    time.sleep(1)
    
    
data = []

for file in files:
    with open(file,'rb') as f:
        info = pkl.load(f) 
    tickers = list(info)
    points = ['symbol','grossMarginTTM','returnOnEquity','peRatio','epsTTM']
    for ticker in tickers:
        tick = []
        for point in points:
            tick.append(info[ticker]['fundamental'][point])
        data.append(tick)
    os.remove(file) #removes redundant files after load
    
points = ['symbol','grossMarginTTM','returnOnEquity','peRatio','epsTTM']

df_results = pd.DataFrame(data,columns=points)
df_gm = df_results[df_results['grossMarginTTM'] > 2]

def view(size):
    start = 0
    stop = size
    while stop < len(df_gm):
        print(df_gm[start:stop])
        start = stop
        stop += size
    print(df_gm[start:stop])
    
#PropScreen
#df_symbols = df_gm['symbol'].tolist()
#new = df['Symbol'].isin(df_symbols)
#companies = df[new]
#companies
