import pandas as pd 
import numpy as np
from ta import add_all_ta_features
import ta

SPY = pd.read_csv("data/csv/SPY.csv", delimiter=',', sep=r', ')
SPY.set_index(["date"], inplace = True)
SPY = SPY.filter(['open', 'high', 'low', 'close', 'volume'])

df = add_all_ta_features(SPY, open="open", high="high", low="low", close="close", volume="volume")

for item in df.columns:
    print(item)