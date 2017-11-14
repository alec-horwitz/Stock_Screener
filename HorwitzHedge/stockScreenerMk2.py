
# coding: utf-8

# In[1]:


import bs4 as bs
from bs4 import BeautifulSoup
import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
import os
import numpy as np
import pandas as pd
import pandas_datareader as web
import pickle
import requests
import urllib
import csv
import quandl


# In[2]:


def main():
    try:
        visualize_data()
    except:
        main()


# In[3]:


def visualize_data():
    compile_data()


# In[4]:


def compile_data():
    get_data_from_yahoo(reload_sp500=True)
    with open("sp500tickers.pickle","rb") as f:
        tickerList = pickle.load(f)
        
    main_df = pd.DataFrame()
    
    for count, ticker in enumerate(tickerList):
        df = pd.read_csv('stock_dfs/{}.csv'.format(ticker))
        df.set_index("Date", inplace=True)
        
        df.rename(columns = {'Adj Close':ticker}, inplace=True)
        df.drop(['Open','High',"Low",'Close','Volume'], 1, inplace=True)
        
        if main_df.empty:
            main_df = df
        else:
            main_df = main_df.join(df, how='outer')
            
        if count % 10 ==0:
            print(count)
        
    print(main_df.head())
    main_df.to_csv('sp500_joined_closes.csv')


# In[5]:


def get_data_from_yahoo(reload_sp500=False):
    if reload_sp500:
        tickerList = save_sp500_tickers()
    else:
        with open("sp500tickers.pickle", "rb") as f:
            tickerList = pickle.load(f)
    if not os.path.exists('stock_dfs'):
        os.makedirs('stock_dfs')
        
    start = dt.datetime(2017,10,30)
    end = dt.datetime(2017,10,31)
    
    for ticker in tickerList:
        print('ticker')
        if not os.path.exists('stock_dfs/{}.csv'.format(ticker)):
#             df = web.DataReader(ticker, 'yahoo', start, end)
            df = web.DataReader(ticker, 'yahoo', end)
            df.to_csv('stock_dfs/{}.csv'.format(ticker))
        else:
            print('Already have {}'.format(ticker))


# In[6]:


def save_sp500_tickers():
    resp = requests.get('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    soup = bs.BeautifulSoup(resp.text)
    table = soup.find('table', {'class':'wikitable sortable'})
    tickerList = []
    for row in table.findAll('tr')[1:10]: #Will only get 10 companies. Delete 10 for whole list.
        ticker=row.findAll('td')[0].text
        mapping = str.maketrans(".","-")
        ticker = ticker.translate(mapping)
        if not ("BHF" in row):
            tickerList.append(ticker)
    with open("sp500tickers.pickle", "wb") as f:
        pickle.dump(tickerList, f)
    
    print(tickerList)
    
    return tickerList


# In[7]:


main()


# In[161]:


def reformatDataFrame(input):
    df = pd.read_csv(input)
    df.pop('Date')
    df = df.transpose()
    df.columns = ["Adj Close Price"] #,"Market Cap", "P/E Ratio", "Div Yield (%)", "52 Week Price Change (%)"]
    df.index.name = "Ticker"
    df2 = pd.DataFrame()
    for ticker in df.index:
#         site = "http://financials.morningstar.com/ajax/exportKR2CSV.html?t="+ticker
#         print(site)
#         fund = pd.read_csv(site, error_bad_lines=False, engine = 'python')
#         fundamentals = urllib.request.urlopen("http://financials.morningstar.com/ajax/exportKR2CSV.html?t="+ticker)
#         fundamentals = csv.reader(fundamentals)
#         print(fundamentals)

#         htmlText = requests.get("http://financials.morningstar.com/ajax/exportKR2CSV.html?t="+ticker).text
#         lines=BeautifulSoup(htmlText,"html.parser")
#         lines = lines.prettify()
#         fout = open("fund.csv", 'w')
#         for line in lines.split("\n"):
#             print(line)
#             fout.write(line + "\n")
#         fout.close()
        df2 = pd.read_csv("MMMKeyRatios.csv", index_col = 0)
        print(ticker)
        df2 = df2['TTM'].head(20)
#         print(df2.index)
#         print(df2[0])
#     tickerDF = pd.DataFrame(index = ticker, columns = [df2.index])
#     print(tickerDF)

    dict = {}
    for i in range(len(df2.index)):
        dict[str(df2.index[i])] = df2[i]
    df3 = pd.DataFrame(data = dict, index = df.index)
#     print(df3)
#     print(df)
    frames = [df,df3]
    df4 = pd.concat(frames, axis=1)
    print(df4)


# In[162]:


reformatDataFrame('sp500_joined_closes.csv')


# In[7]:




