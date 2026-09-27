
> Name

okex-BTC-Contract-Account-Public

> Author

leviyuan





> Source (javascript)

``` javascript
var exchangeRate = 6.4,
    usdprice = 1000

var chartCfg = [{
    title: {
        text: "Account monitoring"
    },
    xAxis: {
        type: 'datetime'
    },
    series: [{
        name: "Current account fund value",
        data: []
    }, {
        name: "Current value of BTC starting this week",
        data: []
    }]
}]

function GetWebJson(url) {
    for (var i = 0; i < 10; i++) {
        try {
            return JSON.parse(HttpQuery(url))
        } catch (e) {
            Sleep(500)
        }
    }
}

function main() {
    exchange.SetRate(1)
    LogReset()

    var chart = Chart(chartCfg)
    chart.reset()

    var nxttime = new Date().getTime()
    while (true) {
        var accountinfo = _C(exchange.GetAccount)
        try {
            var bdata = GetWebJson("https://api-otc.huobipro.com/v1/otc/trade/list/public?coinId=2&tradeType=0&currentPage=1&payWay=&country=&merchant=1&online=1&range=0").data
            var sdata = GetWebJson("https://api-otc.huobipro.com/v1/otc/trade/list/public?coinId=2&tradeType=1&currentPage=1&payWay=&country=&merchant=1&online=1&range=0").data
            var count = 0,
                rate = 0
            for (var k = 0; k < 3; k++) {
                count += bdata[k].tradeCount
                count += sdata[k].tradeCount
                rate += bdata[k].price * bdata[k].tradeCount
                rate += sdata[k].price * sdata[k].tradeCount
            }
            exchangeRate = rate / count
        } catch (e) {}
        try {
            usdprice = GetWebJson("https://www.okex.com/api/v1/future_index.do?symbol=btc_usd").future_index
        } catch (e) {}
        var rmb = accountinfo.Info.info.btc.account_rights * usdprice * exchangeRate
        var startcount = accountinfo.Info.info.btc.account_rights - accountinfo.Info.info.btc.profit_real - accountinfo.Info.info.btc.profit_unreal

        // Refresh chart
        chart.add(0, [new Date().getTime(), rmb])
        chart.add(1, [new Date().getTime(), startcount * exchangeRate * usdprice])

        var message = "Current equity of contract account:฿" + accountinfo.Info.info.btc.account_rights + "btc\n" +
            "Realized P&L this week:฿" + accountinfo.Info.info.btc.profit_real + "btc\n" +
            "Unrealized profit and loss:฿" + accountinfo.Info.info.btc.profit_unreal + "btc\n" +
            "HuobiOTCExchange rate:" + exchangeRate.toFixed(2) + "\n" +
            "BTCPrice index:$" + usdprice + "\n" +
            "ConversionRMBPrice:￥" + (usdprice * exchangeRate).toFixed(0) + "\n" +
            "Asset conversion:¥" + rmb.toFixed(0) + "/ $" + (rmb / exchangeRate).toFixed(0) + "\n" +
            "Account Margin Rate:" + (accountinfo.Info.info.btc.risk_rate * 100).toFixed(1) + "%\n" +
            _D(new Date().getTime())
        LogStatus(message)

        var nowtime = new Date().getTime()
        while (nxttime < nowtime)
            nxttime += 30 * 60 * 1000
        Sleep(nxttime - nowtime)
    }
}
```

> Detail

https://www.fmz.com/strategy/83189

> Last Modified

2018-03-29 09:51:37
