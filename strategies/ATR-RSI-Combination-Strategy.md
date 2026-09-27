
> Name

ATR-RSI-Combination-Strategy

> Author

一刀

> Strategy Description

## AtrIndicator
Average True Range, referred to as ATR indicator. It is mainly used to measure the intensity of market fluctuations and show the market change rate, but it cannot reflect the price direction and trend stability. The higher the value of this indicator, the greater the possibility of a trend change, and conversely, the smaller the possibility of a trend change.

### Calculation Method
The average true fluctuation range is calculated based on the real fluctuations of the past N days and the real fluctuations of the current day. The true single-day fluctuation is based on the maximum value among the three sets of results: (highest price of the day - lowest price of the day), (highest price of the day - yesterday's closing price), (yesterday's closing price - lowest price of the day), with the purpose of obtaining the maximum fluctuation range price difference.

## RsiIndicator
Relative Strength Index (RSI indicator). Technical indicators that determine future market trends by comparing the strength of buying and selling power between long and short parties within a period of time.

### Calculation Method
RSI = 100 - (100/(1+RS));
RS = nSum of days' closing gains/n days' closing number of falls;
Generally, RSI uses 50 as the midpoint; above 50 is considered a bullish market, below 50 is considered a bearish market;
RSIIf it is greater than 70, it is considered an overbought state, and the subsequent market may see a correction or a turnaround. If it is less than 30, it is an oversold state, and there may be a subsequent rise.

## Strategy Principle
ATRis used for filtering. When ATR>ATRMa (the average ATR of the past N days), it means that the market volatility has begun to increase and the trend is strengthening. RSI is used to generate trading signals.

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|rsi_period|20|Strength indicator calculation period|
|atr_period|14|Average true range calculation period|
|atrma_period|20|Average true range average price calculation period|
|tick_interval|60|Time Interval|
|slide_price|0.3|Order sliding value|


> Source (javascript)

``` javascript
/*backtest
start: 2021-02-11 00:00:00
end: 2022-02-10 23:59:00
period: 15m
basePeriod: 5m
exchanges: [{"eid":"Huobi","currency":"BCH_USDT"}]
args: [["rsi_period",12],["atrma_period",18]]
*/

/*
* rsi_period: Strength indicator calculation period
* atr_period: Average true range calculation period
* atrma_period: Average true range mean calculation period
* tick_interval: Time Interval
* slide_price: Order sliding value
*/

// RSIIndicates operation status
var RSI_NONE = 0;
var RSI_BUY = 1;
var RSI_SELL = 2;

var last_rsi_staus;

// ATRActive signal judgment
function isAtrActive(records) {
    let atr = TA.ATR(records, atr_period);
    let atrma = atr[atr.length - 1];
    if (atr.length > atrma_period) {
        let tmp_atr = 0;
        for (let i = atr.length - atrma_period; i < atr.length; i++) {
            tmp_atr += atr[i];
        }
        atrma = tmp_atr / atr_period;
    }
    else {
        atrma = aval(atr.join("+")) / atr.length;
    }
    return atr[atr.length - 1] > atrma;
}

// ObtainRSIOperation Status
function getRsiStatus(records) {
    let rsi = TA.RSI(records, rsi_period)[records.length - 1];
    if (rsi < 30) {
        return RSI_BUY;
    }
    else if (rsi > 70) {
        return RSI_SELL;
    }
    else {
        return RSI_NONE;
    }
}

// Cancel unfilled orders
function canelPendingOrders() {
    while (true) {
        let orders = _C(exchange.GetOrders);
        if (orders.length == 0) {
            break;
        }
        for (let i = 0; i < orders.length; i++) {
            exchange.CancelOrder(orders[i].Id);
        }
    }
}

function onTick() {
    let records = _C(exchange.GetRecords, PERIOD_M15);
    let ticker = _C(exchange.GetTicker);
    if (records == null ||
        ticker == null ||
        records.length < rsi_period ||
        records.length < atr_period) {
        return;
    }

    if (isAtrActive(records)) {
        let rsi = getRsiStatus(records);
        if (rsi != RSI_NONE) {
            let account = _C(exchange.GetAccount);
            if (rsi == RSI_BUY && last_rsi_staus != RSI_BUY) {
                Log("Buy Signal");
                last_rsi_staus = RSI_BUY;
                canelPendingOrders();
                if(account.Balance>0){
                    let price = ticker.Last + slide_price;
                    let amount = account.Balance / price * 0.99;
                    exchange.Buy(price, amount);
                }
            } else if (rsi == RSI_SELL && last_rsi_staus != RSI_SELL) {
                Log("Sell Signal");
                last_rsi_staus = RSI_SELL;
                canelPendingOrders();
                if (account.Stocks > 0) {
                    let price = ticker.Last - slide_price;
                    exchange.Sell(price, account.Stocks);
                }
            }
        }
    }
    last_records = records;
}

function main() {
    while (true) {
        onTick();
        Sleep(tick_interval * 1000);
    }
}
```

> Detail

https://www.fmz.com/strategy/345036

> Last Modified

2022-02-13 17:19:57
