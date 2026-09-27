
> Name

Market-Center-Delay

> Author

fmzero

> Strategy Description

**Test[Quote Center](https://www.fmz.com/strategy/182185)Delay**

![IMG](https://www.fmz.com/upload/asset/3c072bb7197f82f80b68.png)



> Source (javascript)

``` javascript
function main() {
    mcc = $.NewMarketCenterClient()
    Log('support list: '+mcc.GetSupportList())
    mcc.SubscribeSpotTicker('binance.com', 'BTC_USDT', 200)
    Sleep(1000)
    Log("start...")
    var count = 0
    
    var max = -1
    var min = 9999999
    var ave = 0
    var sum = 0
    
    for(var i = 0; i < 1000; i++) {
        var start = new Date().getTime()
        var ticker = mcc.GetSpotTicker('binance.com', 'BTC_USDT')
        var end = new Date().getTime()
        if (ticker === null) {
            continue
        }
        count += 1
        var pass = end - start
        if (pass > max) {
            max = pass
        }
        if (pass < min) {
            min = pass
        }
        sum += pass
    }
    ave = sum / count
    
    var allstatus = 'Market center delay test\n'
    allstatus += "https://www.fmz.com/strategy/183009\n";
    allstatus += "♜Q:6510676#0000ff\n";
    allstatus += "♜QGroup:364655408#0000ff\n";
    allstatus += "♜WeChat: btstarinfo#0000ff\n";
    
    var table = {
        type: 'table',
        title: 'Delay test',
        cols: ['Number of tests', 'Maximum(ms)', 'Minimum(ms)', 'Avg.(ms)'],
        rows: [
            [
                count, max, min, ave
            ]
        ]
    }
    allstatus += "`" + JSON.stringify(table) + "`" + "\n";

    LogStatus(allstatus)
}
```

> Detail

https://www.fmz.com/strategy/183009

> Last Modified

2020-02-10 20:12:47
