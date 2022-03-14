import os
import json
import datetime

import yfinance as yf
import backtrader as bt

from backtest import EMAStrategy, RSIStrategy, CommInfoFractional, get_profit_percentage
from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)

def create_json(path):
    with open(f"{path}", "w+") as f:
        json.dump({}, f)

def file_exists(file, dir):
    return f"{file}" in return_all_files_in_dir(dir)

def return_all_files_in_dir(dir):
    return [f for f in os.listdir(f"{os.path.dirname(os.path.abspath(__file__))}\data\{dir}")]

def execute_strategy():
    pass

@app.route('/update', methods=['GET'])
def update():
    spy = yf.Ticker("SPY")
    hist = spy.history(period="max").filter(['Open', 'High', 'Low', 'Close', 'Volume'])
    hist = hist.rename(columns={"Open": "open", "High": "high", "Low": "low", "Close": "close", "Volume": "volume"})

@app.route('/rsi/', methods=['GET'])
def rsi():
    args = request.args.to_dict()
    rsi_window, rsi_sell, rsi_buy = int(args['rsiWindow']), int(args['rsiSell']), int(args['rsiBuy'])

    if file_exists(f'{rsi_window}{rsi_buy}{rsi_sell}.json', 'rsi'):
        with open(f'./data/rsi/{rsi_window}{rsi_buy}{rsi_sell}.json', 'r') as f:
            return json.load(f)
    else:
        with open(f'./data/rsi/{rsi_window}{rsi_buy}{rsi_sell}.json', 'w') as f:
            json.dump({ "data": {} }, f)

        cerebro = bt.Cerebro()
        feed = bt.feeds.YahooFinanceCSVData(dataname='./data/SPY.csv', fromdate=datetime.datetime(2010, 1, 29), todate=datetime.datetime(2022, 3, 7)) 
        cerebro.adddata(feed) 
        cerebro.addstrategy(RSIStrategy, rsi_window=rsi_window, rsi_buy=rsi_buy, rsi_sell=rsi_sell)
        cerebro.run()
    
        with open(f'./data/rsi/{rsi_window}{rsi_buy}{rsi_sell}.json', 'r') as f:
                return json.load(f)


@app.route('/ema/', methods=['GET'])
def ema():
    args = request.args.to_dict()
    low_ema, medium_ema, high_ema = args['lowEMA'], args['mediumEMA'], args['highEMA']

    data = {}
    with open("./data/SPY.json", "r") as f:
        data = json.load(f)

    cerebro = bt.Cerebro()
    data = bt.feeds.YahooFinanceCSVData(dataname='./data/SPY.csv', fromdate=datetime.datetime(2010, 1, 29), todate=datetime.datetime(2022, 3, 7)) 
    cerebro.adddata(data) 
    cerebro.addstrategy(EMAStrategy, low=low_ema, medium=medium_ema, high=high_ema)
    cerebro.broker.setcash(100000.0)
    cerebro.broker.addcommissioninfo(CommInfoFractional())
    cerebro.broker.setcommission(commission=0.001)
    cerebro.run()


@app.route('/get', methods=['GET'])
def get_data():
    with open('./data/SPY.json', 'r') as f:
        data = json.load(f)
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)