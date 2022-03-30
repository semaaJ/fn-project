import json

LONG_BLOCK = 5
SHORT_BLOCK = 5

class Broker():
    def __init__(self, data, log=True):
        self.data = data
        self.cash = 0
        self.value = 0
        self._logging = log

        self.trade_id = 0
        self.commision = 0.001
        self.open_trades = {}
        self.closed_trades = {}

        self.long_block = 0
        self.short_block = 0

        self._stop = 0.05

    def _log(self, msg):   
        if self._logging:
            print(msg)
    
    def _short_profit(self, buy, sell, amount) -> float:
        '''Calculate the profit/loss of a short
            Args:
                buy (float) : buy price
                sell (float) : sell price
                amount (float) : amount
        '''
        return (buy * amount) - (sell * amount)

    def _short_stop(self, close, stop)  -> float:
        '''Calculate the short gain/loss stops for a price
            Args:
                close (float) : close price
                stop (float) : 
        '''
        return close + (close * stop), close - (close * stop)

    def _long_profit(self, buy, sell, amount) -> float: 
        '''Calculate the profit/loss of a long
            Args:
                buy (float) : buy price
                sell (float) : sell price
                amount (float) : amount
        '''
        return (sell * amount) - (buy * amount)

    def _long_stop(self, close, stop)  -> float:
        '''Calculate the long gain/loss stops for a price
            Args:
                close (float) : closing price
                stop (float) : stop loss percentage
        '''
        return close - (close * stop), close + (close * stop)

    def deposit(self, amount) -> None:
        '''Add money to the brokerage
            Args:
                amount (float) : cash amount
        '''
        self.cash = self.cash + amount

    def _trade_size(self, size=0.03):
        '''Calculates the maximum monetary value for a trade
            Args:
                size (float) : fractional size of total cash available
        '''
        return self.cash * size

    def buy(self, date, close, trade_type, indicator_type) -> bool:
        '''Execute buy order
            Args:
                date (str) : current date
                close (float) : closing price
                trade_type (str) : trade type (buy/sell)
                indicator_type (str) : indicator which notified buy order (rsi/mfi etc.)

        '''
        amount = self._trade_size() / close

        if (self.cash - (amount * close) > 0):
            self.cash -= amount * close

            stop_loss, stop_gain = 0, 0
            if (trade_type == "buy"):
                stop_loss, stop_gain = self._long_stop(close, self._stop)
            elif (trade_type) == "sell":
                stop_loss, stop_gain = self._short_stop(close, self._stop)
                
            self.open_trades[self.trade_id] = {
                "date": date,
                "amount": amount,
                "close": close,
                "tradeType": trade_type,
                "indicatorType": indicator_type,
                "stopLoss": stop_loss,
                "stopGain": stop_gain
            }
            
            self.trade_id += 1
            return True

        return False

    def sell(self, date, close, trade_id) -> None:
        '''Execute sell order
            Args:
                date (str) : current date
                close (float) : closing price
                trade_id (int) : trade id
        '''
        trade = self.open_trades[trade_id]
    
        profit = 0
        if trade["tradeType"] == "buy":
            profit = self._long_profit(trade["close"], close, trade["amount"])
        elif trade["tradeType"] == "sell":
            profit = self._short_profit(trade["close"], close, trade["amount"])

        self.cash += (trade["amount"] * close)
        self.closed_trades[trade_id] = {
            "date": date,
            "amount": trade["amount"],
            "buyPrice": trade["close"],
            "sellPrice": close,
            "profit": profit,
            "tradeType": trade["tradeType"],
        }
    
    def _remove_trades(self, trade_ids) -> None:
        for trade_id in trade_ids:
            del self.open_trades[trade_id]

    def _reduce_block(self) -> None:
        if self.short_block > 0:
            self.short_block -= 1
        if self.long_block > 0:
            self.long_block -= 1

    def run(self) -> None:
        buy_and_hold = self.data["close"][0] / self.cash

        for i, date in enumerate(self.data["date"]):
            RSI_BUY_SIGNAL = self.data["rsiSignal"][i] == 1
            RSI_SELL_SIGNAL = self.data["rsiSignal"][i] == -1

            current = self.data["close"][i]
            
            if RSI_BUY_SIGNAL and self.long_block == 0:            
                if self.buy(date, current, "buy", "rsi"):
                    self.long_block = LONG_BLOCK
                    self._log(f'{date}: RSI BUY SIGNAL - LONG OPENED AT {current}')
                else:
                    self._log("Not enough cash in Broker Account")

            elif RSI_SELL_SIGNAL and self.short_block == 0:
                if self.buy(date, current, "sell", "rsi"):
                    self.short_block = SHORT_BLOCK
                    self._log(f'{date}: RSI SELL SIGNAL - SHORT OPENED AT {current}')
                else:
                    self._log("Not enough cash in Broker Account")

            closed_trade_ids = []
            for trade_id in self.open_trades:
                trade_type = self.open_trades[trade_id]["tradeType"]

                if trade_type == "sell":
                    if current >= self.open_trades[trade_id]["stopLoss"]:
                        self.sell(date, current, trade_id)
                        closed_trade_ids.append(trade_id)
                        self._log(f'{date} SELL STOP LOSS HIT - EXIT SHORT: {self.closed_trades[trade_id]["profit"]}')
                    
                    elif current <= self.open_trades[trade_id]["stopGain"]:
                        self.open_trades[trade_id]["stopLoss"] = self.open_trades[trade_id]["stopGain"]
                        self.open_trades[trade_id]["stopGain"] = self._short_stop(current, self._stop)[1]
                        self._log(f'{date} SELL STOP GAIN HIT')
                
                elif trade_type == "buy":
                    if current <= self.open_trades[trade_id]["stopLoss"]:
                        self.sell(date, current, trade_id)
                        closed_trade_ids.append(trade_id)
                        self._log(f'{date} BUY STOP LOSS HIT - EXIT LONG: {self.closed_trades[trade_id]["profit"]}')
                    
                    elif current >= self.open_trades[trade_id]["stopGain"]:
                        self.open_trades[trade_id]["stopLoss"] = self.open_trades[trade_id]["stopGain"]
                        self.open_trades[trade_id]["stopGain"] = self._long_stop(current, self._stop)[1]
                        self._log(f'{date} BUY STOP GAIN HIT')

            self._reduce_block()
            self.value = self.cash + sum([self.open_trades[trade_id]["amount"] * current for trade_id in self.open_trades])
            self._remove_trades(closed_trade_ids)

        self._log(f'RSI - Gain/Loss Stop {self.value}')
        self._log(f'Buy And Hold {self.data["close"][-1] / buy_and_hold}')
        self._save_data()
        
    def _save_data(self):
        with open('./data/results.json', 'r+') as f:
            f.seek(0)
            f.truncate()
            json.dump({ "open": self.open_trades, "closed": self.closed_trades }, f, indent=4)

if __name__ == "__main__":
    data = {}
    with open('./data/BTCUSDT.json', 'r') as f:
        data = json.load(f)

    broker = Broker(data)
    broker.deposit(100000)
    broker.run()

