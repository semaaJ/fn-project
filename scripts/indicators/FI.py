import math
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from ta import volume


def line_of_best_fit(x, y):
    a, b = np.polyfit(x, y, 1)
    return [a * i + b for i in x]

class FI():
    def __init__(self, close, volume, window):
        self._close = close
        self._volume = volume
        self._window = window
        self._fi_df = None
        self._run()

    def _run(self):
        self._fi_df = volume.ForceIndexIndicator(close=self._close, volume=self._volume, window=self._window).force_index()

    def get_signal_df(self):
        merged = pd.merge(self._fi_df, self._close, how='outer', on='date')

        signal = 0
        fi_signal = []

        for i, item in merged.iterrows():
            if item['close'] > prev_close and prev_fi < 0 and item[f'fi_{self._window}'] > 0:
                if signal != 1:
                    signal = 1
                    fi_signal.append(signal)
                else:
                    fi_signal.append(0)

            # If close is less than previous close, and fi is negative
            elif item['close'] < prev_close and item[f'fi_{self._window}'] < 0:
                if signal != -1:
                    signal = -1
                    fi_signal.append(signal)
                else:
                    fi_signal.append(0)
            else:
                fi_signal.append(0)

            prev_close = item['close']
            prev_fi = item[f'fi_{self._window}']


    def base_strategy(self, equity, graph=False):
        merged = pd.merge(self._fi_df, self._close, how='outer', on='date')

        signal = 0
        buy_price, sell_price, fi_signal = [], [], []

        prev_close = list(self._close)[0]
        prev_fi = list(self._fi_df)[0]
        for i, item in merged.iterrows():
            if item['close'] > prev_close and prev_fi < 0 and item[f'fi_{self._window}'] > 0:
                if signal != 1:
                    buy_price.append(item['close'])
                    sell_price.append(np.nan)
                    signal = 1
                    fi_signal.append(signal)
                else:
                    buy_price.append(np.nan)
                    sell_price.append(np.nan)
                    fi_signal.append(0)

            # If close is less than previous close, and fi is negative
            elif item['close'] < prev_close and item[f'fi_{self._window}'] < 0:
                if signal != -1:
                    buy_price.append(np.nan)
                    sell_price.append(item['close'])
                    signal = -1
                    fi_signal.append(signal)
                else:
                    buy_price.append(np.nan)
                    sell_price.append(np.nan)
                    fi_signal.append(0)
            else:
                buy_price.append(np.nan)
                sell_price.append(np.nan)
                fi_signal.append(0)

            prev_close = item['close']
            prev_fi = item[f'fi_{self._window}']

        # Set positions using FI signals
        position = [0 if fi_signal[i] > 0 else 1 for i in range(len(fi_signal))]
        for i in range(len(fi_signal)):
            if fi_signal[i] == 1:
                position[i] = 1
            elif fi_signal[i] == -1:
                position[i] = 0
            else:
                position[i] = position[i - 1]
        
        fi_signal = pd.DataFrame(fi_signal).rename(columns={0: 'fi_signal'}).set_index(self._close.index)
        position = pd.DataFrame(position).rename(columns={0: 'fi_position'}).set_index(self._close.index)

        strat = pd.concat([self._close, self._fi_df, fi_signal, position], join='inner', axis=1)
        returns = pd.DataFrame(np.diff(self._close.values)).rename(columns={0: 'returns'})

        fi_strategy_ret = [returns['returns'][i] * strat['fi_position'][i] for i in range(len(self._close) - 1)]
        fi_strategy_ret_df = pd.DataFrame(fi_strategy_ret).rename(columns={0: 'fi_returns'})

        # number of stocks * fi_returns
        rsi_investment_ret = [math.floor(equity / strat['close'][i]) * fi_strategy_ret_df['fi_returns'][i] 
            for i in range(len(fi_strategy_ret_df['fi_returns']))]

        rsi_investment_ret_df = pd.DataFrame(rsi_investment_ret).rename(columns={0: 'investment_returns'})
        total_investment_ret = round(sum(rsi_investment_ret_df['investment_returns']), 2)

        if (graph):
            self.display_graph_with_signals(buy_price, sell_price, total_investment_ret)

        print("TOTAL RETURN", total_investment_ret)
        return total_investment_ret 

    def display_graph_with_signals(self, buy_price, sell_price, total_investment_ret):
        # window_sections = math.ceil(len(self._close.index) / 14)
        # dates = [_ for _ in range(len(self._close.index))]

        # # Split data into n sections
        # split_date = np.array_split(dates, window_sections)
        # split_close = np.array_split(list(self._close), window_sections)
        # split_fi = np.array_split(list(self._fi_df), window_sections)

        # # Rejoin data into one arr
        # close_lobf = [[*line_of_best_fit(item, split_close[i])] for i, item in enumerate(split_date)]
        # close_fi = [[*line_of_best_fit(item, split_fi[i])] for i, item in enumerate(split_date)]

        ax1 = plt.subplot2grid((10,1), (0,0), rowspan = 4, colspan = 1)
        ax2 = plt.subplot2grid((10,1), (5,0), rowspan = 4, colspan = 1)
        
        ax1.plot(self._close.values, linewidth=2.5, color='skyblue', label='item')
        ax1.plot([i for i in range(len(self._close.index))], buy_price, marker='^', markersize=10, color='green', label='BUY SIGNAL')
        ax1.plot([i for i in range(len(self._close.index))], sell_price, marker='v', markersize=10, color='r', label='SELL SIGNAL')
        ax1.set_title(f'Profit gained from FI strategy {total_investment_ret}')
        
        ax2.plot(self._fi_df.values, color='orange', linewidth=2.5)
        plt.show()