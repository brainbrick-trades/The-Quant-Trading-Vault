
> Name

Moving-Average-Strategy-Python-Version

> Author

发明者量化-小小梦

> Strategy Description

Moving average strategy (Python version) is for instructional purposes; use with caution in live trading.

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|FastPeriod|3|Market Entry Express Cycle|
|SlowPeriod|7|Slow market entry cycle|
|EnterPeriod|3|Market Entry Observation Period|
|ExitFastPeriod|3|Exit express cycle|
|ExitSlowPeriod|7|Exit slow cycle|
|ExitPeriod|true|Market Exit Observation Period|
|PositionRatio|0.8|Position ratio|
|Interval|10|Polling Interval|


> Source (python)

``` python
import types
def main():
    STATE_IDLE = -1
    state = STATE_IDLE
    initAccount = ext.GetAccount()
    while True:
        if state == STATE_IDLE :
            n = ext.Cross(FastPeriod,SlowPeriod) # Indicator cross function
            if abs(n) >= EnterPeriod :
                opAmount = _N(initAccount.Stocks * PositionRatio,3)
                Dict = ext.Buy(opAmount) if n > 0 else ext.Sell(opAmount)
                if Dict :
                    opAmount = Dict['amount']
                    state = PD_LONG if n > 0 else PD_SHORT
                    Log("Open position details",Dict,"Cross period",n)
        else:
            n = ext.Cross(ExitFastPeriod,ExitSlowPeriod) # Indicator cross function
            if abs(n) >= ExitPeriod and ((state == PD_LONG and n < 0) or (state == PD_SHORT and n > 0)) :
                nowAccount = ext.GetAccount()
                Dict2 = ext.Sell(nowAccount.Stocks - initAccount.Stocks) if state == PD_LONG else ext.Buy(initAccount.Stocks - nowAccount.Stocks)
                state = STATE_IDLE
                nowAccount = ext.GetAccount()
                LogProfit(nowAccount.Balance - initAccount.Balance,'Money: ',nowAccount.Balance,' Coins: ',nowAccount.Stocks,' Closing Details: ',Dict2,' Cross Cycle:',n)
        Sleep(Interval * 1000)


```

> Detail

https://www.fmz.com/strategy/21157

> Last Modified

2016-09-30 23:25:18
