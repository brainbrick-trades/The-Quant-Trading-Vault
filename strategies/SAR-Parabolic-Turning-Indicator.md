
> Name

SAR-Parabolic-Turning-Indicator

> Author

韬奋量化

> Strategy Description

This Strategy Is Modified Based on Piandozi's "One Moving Average Trend Demo"(https://www.fmz.com/strategy/193609),
Using Parabolic SAR Indicator Signals as Buy and Sell Points, a Cryptocurrency Futures Trend Strategy.

The drawing code uses Zero's 'Drawing Library'"(https://www.fmz.com/strategy/27293),
Referenced Xiao Xiao Meng's "Example of Drawing candlestick and Moving Average Charts Using Drawing Libraries""(https://www.fmz.com/strategy/125770).

---- Taofen Quantitative (WeChat):himandy)



=====I am a low-key dividing line=====

A good trading platform can make your strategy soar to 90,000 miles. Register through the link to get a two-month VIP5 handling rate discount.:
(Spot: 0% for pending orders and 0.07% for take orders. Contract: 0% for pending orders, take orders0.04%)
https://www.kucoin.center/ucenter/signup?rcode=1wxJ2fQ&lang=zh_CN&utmsource=VIP_TF

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|Amount|100|Amount|
|time_interval|3600|Custom candlestick period (seconds)|


> Source (javascript)

``` javascript
/*backtest
start: 2017-11-01 00:00:00
end: 2020-09-01 00:00:00
period: 1d
basePeriod: 1h
exchanges: [{"eid":"Futures_BitMEX","currency":"XBT_USD"}]
args: [["Amount",10000],["time_interval",86400]]
*/

/*
This strategy is based on "One Moving Average Trend Demo" by Diandouzi (https://www.fmz.com/strategy/193609)Make modifications,Using Parabolic SAR Indicator Signals as Buy and Sell Points, a Cryptocurrency Futures Trend Strategy.

The drawing code uses Zero's "Line Drawing Library" (https://www.fmz.com/strategy/27293),Referenced Xiao Xiao Meng's "Example of Drawing candlestick and Moving Average Charts Using Drawing Libraries""(https://www.fmz.com/strategy/125770).

---- Taofen Quantitative (WeChat):himandy)
*/

// Define Object

//For Backtesting
if (IsVirtual) {
    if (exchange.GetCurrency() == "BTC_USD") {
        exchange.SetContractType("quarter"); //Select Contract
    } else if (exchange.GetCurrency() == "XBT_USD") {
        exchange.SetContractType("XBTUSD"); //Facilitate strategy selectionBitMEXbacktest
    }
}

exchange.SetMarginLevel(1)

var LastBarTime = 0,
    Idle = -1,
    status = Idle;

var preAccount, account, records, ticker, balance, Bar;
var sar, isFirst, PreBarTime, preTime;

// Connect to exchange, Get relevant information
function UpdateInfo() {
    account = exchange.GetAccount()
    records = exchange.GetRecords(time_interval)
    ticker = exchange.GetTicker()
    //balance = account.Stocks
    //Bar = records[records.length - 1]
}

// Indicator calculation and acquisition
function Get_SAR() {
    sar = talib.SAR(records, 0.02, 0.2);
}

// Open and close position rules
function onTick() {

    ticker = exchange.GetTicker()
    if (status === Idle) {
        if (ticker.Last > sar[sar.length - 1]) {
            exchange.SetDirection("buy")
            exchange.Buy(ticker.Sell, Amount)
            status = PD_LONG
            $.PlotFlag(new Date().getTime(), 'Buy', 'BK');
        } else if (ticker.Last < sar[sar.length - 1]) {
            exchange.SetDirection("sell")
            exchange.Sell(ticker.Buy, Amount)
            status = PD_SHORT
            $.PlotFlag(new Date().getTime(), 'Sell', 'SK');
        }
    } else if (status === PD_LONG) {
        if (ticker.Last < sar[sar.length - 1]) {
            exchange.SetDirection("closebuy")
            exchange.Sell(ticker.Buy, Amount)
            account = exchange.GetAccount()
            status = Idle
            $.PlotFlag(new Date().getTime(), 'CloseBuy', 'SP');
        }
    } else if (status === PD_SHORT) {
        if (ticker.Last > sar[sar.length - 1]) {
            exchange.SetDirection("closesell")
            exchange.Buy(ticker.Sell, Amount)
            account = exchange.GetAccount()
            status = Idle
            $.PlotFlag(new Date().getTime(), 'CloseSell', 'BP');
        }
    }

}

function PlotMA_Kline(records, isFirst) {

    $.PlotRecords(records, "BTC")
    if (isFirst) {
        for (var i = records.length - 1; i >= 0; i--) {
            if (sar[i] !== null) {
                $.PlotLine("SAR", sar[i], records[i].Time);
            }
        }
        PreBarTime = records[records.length - 1].Time;
    } else {
        if (PreBarTime !== records[records.length - 1].Time) {
            $.PlotLine('SAR', sar[sar.length - 2], records[records.length - 2].Time);
            PreBarTime = records[records.length - 1].Time;
        }
        $.PlotLine('SAR', sar[sar.length - 1], records[records.length - 1].Time);
    }
}

function main() {
    preAccount = exchange.GetAccount()
    // Connect to exchange, Get relevant information
    UpdateInfo()

    // Main Function, Continuous Loop
    while (1) {
        records = exchange.GetRecords(time_interval)
        preTime = records[records.length - 1].Time
        //The robot delays waiting until the nextKLine period, unit is milliseconds
        while (new Date().getTime() < (preTime + time_interval * 1000)) { //holdKConvert line period to milliseconds
            records = exchange.GetRecords(time_interval)
            // Indicator calculation and acquisition
            Get_SAR()
            // Open and close position rules
            onTick()
            // PollingsleepTime
            Sleep(5 * 1000)
        }

        //Draw lines
        if (records) {
            PlotMA_Kline(records, isFirst);
            isFirst = false;
        }

        // Printbalance
        LogProfit(account.Stocks - preAccount.Stocks, "&")

    }
}
```

> Detail

https://www.fmz.com/strategy/224799

> Last Modified

2021-11-02 10:53:24
