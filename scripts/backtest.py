import pandas as pd 
import numpy as np
import math

from ta import volume

import matplotlib.pyplot as plt

def line_of_best_fit(x, y):
    a, b = np.polyfit(x, y, 1)
    return [a * i + b for i in x]


SPY = pd.read_csv("data/csv/SPY.csv", delimiter=',', sep=r', ')
SPY.set_index(["date"], inplace = True)
SPY = SPY.filter(['open', 'high', 'low', 'close', 'volume'])

# df = add_all_ta_features(SPY, open="open", high="high", low="low", close="close", volume="volume")

SPY['fi'] = volume.ForceIndexIndicator(close=SPY['close'], volume=SPY['volume'], window=39).force_index()


# Index at which we want data to begin
n = 5000
dates = [_ for _ in range(len(SPY.index))][n:]

# Split data into n sections
split_date = np.array_split(dates, math.ceil(n / 100))
split_close = np.array_split(list(SPY['close'][n:]), math.ceil(n / 100))
split_fi = np.array_split(list(SPY['fi'][n:]), math.ceil(n / 100))

# Rejoin data into one arr
close_lobf = [[*line_of_best_fit(item, split_close[i])] for i, item in enumerate(split_date)]
close_fi = [[*line_of_best_fit(item, split_fi[i])] for i, item in enumerate(split_date)]

close_lobf_slope = [np.polyfit(split_date[i], close_lobf[i], 1)[0] for i in range(len(split_date))]
close_fi_slope = [np.polyfit(split_date[i], close_fi[i], 1)[0] for i in range(len(split_date))]

print(close_fi_slope)


for i in range(len(close_lobf_slope)):
    if close_lobf_slope[i] < 0 and close_fi_slope[i] > 0:
        print(close_lobf_slope[i], close_fi_slope[i], "BULLISH")
    elif close_lobf_slope[i] > 0 and close_fi_slope[i] < 0:
            print(close_lobf_slope[i], close_fi_slope[i], "BEARISH")

# print(close_lobf_slope)
# print(close_fi_slope)

fig, axs = plt.subplots(2)
axs[0].plot(dates, list(SPY['close'][n:]))
axs[0].plot(dates, np.concatenate(close_lobf))


axs[1].plot(dates, list(SPY['fi'][n:]))
axs[1].plot(dates, np.concatenate(close_fi))
axs[1].axhline(y=0)

plt.show()
