import sys
import yfinance as yf  
import json
import math
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression
import datetime as dt
from datetime import date


def linear_regression(x, y):

    x = np.array([i for i in range(len(x))])
    y = np.array([i for i in y])

    print("len X", len(x))
    print("len Y", len(y))
    
    x.reshape(len(x), 1)
    y.reshape(len(y), 1)

    print("X:", x[0:10])
    print("Y:", y[0:10])

    linreg = LinearRegression().fit(x, y)
    linreg.score(x, y)
    predictions = linreg.predict(y)
    # model = model = LinearRegression().fit(x, y)
    # r_sq = model.score(x, y)
    # print('coefficient of determination:', r_sq)

    # y_new = np.arange(20).reshape((-1, 1))
    # y_new = model.predict(y)
    # print(y[-20:s

    plt.plot(y, color = 'magenta')
    # plt.plot(x, color = 'magenta')
    # plt.plot(x_new, color = 'green')
    plt.show()
    plt.close()


def get_historical_data(share_name):
    share = yf.Ticker(share_name)
    historical_data = share.history(period="max")
    share_info = share.info

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

    return share_info, data

def get_current_price(symbol):
    ticker = yf.Ticker(symbol)
    todays_data = ticker.history(period='1d')
    return todays_data['Close'][0]

import sys
share_info, historical_data = get_historical_data(sys.argv[1])
linear_regression([item["date"] for item in historical_data], [item["close"] for item in historical_data])