import pandas as pd 
import numpy as np
import math
import itertools
import json

import datetime as dt
import matplotlib.pyplot as plt

from RSI import RSI
from FI import FI
from ta import add_all_ta_features


class BackTest():
    def __init__(self, open, close, low, high, volume, ema50, ema200, MACD, equity):
        self._open = open
        self._close = close 
        self._low = low 
        self._high = high
        self._equity = equity
        self._volume = volume
        self._50_ema = ema50
        self._200_ema = ema200
        self._MACD = MACD
        self._signals = {}

    def _get_profit_percentage(self, investment_return, investment_value) -> float:
        """ Calculates profit percentage ((IR / IV) * 100)
        Args:
            investment_return (Float) : total return on investment
            investment_value (Float) : total spent purchasing investment
        """
        return math.floor((investment_return / investment_value) * 100)

    def rsi_all_combinations_by_signal_values(self, buy_low, buy_high, sell_low, sell_high, window=14) -> list:
        rsi_signal_values = np.array(np.meshgrid(np.array([_ for _ in range(buy_low, buy_high)]), np.array([_ for _ in range(sell_low, sell_high)]))).T.reshape(-1, 2)

        # This can be done by threading
        results = []
        for rsi_signal in rsi_signal_values[:1000]:
            rsi = RSI(self._close, window, rsi_signal[0], rsi_signal[1])
            rsi_total = rsi.base_strategy(self._equity)
            rsi_profit_percentage = self._get_profit_percentage(rsi_total, self._equity)
            results.append({"rsi_sell_signal": rsi_signal[0], "rsi_buy_signal": rsi_signal[1], "rsi_total": rsi_total, "rsi_profit_percentage": rsi_profit_percentage})
            
        results = sorted(results, key=lambda x: x["rsi_total"])
        print(results)
        return results

    def relative_strength_index(self, window, rsi_sell_signal=70, rsi_buy_signal=30) -> tuple:
        """ Calculates the Relative Strength Index (RSI) 
        Args: 
            window (Integer) : RSI window length
            rsi_sell_signal (Integer) : RSI value at which a stock is deemed overbought
            rsi_buy_signal (Integer) : RSI value at which a stock is deemed underbought
        Returns:
            rsi_total, rsi_profit_percentage (Float, Float)
        """
        rsi = RSI(self._close, window, rsi_sell_signal, rsi_buy_signal, self._200_ema)
        self._signals["rsi_signal"] = rsi.get_signals()
        
        rsi_total = rsi.base_strategy(self._equity, True) # 2nd arg = True for graph
        return rsi_total, self._get_profit_percentage(rsi_total, self._equity)

    def force_index_indicator(self, window=14):
        """ Calculates the Force Index Indicator (FI) 
        Args:
            window (Integer) : FI Window Length
        Returns:
            fi_total, fi_total_percentage (Float, Float)
        """
        fi = FI(self._close, self._volume, window)
        fi.base_strategy(self._equity, window)

    def dollar_cost_average(self, interval=7) -> tuple:
        """ Calculates the total profit generated via Dollar Cost Averaging
        Args:
            interval (Integer) : time interval of when to buy
            
        Returns:
            total_profit, total_profit_percentage (Float, Float)
        """
        #TODO: len_mod required for final few days of information
        len_windows, len_mod = math.floor(len(self._close.index) / interval), len(self._close.index) % interval 
        per_interval_dca = self._equity / len_windows

        total_profit = 0
        for i in range(len_windows):
            total_shares = per_interval_dca / self._close[interval * i]
            # Use latest close to find profit
            total_profit += (total_shares * self._close[-1]) - (total_shares * self._close[interval * i])

        return total_profit, self._get_profit_percentage(total_profit, self._equity)

    def buy_and_hold(self) -> tuple:
        """ Calculate profit generated from purchasing the selected item 
            at its first start date using the full equity amount
        Return:
            total, profit_percentage (Float, Float)
        """
        total_shares_purchased = self._equity / self._close[0]
        total = (total_shares_purchased * self._close[-1]) - (total_shares_purchased * self._close[0])
        profit_percentage = self._get_profit_percentage(total, self._equity)
        return total, profit_percentage

    def merge_data(self):
        df = pd.DataFrame(data=self._signals['rsi_signal'], index=None, columns=['rsi_signal'])
        print(df)
        return pd.concat([self._open, self._close, self._low, self._high, self._volume, self._50_ema, self._200_ema, self._MACD], join='inner', axis=1)


if __name__ == "__main__":
    # df = add_all_ta_features(df, open="open", high="high", low="low", close="close", volume="volume")
    # df = df.filter(['open', 'high', 'low', 'close', 'volume'])
    df = pd.read_csv("../data/csv/SPY.csv", delimiter=',', sep=r', ')
    df.set_index(["date"], inplace = True)
    df["50EMA"] = df['close'].ewm(span=50, adjust=False).mean()
    df["200EMA"] = df['close'].ewm(span=200, adjust=False).mean()
    df["MACD"] = (df["50EMA"] - df["200EMA"]).ewm(span=9, adjust=False).mean()

    bt = BackTest(df['open'], df['close'], df['low'], df['high'], df['volume'], df["50EMA"], df["200EMA"], df["MACD"], 100000)
    
    rsi_total, rsi_profit_percentage = bt.relative_strength_index(2)
    print("RSI Total / %: ", rsi_total, rsi_profit_percentage)

    bah_total, bah_profit_percentage = bt.buy_and_hold()
    print("Buy & Hold Total / %: ", bah_total, bah_profit_percentage)


    new_df = bt.merge_data()
    print(new_df)








    # for interval in [1, 7, 14, 30, 60, 120, 240, 365]:
    #         dca_total, dca_profit_percentage = bt.dollar_cost_average(interval=interval)
    #         rsi_total, rsi_total_percentage = bt.relative_strength_index(window=interval)
    #         print(f"Relative String Index Total, Profit Percentage", rsi_total, rsi_total_percentage)
    #         print(f"Dollar Cost Average {interval}D Total, Profit Percentage:", dca_total, dca_profit_percentage)

    # backtest all combinations of sell/buy values
    # bt.rsi_all_combinations_by_signal_values(45, 48, 62, 65)

