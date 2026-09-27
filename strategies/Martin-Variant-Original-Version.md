
> Name

Martin-Variant-Original-Version

> Author

恐龙宝宝

> Strategy Description

    This was my first simple strategy after entering Macau. It took me 10 minutes to write it. It is a Martin variant with a very small increase interval. It controls the risk of liquidation through fixed investment and gradually increasing the interval. The profit and loss ratio is much better than the traditional Martin.
    In the big bull market in March and April, this Martin performed very well. At its peak, he used a small amount of money to double a day. At that time, he used 12u to run CHR in four days.48u.
    However, times have changed and the bull market is no longer there. If this Martin is used in today's market, it will inevitably make users become text message receivers, so I shared it.
    Actually, there is still some value in the live market, but it requires manual timing. It's no longer the kind of market where Martin opens and counts money at once.
      

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|zuoduo|true|go long|
|zuokong|false|go short|
|CV|3|Price Precision|
|MarginLevel|75|Leverage multiple|
|k|true|First position opening volume|
|n|true|Replenishment Quantity|
|Q|0.03|Take profit point|
|E|0.0046|Increment Interval|


> Source (python)

``` python
'''backtest
start: 2021-05-01 00:00:00
end: 2021-05-14 00:00:00
period: 1m
basePeriod: 1m
exchanges: [{"eid":"Futures_Binance","currency":"EOS_USDT","balance":1000}]
args: [["zuokong",true],["n",3],["E",0.02]]
'''
def main():
    while True:
        exchange.SetContractType("swap")
        exchange.SetMarginLevel(MarginLevel)
        ticker = _C(exchange.GetTicker)
        account = _C(exchange.GetAccount)
        position = _C(exchange.GetPosition)
        if zuoduo:
            if len(position) == 0:   
                    exchange.SetDirection("buy")
                    exchange.Buy(-1, k, "open long")
            if len(position) > 0:
                if position[0].Type==0:
                    
                    if position[0].Price+Q<ticker["Last"]:
                        exchange.SetDirection("closebuy")
                        exchange.Sell(-1, position[0].Amount) 
                        account = exchange.GetAccount()
                        LogProfit(account["Balance"]) 
                    fx=(E/n)*position[0].Amount  
                    if position[0].Profit<position[0].Margin * -fx :
                        #Polling for Increment
                            exchange.SetDirection("buy")
                            exchange.Buy(-1, k)
                            LogProfit(account["Balance"])     
        if zuokong:
            if len(position) == 0:   
                    exchange.SetDirection("sell")
                    exchange.Sell(-1, k, "open short")
            if len(position) > 0:
                if position[0].Type == 1 :
                    fp=Q*position[0].Amount
                    if position[0].Profit > 0.01*fp*ticker["Last"] :
                        exchange.SetDirection("closesell")
                        exchange.Buy(-1, position[0].Amount) 
                        account = exchange.GetAccount()
                        LogProfit(account["Balance"]) 
                    fx=(E/n)*position[0].Amount  
                    if position[0].Profit<position[0].Margin * -fx :
                        #Polling for Increment
                            exchange.SetDirection("sell")
                            exchange.Sell(-1, n)
                            LogProfit(account["Balance"])
        
        Sleep(3000)
```

> Detail

https://www.fmz.com/strategy/293373

> Last Modified

2022-03-02 15:39:53
