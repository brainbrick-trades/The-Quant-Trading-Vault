
> Name

market-center-client

> Author

fmzero

> Strategy Description

## Market Center Client

This [Client](https://github.com/goex-top/market_center_client_fmz) is used with [Quote Center](https://github.com/goex-top/market_center)

## Why there is a market center

There are REST and Websocket for accessing the market. However, due to various irresistible factors, the connection of Websocket is forcibly disconnected. At this time, the strategy needs to prepare various fault-tolerant mechanisms. REST is often the most stable way.
When you have multiple strategies running on the same platform, such as OKEx, and these multiple strategies are on the same server, there are frequency restrictions on access to the REST API (please refer to the individual platform API documentation for details). There are many ways to limit, such as IP restrictions, account restrictions, or a combination of both, etc.
Using the market center can reduce the frequency of REST requests

![Traditional way](https://raw.githubusercontent.com/goex-top/market_center/master/trandition.png)

![Quote Center](https://raw.githubusercontent.com/goex-top/market_center/master/market_center.png)

## Market Center Deployment
1. [Source code](https://github.com/goex-top/market_center) compile and deploy
2. [Binary deployment](https://github.com/goex-top/market_center/releases)
3. Contact for help if neededwx:btstarinfo, Q:6510575

## Please pay attention
* Market center only provides market data interface, does not provide order placement interface
* Market center can only run on Linux, Unix

## API
* GetSupportList
* SubscribeSpotTicker
* SubscribeSpotDepth
* ~~SubscribeSpotTrade~~
* GetSpotTicker
* GetSpotDepth
* ~~GetSpotTrade~~
* SubscribeFutureTicker
* SubscribeFutureDepth
* ~~SubscribeFutureTrade~~
* GetFutureTicker
* GetFutureDepth
* ~~GetFutureTrade~~

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|udspath|/tmp/goex.market.center|Market Center Path|


> Source (javascript)

``` javascript
// a client for market center, https://github.com/goex-top/market_center
// api list 
// * GetSupportList
// * SubscribeSpotTicker
// * SubscribeSpotDepth
// * ~~SubscribeSpotTrade~~
// * GetSpotTicker
// * GetSpotDepth
// * ~~GetSpotTrade~~
// * SubscribeFutureTicker
// * SubscribeFutureDepth
// * ~~SubscribeFutureTrade~~
// * GetFutureTicker
// * GetFutureDepth
// * ~~GetFutureTrade~~

// params wit web
// var udspath = /tmp/goex.market.center //ref to https://github.com/goex-top/market_center/blob/1e1bb15c69a1da6fddbba3d506920e91f9ec7842/const.go#L35

// local variable
// var client = null

var ReqType = {
    ReqType_GetSupportList: 1,
    ReqType_SubscribeSpotDepth: 2,
    ReqType_SubscribeSpotTicker: 3,
    ReqType_SubscribeFutureDepth: 4,
    ReqType_SubscribeFutureTicker: 5,
    ReqType_GetSpotDepth: 6,
    ReqType_GetSpotTicker: 7,
    ReqType_GetFutureDepth: 8,
    ReqType_GetFutureTicker: 9,
}

//---------------------------------------
function newUDSClient() {
    var client = Dial('unix://'+udspath)
    if (null === client) {
        throw 'new usd client fail'
    }
    return client
}

function udsRequest(client, req) {
    try {
        client.write(JSON.stringify(req))
        var rsp = client.read(20)
        if (rsp === null) {
            return null
        }
    
        var obj = JSON.parse(rsp)
        if(obj.status !== 0) {
            return null
        }
        return obj.data
    }
    catch(e) {
        return null
    }
    
}

function GetSupportList(client) {
    var req = {type:ReqType.ReqType_GetSupportList}
    var rsp = udsRequest(client, req)
    if (rsp === null) {
        return null
    }
    return rsp
}

function GetSpotDepth(client, exchangeName, pair) {
    var req = {type:ReqType.ReqType_GetSpotDepth, exchange_name: exchangeName, currency_pair: pair}
    var rsp = udsRequest(client, req)
    if(rsp === null) {
        return null
    }
    return {Asks:rsp.AskList, Bids:rsp.BidList, Time:rsp.UTime, Info:rsp.rsp}
}

function GetSpotTicker(client, exchangeName, pair) {
    var req = {type:ReqType.ReqType_GetSpotTicker, exchange_name: exchangeName, currency_pair: pair}
    var rsp = udsRequest(client, req)
    if(rsp === null) {
        return null
    }
    return {
        Last:parseFloat(rsp.last), 
        Buy:parseFloat(rsp.buy), 
        Sell:parseFloat(rsp.sell), 
        Volume:parseFloat(rsp.vol), 
        Time:parseFloat(rsp.date), 
        High:parseFloat(rsp.high), 
        Low:parseFloat(rsp.low), 
        Info:rsp
    }
}

function SubscribeSpotDepth(client, exchangeName, pair, period) {
    var req = {type:ReqType.ReqType_SubscribeSpotDepth, exchange_name: exchangeName, currency_pair: pair, period: period}
    var rsp = udsRequest(client, req)
    return rsp
}

function SubscribeSpotTicker(client, exchangeName, pair, period) {
    var req = {type:ReqType.ReqType_SubscribeSpotTicker, exchange_name: exchangeName, currency_pair: pair, period: period}
    var rsp = udsRequest(client, req)
    return rsp
}

function GetFutureDepth(client, exchangeName, contractType, pair) {
    var req = {type:ReqType.ReqType_GetFutureDepth, exchange_name: exchangeName, contract_type: contractType, currency_pair: pair}
    var rsp = udsRequest(client, req)
    if(rsp === null) {
        return null
    }
    return {Asks:rsp.AskList, Bids:rsp.BidList, Time:rsp.UTime, Info:rsp.rsp}
}

function GetFutureTicker(client, exchangeName, contractType, pair) {
    var req = {type:ReqType.ReqType_GetFutureTicker, exchange_name: exchangeName, contract_type: contractType, currency_pair: pair}
    var rsp = udsRequest(client, req)
    if(rsp === null) {
        return null
    }
    return {
        Last:parseFloat(rsp.last), 
        Buy:parseFloat(rsp.buy), 
        Sell:parseFloat(rsp.sell), 
        Volume:parseFloat(rsp.vol), 
        Time:parseFloat(rsp.date), 
        High:parseFloat(rsp.high), 
        Low:parseFloat(rsp.low), 
        Info:rsp
    }
}

function SubscribeFutureDepth(client, exchangeName, contractType, pair, period) {
    var req = {type:ReqType.ReqType_SubscribeFutureDepth, exchange_name: exchangeName, contract_type: contractType, currency_pair: pair, period: period}
    var rsp = udsRequest(client, req)
    return rsp
}

function SubscribeFutureTicker(client, exchangeName, contractType, pair, period) {
    var req = {type:ReqType.ReqType_SubscribeFutureTicker, exchange_name: exchangeName, contract_type: contractType, currency_pair: pair, period: period}
    var rsp = udsRequest(client, req)
    return rsp
}

var MarketCenterClient = (function() {
    function MarketCenterClient() {
        if (typeof udspath === 'undefined' || udspath === '') {
            throw 'udspath not defined'
        }
        this.client = newUDSClient()
        this.list = GetSupportList(this.client)
        Log("this.list:" + this.list)
    }

    MarketCenterClient.prototype.GetSpotTicker = function(exchangeName, pair) {
        if (typeof exchangeName === 'undefined' || exchangeName === '') {
            throw 'GetSpotTicker exchangeName not defined'
        }
        if (typeof pair === 'undefined' || pair === '') {
            throw 'GetSpotTicker pair not defined'
        }
        return GetSpotTicker(this.client, exchangeName, pair)
    }

    MarketCenterClient.prototype.GetSpotDepth = function(exchangeName, pair) {
        if (typeof exchangeName === 'undefined' || exchangeName === '') {
            throw 'GetSpotDepth exchangeName not defined'
        }
        if (typeof pair === 'undefined' || pair === '') {
            throw 'GetSpotDepth pair not defined'
        }
    return GetSpotDepth(this.client, exchangeName, pair)
    }

    MarketCenterClient.prototype.SubscribeSpotDepth = function(exchangeName, pair, period) {
        if(typeof(period) === 'undefined') {
            period = 200
        }
        if (typeof exchangeName === 'undefined' || exchangeName === '') {
            throw 'SubscribeSpotDepth exchangeName not defined'
        }
        if (typeof pair === 'undefined' || pair === '') {
            throw 'SubscribeSpotDepth pair not defined'
        }
        var found = false
        _.each(this.list, function(item) {
            if (item === exchangeName) {
                found = true
                return false
            }
        })

        if(!found) {
            throw 'exchange ('+ exchangeName +') not support, please check it again, https://github.com/goex-top/market_center#support-exchanges'
        }
        return SubscribeSpotDepth(this.client, exchangeName, pair, period)
    }

    MarketCenterClient.prototype.SubscribeSpotTicker = function(exchangeName, pair, period) {
        if(typeof(period) === 'undefined') {
            period = 200
        }
        if (typeof exchangeName === 'undefined' || exchangeName === '') {
            throw 'SubscribeSpotTicker exchangeName not defined'
        }
        if (typeof pair === 'undefined' || pair === '') {
            throw 'SubscribeSpotTicker pair not defined'
        }
      var found = false
        _.each(this.list, function(item) {
            if (item === exchangeName) {
                found = true
                return false
            }
        })

        if(!found) {
            throw 'exchange ('+ exchangeName +') not support, please check it again, https://github.com/goex-top/market_center#support-exchanges'
        }
        return SubscribeSpotTicker(this.client, exchangeName, pair, period)
    }


    MarketCenterClient.prototype.GetFutureTicker = function(exchangeName, contractType, pair) {
        if (typeof exchangeName === 'undefined' || exchangeName === '') {
            throw 'GetFutureTicker exchangeName not defined'
        }
        if (typeof pair === 'undefined' || pair === '') {
            throw 'GetFutureTicker pair not defined'
        }
     return GetFutureTicker(this.client, exchangeName, contractType, pair)
    }

    MarketCenterClient.prototype.GetFutureDepth = function(exchangeName, contractType, pair) {
        if (typeof exchangeName === 'undefined' || exchangeName === '') {
            throw 'GetFutureDepth exchangeName not defined'
        }
        if (typeof pair === 'undefined' || pair === '') {
            throw 'GetFutureDepth pair not defined'
        }
     return GetFutureDepth(this.client, exchangeName, contractType, pair)
    }

    MarketCenterClient.prototype.SubscribeFutureDepth = function(exchangeName, contractType, pair, period) {
        if(typeof(period) === 'undefined') {
            period = 200
        }
        if (typeof exchangeName === 'undefined' || exchangeName === '') {
            throw 'SubscribeFutureDepth exchangeName not defined'
        }
        if (typeof pair === 'undefined' || pair === '') {
            throw 'SubscribeFutureDepth pair not defined'
        }
     var found = false
        _.each(this.list, function(item) {
            if (item === exchangeName) {
                found = true
                return false
            }
        })

        if(!found) {
            throw 'exchange ('+ exchangeName +') not support, please check it again, https://github.com/goex-top/market_center#support-exchanges'
        }
        return SubscribeFutureDepth(this.client, exchangeName, contractType, pair, period)
    }

    MarketCenterClient.prototype.SubscribeFutureTicker = function(exchangeName, contractType, pair, period) {
        if(typeof(period) === 'undefined') {
            period = 200
        }
        if (typeof exchangeName === 'undefined' || exchangeName === '') {
            throw 'SubscribeFutureTicker exchangeName not defined'
        }
        if (typeof pair === 'undefined' || pair === '') {
            throw 'SubscribeFutureTicker pair not defined'
        }
     var found = false
        _.each(this.list, function(item) {
            if (item === exchangeName) {
                found = true
                return false
            }
        })

        if(!found) {
            throw 'exchange ('+ exchangeName +') not support, please check it again, https://github.com/goex-top/market_center#support-exchanges'
        }
        return SubscribeFutureTicker(this.client, exchangeName, contractType, pair, period)
    }

    MarketCenterClient.prototype.GetSupportList = function() {
        return GetSupportList(this.client)
    }
    return MarketCenterClient
})()

$.NewMarketCenterClient = function() {
    return new MarketCenterClient()
}

function main() {
    mcc = $.NewMarketCenterClient()
    Log('support list'+mcc.GetSupportList())
    mcc.SubscribeSpotDepth('binance.com', 'BTC_USDT', 200)
    Sleep(1000)
    Log(mcc.GetSpotDepth('binance.com', 'BTC_USDT'))
    mcc.SubscribeSpotTicker('binance.com', 'BTC_USDT', 200)
    Sleep(1000)
    Log(mcc.GetSpotTicker('binance.com', 'BTC_USDT'))
}
  
```

> Detail

https://www.fmz.com/strategy/182185

> Last Modified

2020-02-09 20:15:26
