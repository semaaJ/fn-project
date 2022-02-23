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

@app.route('/share/<string:ticker>', methods = ['GET'])
def share_data(ticker):
    if (f"{ticker}.json" not in os.listdir(f"{os.path.dirname(os.path.abspath(__file__))}\data")):
        with open(f"data/{ticker}.json", "w+") as f:
            json.dump({}, f)
    
    with open(f"data/{ticker}.json", "r+") as f:
        all_data = json.load(f)
        share_info, historical_data = get_historical_data(ticker)

        if (len(historical_data) != 0):
            if ("sector" in share_info):
                all_data = {
                    "zip": share_info["zip"],
                    "city": share_info["city"],
                    "state": share_info["state"],
                    "country": share_info["country"],
                    "website": share_info["website"],
                    "industry": share_info["industry"],
                    "sector": share_info["sector"],
                    "shortName": share_info["shortName"],
                    "fullTimeEmployees": share_info["fullTimeEmployees"],
                    "longBusinessSummary": share_info["longBusinessSummary"],
                    "shortName": share_info["shortName"],

                    "profitMargins": share_info["profitMargins"],
                    "grossMargins": share_info["grossMargins"],
                    "totalRevenue": share_info["totalRevenue"],
                    "totalDebt": share_info["totalDebt"],
                    "totalCash": share_info["totalCash"],
                    "grossProfits": share_info["grossProfits"],
                    "marketCap": share_info["marketCap"],
                    "revenueGrowth": share_info["revenueGrowth"],
                    "operatingMargins": share_info["operatingMargins"],
                    "operatingCashflow": share_info["operatingCashflow"],
                    "targetLowPrice": share_info["targetLowPrice"],
                    "targetMedianPrice": share_info["targetMedianPrice"],
                    "targetMeanPrice": share_info["targetMeanPrice"],
                    "targetHighPrice": share_info["targetHighPrice"],
                    "recommendationKey": share_info["recommendationKey"],
                    "freeCashflow": share_info["freeCashflow"],
                    "returnOnAssets": share_info["returnOnAssets"],
                    "numberOfAnalystOpinions": share_info["numberOfAnalystOpinions"],
                    "totalCashPerShare": share_info["totalCashPerShare"],
                    "revenuePerShare": share_info["revenuePerShare"],
                    "bookValue": share_info["bookValue"],
                    "forwardPE": share_info["forwardPE"],
                   
                    "currentPrice": get_current_price(ticker),
                    "historicalData": historical_data,
                    "fiftyTwoWeekLow": share_info["fiftyTwoWeekLow"],
                    "fiftyTwoWeekHigh": share_info["fiftyTwoWeekHigh"],
                    "fiftyDayAverage": share_info["fiftyDayAverage"],
                    "twoHundredDayAverage": share_info["twoHundredDayAverage"],
                    "fiftyTwoWeekChange": share_info["52WeekChange"],
                }
            
            else:
                all_data = {
                    "shortName": share_info["shortName"],
                    "fiftyTwoWeekLow": share_info["fiftyTwoWeekLow"],
                    "fiftyTwoWeekHigh": share_info["fiftyTwoWeekHigh"],
                    "fiftyDayAverage": share_info["fiftyDayAverage"],
                    "twoHundredDayAverage": share_info["twoHundredDayAverage"],
                    "historicalData": historical_data,
                    "shareInfo": share_info
                }

            f.seek(0)
            json.dump(all_data, f, indent=4)
            return jsonify(all_data)
    
  
if __name__ == '__main__':
    app.run(debug = True)