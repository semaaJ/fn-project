import sys
import yfinance as yf  
import json
import math
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression
import datetime as dt
from datetime import date

import matplotlib.pyplot as plt
from sklearn import preprocessing, svm
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression


def linear_regression(date_list, close_list):

    x = np.array([i for i in range(len(date_list))]).reshape(-1, 1)
    y = np.array(close_list).reshape(-1, 1)

    print("len X", len(x))
    print("len Y", len(y))
    
    # x.reshape(len(x), 1)
    # y.reshape(len(y), 1)

    print("X:", x[0:10])
    print("Y:", y[0:10])

    linreg = LinearRegression().fit(x, y)

    lr_score = linreg.score(x, y)
    print("Score:", lr_score)

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


def import_json(json_path):
    """Loads data from a JSON file into a readable JSON object.
    Args: 
        json_path (JSON): A JSON file containing key point information.
    
    Returns:
        jump_height (Int): The height the user has jumped in centimeters.
    """
    with open(json_path, "r") as f:
        json_data = json.load(f)

    return json_data


# share_info, historical_data = get_historical_data(sys.argv[1])

def display_graph(dists):

    # Colouring lines 
    plt.plot(dists, color = 'magenta')
    # plt.plot(dists2, color = 'green')

    # #plt.savefig(save_path + "/{}.png".format(ref_code))
    # green = mpatches.Patch(color='green', label='leg angles')
    # magenta = mpatches.Patch(color='magenta', label='Spine angles')
    # plt.legend(handles=[green, magenta], bbox_to_anchor=(1, 1), loc='upper left', borderaxespad=0)
    plt.show()
    plt.close()


def utils_main():

    data = import_json("data/AMD.json")

    historical_data = data["historicalData"]
    date_list = []
    close_list = []
    for day in historical_data:
        date_list.append(day["date"])
        close_list.append(day["close"])

    # display_graph(close_list)

    linear_regression(date_list, close_list)

if __name__ == "__main__":
    utils_main()