import json
import yfinance as yf  
from pycoingecko import CoinGeckoAPI
from datetime import date, datetime

def get_historical_data(share_name):
    share = yf.Ticker(share_name)
    historical_data = share.history(period="max")

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

    return share.info, data

def get_current_price(symbol):
    ticker = yf.Ticker(symbol)
    todays_data = ticker.history(period='1d')
    return todays_data['Close'][0]

def from_epoch(epochtime):
    return datetime.fromtimestamp(epochtime / 1000)

def get_crypto_data(id):
    cg = CoinGeckoAPI()
    data = cg.get_coin_market_chart_by_id(id, 'usd', 'max')

    dates = [from_epoch(i[0]) for i in data["prices"]]
    prices = [i[1] for i in data["prices"]]
    total_volume = [i[1] for i in data["total_volumes"]]
    market_cap = [i[1] for i in data["market_caps"]]

    return [{"date": str(dates[i]), "price": prices[i], "volume": total_volume[i], "marketCap": market_cap[i]} for i in range(len(dates))]



    
   

