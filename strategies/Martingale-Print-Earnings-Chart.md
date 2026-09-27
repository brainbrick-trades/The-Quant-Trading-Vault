
> Name

Martingale-Print-Earnings-Chart

> Author

Zer3192





> Source (javascript)

``` javascript
/*backtest
start: 2017-06-26 00:00:00
end: 2022-02-16 00:00:00
period: 1d
basePeriod: 1h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

function main() {
    // For tests that do not use the interface to obtain data, there is no need to useexchange.IO("status")The function determines the connection status, and there is no need to set the contract code, because this is just a test
    for(var i = 0; i < exchanges.length; i++) {
        Log("Index of the added exchange object(The First Is0And So On):", i, "Name:", exchanges[i].GetName(), "Label:", exchanges[i].GetLabel())
    }
}
var n = 0.001 //Initial Order Quantity
var MarginLevel = 30 //Contract Leverage 
var profit = 1//Expected return, cannot be less than the handling fee 
var bet=1//Multiplier
// Connect to exchange, Get relevant information
function UpdateInfo() {
    var account = exchange.GetAccount()
    records = exchange.GetRecords()
    ticker = exchange.GetTicker()
    balance = account.Stocks
    Bar = records[records.length - 1]
}

//Get random number 
function sum(m, n) {  
    var num = Math.floor(Math.random() * (m - n) + n);  
    return num;
}
function onexit() {
    var pos = exchange.GetPosition();
    if (pos.length > 0) {
        Log("Warning, Positions exist when exiting", pos);
    }
}
function main() {
    if (exchange.GetName() !== 'Futures_Binance') {
        throw "Only supports Binance Futures";
    }
    if (exchange.GetPosition().length > 0) {
        throw "No positions should exist before strategy starts.";
    }
}
function main() {
    exchange.SetContractType("swap")
    exchange.SetMarginLevel(MarginLevel)
    var position = []
    while (true) {
        var ticker = exchange.GetTicker()
        var account = exchange.GetAccount()
        var price = ticker.Buy
        var stocks = account.Stocks + account.FrozenStocks
        var balance = account.Balance + account.FrozenBalance
        var value = stocks*price + balance
        Log('Account value is: ', value)
        LogProfit(value)
        Sleep(3000)//sleep 3000ms(3s), A loop must has a sleep, or the rate-limit of the exchange will be exceed
        //when run in debug tool, add a break here
        Log(exchange.GetAccount().Balance)
        Sleep(2000)
        Log('Push to WeChat@')
        Log('This is a log in red font #ff0000')
        

        position = exchange.GetPosition()
        if (position.length == 0) {
            //Get random number0,1As direction
            var redom = sum(0,2)
            Log(redom)
            if (redom == 0) {
                n=0.001
                exchange.SetDirection("sell")
                exchange.Sell(-1, n, "open short")
            }
            if (redom == 1) {
                n=0.001
                exchange.SetDirection("buy")
                exchange.Buy(-1, n, "open long")
            }
        }
        if (position.length > 0) {

            if (position[0].Type == 0) {
                //Profit greater than expected 
                if (position[0].Profit > profit) {
                    exchange.SetDirection("closebuy")
                    exchange.Sell(-1, position[0].Amount)
                    n=0.001
                    exchange.SetDirection("buy")
                    exchange.Sell(-1, n, "open long")
            
                }
                //If the negative profit is greater than the margin, increase the position

                if (position[0].Profit < position[0].Margin * -1) {
                    n=n*bet
                    exchange.SetDirection("buy")
                    exchange.Buy(-1, position[0].Amount=n)
                }
            }
            if (position[0].Type == 1) {
                if (position[0].Profit > profit) {
                    exchange.SetDirection("closesell")
                    exchange.Buy(-1, position[0].Amount)
                    n=0.001
                    exchange.SetDirection("sell")
                    exchange.Sell(-1, n, "open short")
                
            
                }
                if (position[0].Profit < position[0].Margin * -1) {
                    n=n*bet
                    exchange.SetDirection("sell")
                    exchange.Sell(-1, position[0].Amount=n)
                }
            }
            Sleep(60000)
        }
    }
}
```

> Detail

https://www.fmz.com/strategy/353467

> Last Modified

2022-03-28 13:07:36
