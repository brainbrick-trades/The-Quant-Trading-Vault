
> Name

Test-Spot-Buying-and-Selling-Operations-in-Two-Cases-Limit-Price-and-Market-Price

> Author

韬奋量化

> Strategy Description

Backtesting Huobi data and trading on Wexapp's demo both yielded similar results:

If the currently traded spot currency is BTC_USDT, then:

Limit Buy,exchange.Buy(6840, 5)Just using6840Buy at the price of5Individual/Unitbtc.
Market Buy,exchange.Buy(-1, 5)Just buy at market value5 usdtofbtc.(*****Please note, this is4The only special place in this case***)

Limit Sell,exchange.Sell(7350, 3)Just using7350Sell at the price of3Individual/Unitbtc.
Market Sell,exchange.Sell(-1, 3)That is to sell at market price3Individual/Unitbtc.

Strategy Code:https://www.fmz.com/m/edit-strategy/191349

2020April 5, [year]


=====I am a low-key dividing line=====

A good trading platform can make your strategy soar to 90,000 miles. Register through the link to get a two-month VIP5 handling rate discount.:
(Spot: 0% for pending orders and 0.07% for take orders. Contract: 0% for pending orders, take orders0.04%)
https://www.kucoin.cc/ucenter/signup?rcode=1wxJ2fQ&lang=zh_CN&utmsource=VIP_TF



> Source (javascript)

``` javascript
/*backtest
start: 2020-01-01 00:00:00
end: 2020-04-01 00:00:00
period: 1d
exchanges: [{"eid":"Huobi","currency":"BTC_USD","balance":1000000,"stocks":0}]
*/

var id, order, buyAmount, lastPrice;

function main() {
    Log(exchange.GetAccount());

    lastPrice = parseInt(exchange.GetTicker().Last);
    id = exchange.Buy(lastPrice + 50, 5); // Limit Buy5Individual/UnitBTC,Buy price is the current latest price+50          
    Log(order = exchange.GetOrder(id));
    buyAmount = parseFloat(order.DealAmount);
    Log(exchange.GetAccount());

    Sleep(1000);
    last_price = parseInt(exchange.GetTicker().Last);
    id = exchange.Sell(lastPrice - 50, buyAmount); // Limit Sell5Individual/UnitBTC,Sell price is the current latest price-50    
    Log(order = exchange.GetOrder(id));
    Log(exchange.GetAccount());

    Sleep(1000);
    id = exchange.Buy(-1, 5); // Market BuyBTC,Trading Volume is5Individual/Unitusdt    
    Sleep(1000);    
    Log(order = exchange.GetOrder(id));
    buyAmount = parseFloat(order.DealAmount);    
    Log(exchange.GetAccount());

    Sleep(1000);    
    id = exchange.Sell(-1, buyAmount); // Market SellBTC,The trading volume is what was just boughtBTC   
    Sleep(1000);    
    Log(order = exchange.GetOrder(id));
    Log(exchange.GetAccount());

}
```

> Detail

https://www.fmz.com/strategy/191349

> Last Modified

2021-02-05 17:09:03
