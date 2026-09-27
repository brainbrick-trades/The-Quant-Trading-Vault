
> Name

Buy-Hold-Buy-and-Hold

> Author

ipqhjjybj

> Strategy Description

Buy and hold strategy



> Source (javascript)

``` javascript
/*
Strategy Source: rqalpha
Strategy name: buy-hold
Strategy Author: ipqhjjybj
Strategy Description:
Brainless exponential type

*/

LoopInterval  		=   60 	   // Polling interval (seconds)
SlidePrice          =	0.3    // Sliding price (yuan)
minMoney			=   100;		// If the funds are less than this value, no purchase will be made

function adjustFloat(v) {
    return Math.floor(v*1000)/1000;
}

function CancelPendingOrders() {
    while (true) {
        var orders = null;
        while (!(orders = exchange.GetOrders())) {
            Sleep(Interval);
        }

        if (orders.length == 0) {
            return;
        }

        for (var j = 0; j < orders.length; j++) {
            exchange.CancelOrder(orders[j].Id, orders[j]);
            if (j < (orders.length-1)) {
                Sleep(Interval);
            }
        }
    }
}

function GetAccount() {
    var account;
    while (!(account = exchange.GetAccount())) {
        Sleep(Interval);
    }
    return account;
}

function GetTicker() {
    var ticker;
    while (!(ticker = exchange.GetTicker())) {
        Sleep(Interval);
    }
    return ticker;
}

function onTick(exchange) {
	var ticker = GetTicker();
    // Buy or Sell, Cancel pending orders first
    CancelPendingOrders();
    var account = GetAccount();
    var price = ticker.Last + SlidePrice;
    var amount = adjustFloat(account.Balance / price);
    if (account.Balance > minMoney && amount >= exchange.GetMinStock()) {
    	if (exchange.Buy(price, amount, "go long")) {
    		LastBuyPrice = LastHighPrice = price;
    	}
    } 
}

function main() {
    InitAccount = GetAccount();
    Log(exchange.GetName(), exchange.GetCurrency(), InitAccount);
    LoopInterval = Math.max(LoopInterval, 1);  
    while (true) {
        onTick(exchange);
        Sleep(LoopInterval*1000);
    }
}
```

> Detail

https://www.fmz.com/strategy/41786

> Last Modified

2017-06-02 22:18:11
