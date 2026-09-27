
> Name

Short-Unlocking-Strategy-on-FMEX-Starting-from-1-BTC-Bearish-Outlook

> Author

gulishiduan_高频排序

> Strategy Description

FMexInstructions for using the short version code of sort mining. (Note the api address) (WeChat:ying5737)
(It is expected that the daily slow decline will be more than 1%. Earn coins and mines, otherwise the losses will be obvious.)
The risk in the margin market is huge, and you may face 100% loss at any time. We are not responsible for 100% loss due to unknown bugs.

Principle: random execution of orders at market depth/
Hold position firstSHORT1-1000u.//
- Detect whether the existing order exceeds the limit, and if it exceeds the limit, cancel the order immediately/
- Check whether the transaction has formed a position. If it is greater than the position xxu, then reduce the position to below the established position./

Several situations:
Global pending orders: In order to distinguish market makers' strategies, the remote sorting is specifically defined as pending orders. Parameters adjustable.
Market maker:
Maximum long position. If it is larger than this position, the position will be reduced approximately every 6 seconds..
The maximum short position. If it is larger than this position, the position will be reduced approximately every 6 seconds..
If the long position is greater than 1u, start the long position reduction strategy, and the pending order is mainly short.
If it is greater than the short position, start the short position reduction strategy, and the pending orders are mainly long.
Normal position

//The remarks in the parameters are for reference only. Gears can also be added.
Risk at own responsibility / parameters adjustable, WeChat:ying5737

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|Url|https://api.fmex.com|Exchange API address|
|maxPrice|30000|Highest price in range|
|minPrice|9000|Lowest price in range|
|g_maxHoldingLong|5000|Maximum long position|
|g_maxHoldingShort|32000|Maximum short position|
|sp_baseAmountShort|25000|When the short position exceeds this value, prioritize executionlong|
|sp_perAmount|600|Market ranking: single quantity. (Depth sorting order volume = market order volume * 3) (Normal long order volume = market order volume*0.8)|
|sp_baseAmountLong|500|After the long position is larger than this number, the pending order will be adjusted to priority for execution.short|
|Interval|3|Polling time (default parameters are fine))|
|RetryInterval|1000|Fault tolerance retry interval (milliseconds) (default parameters are sufficient)|
|Debug|true|Display retry records (default parameters are fine))|
|EnableErrorFilter|false|Display retry records to block common network error messages (default parameters are sufficient)|
|ApiList|GetAccount,GetDepth,GetTicker,GetRecords,GetTrades,GetOrders,SetContractType|Fault-tolerant API list (default parameters are fine))|


> Source (javascript)

