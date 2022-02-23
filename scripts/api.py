import json
import os

from flask import Flask, jsonify, request
from utils import  get_current_price, get_historical_data, get_crypto_data
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)


def file_exists(file, dir):
    return f"{file}.json" in os.listdir(f"{os.path.dirname(os.path.abspath(__file__))}\data\{dir}")

def return_all_files_in_dir(dir):
    return [f for f in os.listdir(f"{os.path.dirname(os.path.abspath(__file__))}\data\{dir}")]
  
@app.route('/cache', methods=['GET'])
def get_cached_data():
    data = {"equities": {}, "crypto": {}}
    for f in return_all_files_in_dir("share"):
        with open(f"data/share/{f}", "r") as fil:
            data["equities"][f.split(".")[0]] = json.load(fil)

    for f in return_all_files_in_dir("crypto"):
        print("filename", f)
        with open(f"data/crypto/{f}", "r") as fil:
            data["crypto"][f.split(".")[0]] = json.load(fil)

    return jsonify(data)

@app.route('/share/<string:ticker>', methods=['GET'])
def share_data(ticker):
    if (not file_exists(ticker, "share")):
        with open(f"data/share/{ticker}.json", "w+") as f:
            json.dump({}, f)
    
    with open(f"data/share/{ticker}.json", "r+") as f:
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
    
@app.route('/crypto/<string:id>', methods=['GET'])
def crypto_data(id):
    if (not file_exists(id, "crypto")):
        with open(f"data/crypto/{id}.json", "w+") as f:
            json.dump({}, f)

    data = get_crypto_data(id)
    with open(f"data/crypto/{id}.json", "r+") as f:
        json.dump({ "historicalData": data }, f, indent=4)
        return jsonify({ id: {
            "historicalData": data
        } })

    



if __name__ == '__main__':
    app.run(debug = True)