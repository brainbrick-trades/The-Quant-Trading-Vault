
> Name

Hedge-on-Two-Contracts

> Author

小草

> Strategy Description

can automatically hedge two contracts immediately. Note that adding appropriate price slips may result in unfilled trades. For larger positions, multiple clicks can be made.

The plug-in can be started with one click on the trading terminal, free of charge, and convenient for manual trading. Detailed introduction:https://www.fmz.com/digest-topic/5051

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|Contract_A|this_week|Trading ContractA|Contract A|
|Contract_B|quarter|Trading ContractB|Contract B|
|Amount|10|Open position quantity|Open Amount|
|Slip|2|Slippage|Slip Price|
|Reverse|false|Reverse transaction|Reverse Direction|


> Source (javascript)

``` javascript

function main(){
    exchange.SetContractType(Reverse ? Contract_B : Contract_A)
    var ticker_A = exchange.GetTicker()
    if(!ticker_A){return 'Unable to get quotes'}
    exchange.SetDirection('buy')
    var id_A = exchange.Buy(ticker_A.Sell+Slip, Amount)
    exchange.SetContractType(Reverse ? Contract_B : Contract_A)
    var ticker_B = exchange.GetTicker()
    if(!ticker_B){return 'Unable to get quotes'}
    exchange.SetDirection('sell')
    var id_B = exchange.Sell(ticker_B.Buy-Slip, Amount)
    if(id_A){
        exchange.SetContractType(Reverse ? Contract_B : Contract_A)
        exchange.CancelOrder(id_A)
    }
    if(id_B){
        exchange.SetContractType(Reverse ? Contract_B : Contract_A)
        exchange.CancelOrder(id_B)
    }
    return 'Position: ' + JSON.stringify(exchange.GetPosition())
}

```

> Detail

https://www.fmz.com/strategy/191348

> Last Modified

2020-03-24 10:52:08
