import sys
import yfinance as yf  
import json
import math
import csv
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from pycoingecko import CoinGeckoAPI
from datetime import date, datetime


def get_historical_data(share_name):
    share = yf.Ticker(share_name)
    historical_data = share.history(period="max")

    data = []
    for row in historical_data.iterrows():
        row_data = row[1]

        data.append({
            "date": str(row[0]),
            "close": row_data["Close"],
            "volume": row_data["Volume"],
            "open": row_data["Open"],
            "low": row_data["Low"],
            "high": row_data["High"]
        })

    return share.info, data

def get_current_price(symbol):
    ticker = yf.Ticker(symbol)
    todays_data = ticker.history(period='1d')
    return todays_data['Close'][0]

def from_epoch(epochtime):
    return datetime.fromtimestamp(epochtime / 1000)

def get_crypto_data(id):
    cg = CoinGeckoAPI()
    data = cg.get_coin_market_chart_by_id(id, 'usd', 'max')

    dates = [from_epoch(i[0]) for i in data["prices"]]
    prices = [i[1] for i in data["prices"]]
    total_volume = [i[1] for i in data["total_volumes"]]
    market_cap = [i[1] for i in data["market_caps"]]

    return [{"date": str(dates[i]), "price": prices[i], "volume": total_volume[i], "marketCap": market_cap[i]} for i in range(len(dates))]


# df = pd.DataFrame.from_dict(data, orient='columns')
# df["price"].fillna(method="ffill", inplace=True)
# df["volume"].fillna(method="ffill", inplace=True)
# df["market_cap"].fillna(method="ffill", inplace=True)


# plt.plot(df["price"], color='blue')
# plt.plot(df["volume"], color='magenta')
# plt.plot(df["market_cap"], color='black')

# plt.show()

# split_date =  df.index[df['date'] == datetime.strptime("2018-02-25 00:00:00", "%Y-%m-%d %H:%M:%S")].tolist()[0]
# print("splite_date", split_date, df["date"][split_date])
# data_train = df[:split_date].copy()
# data_test = df[split_date:].copy()

# print("len train", len(data_train))
# print("len test", len(data_test))


# print(data_train.head())
# print(data_test.tail())

# training_set = data_train.values
# reshape_amt = abs(len(data_train.values) - len(data_test.values))
# print("train set length", training_set)
# training_set = np.reshape(training_set, (len(training_set), 1))

# sc = MinMaxScaler()
# training_set = sc.fit_transform(training_set)
# X_train = training_set[0:len(training_set) - 1]
# y_train = training_set[1:len(training_set)]
# X_train = np.reshape(X_train, (len(X_train), 1, 1))



    
   

