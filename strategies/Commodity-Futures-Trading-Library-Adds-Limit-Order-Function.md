
> Name

Commodity-Futures-Trading-Library-Adds-Limit-Order-Function

> Author

edwardgyw

> Strategy Description

6.24Updated, improved 4 night trading time types, Saturday morning night trading time is included in the trading period
Based on the original zero version, it adds lower limit orders and flat limit orders to facilitate order placement
Added the function of determining whether it is a trading session, and also provided the function of customizing holidays

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|Interval|500|Retry interval on failure (milliseconds))|
|SlidePrice|false|Order slippage (Yuan))|
|nightType|true|Night session situation of the commodity|
|holidaysList|5.1,5.2|Holiday situation|


> Source (javascript)

``` javascript
function GetPosition(e, contractType, direction) {
    var allCost = 0;
    var allAmount = 0;
    var allProfit = 0;
    var allFrozen = 0;
    var posMargin = 0;
    var positions = _C(e.GetPosition);
    for (var i = 0; i < positions.length; i++) {
        if (positions[i].ContractType == contractType &&
            (((positions[i].Type == PD_LONG || positions[i].Type == PD_LONG_YD) && direction == PD_LONG) || ((positions[i].Type == PD_SHORT || positions[i].Type == PD_SHORT_YD) && direction == PD_SHORT))
        ) {
            posMargin = positions[i].MarginLevel;
            allCost += (positions[i].Price * positions[i].Amount);
            allAmount += positions[i].Amount;
            allProfit += positions[i].Profit;
            allFrozen += positions[i].FrozenAmount;
        }
    }
    if (allAmount === 0) {
        return null;
    }
    return {
        MarginLevel: posMargin,
        FrozenAmount: allFrozen,
        Price: _N(allCost / allAmount),
        Amount: allAmount,
        Profit: allProfit,
        Type: direction,
        ContractType: contractType
    };
}



function Open(e, contractType, direction, opAmount, price) {
    var initPosition = GetPosition(e, contractType, direction);
    var isFirst = true;
    var initAmount = initPosition ? initPosition.Amount : 0;
    var positionNow = initPosition;
    while (true) {
        var needOpen = opAmount;
        if (isFirst) {
            isFirst = false;
        } else {
            positionNow = GetPosition(e, contractType, direction);
            if (positionNow) {
                needOpen = opAmount - (positionNow.Amount - initAmount);
            }
        }
        var insDetail = _C(e.SetContractType, contractType);
        //Log("Initial position", initAmount, "Current position", positionNow, "Need to Add Position", needOpen);
        if (needOpen < insDetail.MinLimitOrderVolume) {
            break;
        }
        var depth = _C(e.GetDepth);
        var pr = price;
        if (!price) pr = direction == PD_LONG ? depth.Asks[0].Price : depth.Bids[0].Price;
        var amount = Math.min(insDetail.MaxLimitOrderVolume, needOpen);
        e.SetDirection(direction == PD_LONG ? "buy" : "sell");
        var orderId;
        if (direction == PD_LONG) {
            orderId = e.Buy(pr + SlidePrice, Math.min(amount, depth.Asks[0].Amount), contractType, 'Ask', depth);
        } else {
            orderId = e.Sell(pr - SlidePrice, Math.min(amount, depth.Bids[0].Amount), contractType, 'Bid', depth);
        }
        // CancelPendingOrders
        while (true) {
            Sleep(Interval);
            var orders = _C(e.GetOrders);
            if (orders.length === 0) {
                break;
            }
            for (var j = 0; j < orders.length; j++) {
                e.CancelOrder(orders[j].Id);
                if (j < (orders.length - 1)) {
                    Sleep(Interval);
                }
            }
        }
    }
    var ret = {
        price: 0,
        amount: 0,
        position: positionNow
    };
    if (!positionNow) {
        return ret;
    }
    if (!initPosition) {
        ret.price = positionNow.Price;
        ret.amount = positionNow.Amount;
    } else {
        ret.amount = positionNow.Amount - initPosition.Amount;
        ret.price = _N(((positionNow.Price * positionNow.Amount) - (initPosition.Price * initPosition.Amount)) / ret.amount);
    }
    return ret;
}

function Cover(e, contractType, price) {
    var insDetail = _C(e.SetContractType, contractType);
    while (true) {
        var n = 0;
        var positions = _C(e.GetPosition);
        for (var i = 0; i < positions.length; i++) {
            if (positions[i].ContractType != contractType) {
                continue;
            }
            while (positions[i].FrozenAmount !== 0) {
                var orders = _C(e.GetOrders);
                if (orders.length === 0) {
                    break;
                }
                for (var j = 0; j < orders.length; j++) {
                    e.CancelOrder(orders[j].Id);
                    if (j < (orders.length - 1)) {
                        Sleep(Interval);
                    }
                }
                positions = _C(e.GetPosition);
            }
            var amount = Math.min(insDetail.MaxLimitOrderVolume, positions[i].Amount);
            var depth;
            if (positions[i].Type == PD_LONG || positions[i].Type == PD_LONG_YD) {
                depth = _C(e.GetDepth);
                var pr = price;
                if (!price) pr = depth.Bids[0].Price;
                e.SetDirection(positions[i].Type == PD_LONG ? "closebuy_today" : "closebuy");
                e.Sell(pr - SlidePrice, Math.min(amount, depth.Bids[0].Amount), contractType, positions[i].Type == PD_LONG ? "Today's close" : "Yesterday's close", 'Bid', depth.Bids[0]);
                n++;
            } else if (positions[i].Type == PD_SHORT || positions[i].Type == PD_SHORT_YD) {
                depth = _C(e.GetDepth);
                var pr = price;
                if (!price) pr = depth.Asks[0].Price;
                e.SetDirection(positions[i].Type == PD_SHORT ? "closesell_today" : "closesell");
                e.Buy(pr + SlidePrice, Math.min(amount, depth.Asks[0].Amount), contractType, positions[i].Type == PD_SHORT ? "Today's close" : "Yesterday's close", 'Ask', depth.Asks[0]);
                n++;
            }
        }
        if (n === 0 || price) {
            break;
        }
        while (true) {
            Sleep(Interval);
            var orders = _C(e.GetOrders);
            if (orders.length === 0) {
                break;
            }
            for (var j = 0; j < orders.length; j++) {
                e.CancelOrder(orders[j].Id);
                if (j < (orders.length - 1)) {
                    Sleep(Interval);
                }
            }
        }
    }
}


var PositionManager = (function() {
    function PositionManager(e) {
        if (typeof(e) === 'undefined') {
            e = exchange;
        }
        if (e.GetName() !== 'Futures_CTP') {
            throw 'Only support CTP';
        }
        this.e = e;
        this.account = null;
    }
    PositionManager.prototype.GetAccount = function() {
        return _C(this.e.GetAccount);
    };

    PositionManager.prototype.OpenLong = function(contractType, shares, price) {
        if (!this.account) {
            this.account = _C(exchange.GetAccount);
        }
        return Open(this.e, contractType, PD_LONG, shares, price, price);
    };

    PositionManager.prototype.OpenShort = function(contractType, shares, price) {
        if (!this.account) {
            this.account = _C(exchange.GetAccount);
        }
        return Open(this.e, contractType, PD_SHORT, shares, price);
    };

    PositionManager.prototype.Cover = function(contractType, price) {
        if (!this.account) {
            this.account = _C(exchange.GetAccount);
        }
        return Cover(this.e, contractType, price);
    };

    PositionManager.prototype.Profit = function(contractType) {
        var accountNow = _C(this.e.GetAccount);
        return _N(accountNow.Balance - this.account.Balance);
    };

    return PositionManager;
})();

$.NewPositionManager = function(e) {
    return new PositionManager(e);
};

function getHolidays(holidaysList) {
    if (!holidaysList) return {
        'mon': [],
        'day': []
    };
    var x = holidaysList.split(',');
    var t = {
        'mon': [],
        'day': []
    };
    for (var i = 0; i < x.length; i++) {
        var m = x[i].split('.');
        t.mon.push(m[0]);
        t.day.push(m[1]);
    }
    return t;
}

$.judgeTrading = function() {
    var now = new Date();
    var day = now.getDay();
    var mon = now.getMonth() + 1;
    var min = now.getMinutes();
    var date = now.getDate();
    var hours = now.getHours();
    var isHolidays = false;
    var holidays = getHolidays(holidaysList);
    if (holidays) {
        for (var i = 0; i < holidays.mon.length; i++) {
            if (holidays.mon[i] == mon && holidays.day[i] == date) {
                isHolidays = true;
                break;
            }
        }
    }
    if (day === 0 || (day === 6 && hours>=3) || isHolidays) return false;
    else if ((hours >= 9 && hours <= 11) || (hours >= 13 && hours < 15)) {
        if (hours == 11 && min >= 30) return false;
        else if (hours == 13 && min < 30) return false;
        else if ((hours == 10 && min >= 15) && (hours == 10 && min < 30)) return false;
        else return true;
    } else if (nightType == 1 && hours >= 21 && hours < 23) return true;
    else if (nightType == 2 && ((hours >= 21 && hours < 24) || (hours >= 0 && hours < 1 && day !== 1))) return true;
    else if(nightType===3&& ((hours>=21&&hours<23)||(hours===23&&min<30))) return true;
    else if(nightType===4&&((hours >= 21 && hours < 24)||(hours>=0&&hours<2)||(hours===2&&min<30))&&day!==1) return true;
    else return false;
};

//Please try multiple times before logging in successfully.login,So I wrote a function to prepare trading, which can be placed inmainBeginning of function
$.ready4ctp = function(contractType) {
    var insDetail;
    var retry = 0;
    while (!(insDetail = exchange.SetContractType(contractType)) && retry < 20) {
        Sleep(2000);
        retry++;
    }
    if (insDetail) Log("contract", insDetail.InstrumentName, "One hand", insDetail.VolumeMultiple, "portion, Maximum Order Quantity", insDetail.MaxLimitOrderVolume, "Margin Rate:", insDetail.LongMarginRatio, "Delivery date", insDetail.StartDelivDate);
    else throw ('Connection timed out, please check your account');
    return insDetail;
};

function main() {
    $.ready4ctp('MA609');
    var isTrading = $.judgeTrading();
    Log('Currently trading?:'+isTrading);
    var p = $.NewPositionManager();
    p.OpenShort("MA609", 1, 1000);
    Sleep(60000 * 10);
    p.Cover("MA609", 1000);
    p.Cover('MA609');
    LogProfit(p.Profit());

}
```

> Detail

https://www.fmz.com/strategy/14198

> Last Modified

2016-06-24 16:28:23
