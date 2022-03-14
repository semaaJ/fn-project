import math
import json
import argparse
import datetime
import itertools

import backtrader as bt

def get_profit_percentage(investment_return, investment_value) -> float:
    """ Calculates profit percentage ((IR / IV) * 100)
    Args:
        investment_return (Float) : total return on investment
        investment_value (Float) : total spent purchasing investment
    """
    return math.floor((investment_return / investment_value) * 100)

def slope(x1, y1, x2, y2):
    return (y2 - y1) / (x2 - x1)

class CommInfoFractional(bt.CommissionInfo):
    def getsize(self, price, cash):
        '''Returns fractional size for cash operation @price'''
        return self.params.leverage * (cash / price)


class BuyAndHold(bt.Strategy):
    def start(self):
        self._val_start = self.broker.get_cash()
    
    def nextstart(self):
        self.order_target_percent(target=1)

    def stop(self):
        self.roi = (self.broker.get_value() / self._val_start) - 1.0
        print(f'ROI: {100.0 * self.roi:2f}')


class DollarCostAverage(bt.Strategy):
    params = dict(
        monthly=True,           # False when weekly
        contribution=1000.0,
    )

    def log(self, txt, dt=None):
        dt = dt or self.datas[0].datetime.date(0)
        print(f'{dt.isoformat()} {txt}')

    def __init__(self):
        self.cash_start = self.broker.get_cash()
        self.val_start = 100.0

        if self.params.monthly:
            self.add_timer(bt.timer.SESSION_END, monthdays=[1], monthCarry=True)
        else:
            self.add_timer(bt.timer.SESSION_END, weekdays=[1], weekcarry=True)

    def notify_timer(self, timer, when, *args, **kwargs):
        self.broker.add_cash(self.params.contribution)
        self.order_target_percent(target=1) # fractional

    def stop(self):
        self.roi = (self.broker.get_value() / self.val_start) - 1.0
        print(f'ROI: {100.0 * self.roi:2f}')


class EMAStrategy(bt.Strategy):
    params = dict(
        low=7,
        medium=25,
        high=99,
        rsi_window=30
    )

    def log(self, txt, dt=None):
        dt = dt or self.datas[0].datetime.date(0)
        # print(f'{dt.isoformat()} {txt}')

    def __init__(self):
        self.dataclose = self.datas[0].close
        self._low_ema = bt.indicators.EMA(self.dataclose, period=self.params.low)
        self._medium_ema = bt.indicators.EMA(self.dataclose, period=self.params.medium)
        self._high_ema = bt.indicators.EMA(self.dataclose, period=self.params.high)
        self._rsi = bt.indicators.RSI(self.dataclose, period=self.params.rsi_window)
        self.requires_update = True

    def next(self):
        if self.requires_update:
            self._update(self._low_ema, self._medium_ema, self._high_ema, self._rsi)
        
    def _update(self, low_ema, medium_ema, high_ema, rsi):
        with open("./data/SPY.json", "r+") as f:
            data = json.load(f)
            # Not writing to json correctly
            data["data"]["ema"] = {
                    "lowEMA": list(low_ema),
                    "mediumEMA": list(medium_ema),
                    "highEMA": list(high_ema),
            }

            data['data']['open'] = list(self.datas[0].open)
            data['data']['close'] = list(self.datas[0].close)
            data['data']['low'] = list(self.datas[0].low)
            data['data']['high'] = list(self.datas[0].high)

            f.seek(0)
            f.truncate()
            json.dump(data, f, indent=4)

        self.requires_update = False

