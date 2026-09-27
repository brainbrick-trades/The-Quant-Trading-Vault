
> Name

Simple-Arithmetic-Contract-Grid

> Author

恐龙宝宝

> Strategy Description

**The parameters are very simple, they areBTCFor example, when you reach the area where you open a long position, close short to buy a bottom position and open a long position; when you reach the area where you open a short position, you buy a bottom position and open a short position, repeating this cycle**
**Obviously, in the crypto world, in the long run, any complex model cannot outperform a mindless grid strategy**
**Wealth code is brainless grid+Reckless all-in local dog**
**Hopefully, like the earliest Martin, this is the simplest and most brutal yet profitable strategy**
 ![IMG](https://www.fmz.com/upload/asset/1bdae37080236f7ea7077.png) 


> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|M|20|Leverage Size|
|H|50|Initial base position quantity|
|n1|true|Quantity per single grid trade|
|grid|200|Spacing per single grid trade|
|xia|35000|Open multiple points|
|shang|60000|Open short position|


> Source (python)

``` python
'''backtest
start: 2021-01-01 00:00:00
end: 2021-11-17 00:00:00
period: 1m
basePeriod: 1m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT","balance":2500}]
args: [["H",30],["n1",0.001],["grid",300],["xia",50000]]
'''

def CancelPendingOrders():
    orders = _C(exchanges[0].GetOrders)
    if len(orders)>0:
        for j in range(len(orders)):
            exchanges[0].CancelOrder(orders[j].Id, orders[j])
            j=j+1

def main():
    exchange.SetContractType('swap')
    exchange.SetMarginLevel(M)
    currency=exchange.GetCurrency()
    if _G('buyp') and _G('sellp'):
        buyp=_G('buyp')
        sellp=_G('sellp')
        Log('Read grid prices')
    else:
        ticker=exchange.GetTicker()
        buyp=ticker["Last"]-grid
        sellp=ticker["Last"]+grid
        _G('buyp',buyp)
        _G('sellp',sellp)
        Log('Initialize grid data')
    while True:
            account=exchange.GetAccount()
            ticker=exchange.GetTicker()
            position=exchange.GetPosition()
            orders=exchange.GetOrders()
            if len(position)==0:
                if ticker["Last"]>shang:
                    exchange.SetDirection('sell')
                    exchange.Sell(-1,n1*H)
                    Log(currency,'Reached short opening area,Buy short base position')
                    
                else:
                    exchange.SetDirection('buy')
                    exchange.Buy(-1,n1*H)
                    Log(currency,'Reached long opening area,Buy long base position')
            if len(position)==1:
                if position[0]["Type"]==1:
                    if ticker["Last"]<xia:
                        Log(currency,'Take profit and reverse all short orders')
                        exchange.SetDirection('closesell')
                        exchange.Buy(-1,position[0].Amount)
                    else:
                        orders=exchange.GetOrders()
                        if len(orders)==0:
                            exchange.SetDirection('sell')
                            exchange.Sell(sellp,n1)
                            exchange.SetDirection('closesell')
                            exchange.Buy(buyp,n1)
                        if len(orders)==1:
                            if orders[0]["Type"]==1: #take profit transaction
                                Log(currency,'Grid reduction,Current number of copies:',position[0].Amount)
                                CancelPendingOrders()
                                buyp=buyp-grid
                                sellp=sellp-grid
                                LogProfit(account["Balance"])
                            if orders[0]["Type"]==0:
                                Log(currency,'Grid increase position,Current number of copies:',position[0].Amount)
                                CancelPendingOrders()
                                buyp=buyp+grid
                                sellp=sellp+grid
                                LogProfit(account["Balance"])
            
                if position[0]["Type"]==0:
                    if ticker["Last"]>float(shang):
                        Log(currency,'Take profit and reverse all long orders')
                        exchange.SetDirection('closebuy')
                        exchange.Sell(-1,position[0].Amount)
                    else:
                        orders=exchange.GetOrders()
                        if len(orders)==0:
                            exchange.SetDirection('buy')
                            exchange.Buy(buyp,n1)
                            exchange.SetDirection('closebuy')
                            exchange.Sell(sellp,n1)
                        if len(orders)==1:
                            if orders[0]["Type"]==0: #take profit transaction
                                Log(currency,'Grid reduction,Current number of copies:',position[0].Amount)
                                CancelPendingOrders()
                                buyp=buyp+grid
                                sellp=sellp+grid
                                LogProfit(account["Balance"])
                            if orders[0]["Type"]==1:
                                Log(currency,'Grid increase position,Current number of copies:',position[0].Amount)
                                CancelPendingOrders()
                                buyp=buyp-grid
                                sellp=sellp-grid
                                LogProfit(account["Balance"])
                            
                    
                
                                     
            

```

> Detail

https://www.fmz.com/strategy/330440

> Last Modified

2021-11-18 21:40:30
