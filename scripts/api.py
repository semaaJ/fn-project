import os
import json
import datetime
import pandas as pd

from binance import Client
from ta import momentum, trend, volume
from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)

API_KEY = ''
API_SECRET = ''
client = Client(API_KEY, API_SECRET)

def create_json(path):
    with open(f"{path}", "w+") as f:
        json.dump({}, f)

def file_exists(file, dir):
    return f"{file}" in return_all_files_in_dir(dir)

def return_all_files_in_dir(dir):
    return [f for f in os.listdir(f"{os.path.dirname(os.path.abspath(__file__))}\data\{dir}")]

@app.route('/close', methods=['GET'])
def close():
    args = request.args.to_dict()
    tradeId, sell_price = args["tradeId"], float(args["current"])

    with open('./data/portfolio.json', "r+") as f:
            portfolio = json.load(f)

            trade = portfolio['openTrades'][tradeId] 
            trade['sellPrice'] = sell_price
            if trade['orderType'] == 'buy':
                trade['profitLoss'] = (sell_price * trade["amount"]) - (trade["buyPrice"] * trade["amount"])
            else:
                trade['profitLoss'] = (trade["buyPrice"] * trade["amount"]) - (sell_price * trade["amount"])

            del portfolio['openTrades'][tradeId] 
            portfolio['closedTrades'][tradeId] = trade
            portfolio['equity'] += (sell_price * trade["amount"])

            f.seek(0)
            f.truncate()
            json.dump(portfolio, f, indent=4)

            return {}

@app.route('/order', methods=['GET'])
def order():
    args = request.args.to_dict()
    order_type, amount, buy_price = args['orderType'], float(args['amount']), float(args['buyPrice'])

    if all([order_type, amount, buy_price]):
        with open('./data/portfolio.json', "r+") as f:
            portfolio = json.load(f)

            portfolio['openTrades'][portfolio['tradeId']] = { "orderType": order_type, "amount": amount, "buyPrice": buy_price }
            portfolio['tradeId'] += 1
            portfolio['equity'] -= amount * buy_price

            f.seek(0)
            f.truncate()
            json.dump(portfolio, f, indent=4)

            return {}
    
    return {}


@app.route('/current', methods=['GET'])
def current():
    price = client.get_symbol_ticker(symbol="BTCUSDT")
    return jsonify(price)

@app.route('/cache', methods=['GET'])
def cache():
    btc_history = []
    portfolio = []

    with open('./data/BTC.json', 'r') as f:
        btc_history = json.load(f)

    with open('./data/portfolio.json', 'r') as f:
        portfolio = json.load(f)

    return jsonify({ "history": btc_history, "portfolio": portfolio})


@app.route('/update', methods=['GET'])
def update():    
    # date, open, high, low, close, volume
    klines = client.get_historical_klines("BTCUSDT", Client.KLINE_INTERVAL_1MINUTE, "23 Mar, 2022", "30 Mar, 2022")

    date, op, high, low, close, vol = [], [], [], [], [], []
    for item in klines:
        date.append(item[0])
        op.append(float(item[1]))
        high.append(float(item[2]))
        low.append(float(item[3]))
        close.append(float(item[4]))
        vol.append(float(item[5]))

    results = pd.DataFrame({ "date": date, "open": op, "high": high, "low": low, "close": close, "volume": vol })
    
    results["date"] = pd.to_datetime(results["date"], unit='ms').apply(lambda x: str(x))
    results["ema7"] = trend.EMAIndicator(close=results['close'], window=7).ema_indicator()
    results["ema25"] = trend.EMAIndicator(close=results['close'], window=25).ema_indicator()
    results["ema99"] = trend.EMAIndicator(close=results['close'], window=99).ema_indicator()
    results["mfi"] = volume.MFIIndicator(close=results['close'], high=results['high'], low=results['low'], volume=results['volume'], window=14).money_flow_index()
    results["rsi14"] = momentum.RSIIndicator(close=results['close'], window=14).rsi()

    results = results.dropna()
    results = results.to_dict()
    results = { k: list(results[k].values()) for k in results }

    with open('./data/BTC.json', 'w+') as f:
        f.seek(0)
        f.truncate()
        json.dump(results, f)

    return jsonify(results)


if __name__ == '__main__':
    app.run(debug=True)