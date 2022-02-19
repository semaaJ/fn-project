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
    x = np.array([i for i in range(len(x))]).reshape((-1, 1))
    y = np.array([i for i in y])
    
    model = model = LinearRegression().fit(x, y)
    r_sq = model.score(x, y)
    print('coefficient of determination:', r_sq)

    x_new = np.arange(20).reshape((-1, 1))
    y_new = model.predict(x_new)
    print(y[-20:])
    print(y_new)

    plt.plot(x, color = 'magenta')
    plt.plot(x_new, color = 'green')
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


if __name__ == "__main__":
    share_name = sys.argv[1]

    with open("data.json", "r+") as f:
        all_data = json.load(f)
        share_info, historical_data = get_historical_data(share_name)

        # linear_regression([item["date"] for item in historical_data], [item["close"] for item in historical_data])

        if (len(historical_data) != 0):
            all_data[share_name] = {
                "historicalData": historical_data,
                "fiftyTwoWeekLow": share_info["fiftyTwoWeekLow"],
                "fiftyTwoWeekHigh": share_info["fiftyTwoWeekHigh"],
                "fiftyDayAverage": share_info["fiftyDayAverage"],
                "twoHundredDayAverage": share_info["twoHundredDayAverage"],
                "52WeekChange": share_info["52WeekChange"],
                "shortName": share_info["shortName"],
                "totalRevenue": share_info["totalRevenue"],
                "totalDebt": share_info["totalDebt"],
                "totalCash": share_info["totalCash"],
                "grossProfits": share_info["grossProfits"],
                "industry": share_info["industry"],
                "marketCap": share_info["marketCap"],
            }

        f.seek(0)
        json.dump(all_data, f, indent=4)

        

     