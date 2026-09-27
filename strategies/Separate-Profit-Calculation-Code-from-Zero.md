
> Name

Separate-Profit-Calculation-Code-from-Zero

> Author

小草

> Strategy Description

Income can be put together with the strategy, but it is better to be independent. Reasons: 1. When the trading strategy change is interrupted, the income will not be reset. 2. The income calculation itself will call API functions, which often causes strategy API network errors and affects transaction operation. Being independent can reduce this possibility. 3. You can customize the cycle interval.



> Source (javascript)

``` javascript

function adjustFloat(v) {

    return Math.floor(v*1000)/1000;
}


function GetAccount() {
    var account;
    while (!(account = exchange.GetAccount())) {
        Sleep(1000);
    }
    return account;
}

function GetTicker() {
    var ticker;
    while (!(ticker = exchange.GetTicker())) {
        Sleep(1000);
    }
    return ticker;
}

function updateProfit(accountInit, accountNow, ticker) {
    var netNow = accountNow.Balance + accountNow.FrozenBalance + ((accountNow.Stocks + accountNow.FrozenStocks) * ticker.Buy);
    var netInit = accountInit.Balance + accountInit.FrozenBalance + ((accountInit.Stocks + accountInit.FrozenStocks) * ticker.Buy);
    LogProfit(adjustFloat(netNow - netInit), accountNow);

}

function main() {
    InitAccount = GetAccount(); 
    while (true) {
        updateProfit(InitAccount, GetAccount(), GetTicker());
        Sleep(5000);
    }
}
```

> Detail

https://www.fmz.com/strategy/1084

> Last Modified

2016-05-10 20:05:02
