
> Name

Two-Way-Contract-Grid-Trading-V102

> Author

wind

> Strategy Description

# Two-way contract grid tradingv1.0.2

> Function

Futures grid trading
At the same time, arbitrage is done by shorting and going long
Because the probability of liquidation in a bidirectional strategy is very low
* Buy order timeout judgment
* Multiple Betting
* Auto Copy Trading
* Trend orders (to be developed, paid version))
* Dynamically modify the order quantity based on price change speed (under development, paid version))
* Golden cross and death cross trend added (to be developed, paid version))

> Backtest Data

  ![IMG](https://www.fmz.com/upload/asset/20322178b3e84a01941d3.jpg) 
  
  ![IMG](https://www.fmz.com/upload/asset/2038958a58a5471a594f9.jpg) 
  
  
2000uDouble in Half a Year
Profits are very obvious, can withstand both large rises and falls

> Maintenance

Continuous Optimization



> Source (javascript)

``` javascript

/*backtest
start: 2021-01-01 00:00:00
end: 2021-06-21 23:59:00
period: 1m
basePeriod: 1m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT","balance":2000}]
*/

// First Purchase
let FIRST_BUY = true;
// There is already a buy order
let MANY_BUYING = false;
// A short order already exists
let SHORT_BUYING = false;
// Long order creation time
let MANY_BUY_TIME = null;
// Short order creation time
let SHORT_BUY_TIME = null;
// Buy long short positions
let MANY_EMPTY_STEP_TIME = null;
// Short Short Position
let SHORT_EMPTY_STEP_TIME = null;
// Check the empty position time
let CHECK_TIME = null;

let QUANTITY = [0.001, 0.002, 0.004, 0.008, 0.016, 0.032, 0.064];
// Next purchase price(Long position)
let MANY_NEXT_BUY_PRICE = 0;
// Next purchase price(Short position)
let SHORT_NEXT_BUY_PRICE = 0;
// Current Position(Long position)
let MANY_STEP = 0;
// Current Position(Short position)
let SHORT_STEP = 0;
// Take Profit Ratio
let PROFIT_RATIO = 1;
// Add Position Ratio
let DOUBLE_THROW_RATIO = 1.5;
// The downward percentage of the amount spent after selling
let BUY_PRICE_RATIO = 1;
// Trade order list(Long position)
let MANY_ORDER_LIST = [];
// Trade order list(Short position)
let SHORT_ORDER_LIST = [];

function getManyQuantity() {
    if (MANY_STEP < QUANTITY.length) {
        return QUANTITY[MANY_STEP]
    }
    return QUANTITY[0]
}

function getShortQuantity() {
    if (SHORT_STEP < QUANTITY.length) {
        return QUANTITY[SHORT_STEP]
    }
    return QUANTITY[0]
}

function firstManyBuy(ticker) {
    if (MANY_BUYING) {
        return
    }
    exchange.SetDirection("buy")
    let orderId = exchange.Buy(ticker.Last, getManyQuantity())
    if (!orderId) {
        return
    }
    MANY_BUYING = true
    while (true) {
        exchange.SetDirection("buy") 
        let order = exchange.GetOrder(orderId)
        if (null === order) {
            continue
        }
        if (1 === order.Status || 2 === order.Status) {
            MANY_NEXT_BUY_PRICE = order.Price * ((100 - DOUBLE_THROW_RATIO) / 100)
            MANY_STEP = MANY_STEP + 1
            MANY_BUYING = false
            MANY_EMPTY_STEP_TIME = null
            let sellPrice = order.Price * ((100 + PROFIT_RATIO) / 100)
            MANY_ORDER_LIST.push({
                buyPrice: order.Price,
                sellPrice: sellPrice,
                quantity: order.Amount,
                isSell: false,
            })
            break
        }
    }
}

function firstShortBuy(ticker) {
    if (SHORT_BUYING) {
        return
    }
    exchange.SetDirection("sell")
    let orderId = exchange.Sell(ticker.Last, getShortQuantity())
    if (!orderId) {
        return
    }
    SHORT_BUYING = true
    while (true) {
        let order = exchange.GetOrder(orderId)
        if (null === order) {
            continue
        }
        if (1 === order.Status || 2 === order.Status) {
            SHORT_NEXT_BUY_PRICE = order.Price * ((100 + DOUBLE_THROW_RATIO) / 100)
            SHORT_STEP = SHORT_STEP + 1
            SHORT_BUYING = false
            SHORT_EMPTY_STEP_TIME = null
            let sellPrice = order.Price * ((100 - PROFIT_RATIO) / 100)
            SHORT_ORDER_LIST.push({
                buyPrice: order.Price,
                sellPrice: sellPrice,
                quantity: order.Amount,
                isSell: false,
            })
            break
        }
    }
}

function manyBuy(ticker) {
    if (MANY_BUYING) {
        return
    }
    Log('ticker: ' + ticker.Last + ' MANY_NEXT_BUY_PRICE: ' + MANY_NEXT_BUY_PRICE)
    if (ticker.Last > MANY_NEXT_BUY_PRICE) {
        return
    }
    exchange.SetDirection("buy")
    let orderId = exchange.Buy(ticker.Last, getManyQuantity())
    if (!orderId) {
        return
    }
    MANY_BUYING = true
    MANY_BUY_TIME = Unix()
    while (true) {
        let now = Unix()
        let order = exchange.GetOrder(orderId)
        let expire = MANY_BUY_TIME + (60 * 30)
        if (null === order) {
            continue
        }
        // Purchase successfully processed
        if (1 === order.Status || 2 === order.Status) {
            MANY_NEXT_BUY_PRICE = order.Price * ((100 - DOUBLE_THROW_RATIO) / 100)
            MANY_STEP = MANY_STEP + 1
            MANY_BUYING = false
            MANY_EMPTY_STEP_TIME = null
            let sellPrice = order.Price * ((100 + PROFIT_RATIO) / 100)
            MANY_ORDER_LIST.push({
                buyPrice: order.Price,
                sellPrice: sellPrice,
                quantity: order.Amount,
                isSell: false,
            })
            break
        }
        // Buy timeout processing
        if (now >= expire) {
            exchange.CancelOrder(orderId)
            MANY_BUYING = false
            MANY_BUY_TIME = null
            MANY_NEXT_BUY_PRICE = ticker.Last * ((100 - DOUBLE_THROW_RATIO) / 100)
            return
        }
    }
}

function shortBuy(ticker) {
    if (SHORT_BUYING) {
        return
    }
    Log('ticker: ' + ticker.Last + ' SHORT_NEXT_BUY_PRICE: ' + SHORT_NEXT_BUY_PRICE)
    if (ticker.Last < SHORT_NEXT_BUY_PRICE) {
        return
    }
    exchange.SetDirection("sell")
    let orderId = exchange.Sell(ticker.Last, getShortQuantity())
    if (!orderId) {
        return
    }
    SHORT_BUYING = true
    SHORT_BUY_TIME = Unix()
    while (true) {
        let now = Unix()
        let expire = SHORT_BUY_TIME + (60 * 30)
        let order = exchange.GetOrder(orderId)
        if (null === order) {
            continue
        }
        // Purchase successfully processed
        if (1 === order.Status || 2 === order.Status) {
            SHORT_NEXT_BUY_PRICE = order.Price * ((100 + DOUBLE_THROW_RATIO) / 100)
            SHORT_STEP = SHORT_STEP + 1
            SHORT_BUYING = false
            SHORT_EMPTY_STEP_TIME = null
            let sellPrice = order.Price * ((100 - PROFIT_RATIO) / 100)
            SHORT_ORDER_LIST.push({
                buyPrice: order.Price,
                sellPrice: sellPrice,
                quantity: order.Amount,
                isSell: false,
            })
            break
        }
        // Buy timeout processing
        if (now >= expire) {
            exchange.CancelOrder(orderId)
            SHORT_BUYING = false
            SHORT_BUY_TIME = null
            SHORT_NEXT_BUY_PRICE = ticker.Last * ((100 + DOUBLE_THROW_RATIO) / 100)
            return
        }
    }
}


function manySell(ticker) {
    // Traverse sell orders
    for (let item of MANY_ORDER_LIST) {
        if (item.isSell) {
            continue
        }
        if (ticker.Last >= item.sellPrice) {
            item.isSell = true;
            exchange.SetDirection("closebuy")
            let orderId = exchange.Sell(ticker.Last, item.quantity)
            if (!orderId) {
                return
            }
            while (true) {
                let order = exchange.GetOrder(orderId)
                if (null === order) {
                    continue
                }
                if (1 === order.Status || 2 === order.Status) {
                    MANY_NEXT_BUY_PRICE = ticker.Last * ((100 - BUY_PRICE_RATIO) / 100)
                    MANY_STEP = MANY_STEP - 1
                    if (0 === MANY_STEP) {
                        MANY_EMPTY_STEP_TIME = Unix()
                    }
                    break
                }
            }
        }
    }
}

function shortSell(ticker) {
    // Traverse sell orders
    for (let item of SHORT_ORDER_LIST) {
        if (item.isSell) {
            continue
        }
        if (ticker.Last <= item.sellPrice) {
            item.isSell = true;
            exchange.SetDirection("closesell")
            let orderId = exchange.Buy(ticker.Last, item.quantity)
            if (!orderId) {
                return
            }
            while (true) {
                let order = exchange.GetOrder(orderId)
                if (null === order) {
                    continue
                }
                if (1 === order.Status || 2 === order.Status) {
                    SHORT_NEXT_BUY_PRICE = ticker.Last * ((100 + BUY_PRICE_RATIO) / 100)
                    SHORT_STEP = SHORT_STEP - 1
                    if (0 === SHORT_STEP) {
                        SHORT_EMPTY_STEP_TIME = Unix()
                    }
                    break
                }
            }
        }
    }
}

function check(ticker) {
    let now = Unix()
    if (null !== CHECK_TIME) {
        let expire = CHECK_TIME + (60 * 10)
        if (now < expire) {
            return
        }
    }
    CHECK_TIME = now

    if (null !== MANY_EMPTY_STEP_TIME) {
        let expire = MANY_EMPTY_STEP_TIME + (60 * 30)
        if (now >= expire) {
            MANY_NEXT_BUY_PRICE = ticker.Last * ((100 - DOUBLE_THROW_RATIO) / 100)
            Log('No long positions, Adjust Buying Price: ' + MANY_NEXT_BUY_PRICE)
        }
    }
    
    if (null !== SHORT_EMPTY_STEP_TIME) {
        let expire = SHORT_EMPTY_STEP_TIME + (60 * 30)
        if (now >= expire) {
            SHORT_NEXT_BUY_PRICE = ticker.Last * ((100 + DOUBLE_THROW_RATIO) / 100)
            Log('No short positions, Adjust Buying Price: ' + SHORT_NEXT_BUY_PRICE)
        }
    }
}

function onTick() {
    // Write strategy logic here, will be called repeatedly, e.g., to print market information
    let ticker = exchange.GetTicker()
    if (!ticker) {
        return
    }
    if (FIRST_BUY) {
        // First long buy
        firstManyBuy(ticker)
        // First short buy
        firstShortBuy(ticker)
        FIRST_BUY = false
        return
    }
    
    // Long Buy
    manyBuy(ticker)
    // Short Buy
    shortBuy(ticker)
    // Long Sell
    manySell(ticker)
    // Short Sell
    shortSell(ticker)
    // Empty Position Detection
    check(ticker)
}

function main() {
    // Open contract
    exchange.SetContractType("swap")

    while(true){
        onTick()
        // Sleepfunctions are mainly used to control the polling frequency of digital currency strategies and prevent access to exchangesAPIinterfaces are too frequent
        Sleep(60000)
    }
}

```

> Detail

https://www.fmz.com/strategy/293325

> Last Modified

2021-06-28 17:37:41
