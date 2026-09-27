
> Name

KingKeltner-Trend-Strategy-Low-Frequency

> Author

ipqhjjybj





> Source (javascript)

``` javascript
/*
Strategy Source: vnpy
Strategy name: KingKeltner Trend Strategy
Strategy Author: ipqhjjybj
Strategy Description:
Trend-following strategy

*/

KK_Length  			=	11	   // Calculate the number of windows in the channel
kkDev 				=   1.3    // Calculate deviation of channel width   
trailingPrcnt 		=   15    // Trailing Stop
LoopInterval  		=   60 	   // Polling interval (seconds)
SlidePrice          =	0.3    // Sliding price (yuan)
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

var intraTradeHigh		= 0;		// Moving highest price
var intraTradeLow		= 99999999; // Move Minimum Price
var LastBuyPrice		= 0;		// Last buy price
var LastSellPrice		= 0;		// Last sell price
var minMoney			= 100;		// If the funds are less than this value, no purchase will be made
var LastRecord 			= null;		// Initialize the previous record
function onTick(exchange) {

	var ticker = GetTicker();
    // Buy or Sell, Cancel pending orders first
    CancelPendingOrders();
    var account = GetAccount();

    if (true) {
        var records = exchange.GetRecords();
        if (!records || records.length < (KK_Length + 3)) {
            return;
        }
        // Price not change
        var newLast = records[records.length-1];
        if ((!LastRecord) || (LastRecord.Time == newLast.Time && LastRecord.Close == newLast.Close)) {
            LastRecord = newLast;
            return;
        }
        LastRecord = newLast;

        //Log(newLast);
        var kk_ATR = TA.ATR(records , KK_Length);
        var kk_Mid = TA.MA(records, KK_Length);
        var kk_Up  = kk_Mid[kk_Mid.length-1] + kk_ATR[kk_ATR.length-1] * kkDev;
        //var kk_Down= kk_Mid - kk_ATR * kkDev

        //Log("LastRecord.Close",LastRecord.Close ,"kk_up",kk_Up,"intraTradeHigh",intraTradeHigh);
        if( account.Stocks <= exchange.GetMinStock() ){
        	if(LastRecord.Close > kk_Up){
        		Log("start buy");
        		var price = ticker.Last + SlidePrice;
		        var amount = adjustFloat(account.Balance / price);
		        if (account.Balance > minMoney && amount >= exchange.GetMinStock()) {
		        	if (exchange.Buy(price, amount, "go long")) {
		        		intraTradeHigh = LastRecord.High
        				intraTradeLow  = LastRecord.Low
		        		LastBuyPrice = LastHighPrice = price;
		        	}
		        } 
        	}
        }
        else if( exchange.GetMinStock() < account.Stocks ){
        	Log("Close",LastRecord.Close, "intraTradeHigh",intraTradeHigh ,"intraTradeHigh * ( 1 - trailingPrcnt)",intraTradeHigh * ( 1 - trailingPrcnt/100.0))
        	intraTradeHigh = Math.max(intraTradeHigh , LastRecord.High)
        	intraTradeLow  = LastRecord.Low
        	if(LastRecord.Close < intraTradeHigh * ( 1 - trailingPrcnt/100.0)){	// Trailing Stop
        		Log("start sell");
        		var price = ticker.Last - SlidePrice;
		    	var sellAmount = account.Stocks;
		    	if (sellAmount > exchange.GetMinStock()) {
		    		exchange.Sell(ticker.Last - SlidePrice, sellAmount, "sell");
		    		LastSellPrice = LastLowPrice = price;
		    	} 
        	}
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

https://www.fmz.com/strategy/42283

> Last Modified

2017-06-02 23:06:08
