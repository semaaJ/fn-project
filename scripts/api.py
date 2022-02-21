import json

from flask import Flask, jsonify, request
from utils import  get_current_price, get_historical_data
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)
  
@app.route('/cache', methods=['GET'])
def get_cached_data():
    with open("data.json", "r") as f:
        all_data = json.load(f)
        return jsonify({
            'data': all_data
        })

@app.route('/<string:ticker>', methods = ['GET'])
def share_data(ticker):
     with open("data.json", "r+") as f:
        all_data = json.load(f)
        share_info, historical_data = get_historical_data(ticker)

        if (len(historical_data) != 0):
            all_data[ticker] = {
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

        f.seek(0)
        json.dump(all_data, f, indent=4)

        return jsonify({
            'data': all_data[ticker]
        })
  
  
if __name__ == '__main__':
    app.run(debug = True)