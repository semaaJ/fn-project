import pandas as pd 
import numpy as np
import math
import itertools

from ta import volume, momentum, add_all_ta_features

import matplotlib.pyplot as plt

WINDOW = 13

def line_of_best_fit(x, y):
    a, b = np.polyfit(x, y, 1)
    return [a * i + b for i in x]

def force_index_indicator(df):
    df['fi'] = volume.ForceIndexIndicator(close=df['close'], volume=df['volume'], window=WINDOW).force_index()

    # Index at which we want data to begin
    n = len(df.index)
    window_sections = math.ceil(n / WINDOW)
    dates = [_ for _ in range(len(df.index))]

    # Split data into n sections
    split_date = np.array_split(dates, window_sections)
    split_close = np.array_split(list(df['close']), window_sections)
    split_fi = np.array_split(list(df['fi']), window_sections)

    # Rejoin data into one arr
    close_lobf = [[*line_of_best_fit(item, split_close[i])] for i, item in enumerate(split_date)]
    close_fi = [[*line_of_best_fit(item, split_fi[i])] for i, item in enumerate(split_date)]

    # Get sliding slopes
    close_lobf_slope = [np.polyfit(split_date[i], close_lobf[i], 1)[0] for i in range(len(split_date))]
    close_fi_slope = [np.polyfit(split_date[i], close_fi[i], 1)[0] for i in range(len(split_date))]

    # for i in range(len(close_lobf_slope)):
    #     if close_lobf_slope[i] < 0 and close_fi_slope[i] > 0:
    #         print(close_lobf_slope[i], close_fi_slope[i], "BULLISH")
    #     elif close_lobf_slope[i] > 0 and close_fi_slope[i] < 0:
    #         print(close_lobf_slope[i], close_fi_slope[i], "BEARISH")

    fig, axs = plt.subplots(2)
    axs[0].plot(dates, list(df['close']))
    axs[0].plot(dates, np.concatenate(close_lobf))


    axs[1].plot(dates, list(df['fi']))
    axs[1].plot(dates, np.concatenate(close_fi))
    axs[1].axhline(y=0)

    plt.show()



class RSI():
    def __init__(self, close, window):
        self._close = close
        self._window = window
        self._rsi_df = None
        self._run()

    def _run(self):
        self._rsi_df = momentum.RSIIndicator(close=self._close, window=self._window).rsi()

    def base_rsi_strategy(self):
        buy_price = []
        sell_price = []
        rsi_signal = []
        signal = 0

        prev = list(self._rsi_df)[0]
        merged = pd.merge(self._rsi_df, self._close, how='outer', on='date')

        for i, item in merged.iterrows():
            if prev > 30 and item['rsi'] < 30:
                if signal != 1:
                    buy_price.append(item['close'])
                    sell_price.append(np.nan)
                    signal = 1
                    rsi_signal.append(signal)
                else:
                    buy_price.append(np.nan)
                    sell_price.append(np.nan)
                    rsi_signal.append(0)
            
            elif prev < 70 and item['rsi'] > 70:
                if signal != -1:
                    buy_price.append(np.nan)
                    sell_price.append(item['close'])
                    signal = -1
                    rsi_signal.append(signal)
                else:
                    buy_price.append(np.nan)
                    sell_price.append(np.nan)
                    rsi_signal.append(0)

            else:
                buy_price.append(np.nan)
                sell_price.append(np.nan)
                rsi_signal.append(0)

            prev = item['rsi']

        position = []
        for i in range(len(rsi_signal)):
            if rsi_signal[i] > 1:
                position.append(0)
            else:
                position.append(1)

        for i in range(len(self._close.index)):
            if rsi_signal[i] == 1:
                position[i] = 1
            elif rsi_signal[i] == -1:
                position[i] = 0
            else:
                position[i] = position[i - 1]

        rsi_signal = pd.DataFrame(rsi_signal).rename(columns={0: 'rsi_signal'}).set_index(self._close.index)
        position = pd.DataFrame(position).rename(columns={0: 'rsi_position'}).set_index(self._close.index)

        strat = pd.concat([self._close, self._rsi_df, rsi_signal, position], join='inner', axis=1).dropna()

        returns = pd.DataFrame(np.diff([self._close.values])).rename(columns={0: 'returns'})
        rsi_strategy_ret = []

        print("RETURNS", returns)

        for i in range(len(returns)):
            ret = returns['returns'][i] * strat['rsi_position'][i]
            rsi_strategy_ret.append(ret)

        print("rsi strat ret", rsi_strategy_ret)
        
        rsi_strategy_ret_df = pd.DataFrame(rsi_strategy_ret).rename(columns={0: 'rsi_returns'})
        investment_value = 100000
        number_of_stocks = math.floor(investment_value / self._close.values[-1])
        rsi_investment_ret = []

        for i in range(len(rsi_strategy_ret_df['rsi_returns'])):
            returns = number_of_stocks * rsi_strategy_ret_df['rsi_returns'][i]
            rsi_investment_ret.append(returns)

        print(rsi_investment_ret)

        rsi_investment_ret_df = pd.DataFrame(rsi_investment_ret).rename(columns={0: 'investment_returns'})
        total_investment_ret = round(sum(rsi_investment_ret_df['investment_returns']), 2)
        profit_percentage = math.floor((total_investment_ret / investment_value) * 100)

        print(f'Profit gained from RSI strategy {total_investment_ret}')
        print(f'Profit percentage gained from RSI strategy {profit_percentage}')


        ax1 = plt.subplot2grid((10,1), (0,0), rowspan = 4, colspan = 1)
        ax2 = plt.subplot2grid((10,1), (5,0), rowspan = 4, colspan = 1)
        
        ax1.plot(self._close.values, linewidth=2.5, color='skyblue', label='item')
        ax1.plot([i for i in range(len(self._close.index))], buy_price, marker='^', markersize=10, color='green', label='BUY SIGNAL')
        ax1.plot([i for i in range(len(self._close.index))], sell_price, marker='v', markersize=10, color='r', label='SELL SIGNAL')
        # ax1.set_title('item RSI TRADE SIGNALS')
        
        ax2.plot(self._rsi_df.values, color='orange', linewidth=2.5)
        ax2.axhline(30, linestyle='--', linewidth=1.5, color='grey')
        ax2.axhline(70, linestyle='--', linewidth=1.5, color='grey')
        plt.show()

        return buy_price, sell_price, rsi_signal


    def base_graph(self):
        fig, axs = plt.subplots(2)
        axs[0].plot([_ for _ in range(len(self._close))], list(self._close))
        axs[1].plot([_ for _ in range(len(self._rsi_df))], list(self._rsi_df))
        plt.show()



# FI
# df = df.filter(['open', 'high', 'low', 'close', 'volume'])
# force_index_indicator(df)

# df = add_all_ta_features(df, open="open", high="high", low="low", close="close", volume="volume")


df = pd.read_csv("data/csv/SPY.csv", delimiter=',', sep=r', ')
df.set_index(["date"], inplace = True)

rsi = RSI(df['close'], 7)
rsi.base_rsi_strategy()