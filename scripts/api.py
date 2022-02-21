import json
import os

from flask import Flask, jsonify, request
from utils import  get_current_price, get_historical_data
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)
  
@app.route('/cache', methods=['GET'])
def get_cached_data():
    data = {}
    for f in os.listdir(f"{os.path.dirname(os.path.abspath(__file__))}\data"):
        with open(f"data/{f}", "r") as fil:
            data[f.split(".")[0]] = json.load(fil)

    return jsonify(data)

@app.route('/<string:ticker>', methods = ['GET'])
def share_data(ticker):
    if (f"{ticker}.json" not in os.listdir(f"{os.path.dirname(os.path.abspath(__file__))}\data")):
        with open(f"data/{ticker}.json", "w+") as f:
            json.dump({}, f, indent=4)
    
    with open(f"data/{ticker}.json", "r+") as f:
        all_data = json.load(f)
        share_info, historical_data = get_historical_data(ticker)

        if (len(historical_data) != 0):
            if ("sector" in share_info):
                all_data = {
                    "currentPrice": get_current_price(ticker),
                    "historicalData": historical_data,
                    "fiftyTwoWeekLow": share_info["fiftyTwoWeekLow"],
                    "fiftyTwoWeekHigh": share_info["fiftyTwoWeekHigh"],
                    "fiftyDayAverage": share_info["fiftyDayAverage"],
                    "twoHundredDayAverage": share_info["twoHundredDayAverage"],
                    "fiftyTwoWeekChange": share_info["52WeekChange"],
                    "shortName": share_info["shortName"],
                    "totalRevenue": share_info["totalRevenue"],
                    "totalDebt": share_info["totalDebt"],
                    "totalCash": share_info["totalCash"],
                    "grossProfits": share_info["grossProfits"],
                    "industry": share_info["industry"],
                    "marketCap": share_info["marketCap"],
                }
            
            else:
                all_data = {
                    "shortName": share_info["shortName"],
                    "fiftyTwoWeekLow": share_info["fiftyTwoWeekLow"],
                    "fiftyTwoWeekHigh": share_info["fiftyTwoWeekHigh"],
                    "fiftyDayAverage": share_info["fiftyDayAverage"],
                    "twoHundredDayAverage": share_info["twoHundredDayAverage"],
                    "historicalData": historical_data
                }

            f.seek(0)
            json.dump(all_data, f, indent=4)
            return jsonify(all_data)
    
  
if __name__ == '__main__':
    app.run(debug = True)