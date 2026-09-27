
> Name

HUSD-USD-Stablecoin-Arbitrage

> Author

一拳男孩

> Strategy Description

### HUSD/USDT Stablecoin Arbitrage
Huobi had a promotion for a while, no fees in the HUSD area, so I made a script to take advantage of it.
Perform stable arbitrage based on the characteristic that it always **reverts to 1**


> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|MAX_ATR|0.0001|Maximum average width|
|ORDER_AMOUNT|1000|Single order quantity|
|PRICE_CEIL|false|(?Price range) resistance level|
|PRICE_FLOOR|false|support level|
|FEE_RATE|false|(?Profit rate) handling fee|
|PROFIT_RATE|1e-05|profit margin|
|PRICE_PRECISION|4|(?Accuracy) Price Accuracy|
|AMOUNT_PRECISION|4|Order quantity accuracy|
|MIN_ORDER_AMOUNT|true|Minimum order quantity|




|Button|Default|Description|
|----|----|----|
|profitRate|1e-05|profit margin|
|orderAmount|1000|Single order quantity|
|Start|__button__|Start|
|Pause|__button__|Pause|
|priceCeil|false|(?Price range) resistance level|
|priceFloor|false|support level|
|maxATR|0.0001|Maximum average width|


> Source (javascript)