class RSIStrategy(bt.Strategy):
    params = dict(
        rsi_window=14,
        rsi_buy=30,
        rsi_sell=70
    ) 

    def __init__(self):
        self.dataclose = self.datas[0].close
        self.order = None
        
        self._rsi = bt.indicators.RSI(self.dataclose, period=self.params.rsi_window)
        self._rsi_ema = bt.indicators.RSI_EMA(self.dataclose, period=self.params.rsi_window)

        self._count = 0

        self._log = []
        self._portfolio_value = []
        self._portfolio_cash = []
        
        self.requires_update = True

    def log(self, txt, dt=None):
        dt = dt or self.datas[0].datetime.date(0)
        self._log.append(f'{dt.isoformat()} {txt}')
        # print(f'{dt.isoformat()} {txt}')   

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            return

        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(f'BUY EXECUTED, Price: {order.executed.price}, Cost: {order.executed.value}, Comm {order.executed.comm}')
            else: 
                self.log(f'SELL EXECUTED, Price: {order.executed.price}, Cost: {order.executed.value}, Comm {order.executed.comm}')
            self.bar_executed = len(self)
        
        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

        self.order = None

    def notify_trade(self, trade):
        if not trade.isclosed:
            return
        self.log(f'OPERATION: GROSS {trade.pnl}, NET {trade.pnlcomm}')
        
    def next(self):
        self._portfolio_value.append(self.broker.getvalue())
        self._portfolio_cash.append(self.broker.getcash())

        if self._count == 0 and self.requires_update:
              with open(f"./data/rsi/{self.params.rsi_window}{self.params.rsi_buy}{self.params.rsi_sell}.json", "r+") as f:
                data = json.load(f)
                data["data"].update({ 
                    "rsi": list(self._rsi),
                    "rsiEMA": list(self._rsi_ema),
                    "open": list(self.datas[0].open),
                    "close": list(self.datas[0].close),
                    "low": list(self.datas[0].low),
                    "high": list(self.datas[0].high),
                })
                f.seek(0)
                f.truncate()
                json.dump(data, f, indent=4)

        if self.requires_update and self.params.rsi_window + self._count ==  len(self.datas[0].close) - 1:
            self._update()

        self._count += 1

        if self.order:
            return

        rsi_sell_condition = self._rsi[0] >= self.params.rsi_sell
        rsi_buy_condition = self._rsi[0] <= self.params.rsi_buy

        if self.position:
            if rsi_buy_condition:
                self.log(f'SELL CREATE {self.dataclose[0]:2f}')
                self.order = self.close()
        else:
            if rsi_buy_condition:
                self.log(f'BUY CREATE {self.dataclose[0]:2f}')
                self.order = self.buy()
    
    def _update(self):
        with open(f"./data/rsi/{self.params.rsi_window}{self.params.rsi_buy}{self.params.rsi_sell}.json", "r+") as f:
            data = json.load(f)
            data["data"].update({
                "portfolioCash": self._portfolio_cash,
                "portfolioValue": self._portfolio_value,
                "profitPercentage": get_profit_percentage(self._portfolio_cash[-1], self._portfolio_cash[0]),
                "trades": self._log
            })

            f.seek(0)
            f.truncate()
            json.dump(data, f, indent=4)