``` javascript
//The risk in the margin market is huge, and you may face 100% loss at any time. We are not responsible for 100% loss due to unknown bugs.The leverage used by this strategy is relatively low, so you can try it with confidence.
//Note: By default, near-end sorting is not activated(Reserve space for manual closing of positions),Long version hold position firstlong1u-1000u,Short version hold position firstshort1u-1000u.Used to activate near-end sorting
var eName = exchange.GetName();
            if (eName == "Futures_FMex") {
                exchange.IO("extend", '{"POST/v3/contracts/orders$":{"affiliate_code":"9y40d8"}}');
            } if (eName == "FCoin") {
                exchange.IO("extend", '{"POST/v2/orders$":{"affiliate_code":"9y40d8"}}');
            }
exchange.IO("base", Url)//(Contact WeChat:ying5737)The strategy is for personal use only. If it is used for commercial communication, please contact us in advance
var ordersInfo = {
    buyId: 0,    buyPrice: 0,    sellId: 0,    sellPrice: 0,    minPrice: 0,    maxPrice: 0
}
var depthInfo = {
    asks: [],
    bids: []
}
var symbol = "BTCUSD_P"
function getTicker(symbol) {
    url = "/v2/market/ticker/" + symbol;
    data = _C(exchange.IO,"api", "GET", url);
    return data.data;
}    
function getAccounts() {
    data = _C(exchange.IO,"api", "GET", "/v3/contracts/accounts")
    return data.data;
}
function createOrderPrice(body) {
    parameter = "symbol=" + body.symbol + "&type=" + body.type + "&direction=" + body.direction + "&post_only=" + body.post_only +  "&price=" + body.price + "&quantity=" + body.quantity + "&affiliate_code=9y40d8";   
    resultData = exchange.IO("api", "POST", "/v3/contracts/orders", parameter)
    return resultData;
}
function createOrder(body) {
    parameter = "symbol=" + body.symbol + "&type=" + body.type + "&direction=" + body.direction + "&quantity=" + body.quantity + "&affiliate_code=9y40d8";   
    resultData = exchange.IO("api", "POST", "/v3/contracts/orders", parameter)    
    return resultData;
}
function getOrders() {
    resultData = _C(exchange.IO,"api", "GET", "/v3/contracts/orders/open");
    return resultData.data
}
function cancelOrder(id) {
    if (typeof(id) == 'undefined') {
        return
    }
    resultData = exchange.IO("api", "POST", "/v3/contracts/orders/" + id + "/cancel");//+ id 
    return resultData;    
}
function cancelAllOrder() {
    resultData = exchange.IO("api", "POST", "/v3/contracts/orders/cancel");
    return resultData;    
}
function getPosition() {
    resultData = _C(exchange.IO,"api", "GET", "/v3/broker/auth/contracts/positions");
    return resultData.data;
}
function getMatches(id) {
    resultData = _C(exchange.IO,"api", "GET", "/v3/contracts/orders/" + id + "/matches");
    return resultData.data;
}
function getCandles(resolution, symbol) {
    resultData = _C(exchange.IO,"api", "GET", "/v2/market/candles/" + resolution + "/" + symbol);
    return resultData.data;
}

function cleanPosition() {
    res = getPosition();    
    res.results.forEach(function(it) {
        if (it.symbol == symbol) {
            if (it.quantity) {
                if (it.quantity > g_maxHoldingLong && it.direction.toUpperCase() == 'LONG') { 
                    data = createOrder({symbol: symbol,type: "MARKET",direction: "SHORT",quantity:sp_perAmount * 2
                    })
                    Log("LONGExceeded maximum position,reduce position");
                }
                if (it.quantity > g_maxHoldingShort && it.direction.toUpperCase() == 'SHORT') {
                    data = createOrder({symbol: symbol,type: "MARKET",direction: 'LONG',quantity: sp_perAmount * 2
                    })
                    Log("SHORTExceeded maximum position,reduce position");
                }
            }
        }
    });
}
// add new 
var hasElephantOrder = false
// var elephantOrder  = []
var elephantOrderTime = 0
function underElephant (ticker) {
    var buyPrice = ticker[2] 
    var sellPrice = ticker[4] 
    var bestAskAmount = ticker[5];
    var bestBidAmount = ticker[3];
    var now = new Date().getTime()
    if (hasElephantOrder) {
        if (now - elephantOrderTime < 3000) {
            return
        }
        // for (var index = 0; index < elephantOrder.length; index++) {
        //     cancelOrder(elephantOrder[index].id)
        //     Sleep(1000)
        // }
        hasElephantOrder = false
    }
    if (bestBidAmount > 40000 && bestBidAmount > bestAskAmount * 2) {
        //If the quantity at the buy one tier＞XTen thousand, and the buy one order quantity is greater than the sell one order quantityYTimes, order.
        //Wait, cancel the order. Recheck and re-place.       
        // elephantOrder.push(order.data)
      //  order = createOrderPrice({symbol: symbol,type: "LIMIT",direction: "LONG",post_only: true,price: buyPrice - 2,quantity: sp_perAmount * 2 })
      //  Log("Elephant pending order buy4 LONG" );
       order = createOrderPrice({symbol: symbol,type: "LIMIT",direction: "LONG",post_only: true,price: buyPrice - 3,quantity: sp_perAmount * 3})
       Log("Elephant pending order buy6 LONG" );
        // elephantOrder.push(order.data)
        order = createOrderPrice({symbol: symbol,type: "LIMIT",direction: "LONG",post_only: true,price: buyPrice - 4,quantity: sp_perAmount * 3})
        Log("Elephant pending order buy8 LONG" );        
        // elephantOrder.push(order.data)
        order = createOrderPrice({symbol: symbol,type: "LIMIT",direction: "LONG",post_only: true,price: buyPrice - 4.5,quantity: sp_perAmount * 3})
        Log("Elephant pending order buy9 LONG" );
        order = createOrderPrice({symbol: symbol,type: "LIMIT",direction: "LONG",post_only: true,price: buyPrice - 5,quantity: sp_perAmount * 3})
        Log("Elephant pending order buy10 LONG" );        
        // elephantOrder.push(order.data)
        order = createOrderPrice({symbol: symbol,type: "LIMIT",direction: "LONG",post_only: true,price: buyPrice - 6.5,quantity: sp_perAmount * 3})
        Log("Elephant pending order buy13 LONG" );
        order = createOrderPrice({symbol: symbol,type: "LIMIT",direction: "LONG",post_only: true,price: buyPrice - 7,quantity: sp_perAmount * 3})
        Log("Elephant pending order buy14 LONG" );        
        // elephantOrder.push(order.data)
        
        // elephantOrder.push(order.data)
        hasElephantOrder = true
        elephantOrderTime = now
    }  if (bestAskAmount > 40000 && bestAskAmount > bestBidAmount * 2) {
        //If the quantity at the sell one tier＞XTen thousand, and the sell one order quantity is greater than the buy one order quantityYTimes, order.
        //Wait, cancel the order. Recheck and re-place.
       // order = createOrderPrice({symbol: symbol,type: "LIMIT",direction: "SHORT",post_only: true,price: sellPrice + 1,quantity: sp_perAmount * 3})
       // Log("Elephant pending order sell2 LONG" );
        // elephantOrder.push(order.data)
        order = createOrderPrice({symbol: symbol,type: "LIMIT",direction: "SHORT",post_only: true,price: sellPrice + 2,quantity: sp_perAmount * 3})
        Log("Elephant pending order sell4 LONG" );
        order = createOrderPrice({symbol: symbol,type: "LIMIT",direction: "SHORT",post_only: true,price: sellPrice + 3,quantity: sp_perAmount * 3})
        Log("Elephant pending order sell6 LONG" );
        // elephantOrder.push(order.data)
        order = createOrderPrice({symbol: symbol,type: "LIMIT",direction: "SHORT",post_only: true,price: sellPrice + 4,quantity: sp_perAmount * 3})
        Log("Elephant pending order sell8 LONG" );
        order = createOrderPrice({symbol: symbol,type: "LIMIT",direction: "SHORT",post_only: true,price: sellPrice + 5,quantity: sp_perAmount * 3})
        Log("Elephant pending order sell10 LONG" );
        order = createOrderPrice({symbol: symbol,type: "LIMIT",direction: "SHORT",post_only: true,price: sellPrice + 6,quantity: sp_perAmount * 3})
        Log("Elephant pending order sell12 LONG" );
        // elephantOrder.push(order.data)
        order = createOrderPrice({symbol: symbol,type: "LIMIT",direction: "SHORT",post_only: true,price: sellPrice + 7,quantity: sp_perAmount * 3})
        Log("Elephant pending order sell14 LONG" );
        // elephantOrder.push(order.data)
        hasElephantOrder = true
        elephantOrderTime = now
    }
}
function marketMaker(ticker) {
    Log("Market maker/Sorting mining**********************************");
    lastPrice = ticker[0] 
    buyPrice = ticker[2] 
    sellPrice = ticker[4] 
    Log("lastPrice:"+lastPrice+":buyPrice:"+buyPrice+":sellPrice:" + sellPrice);
    if (lastPrice == buyPrice) {
        sellPrice = (buyPrice + 0.5).toFixed(1)
    }
    if (lastPrice == sellPrice) {
        buyPrice = (sellPrice - 0.5).toFixed(1)
    }
    Log("buyPrice:"+buyPrice+":sellPrice:" + sellPrice);    
    res = getPosition();
    Log("Market maker/Sorting miningPosition:" + JSON.stringify(res));

    res.results.forEach(function(it) {
        if (it.quantity) {
            var index = 0
            if (it.quantity > sp_baseAmountLong && it.direction.toUpperCase() == 'LONG') {//Too many long positions, change the order tier,short3-9,long9-10
                for (index = 0; index < 9; index++) {
                    order = createOrderPrice({symbol: symbol, type: "LIMIT", direction: "SHORT",  post_only: true,  price: lastPrice + 1 + 0.5 * index,   quantity: sp_perAmount                   })
                    Log("Market maker/SortSHORTSell" + (2 + index) );                            
                }
        
                for (index = 0; index < 3; index++) {
                    order = createOrderPrice({ symbol: symbol,  type: "LIMIT",   direction: "LONG",   post_only: true,   price: lastPrice - 4 - (0.5 * index),   quantity: sp_perAmount                 })
                    Log("Market maker/SortLONGBuy" + (8 + index));
                }
                
            } else if (it.quantity > sp_baseAmountShort && it.direction.toUpperCase() == 'SHORT' ) {       
                for (index = 0; index < 9; index++) {
                    order = createOrderPrice({symbol: symbol, type: "LIMIT", direction: "LONG",  post_only: true,  price: lastPrice - 1 - 0.5 * index,   quantity: sp_perAmount                   })
                    Log("Market maker/SortLONGBuy" + (2 + index) );                            
                }
            } else {//Normal holding state, long (not full position))           short  
              
               order = createOrderPrice({  symbol: "BTCUSD_P",  type: "LIMIT",   direction: "SHORT",    post_only: true,     price: lastPrice + 1.5,     quantity: sp_perAmount                    })
                    Log("Market maker/SortSHORT3" );
                    order = createOrderPrice({  symbol: "BTCUSD_P",     type: "LIMIT",   direction: "SHORT",   post_only: true,  price: lastPrice + 2,     quantity: sp_perAmount                    })
                    Log("Market maker/SortSHORT4" );
                    order = createOrderPrice({symbol: "BTCUSD_P",    type: "LIMIT",     direction: "SHORT",  post_only: true,    price: lastPrice + 2.5,    quantity: sp_perAmount                    })
                    Log("Market maker/SortSHORT5" ); 
                    order = createOrderPrice({  symbol: "BTCUSD_P",  type: "LIMIT",   direction: "SHORT",    post_only: true,     price: lastPrice + 3,     quantity: sp_perAmount                   })
                    Log("Market maker/SortSHORT6" );
                  //  order = createOrderPrice({  symbol: "BTCUSD_P",     type: "LIMIT",   direction: "SHORT",   post_only: true,  price: lastPrice + 3.5,     quantity: sp_perAmount                   })
                   // Log("Market maker/SortSHORT7" );
                    order = createOrderPrice({symbol: "BTCUSD_P",    type: "LIMIT",     direction: "SHORT",  post_only: true,    price: lastPrice + 4,    quantity: sp_perAmount                     })
                    Log("Market maker/SortSHORT8" );   
                    order = createOrderPrice({  symbol: "BTCUSD_P",     type: "LIMIT",   direction: "SHORT",   post_only: true,  price: lastPrice + 6.5,     quantity: sp_perAmount                     })
                    Log("Market maker/SortSHORT7" );
                    order = createOrderPrice({symbol: "BTCUSD_P",    type: "LIMIT",     direction: "SHORT",  post_only: true,    price: lastPrice + 7,    quantity: sp_perAmount                         })
                    Log("Market maker/SortSHORT8" ); 
                    order = createOrderPrice({ symbol: "BTCUSD_P",  type: "LIMIT",   direction: "LONG",   post_only: true,   price: lastPrice - 3.5,   quantity: sp_perAmount  * 0.6            })
                    Log("Market maker/SortLONGBuy7" );
                    order = createOrderPrice({ symbol: "BTCUSD_P",  type: "LIMIT",   direction: "LONG",   post_only: true,   price: lastPrice - 4,   quantity: sp_perAmount   * 0.6            })
                    Log("Market maker/SortLONGBuy8" );
                    order = createOrderPrice({ symbol: "BTCUSD_P",  type: "LIMIT",   direction: "LONG",   post_only: true,   price: lastPrice - 4.5,   quantity: sp_perAmount    * 0.6           })
                    Log("Market maker/SortLONGBuy9" ); 
            }
        }
    })
}

var lastPrintfTime = null
function printfBanner() {
    var now = new Date().getTime()

    if (lastPrintfTime == null || now - lastPrintfTime > 60 * 5 * 1000) {
        Log("FMexPlease see the description for usage instructions of the multi-head version of sorted mining. (Note the api address) WeChat:ying5737)#ff0000")
        lastPrintfTime = now
    }
}

/********************END Market maker/Sorting mining***************************************************************************************************/
// Called during template initialization
function init() {    // Filter common errors
    if (EnableErrorFilter) {
        SetErrorFilter("502:|503:|tcp|character|connection|unexpected|network|timeout|WSARecv|Connect|GetAddr|no such|reset|http|received|EOF|reused");
    }
     _CDelay(RetryInterval)
   // Redefine functions that require fault tolerance
    var names = ApiList.split(',');
    _.each(exchanges, function(e) {
        _.each(names, function(name) {
            if (typeof(e[name]) !== 'function') {
                throw "Try fault tolerance " + name + " Failed, Please confirm existence of thisAPIAnd enter correctly.";
            }
            var old = e[name];
            e[name] = function() {
                var r;
                while (!(r = old.apply(this, Array.prototype.slice.call(arguments)))) {
                    if (Debug) {
                        Log(e.GetLabel(), name, "Call failed", RetryInterval, "Retry after milliseconds...");
                    }
                    Sleep(RetryInterval);
                }
                return r;
            };
        });
    });
    Log("Fault-tolerance mechanism enabled", names);
}

function checkRisk(ticker) {
    lastPrice = ticker[0]
    if (lastPrice< minPrice || lastPrice > maxPrice) {
        Log(
        '===== Price has exceeded the box fluctuation range [',
        minPrice,
        ',',
        maxPrice,
        '],Order pause 1 Minute,1Retest after minutes ====='
        );
        Sleep(1000 * 60);
        return true;
    }
    return false
}

function main() {
    while(true){
        cancelAllOrder()
        tickerInfo = getTicker(symbol);
        ticker = tickerInfo.ticker;
        if (!checkRisk(ticker)) {
            marketMaker(ticker);
            underElephant(ticker)
        }
        cleanPosition();
        printfBanner()
        Sleep(Interval * 1000) 
    }    
}//FMexPlease see the description for usage instructions of the multi-head version of sorted mining. (Note the api address) WeChat:ying5737)

function onexit() {
    Log("Exit, cancel all orders")
    cancelAllOrder()
}

```

> Detail

https://www.fmz.com/strategy/178417

> Last Modified

2020-12-25 23:51:31