``` javascript
var _running = false
var _tickTimeCost = 0
var _profit = _G('profit') || 0
var _config = {
    orderAmount: ORDER_AMOUNT,
    priceCeil: PRICE_CEIL,
    priceFloor: PRICE_FLOOR,
    maxATR: MAX_ATR,
    profitRate: PROFIT_RATE
}
var _arbitCount = _G('arbit_count') || 0
var _depthHistory = _G('depth_history') || []

function getNow() {
    return UnixNano() / 1000000
}

function getDepth() {
    var depth = _C(exchange.GetDepth)
    _depthHistory.push(depth)
    _depthHistory = _depthHistory.slice(-5)
    _G('_depthHistory', JSON.stringify(_depthHistory))
    return depth
}

function getBase(ex) {
    return ex.GetCurrency().split('_')[0]
}

function getTypeText(type) {
    var list = [
        [ORDER_TYPE_BUY, 'Buy', 'purchase', '#01bf6a'],
        [ORDER_TYPE_SELL, 'Sell', 'sell', '#ff0000']
    ]
    var found = _.find(list, function(items) {
        return items[0] === type || items[1] === type
    })
    return found ? found[2] + found[3] : ''
}

function getPriceTypeText(type) {
    if (type === 0) {
        return 'opponent price'
    } else if (type === 1) {
        return 'transaction price'
    } else if (type === 2) {
        return 'Hang up1price'
    }
}

function getStatusText(st, showColor) {
    showColor = showColor == null ? true : showColor
    var list = [
        [ORDER_STATE_CLOSED, 'completed', '#f4b300'],
        [ORDER_STATE_PENDING, 'not completed', '#000000'],
        [ORDER_STATE_CANCELED, 'canceled', '#a3a3a3'],
        [ORDER_STATE_UNKNOWN, 'Unknown status', '#777777']
    ]
    var found = _.find(list, function(item) {
        return item[0] === st
    })
    return found && found.length > 0 ? found[1] + (showColor ? found[2] : '') : ''
}

function logMyProfit(num) {
    var newProfit = _profit + num
    if (newProfit !== _profit) {
        LogProfit(newProfit)
        _profit = newProfit
        _G('profit', _profit)
    }
}

function cancelOrder(id) {
    while (1) {
        var order = _C(exchange.GetOrder, id)
        if (order.Status === ORDER_STATE_PENDING) {
            exchange.CancelOrder(id)
        } else {
            return
        }
        Sleep(200)
    }
}

function getLastATR() {
    var askPrices = _.flatten(_.pluck(_depthHistory, 'Asks').map(function(d) { return d[0].Price }))
    var slicedPrices = askPrices.slice(-5)
    var avgPrice = new Decimal(_.reduce(slicedPrices, function(p, n) {
        return new Decimal(p).plus(n).toNumber()
    }, 0)).div(slicedPrices.length).toNumber()
    var askVaiance = new Decimal(_.reduce(slicedPrices, function(p, n) {
        return new Decimal(p).plus(new Decimal(n).minus(avgPrice).pow(2)).toNumber()
    }, 0)).div(slicedPrices.length).toNumber()
    var askSD = new Decimal(askVaiance).sqrt().toNumber()
    return askSD
}

function getHighestPrice() {
    var records = _C(exchange.GetRecords, PERIOD_H1)
    var highestPrice = TA.Highest(records, 8, 'Close')
    return highestPrice
}

function onTick() {
    var depth = getDepth() //_C(exchange.GetDepth)
    var arbitOrders = JSON.parse(_G('arbit_orders')) || []

    arbitOrders = _.map(arbitOrders, function(arbitOrder) {
        if (arbitOrder.Status === ORDER_STATE_CLOSED) {
            var buyOrder = arbitOrder.BuyOrder || {}
            var sellOrder = arbitOrder.SellOrder || {}
            var buyTradePrice = new Decimal(buyOrder.AvgPrice || 0).mul(buyOrder.DealAmount || 0).toNumber()
            var sellTradePrice = new Decimal(sellOrder.AvgPrice || 0).mul(sellOrder.DealAmount || 0).toNumber()
            var profit = new Decimal(sellTradePrice).minus(buyTradePrice).toNumber()
            if (profit > 0) {
                _arbitCount++
                _G('arbit_count', _arbitCount)
                logMyProfit(profit)
                $.ddNotice('Arbitrage successful', [
                    '### Arbitrage successful',
                    '- Buy Price: ' + buyOrder.Price,
                    '- Sell Price: ' + sellOrder.Price,
                    '- Buy Volume: ' + buyOrder.DealAmount,
                    '- Sell Volume: ' + sellOrder.DealAmount,
                    '- Buy transaction amount: ' + buyTradePrice,
                    '- Selling transaction amount: ' + sellTradePrice,
                    '- profit: ' + profit,
                    '- time-consuming: ' + ((getNow() - arbitOrder.CreatedAt) / 1000).toFixed(2) + 's',
                ])
            }
            return null
        }
        return arbitOrder
    })
    arbitOrders = _.compact(arbitOrders)
    _G('arbit_orders', JSON.stringify(arbitOrders))

    arbitOrders = _.map(arbitOrders, function(arbitOrder) {
        if (arbitOrder.Status === ORDER_STATE_PENDING) {
            var buyOrder = _C(exchange.GetOrder, arbitOrder.BuyOrder.Id)
            var sellOrder = arbitOrder.SellOrder ? _C(exchange.GetOrder, arbitOrder.SellOrder.Id) : null

            // Mark order completed
            if (buyOrder && sellOrder && buyOrder.Status !== ORDER_STATE_PENDING && sellOrder.Status !== ORDER_STATE_PENDING) {
                return _.extend(arbitOrder, {
                    Status: ORDER_STATE_CLOSED,
                    BuyOrder: buyOrder,
                    SellOrder: sellOrder,
                })
            }

            // Initiate a sell order after the purchase is completed
            if (buyOrder.Status !== ORDER_STATE_PENDING && !sellOrder) {
                var sellAmount = _N(buyOrder.DealAmount, AMOUNT_PRECISION)
                if (sellAmount >= MIN_ORDER_AMOUNT) {
                    var sellPrice = +(new Decimal(buyOrder.Price).mul(1 + FEE_RATE).div(1 - _config.profitRate).div(1 - FEE_RATE).toFixed(PRICE_PRECISION, Decimal.ROUND_UP))
                    var sellId = exchange.Sell(sellPrice, sellAmount)
                    if (sellId) {
                        sellOrder = _C(exchange.GetOrder, sellId)
                    }
                } else {
                    return _.extend(arbitOrder, {
                        Status: ORDER_STATE_CLOSED
                    })
                }
            }

            if (buyOrder.Status === ORDER_STATE_PENDING) {
                /*
                Cancellation conditions
                1. Buy 1 price changes
                2. The amplitude fluctuates beyond the set value
                3. When the amount of buy 1 equals the remaining amount of the buy order (meaning you placed the order yourself).)
                */
                if (buyOrder.Price !== depth.Bids[0].Price || getLastATR() > _config.maxATR || depth.Bids[0].Amount === _N(new Decimal(buyOrder.Amount).minus(buyOrder.DealAmount).toNumber(), AMOUNT_PRECISION)) {
                    cancelOrder(buyOrder.Id)
                    buyOrder = _C(exchange.GetOrder, buyOrder.Id)
                }
            }

            return _.extend(arbitOrder, {
                BuyOrder: buyOrder,
                BuyPrice: buyOrder.Price,
                SellOrder: sellOrder,
                SellPrice: sellOrder ? sellOrder.Price || 0 : 0
            })
        }
        return arbitOrder
    })

    _G('arbit_orders', JSON.stringify(arbitOrders))

    var buyPrice = depth.Bids[0].Price
    
    // A new round only begins after the previous buy order at the same price ends
    if (!_.findWhere(arbitOrders, {
            Status: ORDER_STATE_PENDING,
            BuyPrice: buyPrice
        }) && buyPrice >= _config.priceFloor && buyPrice <= (_config.priceCeil > 0 ? _config.priceCeil : getHighestPrice()) && getLastATR() <= _config.maxATR) {
        var account = _C(exchange.GetAccount)
        var buyTradePrice = _N(new Decimal(buyPrice).mul(_config.orderAmount).toNumber(), PRICE_PRECISION)
        if (account.Balance >= buyTradePrice) {
            var buyId = exchange.Buy(buyPrice, _config.orderAmount)
            if (buyId) {
                var buyOrder = _C(exchange.GetOrder, buyId)
                arbitOrders.push({
                    Status: ORDER_STATE_PENDING,
                    BuyOrder: buyOrder,
                    BuyPrice: buyPrice,
                    SellOrder: null,
                    SellPrice: 0,
                    CreatedAt: getNow()
                })
                _G('arbit_orders', JSON.stringify(arbitOrders))
            }
        }

    }
}

function logMyStatus() {
    var account = _C(exchange.GetAccount)
    var arbitOrders = JSON.parse(_G('arbit_orders')) || []
    var basicStatus = {
        type: 'table',
        title: 'Basic information',
        cols: ['Running status', 'Time consuming', 'Number of arbitrage', 'Achieved profit and loss', 'Maximum average range (last 5 sales 1 standard deviation | set maximum value)', 'Single order amount', 'Resistance level', 'Support level''],
        rows: [
            [
                _running ? 'Running#01c401' : 'Not running#a3a3a3',
                new Date().toLocaleString() + ' - ' + (_tickTimeCost / 1000).toFixed(2) + 's',
                _arbitCount,
                (_profit || 0) + '#ff0000',
                getLastATR() + ' | ' + _config.maxATR,
                _config.orderAmount,
                _config.priceCeil > 0 ? _config.priceCeil : getHighestPrice(),
                _config.priceFloor
            ]
        ]
    }

    var assetsStatus = {
        type: 'table',
        title: 'Asset information',
        cols: [exchanges[0].GetQuoteCurrency() + ' (Available | freeze)', getBase(exchanges[0]) + ' (Available | freeze)'],
        rows: [
            [
                new Decimal(account.Balance).plus(account.FrozenBalance).toNumber() + ' (' + account.Balance + ' | ' + account.FrozenBalance + ')',
                new Decimal(account.Stocks).plus(account.FrozenStocks).toNumber() + ' (' + account.Stocks + ' | ' + account.FrozenStocks + ')',
            ]
        ]
    }

    var arbitOrdersStatus = {
        type: 'table',
        title: 'Arbitrage order list',
        cols: ['Arbitrage status', 'Buy order (Status | Price | Volume)', 'Sell order (Status | Price | Volume)', 'Creation time'],
        rows: _.map(arbitOrders, function(arbitOrder) {
            var sideOrders = _.map([arbitOrder.BuyOrder, arbitOrder.SellOrder], function(order) {
                if (order) {
                    return getStatusText(order.Status, false) + ' | ' + order.Price + ' | ' + order.DealAmount
                } else {
                    return '-'
                }
            })
            return [getStatusText(arbitOrder.Status), sideOrders[0], sideOrders[1], new Date(arbitOrder.CreatedAt).toLocaleString()]
        })
    }

    var statusList = _.flatten([
        basicStatus,
        assetsStatus,
        arbitOrdersStatus
    ])

    LogStatus(_.compact(statusList).map(function(d) {
        return '`' + JSON.stringify(d) + '`'
    }).join('\n'))
}

function main() {
    _.each(_config, function(v, k) {
        $.BindingFunc(k, function(cmd, val) {
            if (typeof(v) === 'number') {
                val = +val
            }
            _config[k] = val
        })
    })
    $.BindingFunc("Start", function() {
        _running = true
    })
    $.BindingFunc("pause", function() {
        _running = false
    })
    while (true) {
        var _tickStartTime = getNow()
        LogReset(1000)
        $.GetCommand()
        if (_running) {
            onTick()
        }
        _tickTimeCost = getNow() - _tickStartTime
        logMyStatus()
        Sleep(500)
    }
}
```

> Detail

https://www.fmz.com/strategy/164047

> Last Modified

2022-02-16 01:28:18
