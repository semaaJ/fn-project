import math
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from ta import momentum

class RSI():
    def __init__(self, close, window, rsi_sell_signal, rsi_buy_signal, ema):
        self._close = close
        self._window = window
        self._rsi_df = None
        self._rsi_sell_signal = rsi_sell_signal
        self._rsi_buy_signal = rsi_buy_signal
        self._ema = ema
        self._run()

    def _run(self):
        self._rsi_df = momentum.RSIIndicator(close=self._close, window=self._window).rsi()

    def get_signals(self) -> list:
        """ Get buy/sell signals when RSI value is less/greater than the buy/sell values
        Returns:
            signals (list) : Array of buy/sell signals (1/-1)
        """
        signals = []
        for i, rsi in self._rsi_df.iteritems():
            if rsi <= self._rsi_buy_signal:
                signals.append(1)
            elif rsi >= self._rsi_sell_signal:
                signals.append(-1)
            else:
                signals.append(np.nan)
        return signals

    def base_strategy(self, equity, graph=False):
        """ Basic RSI strategy that goes long/short on long/short signals
        Args:
            equity (Float) : total amount of investment
        Returns:
            total_investment_ret (Float) : total return on investment
        """
        signal = 0
        buy_price, sell_price = [], []
        short_price, short_sell = [], []
        rsi_signal =  self.get_signals()

        prev = list(self._rsi_df)[0]
        merged = pd.merge(self._rsi_df, self._close, how='outer', on='date')

        for i, item in merged.iterrows():
            if prev > self._rsi_buy_signal and item['rsi'] < self._rsi_buy_signal:
                if signal != 1:
                    buy_price.append(item['close'])
                    short_sell.append(item['close'])
                    short_price.append(np.nan)
                    sell_price.append(np.nan)
                    signal = 1
                else:
                    buy_price.append(np.nan)
                    sell_price.append(np.nan)
                    short_price.append(np.nan)
                    short_sell.append(np.nan)
            elif prev < self._rsi_sell_signal and item['rsi'] > self._rsi_sell_signal:
                if signal != -1:
                    buy_price.append(np.nan)
                    sell_price.append(item['close'])
                    short_price.append(np.nan)
                    short_sell.append(item['close'])
                    signal = -1
                else:
                    buy_price.append(np.nan)
                    sell_price.append(np.nan)
                    short_price.append(np.nan)
                    short_sell.append(np.nan)
            else:
                buy_price.append(np.nan)
                sell_price.append(np.nan)
                short_price.append(np.nan)
                short_sell.append(np.nan)

            prev = item['rsi']



        # 0 is signal is buy, 
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
           self.display_graph_with_signals(buy_price, sell_price)

        return total_investment_ret

    def base_graph(self):
        """ Plots close & RSI graphs """
        fig, axs = plt.subplots(2)
        axs[0].plot([_ for _ in range(len(self._close))], list(self._close))
        axs[1].plot([_ for _ in range(len(self._rsi_df))], list(self._rsi_df))
        plt.show()

    def display_graph_with_signals(self, buy_price, sell_price):
        ax1 = plt.subplot2grid((10,1), (0,0), rowspan = 4, colspan = 1)
        ax2 = plt.subplot2grid((10,1), (5,0), rowspan = 4, colspan = 1)
        
        ax1.plot(self._close.values, linewidth=2.5, color='skyblue', label='item')
        ax1.plot([i for i in range(len(self._close.index))], buy_price, marker='^', markersize=10, color='green', label='BUY SIGNAL')
        ax1.plot([i for i in range(len(self._close.index))], sell_price, marker='v', markersize=10, color='r', label='SELL SIGNAL')
        
        ax2.plot(self._rsi_df.values, color='orange', linewidth=2.5)
        ax2.axhline(30, linestyle='--', linewidth=1.5, color='grey')
        ax2.axhline(70, linestyle='--', linewidth=1.5, color='grey')
        plt.show()