import json
import os

from flask import Flask, jsonify, request
from data_collection import get_current_price, get_historical_data, get_crypto_data, get_google_trends
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)

CRYPTOS = ['bitcoin', 'cardano', 'chainlink', 'cosmos', 'ethereum', 'litecoin', 'stellar', 'vechain', 'algorand', 'ripple']
EQUITIES = ['AMD', 'BRK-A', 'BRK-B', 'FB', 'GE', 'GOOG', 'JPM', 'PYPL', 'SPY', 'TSM'] 

def create_json(path):
    with open(f"{path}", "w+") as f:
        json.dump({}, f)

def file_exists(file, dir):
    return f"{file}.json" in os.listdir(f"{os.path.dirname(os.path.abspath(__file__))}\data\{dir}")

def return_all_files_in_dir(dir):
    return [f for f in os.listdir(f"{os.path.dirname(os.path.abspath(__file__))}\data\{dir}")]

@app.route('/cache', methods=['GET'])
def get_cached_data():
    data = {"equities": {}, "crypto": {}, "trends": {}}
    for f in return_all_files_in_dir("share"):
        with open(f"data/share/{f}", "r") as fil:
            data["equities"][f.split(".")[0]] = json.load(fil)

    for f in return_all_files_in_dir("trends"):
        with open(f'data/trends/{f}', "r") as fil:
            data["trends"][f.split(".")[0]] = json.load(fil)

    for f in return_all_files_in_dir("crypto"):
        print("filename", f)
        with open(f"data/crypto/{f}", "r") as fil:
            data["crypto"][f.split(".")[0]] = json.load(fil)

    return jsonify(data)
    
@app.route('/update', methods=['GET'])
def update_data():
    data = { "crypto": {}, "equities": {}, "trends": {}}
    
    for crypto in CRYPTOS:
        print("CRYPTO", crypto)
        if (not file_exists(crypto, "crypto")):
            create_json(f'data/crypto/{crypto}.json')

        current_data, historical = get_crypto_data(crypto)
        historical_trend_data, related_topics, related_queries, country_trend = get_google_trends([crypto])
        
        with open(f"data/crypto/{crypto}.json", "r+") as f:
            f.seek(0)
            json.dump({ 
                "historicalData": historical,
                "currentPrice": current_data['usd'],
                "marketCap": current_data["usd_market_cap"],
                "24hVol": current_data["usd_24h_vol"],
                "24hChange": current_data["usd_24h_change"],
                "googleTrends": {
                    "historicalTrendData": historical_trend_data,
                    "relatedTopics": related_topics,
                    "relatedQueries": related_queries,
                    "trendByCountry": country_trend
                }  
            }, f, indent=4)

            data["crypto"][crypto] = {
                "historicalData": historical,
                "currentPrice": current_data['usd'],
                "marketCap": current_data["usd_market_cap"],
                "24hVol": current_data["usd_24h_vol"],
                "24hChange": current_data["usd_24h_change"],
                "googleTrends": {
                    "historicalTrendData": historical_trend_data,
                    "relatedTopics": related_topics,
                    "relatedQueries": related_queries,
                    "trendByCountry": country_trend
                }
            }  
    
    for equity in EQUITIES:
        print("EQUITY", equity)
        if (not file_exists(equity, "share")):
            create_json(f'data/share/{equity}.json')
        with open(f"data/share/{equity}.json", "r+") as f:
            all_data = json.load(f)
            share_info, historical_data = get_historical_data(equity)
            historical_trend_data, related_topics, related_queries, country_trend = get_google_trends([equity])

            if (len(historical_data) != 0):
                if ("sector" in share_info):
                    all_data = {
                         "googleTrends": {
                            "historicalTrendData": historical_trend_data,
                            "relatedTopics": related_topics,
                            "relatedQueries": related_queries,
                            "trendByCountry": country_trend
                        },
                        "zip": share_info["zip"],
                        "city": share_info["city"],
                        "country": share_info["country"],
                        "website": share_info["website"],
                        "industry": share_info["industry"],
                        "sector": share_info["sector"],
                        "shortName": share_info["shortName"],
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
                    
                        "currentPrice": get_current_price(equity),
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
                        "shareInfo": share_info,
                        "googleTrends": {
                            "historicalTrendData": historical_trend_data,
                            "relatedTopics": related_topics,
                            "relatedQueries": related_queries,
                            "trendByCountry": country_trend
                        },
                    }

                f.seek(0)
                json.dump(all_data, f, indent=4)
                data["equities"][equity] = all_data

    return jsonify(data)


if __name__ == '__main__':
    app.run(debug=True)