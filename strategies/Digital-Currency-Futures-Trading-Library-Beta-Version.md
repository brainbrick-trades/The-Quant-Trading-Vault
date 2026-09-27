
> Name

Digital-Currency-Futures-Trading-Library-Beta-Version

> Author

发明者量化-小小梦

> Strategy Description

## Cryptocurrency futures trading library (test version))

- mainThe function is a test function, calling example

Feel free to leave a message if you have questions.

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|Interval|500|Retry interval on failure (milliseconds))|
|MinAmount|true|Minimum trading quantity|
|SlidePrice|5|Order Slippage|


> Source (javascript)

``` javascript
// Parameters
/*
var MinAmount = 1
var SlidePrice = 5
var Interval = 500
*/

function GetPosition(e, contractType, direction) {
    e.SetContractType(contractType)
    var positions = _C(e.GetPosition);
    for (var i = 0; i < positions.length; i++) {
        if (positions[i].ContractType == contractType && positions[i].Type == direction) {
            return positions[i]
        }
    }

    return null
}

function Open(e, contractType, direction, opAmount) {
    var initPosition = GetPosition(e, contractType, direction);
    var isFirst = true;
    var initAmount = initPosition ? initPosition.Amount : 0;
    var nowPosition = initPosition;
    var directBreak = false 
    var preNeedOpen = 0
    var timeoutCount = 0
    while (true) {
        var ticker = _C(e.GetTicker)
        var needOpen = opAmount;
        if (isFirst) {
            isFirst = false;
        } else {
            nowPosition = GetPosition(e, contractType, direction);
            if (nowPosition) {
                needOpen = opAmount - (nowPosition.Amount - initAmount);
            }
            // DetectdirectBreak And when the position has not changed
            if (preNeedOpen == needOpen && directBreak) {
                Log("Suspected position data delay, waiting30second", "#FF0000")
                Sleep(30000)
                nowPosition = GetPosition(e, contractType, direction);
                if (nowPosition) {
                    needOpen = opAmount - (nowPosition.Amount - initAmount);
                }
                /*
                timeoutCount++
                if (timeoutCount > 10) {
                    Log("Continuous10Suspected position delays, order placement failed!", "#FF0000")
                    break
                }
                */
            } else {
                timeoutCount = 0
            }
        }
        if (needOpen < MinAmount) {
            break;
        }
        
        var amount = needOpen;
        preNeedOpen = needOpen
        e.SetDirection(direction == PD_LONG ? "buy" : "sell");
        var orderId;
        if (direction == PD_LONG) {
            orderId = e.Buy(ticker.Sell + SlidePrice, amount, "Open long position", contractType, ticker);
        } else {
            orderId = e.Sell(ticker.Buy - SlidePrice, amount, "Open short position", contractType, ticker);
        }

        directBreak = false
        var n = 0
        while (true) {
            Sleep(Interval);
            var orders = _C(e.GetOrders);
            if (orders.length == 0) {
                if (n == 0) {
                    directBreak = true
                }
                break;
            }
            for (var j = 0; j < orders.length; j++) {
                e.CancelOrder(orders[j].Id);
                if (j < (orders.length - 1)) {
                    Sleep(Interval);
                }
            }
            n++
        }
    }

    var ret = {
        price: 0,
        amount: 0,
        position: nowPosition
    };
    if (!nowPosition) {
        return ret;
    }
    if (!initPosition) {
        ret.price = nowPosition.Price;
        ret.amount = nowPosition.Amount;
    } else {
        ret.amount = nowPosition.Amount - initPosition.Amount;
        ret.price = _N(((nowPosition.Price * nowPosition.Amount) - (initPosition.Price * initPosition.Amount)) / ret.amount);
    }
    return ret;
}

function Cover(e, contractType, opAmount, direction) {
    var initPosition = null;
    var position = null;
    var isFirst = true;

    while (true) {
        while (true) {
            Sleep(Interval);
            var orders = _C(e.GetOrders);
            if (orders.length == 0) {
                break;
            }
            for (var j = 0; j < orders.length; j++) {
                e.CancelOrder(orders[j].Id);
                if (j < (orders.length - 1)) {
                    Sleep(Interval);
                }
            }
        }

        position = GetPosition(e, contractType, direction)
        if (!position) {
            break
        }
        if (isFirst == true) {
            initPosition = position;
            opAmount = Math.min(opAmount, initPosition.Amount)
            isFirst = false;
        }

        var amount = opAmount - (initPosition.Amount - position.Amount)
        if (amount <= 0) {
            break
        }

        var ticker = _C(e.GetTicker)
        if (position.Type == PD_LONG) {
            e.SetDirection("closebuy");
            e.Sell(ticker.Buy - SlidePrice, amount, "Close Long Position", contractType, ticker);
        } else if (position.Type == PD_SHORT) {
            e.SetDirection("closesell");
            e.Buy(ticker.Sell + SlidePrice, amount, "Close Short Position", contractType, ticker);
        }

        Sleep(Interval)
    }

    return position
}

$.OpenLong = function(e, contractType, amount) {
    if (typeof(e) == "string") {
        amount = contractType
        contractType = e
        e = exchange
    }

    return Open(e, contractType, PD_LONG, amount);
}

$.OpenShort = function(e, contractType, amount) {
    if (typeof(e) == "string") {
        amount = contractType
        contractType = e
        e = exchange
    }

    return Open(e, contractType, PD_SHORT, amount);
};

$.CoverLong = function(e, contractType, amount) {
    if (typeof(e) == "string") {
        amount = contractType
        contractType = e
        e = exchange
    }

    return Cover(e, contractType, amount, PD_LONG);
};

$.CoverShort = function(e, contractType, amount) {
    if (typeof(e) == "string") {
        amount = contractType
        contractType = e
        e = exchange
    }

    return Cover(e, contractType, amount, PD_SHORT);
};


function main() {
    Log(exchange.GetPosition())
    var info = $.OpenLong(exchange, "quarter", 100)
    Log(info, "#FF0000")

    Log(exchange.GetPosition())
    info = $.CoverLong(exchange, "quarter", 30)
    Log(exchange.GetPosition())
    Log(info, "#FF0000")

    info = $.CoverLong(exchange, "quarter", 80)
    Log(exchange.GetPosition())
    Log(info, "#FF0000")
}
```

> Detail

https://www.fmz.com/strategy/203258

> Last Modified

2022-01-07 09:42:47
