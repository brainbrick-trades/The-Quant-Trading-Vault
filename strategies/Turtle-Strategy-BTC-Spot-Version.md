
> Name

Turtle-Strategy-BTC-Spot-Version

> Author

groot

> Strategy Description

Seeing that there is no public Python turtle strategy on the platform, I wrote a simple one to throw a brick.
The system is close to the original Turtle system, not much optimized, so treat it as a backtest, or you can further optimize it yourself and run live trading.

Open position: open when above Donchian upper band
Add positions: add positions if it exceeds the previous price by 0.5 ATR
Stop loss and take profit: if it falls below the lower track or falls below the last opening price - 2ATR, all profits will be taken.

Backtested 1 year of data, annualized 80%, maximum drawdown16%

Spot fund utilization is low; after switching to the contract version, the return will be higher.

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|fresh_rete|24|Trading frequency (hours)|
|trade_percent|0.01|Asset ratio|
|DC_range|30|Channel period count|
|atrlength|24|atrnumber of cycles|


> Source (python)

``` python
'''backtest
start: 2019-01-01 00:00:00
end: 2020-03-02 00:00:00
period: 1d
exchanges: [{"eid":"OKEX","currency":"BTC_USDT","stocks":0}]
args: [["fresh_rete",24],["DC_range",20],["atrlength",14]]
'''


import numpy as np
import pandas as pd
import datetime


data = {'ordertime':[],'id':[],'price':[]}
hisorder = pd.DataFrame(data)
    
def turtle():
    #Declare global variables
    global hisorder
    
    acct = exchange.GetAccount()

    records=exchange.GetRecords(fresh_rete*60*60)

    ticker = exchange.GetTicker()
    

    portfolio_value = acct.Balance+acct.FrozenBalance+(acct.Stocks+acct.FrozenStocks)*records[-1]['Close']
    atr = TA.ATR(records, atrlength)[-1]
    #CalculatedunitSize
    value = portfolio_value*trade_percent
    unit =  min(round(value/atr,4),round(acct.Balance/(ticker['Last']+100),4))
    #unit =  round(value/atr,2)

    df = pd.DataFrame(records)
    current_price = records[-1]['Close']
    last_price = 0
    if len(hisorder)!=0:
        last_price = hisorder.iloc[-1]['price']
    max_price = df[-DC_range:-2]['High'].max()
    min_price = df[-int(DC_range/2):-2]['Low'].min() 
    
    opensign = len(hisorder)==0 and current_price > max_price
    

    addsign = len(hisorder)!=0 and current_price > last_price + 0.5*atr


    stopsign = len(hisorder)!=0 and current_price < min_price
    
    
    closesign = len(hisorder)!=0 and current_price < (last_price - 2*atr)

    
#    if _D(records[-1]['Time']/1000) == '2020-01-25 00:00:00':
#        Log("records[-1]",records[-1])





    if opensign | addsign:
        if acct.Balance >= (ticker['Last']+10)*unit and unit >0:
            id = exchange.Buy(ticker['Last']+10,unit)
            orderinfo = exchange.GetOrder(id)
            data = {'ordertime':_D(records[-1]['Time']/1000),'id':id,'price':records[-1]['Close']}
            hisorder = hisorder.append(data,ignore_index=True)
            Log('Latest account information after buying:', exchange.GetAccount())
            Log("opensign",opensign,"addsign",addsign)
    #    else:
    #        Log('Insufficient balance, please top up......', exchange.GetAccount())
    if stopsign | closesign:
        exchange.Sell(-1, acct.Stocks+acct.FrozenStocks)
        data = {'ordertime':[],'id':[],'price':[]}
        hisorder = pd.DataFrame(data)
        Log('Latest account information after selling:', exchange.GetAccount())
        Log("stopsign",stopsign,"closesign",closesign)

    

    
def main():
    while True:
        turtle()
        Sleep(fresh_rete*60*60*1000)        
```

> Detail

https://www.fmz.com/strategy/186598

> Last Modified

2020-03-06 12:04:41
