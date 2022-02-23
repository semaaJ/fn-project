import json
import math
import datetime
import time

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.ensemble import RandomForestRegressor
from sklearn.svm import SVR
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_log_error

def convert_to_timestamp(x):
    """Convert date objects to integers"""
    return time.mktime(x.to_pydatetime().timetuple())


with open("data/share/SPY.json", "r") as f:
    data = json.load(f)

    df = pd.DataFrame.from_dict(data["historicalData"], orient='columns')
    base_df = pd.DataFrame.from_dict(data["historicalData"], orient='columns')


    df['date'] = pd.to_datetime(df['date'])
    # Convert to UNIX
    df['date'] = df['date'].apply(convert_to_timestamp)
    df["open"].fillna(method="ffill", inplace=True)
    df["close"].fillna(method="ffill", inplace=True)
    df["low"].fillna(method="ffill", inplace=True)
    df["high"].fillna(method="ffill", inplace=True)
    df["volume"].fillna(method="ffill", inplace=True)
    df['HL_PCT'] = (df['high'] - df['low']) / df['low'] * 100.0
    df['PCT_change'] = (df['close'] - df['open']) / df['open'] * 100.0
    
    forecast_out = int(math.ceil(0.005 * len(df)))
    df['label'] = df['close'].shift(-forecast_out)

    scaler = StandardScaler()
    X = np.array(df.drop(['label'], 1))
    scaler.fit(X)
    X = scaler.transform(X)

    X_Predictions = X[-forecast_out:]
    X = X[:-forecast_out]

    df.dropna(inplace=True)
    y = np.array(df['label'])

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=123)

    lr = LinearRegression()
    lr.fit(X_train, y_train)
    print("Linear Regression", lr.score(X_test, y_test))

    rf = RandomForestRegressor()
    rf.fit(X_train, y_train)
    print("Random Forest", rf.score(X_test, y_test))

    rg = Ridge()
    rg.fit(X_train, y_train)
    print("Ridge", rg.score(X_test, y_test))

    svr = SVR()
    svr.fit(X_train, y_train)
    print("SVR", svr.score(X_test, y_test))
    
    forecast_set = rg.predict(X_Predictions) 
    print(forecast_set)
    df['forecast'] = np.nan

    for (i, val) in enumerate(forecast_set):
        df.loc[df.index[-1] + i] = [np.nan for _ in range(len(df.columns) - 1)] + [val]

    plt.figure(figsize=(18, 8))
    df['date']
    df['close'].plot()
    df['forecast'].plot(color='green')
    plt.legend(loc=4)
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.show()

