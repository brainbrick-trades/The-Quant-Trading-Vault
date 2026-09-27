
> Name

Cross-Platform-Arbitrage-Beginner-Test

> Author

cnxzcxy



> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|minRate|1.02|Price difference ratio|


> Source (javascript)

``` javascript
/*backtest
start: 2018-01-01 00:00:00
end: 2018-08-01 14:00:00
period: 1h
exchanges: [{"eid":"Bitfinex","currency":"ETH","balance":5000,"stocks":10},{"eid":"OKCoin_EN","currency":"ETH","balance":5000,"stocks":10}]
*/
var buyExchange;
var sellExchange;

function calc(sellExchange, buyExchange){
        var date = _D();
        sellDepth = sellExchange.GetDepth();
        sellAccount = sellExchange.GetAccount();
        sellPrice = sellDepth.Bids[1].Price;
        sellAmount = sellDepth.Bids[1].Amount;
        
        buyDepth = buyExchange.GetDepth();
        buyAccount = buyExchange.GetAccount();
        buyPrice = buyDepth.Asks[1].Price;
        buyAmount = buyDepth.Asks[1].Amount;
        
        amount = (sellAmount > buyAmount) ? buyAmount : sellAmount;
        amount = (amount > sellAccount.Stocks) ? sellAccount.Stocks : amount;
        amount = (amount > buyAccount.Balance / buyPrice) ? buyAccount.Balance / buyPrice : amount;
        priceRate = sellPrice / buyPrice;
        if(amount > 0){
            if(priceRate >= minRate){
                buyExchange.Buy(-1, amount);
                sellExchange.Sell(-1, amount);
                Log(date);
                Log("sell:", sellExchange.GetName(), "Selling price:", sellPrice, "buy:", buyExchange.GetName(), " Buy price:", buyPrice, " Proportion:", priceRate, " Total:", amount);
                Log('Statistics assets...');
                Log('exchange:', exchanges[0].GetName(), ' Account:', exchanges[0].GetAccount());
                Log('exchange:', exchanges[1].GetName(), ' Account:', exchanges[1].GetAccount());
            }
        }
    
}

function main(){
    while(true){
        calc(exchanges[0], exchanges[1]);
        calc(exchanges[1], exchanges[0]);
    }

}

```

> Detail

https://www.fmz.com/strategy/115574

> Last Modified

2018-09-12 15:50:04
