
> Name

WebSocket-Version-OKEx-Cross-Period-Hedging-Strategy-Lesson

> Author

发明者量化-小小梦

> Strategy Description

## Minimal OKEX cross-period hedging strategy (tutorial)
   
   - Live Screenshot:
     ![IMG](https://www.fmz.com/upload/asset/16f45ddc33e43f3248db.png) 

  - Only do bull spreads; bear spreads can be done by swapping contracts, which is the bear spread.

  - Add Two Exchange Objects, the First for the Quarter, the Second for the Week.

  - Streamlined all code that could be simplified, with significant room for optimization; teaching strategy is cautious in real trading, and there is some risk across periods.

  - Use counterparty price to place the order.

  - Feedback welcomeBUG.


  ### Teaching strategy, use in live trading with caution.
  ### Teaching strategy, use in live trading with caution.
  ### Teaching strategy, use in live trading with caution.

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|_Begin|true|Starting spread|
|_Add|true|Price difference|
|_Profit|true|Closing price spread profit|
|_Count|10|Number of nodes|
|_ContractNum|true|Node order quantity|
|_Instrument_id_A|LTC-USD-190628|AExchange quarterly contractID|
|_Instrument_id_B|LTC-USD-190426|BExchange current week contractID|


> Source (javascript)

``` javascript
function Hedge (isOpen, retSetA, retSetB) {
    exchanges[0].SetDirection(isOpen ? "sell" : "closesell")
    exchanges[1].SetDirection(isOpen ? "buy" : "closebuy");
    (function (routineA, routineB) {
        Log(routineA.wait(), routineB.wait(), retSetA, retSetB)
    })(exchanges[0].Go(isOpen ? "Sell" : "Buy", -1, _ContractNum), exchanges[1].Go(isOpen ? "Buy" : "Sell", -1, _ContractNum))
}

function main () {
    var param = {"op": "subscribe", "args": ["futures/ticker:" + _Instrument_id_A, "futures/ticker:" + _Instrument_id_B]}
    var client = Dial("wss://real.okex.com:8443/ws/v3|compress=gzip_raw&mode=recv&reconnect=true&payload=" + JSON.stringify(param))
    client.write(JSON.stringify(param))
    var tickerA, tickerB 
    var arr = []
    for (var i = 0 ; i < _Count ; i++) {
        arr.push({open: _Begin + i * _Add, cover: _Begin + i * _Add - _Profit, isHold: false})
    }
    while (1) {
        var tab = {type: "table", title: "Status", cols: ["Node Information"], rows: []}
        Sleep(10) 
        var ret = client.read(-2)
        if (!ret || ret == "") {
            continue
        }

        var obj = null
        try {
            obj = JSON.parse(ret)
        } catch (e) {
            Log(e)
            continue
        }

        if (obj.table == "futures/ticker" && obj.data[0].instrument_id == _Instrument_id_A) {   
            tickerA = obj.data[0]
        } else if (obj.table == "futures/ticker" && obj.data[0].instrument_id == _Instrument_id_B) {
            tickerB = obj.data[0]
        }

        if (tickerA && tickerB) {
            $.PlotLine(tickerA.instrument_id + "-" + tickerB.instrument_id, tickerA.last - tickerB.last)
            for (var j = 0 ; j < arr.length; j++) {
                if (tickerA.best_bid - tickerB.best_ask > arr[j].open && !arr[j].isHold) {   
                    Hedge(true, exchanges[0].SetContractType("quarter"), exchanges[1].SetContractType("this_week"))
                    arr[j].isHold = true
                }
                if (tickerA.best_ask - tickerB.best_bid < arr[j].cover && arr[j].isHold) {
                    Hedge(false, exchanges[0].SetContractType("quarter"), exchanges[1].SetContractType("this_week"))
                    arr[j].isHold = false 
                }
                tab.rows.push([JSON.stringify(arr[j])])
            }
        }
        LogStatus(_D(), "\n `" + JSON.stringify(tab) + "`")
    }
}
```

> Detail

https://www.fmz.com/strategy/144378

> Last Modified

2020-04-27 16:58:34
