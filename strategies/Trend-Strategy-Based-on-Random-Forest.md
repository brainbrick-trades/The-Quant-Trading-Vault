
> Name

Trend-Strategy-Based-on-Random-Forest

> Author

发明者量化





> Source (python)

``` python
'''backtest
start: 2019-02-09 00:00:00
end: 2019-03-11 00:00:00
period: 1h
basePeriod: 15m
exchanges: [{"eid":"Bitfinex","currency":"BTC_USD"}]
'''

import itertools
from collections import deque

import numpy as np
from sklearn.ensemble import RandomForestClassifier

def main():
    initAccount = _C(exchange.GetAccount)
    position = 0
    classifier = RandomForestClassifier()
    win_len = 8
    input = deque(maxlen=300)
    output = deque(maxlen=300)
    recent_prices = deque(maxlen=win_len + 2)
    interval = 3600000 # Sample once per hour
    
    while True:
        ticker = _C(exchange.GetTicker)
        recent_prices.append(ticker.Last)
        
        if len(recent_prices) > 0:
            Sleep(interval)
            
        if len(recent_prices) < recent_prices.maxlen:
            continue
        # Calculate volatility
        price_list = list(itertools.islice(recent_prices, 0, recent_prices.maxlen - 1))
        volt_list = np.divide(np.diff(recent_prices), price_list)
        # According to the fluctuation range, the categories are marked as: rising (>+0.5%), falling (<-0.5%), stable(-0.5%~+0.5%)
        trend_list = []
        for volt in volt_list:
            if 0.005 > volt > -0.005:
                trend_list.append(0)
            elif volt >= 0.005:
                trend_list.append(1)
            else:
                trend_list.append(-1)

        # Add volatility data to the training set
        input.append(trend_list[:-1])
        output.append(trend_list[-1])

        # When the training set contains 200 sets of data, it is considered feasible to fit a random forest.
        if len(input) < 200:
            continue
        classifier.fit(input, output)            # Fit
        prediction = classifier.predict([trend_list[1:]])  # Predict
        if position == 0:
            if prediction == 1:
                exchange.Buy(-1, _C(exchange.GetAccount).Balance)
                position = 1
        else:
            if prediction == -1:
                exchange.Sell(-1, _C(exchange.GetAccount).Stocks - initAccount.Stocks)
                position = 0
```

> Detail

https://www.fmz.com/strategy/140199

> Last Modified

2022-05-20 01:16:44