class Strategy(bt.Strategy):
    params = dict(
        rsi_buy=30,
        rsi_sell=70,
        rsi_window=7,

        short_term_window=3,
        medium_term_window=7,
        long_term_window=21,

        monthly=True,                   # False when weekly
        contribution=False,
        contribution_amount=1000.0,
        stop_loss=0.5
    )

    def log(self, txt, dt=None):
        dt = dt or self.datas[0].datetime.date(0)
        print(f'{dt.isoformat()} {txt}')

    def __init__(self):
        self.dataclose = self.datas[0].close
            
        self.order = None

        self._rsi = bt.indicators.RSI(self.dataclose, period=self.params.rsi_window)
        self._rsi_ema = bt.indicators.RSI_EMA(self.dataclose, period=self.params.rsi_window)

        # used to indicate increasing/decreasing short-term momentum
        # distance between two lines gives an indiciator to momentum strength
        self._12_ema = bt.indicators.EMA(self.dataclose, period=12)
        self._26_ema = bt.indicators.EMA(self.dataclose, period=26)
        self._short_ema_crossover = bt.indicators.CrossOver(self._12_ema, self._26_ema)

        # used to indicate increasing/decreasing long-term momentum
        self._50_ema = bt.indicators.EMA(self.dataclose, period=50)
        self._200_ema = bt.indicators.EMA(self.dataclose, period=200)
        self._long_ema_crossover = bt.indicators.CrossOver(self._50_ema, self._200_ema)

        # MACD crossing above zero is considered bullish, while crossing below zero is bearish. 
        # Secondly, when MACD turns up from below zero it is considered bullish. 
        # When it turns down from above zero it is considered bearish.
        self._macd = bt.indicators.MACD(self._50_ema, self._200_ema)

        # Weekly/Monthly contributions
        if self.params.contribution:
            if self.params.monthly:
                self.add_timer(bt.timer.SESSION_END, monthdays=[1], monthCarry=True)
            else:
                self.add_timer(bt.timer.SESSION_END, weekdays=[1], weekcarry=True)

        self.tradeid = itertools.cycle([0, 1, 2])


    def notify_timer(self, timer, when, *args, **kwargs):
        self.broker.add_cash(self.params.contribution_amount)
        self.order_target_percent(target=1)

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            return

        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(f'BUY EXECUTED, Price: {order.executed.price}, Cost: {order.executed.value}, Comm {order.executed.comm}')
            else: 
                self.log(f'SELL EXECUTED, Price: {order.executed.price}, Cost: {order.executed.value}, Comm {order.executed.comm}')
            self.bar_executed = len(self)
        
        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

        self.order = None

    def notify_trade(self, trade):
        if not trade.isclosed:
            return
        self.log(f'OPERATION: GROSS {trade.pnl}, NET {trade.pnlcomm}')
        
    def next(self):
        if self.order:
            return

        rsi_3d_direction = self._rsi[-3] - self._rsi[0]
        rsi_7d_direction = self._rsi[-7] - self._rsi[0]
        rsi_sell_condition = self._rsi[0] >= self.params.rsi_sell
        rsi_buy_condition = self._rsi[0] <= self.params.rsi_buy
        # print("RSI", self._rsi[0], rsi_3d_direction, rsi_7d_direction, rsi_sell_condition, rsi_buy_condition)
        
        short_ema_condition = self._short_ema_crossover[0] < 0
        long_ema_condition = self._short_ema_crossover[0] > 0
        # print("EMA", short_ema_condition, long_ema_condition)

        macd_3d_direction = self._macd[-3] - self._macd[0] 
        macd_7d_direction = self._macd[-7] - self._macd[0]
        macd_condition = self._macd[0] > 0
        # print("MACD", self._macd[0], macd_3d_direction, macd_7d_direction, macd_condition)
        # print("\n")


        if self.position:
            if rsi_buy_condition and self.dataclose[0] > 0:
                self.log(f'SELL CREATE {self.dataclose[0]:2f}')
                self.order = self.close()
        else:
            if rsi_buy_condition:
                self.log(f'BUY CREATE {self.dataclose[0]:2f}')
                self.order = self.buy()

            elif rsi_sell_condition:
                self.log(f'SHORT CREATE {self.dataclose[0]:2f}')
                self.order = self.sell()



if __name__ == '__main__':
    
    data = {}
    with open("./data/SPY.json", "r") as f:
        data = json.load(f)

    cerebro = bt.Cerebro()

    data = bt.feeds.YahooFinanceCSVData(dataname='./data/SPY.csv', fromdate=datetime.datetime(2010, 1, 29), todate=datetime.datetime(2022, 3, 7)) 
    cerebro.adddata(data) 
    
    # cerebro.addstrategy(DollarCostAverage)
    # cerebro.addstrategy(BuyAndHold)
    # cerebro.addstrategy(Strategy)
    cerebro.addstrategy(RSIStrategy)
    # cerebro.addstrategy(EMAStrategy)


    cerebro.broker.setcash(100000.0)
    cerebro.broker.addcommissioninfo(CommInfoFractional())
    cerebro.broker.setcommission(commission=0.001)

    start = cerebro.broker.getcash()
    cerebro.run()
    end = cerebro.broker.getvalue()

    print(f'Starting Value: { start }')
    print(f'Ending Value: { end }')
    print(f'Profit Percentage: { get_profit_percentage(end, 100000.0) }')
    cerebro.plot()