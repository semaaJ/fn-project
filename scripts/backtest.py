import pandas as pd 
import numpy as np
import math
import itertools

import datetime as dt
import matplotlib.pyplot as plt

from ta import volume, momentum, add_all_ta_features


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


class BackTest():
    def __init__(self, open, close, low, high, equity):
        self._open = open
        self._close = close 
        self._low = low 
        self._high = high
        self._equity = equity

    def _get_profit_percentage(self, investment_return, investment_value) -> float:
        """ Calculates profit percentage ((IR / IV) * 100)
        Args:
            investment_return (Float) : total return on investment
            investment_value (Float) : total spent purchasing investment
        """
        return math.floor((investment_return / investment_value) * 100)

    def relative_strength_index(self, window, rsi_sell_signal=70, rsi_buy_signal=30) -> tuple:
        """ Calculates the Relative Strength Index (RSI) of a df
        Args: 
            window (Integer) : RSI window length
            rsi_sell_signal (Integer) : RSI value at which a stock is deemed overbought
            rsi_buy_signal (Integer) : RSI value at which a stock is deemed underbought

        Returns:
            rsi_total, rsi_profit_percentage (Float, Float)
        """
        rsi = RSI(self._close, window, rsi_sell_signal, rsi_buy_signal)
        rsi_total = rsi.base_rsi_strategy(self._equity) # 2nd arg = True for raph
        return rsi_total, self._get_profit_percentage(rsi_total, self._equity)

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


class RSI():
    def __init__(self, close, window, rsi_sell_signal, rsi_buy_signal):
        self._close = close
        self._window = window
        self._rsi_df = None
        self._rsi_sell_signal = rsi_sell_signal
        self._rsi_buy_signal = rsi_buy_signal
        self._run()

    def _run(self):
        self._rsi_df = momentum.RSIIndicator(close=self._close, window=self._window).rsi()

    def base_rsi_strategy(self, equity, graph=False):
        """ Basic RSI strategy that buys/sells on buy/sell signals
        Args:
            equity (Float) : total amount of investment
        Returns:
            total_investment_ret (Float) : total return on investment
        """
        signal = 0
        buy_price, sell_price, rsi_signal = [], [], []

        prev = list(self._rsi_df)[0]
        merged = pd.merge(self._rsi_df, self._close, how='outer', on='date')

        for i, item in merged.iterrows():
            if prev > self._rsi_buy_signal and item['rsi'] < self._rsi_buy_signal:
                if signal != 1:
                    buy_price.append(item['close'])
                    sell_price.append(np.nan)
                    signal = 1
                    rsi_signal.append(signal)
                else:
                    buy_price.append(np.nan)
                    sell_price.append(np.nan)
                    rsi_signal.append(0)
            elif prev < self._rsi_sell_signal and item['rsi'] > self._rsi_sell_signal:
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

        # Set positions using RSI signals
        position = [0 if rsi_signal[i] > 0 else 1 for i in range(len(rsi_signal))]
        for i in range(len(rsi_signal)):
            if rsi_signal[i] == 1:
                position[i] = 1
            elif rsi_signal[i] == -1:
                position[i] = 0
            else:
                position[i] = position[i - 1]

        rsi_signal = pd.DataFrame(rsi_signal).rename(columns={0: 'rsi_signal'}).set_index(self._close.index)
        position = pd.DataFrame(position).rename(columns={0: 'rsi_position'}).set_index(self._close.index)

        strat = pd.concat([self._close, self._rsi_df, rsi_signal, position], join='inner', axis=1)
        returns = pd.DataFrame(np.diff(self._close.values)).rename(columns={0: 'returns'})

        rsi_strategy_ret = [returns['returns'][i] * strat['rsi_position'][i] for i in range(len(self._close) - 1)]
        rsi_strategy_ret_df = pd.DataFrame(rsi_strategy_ret).rename(columns={0: 'rsi_returns'})

        # number of stocks * rsi_returns
        rsi_investment_ret = [math.floor(equity / strat['close'][i]) * rsi_strategy_ret_df['rsi_returns'][i] 
            for i in range(len(rsi_strategy_ret_df['rsi_returns']))]

        rsi_investment_ret_df = pd.DataFrame(rsi_investment_ret).rename(columns={0: 'investment_returns'})
        total_investment_ret = round(sum(rsi_investment_ret_df['investment_returns']), 2)

        if (graph):
            ax1 = plt.subplot2grid((10,1), (0,0), rowspan = 4, colspan = 1)
            ax2 = plt.subplot2grid((10,1), (5,0), rowspan = 4, colspan = 1)
            
            ax1.plot(self._close.values, linewidth=2.5, color='skyblue', label='item')
            ax1.plot([i for i in range(len(self._close.index))], buy_price, marker='^', markersize=10, color='green', label='BUY SIGNAL')
            ax1.plot([i for i in range(len(self._close.index))], sell_price, marker='v', markersize=10, color='r', label='SELL SIGNAL')
            ax1.set_title(f'Profit gained from RSI strategy {total_investment_ret}')
            
            ax2.plot(self._rsi_df.values, color='orange', linewidth=2.5)
            ax2.axhline(30, linestyle='--', linewidth=1.5, color='grey')
            ax2.axhline(70, linestyle='--', linewidth=1.5, color='grey')
            plt.show()

        return total_investment_ret

    def base_graph(self):
        """ Plots close & RSI graphs """
        fig, axs = plt.subplots(2)
        axs[0].plot([_ for _ in range(len(self._close))], list(self._close))
        axs[1].plot([_ for _ in range(len(self._rsi_df))], list(self._rsi_df))
        plt.show()



if __name__ == "__main__":
    # df = add_all_ta_features(df, open="open", high="high", low="low", close="close", volume="volume")
    # df = df.filter(['open', 'high', 'low', 'close', 'volume'])
    df = pd.read_csv("data/csv/SPY.csv", delimiter=',', sep=r', ')
    df.set_index(["date"], inplace = True)

    bt = BackTest(df['open'], df['close'], df['low'], df['high'], 100000)
    # rsi_total, rsi_profit_percentage = bt.relative_strength_index(14)
    # print(rsi_total, rsi_profit_percentage)

    bah_total, bah_profit_percentage = bt.buy_and_hold()

    for interval in [1, 7, 14, 30, 60, 120, 240, 365]:
            dca_total, dca_profit_percentage = bt.dollar_cost_average(interval=interval)
            rsi_total, rsi_total_percentage = bt.relative_strength_index(window=interval)
            print(f"Relative String Index Total, Profit Percentage", rsi_total, rsi_total_percentage)
            print(f"Dollar Cost Average {interval}D Total, Profit Percentage:", dca_total, dca_profit_percentage)


    print("Buy & Hold Total, Profit Percentage:", bah_total, bah_profit_percentage)
