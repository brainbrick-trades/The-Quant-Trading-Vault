
> Name

Version-C-Multi-Chart-Test

> Author

发明者量化-小小梦





> Source (cpp)

``` cpp
/*backtest
start: 2019-01-22 00:00:00
end: 2019-01-23 00:00:00
period: 30m
exchanges: [{"eid":"OKCoin_EN","currency":"BTC_USD"}]
*/

void main() {
    json cfgA = R"({
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
    })"_json;    

    json cfgB = R"({
        "title" : {
            "text" : "Price Difference Chart"
        }, 
        "xAxis" : {
            "type" : "datetime"
        }, 
        "series" : [{
            "name" : "Spread", 
            "type" : "column", 
            "data" : []
        }]
    })"_json;    
    
    json cfgC = R"({
        "__isStock" : false,
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
                ["D", 25]
            ]
        }]
    })"_json;    
    
    json cfgD = R"({
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
    })"_json;    
    
    json cfgE = R"({
        "__isStock" : false, 
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
    })"_json;

    auto chart = Chart({cfgA, cfgB, cfgC, cfgD, cfgE});
    chart.reset();
    json zz = R"({
        "name" : "ZZ", 
        "y" : 0
    })"_json;
    zz["y"] = rand() % 100;
    chart.add(3, zz);
    
    while(true) {
        Sleep(1000);
        auto ticker = exchange.GetTicker();
        if(!ticker.Valid) {
            continue;
        }
        auto diff = ticker.Sell - ticker.Buy;
        json cfgASubTitle = R"({"text" : ""})"_json;
        cfgASubTitle["text"] = format("Buy one %f, sell one %f", ticker.Buy, ticker.Sell);
        cfgA["subtitle"] = cfgASubTitle;
        
        json cfgBSubTitle = R"({"text" : ""})"_json;
        cfgBSubTitle["text"] = format("Price difference %f", diff);
        cfgB["subtitle"] = cfgBSubTitle;

        chart.add(0, {Unix() * 1000, ticker.Buy});
        chart.add(1, {Unix() * 1000, ticker.Sell});
        chart.add(2, {Unix() * 1000, diff});
        chart.add(4, {Unix() * 1000, ticker.Buy});
        chart.add(5, {Unix() * 1000, ticker.Buy});
        cfgC["series"][0]["data"][0][1] = rand() % 100;
        cfgE["series"][0]["data"][0][1] = rand() % 100;
        chart.update({cfgA, cfgB, cfgC, cfgD, cfgE});
    }
}
```

> Detail

https://www.fmz.com/strategy/190848

> Last Modified

2020-03-16 11:48:16
