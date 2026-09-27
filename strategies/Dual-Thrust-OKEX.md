
> Name

Dual-Thrust-OKEX

> Author

发明者量化-小小梦

> Strategy Description

> Basic principle

- At the close of the day, two values are calculated: high price - closing price, and closing price - low price. Then take the larger of the two values and multiply it by the k value. The result is called the trigger value.
- At the opening of the next day, record the opening price, and then buy immediately when the price exceeds (opening + trigger value), or sell short when the price is lower than (opening - trigger value).
- This system is a reversal system with no separate stop-loss. That is, a reverse signal is also a closing signal.


> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|NPeriod|4|Calculation cycle|
|Ks|0.5|Upper rail coefficient|
|Kx|0.5|Lower rail coefficient|
|AmountOP|true|Open contract quantity|


> Source (javascript)

``` javascript
var STATE_IDLE = 0
var STATE_LONG = 1
var STATE_SHORT = 2
var State = STATE_IDLE
var LastBarTime = 0
var UpTrack = 0
var DownTrack = 0
var InitAccount = null

function GetPosition(posType) {
    var positions = exchange.GetPosition()
    for (var i = 0; i < positions.length; i++) {
        if (positions[i].Type === posType) {
            return [positions[i].Price, positions[i].Amount];
        }
    }
    return [0, 0]
}

function CancelPendingOrders() {
    while (true) {
        var orders = exchange.GetOrders()
        for (var i = 0; i < orders.length; i++) {
            exchange.CancelOrder(orders[i].Id)
            Sleep(500)
        }
        if (orders.length === 0) {
            break
        }
    }
}

function Trade(currentState, nextState) {
    var pfn = nextState === STATE_LONG ? exchange.Buy : exchange.Sell
    if (currentState !== STATE_IDLE) {
        exchange.SetDirection(currentState === STATE_LONG ? "closebuy" : "closesell")
        while (true) {
            var amount = GetPosition(currentState === STATE_LONG ? PD_LONG : PD_SHORT)[1]
            if (amount === 0) {
                break
            }
            pfn(nextState === STATE_LONG ? _C(exchange.GetTicker).Sell * 1.001 : _C(exchange.GetTicker).Buy * 0.999, amount)
            Sleep(500)
            CancelPendingOrders()
        }
        var account = exchange.GetAccount()
        LogProfit(_N(account.Stocks - InitAccount.Stocks, 3), "Yield:", _N((account.Stocks - InitAccount.Stocks) * 100 / InitAccount.Stocks, 3) + '%')
    }
    exchange.SetDirection(nextState === STATE_LONG ? "buy" : "sell")
    while (true) {
        var pos = GetPosition(nextState === STATE_LONG ? PD_LONG : PD_SHORT)
        if (pos[1] >= AmountOP) {
            Log("Average position price", pos[0], "Quantity:", pos[1])
            break
        }
        pfn(nextState === STATE_LONG ? _C(exchange.GetTicker).Sell * 1.001 : _C(exchange.GetTicker).Buy * 0.999, AmountOP-pos[1])
        Sleep(500)
        CancelPendingOrders()
    }
}

function onTick() {
    var records = exchange.GetRecords()
    if (!records || records.length <= NPeriod) {
        return
    }
    var Bar = records[records.length - 1]
    $.PlotRecords(records, 'KLine')
    if (LastBarTime !== Bar.Time) {
        var HH = TA.Highest(records, NPeriod, 'High')
        var HC = TA.Highest(records, NPeriod, 'Close')
        var LL = TA.Lowest(records, NPeriod, 'Low')
        var LC = TA.Lowest(records, NPeriod, 'Close')
        var Range = Math.max(HH - LC, HC - LL)
        UpTrack = _N(Bar.Open + (Ks * Range), 3)
        DownTrack = _N(Bar.Open - (Kx * Range), 3)
        $.PlotHLine(UpTrack, 'UpTrack')
        $.PlotHLine(DownTrack, 'DownTrack')
        LastBarTime = Bar.Time
    }

    LogStatus("Price:", Bar.Close, "Up:", UpTrack, "Down:", DownTrack, "Date:", new Date())
    var msg
    if (State === STATE_IDLE || State === STATE_SHORT) {
        if (Bar.Close >= UpTrack) {
            msg  = 'Long trigger price: ' + Bar.Close + ' Upper rail:' + UpTrack
            Log(msg)
            Trade(State, STATE_LONG)
            State = STATE_LONG
            $.PlotFlag(Bar.Time, msg, 'Many', 'flag', 'red') 
        }
    }

    if (State === STATE_IDLE || State === STATE_LONG) {
        if (Bar.Close <= DownTrack) {
            msg = 'Short trigger price: ' + Bar.Close + ' Lower Band:' + DownTrack
            Log(msg)
            Trade(State, STATE_SHORT)
            $.PlotFlag(Bar.Time, msg, 'Empty', 'circlepin', 'green')
            State = STATE_SHORT
        }
    }
}

function main() {
    exchange.SetContractType("quarter")
    exchange.SetMarginLevel(10)
    if (exchange.GetPosition().length > 0) {
        throw "No positions should exist before strategy starts."
    }
    CancelPendingOrders()
    InitAccount = exchange.GetAccount()
    while (true) {
        onTick()
        Sleep(500)
    }
}
```

> Detail

https://www.fmz.com/strategy/112425

> Last Modified

2020-02-24 09:56:09
