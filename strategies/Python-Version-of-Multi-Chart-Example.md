
> Name

Python-Version-of-Multi-Chart-Example

> Author

发明者量化-小小梦





> Source (python)

``` python
'''backtest
start: 2019-01-22 00:00:00
end: 2019-01-23 00:00:00
period: 30m
exchanges: [{"eid":"OKCoin_EN","currency":"BTC_USD"}]
'''

import random
import time
def main():
    cfgA = {
        "extension" : {
            "layout" : "single", 
            "height" : 300,
            "col" : 8
        }, 
        "title" : {
            "text" : "Handicap chart"
        },
        "xAxis" : {
            "type" : "datetime" 
        }, 
        "series" : [{
            "name" : "Buy one",
            "data" : []
        }, {
            "name" : "Sell one", 
            "data" : []
        }]
    }    

    cfgB = {
        "title" : {
            "text" : "Price Difference Chart"
        }, 
        "xAxis" : {
            "type" : "datetime",
        }, 
        "series" : [{
            "name" : "Spread", 
            "type" : "column", 
            "data" : []
        }]
    }    

    cfgC = {
        "__isStock" : False,
        "title" : {
            "text" : "Pie chart"
        }, 
        "series" : [{
            "type" : "pie", 
            "name" : "one", 
            "data" : [
                ["A", 25],
                ["B", 25],
                ["C", 25],
                ["D", 25],
            ]
        }]
    }    

    cfgD = {
        "extension" : {
            "layout" : "single",
            "col" : 8,
            "height" : "300px"
        }, 
        "title" : {
            "text" : "Handicap chart"
        }, 
        "series" : [{
            "name" : "Buy one", 
            "data" : []
        }, {
            "name" : "Sell one",
            "data" : []
        }]
    }    

    cfgE = {
        "__isStock" : False, 
        "extension" : {
            "layout" : "single", 
            "col" : 4,
            "height" : "300px"
        }, 
        "title" : {
            "text" : "Pie chart2"
        },
        "series" : [{
            "type" : "pie",
            "name" : "one", 
            "data" : [
                ["A", 25], 
                ["B", 25], 
                ["C", 25], 
                ["D", 25]
            ]
        }]
    }
    
    chart = Chart([cfgA, cfgB, cfgC, cfgD, cfgE])
    chart.reset()
    chart.add(3, {
        "name" : "ZZ",
        "y" : random.random() * 100
    })
    
    while True:
        Sleep(1000)
        ticker = exchange.GetTicker()
        if not ticker :
            continue
        diff = ticker["Sell"] - ticker["Buy"]
        cfgA["subtitle"] = {
            "text" : "Buy one" + str(ticker["Buy"]) + "Sell one" + str(ticker["Sell"])
        }
        cfgB["subtitle"] = {
            "text" : "Price difference " + str(diff)
        }
        
        chart.add(0, [time.time() * 1000, ticker["Buy"]])
        chart.add(1, [time.time() * 1000, ticker["Sell"]])
        chart.add(2, [time.time() * 1000, diff])
        chart.add(4, [time.time() * 1000, ticker["Buy"]])
        chart.add(5, [time.time() * 1000, ticker["Buy"]])
        cfgC["series"][0]["data"][0][1] = random.random() * 100
        cfgE["series"][0]["data"][0][1] = random.random() * 100
```

> Detail

https://www.fmz.com/strategy/190826

> Last Modified

2020-03-16 10:12:22
