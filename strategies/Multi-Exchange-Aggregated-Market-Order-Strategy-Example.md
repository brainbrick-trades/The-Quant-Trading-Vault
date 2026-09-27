
> Name

Multi-Exchange-Aggregated-Market-Order-Strategy-Example

> Author

发明者量化-小小梦

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/20dd683abc5a0e70f84c5f2ae37c1753.png)

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|StrProxy|socks5://|Agent configuration|




|Button|Default|Description|
|----|----|----|
|UpdateAmount|0.1|Modify order volume|


> Source (javascript)

``` javascript
// Parameters,Can be set on the interface.
var Interval = 100
var TickerInterval = 1000
var RecordsInterval = 1000

// Global Variables
var Amount = 0.1

function CreateExchanges(){
    var exs = {
        // Exchange object
        ex_objs : [],

        // exs 's attributes
        table : null,
        tickerInterval : 0,
        recordsInterval : 0,
        runCount : 0, 
    }
    // Initialize
    exs.tickerInterval = TickerInterval
    exs.recordsInterval = RecordsInterval

    var funcDict = {
        "GetTicker" : ["routine_ticker", "ticker", "tickerPreTime"],
        "GetRecords" : ["routine_records", "records", "recordsPreTime"],
        "Trade" : ["routine_trade", "trade", "tradePreTime"],                   // Extensible pending orders, multi-threaded order issuance and other functions
    }

    // Initialize
    var timeStamp = new Date().getTime()
    for(var i = 0 ; i < exchanges.length ; i++){
        var obj = {
            name : exchanges[i].GetName(),
            currency : exchanges[i].GetCurrency(),
            index : i,
            routine_ticker : null,
            ticker : null,
            tickerPre : null,
            tickerPreTime : timeStamp,
            routine_trade : null,
            trade : null,
            tradePreTime : timeStamp,
            routine_records : null,
            records : null,
            recordsPre : null,
            recordsPreTime : timeStamp,
            recordsPreBarTime : 0,
            rows : null,

        }
        // Set proxy
        exchanges[i].SetProxy(StrProxy)
        
        exs.ex_objs.push(obj)
    }

    exs.Go = function(func, interval){
        var self = this
        if(typeof(func) == "undefined"){
            throw "error, no param func"
        }

        _.each(self.ex_objs, function(obj){
            if(typeof(obj[funcDict[func][1]]) !== "undefined"){
                obj[funcDict[func][0]] = exchanges[obj.index].Go(func)
                obj[funcDict[func][2]] = new Date().getTime()
            }
        })

        Sleep(interval)
        
        _.each(self.ex_objs, function(obj){
            obj[funcDict[func][1]] = obj[funcDict[func][0]].wait(10)
        })
    }

    exs.TableUpdate = function(){
        var self = this

        self.table = {
            type : "table", 
            title : "Exchange market data", 
            cols : ["Name", "Trading pair", "Sell price", "Buy price", "Latest transaction price", "Operation A", "Operation B", "Latest request time"], 
            rows : [],
        }

        _.each(self.ex_objs, function(obj){
            var ticker = obj.ticker
            if(typeof(ticker) == "undefined" || !ticker){
                ticker = obj.tickerPre ? obj.tickerPre : {Buy : "Nan", Sell : "Nan", Last : "Nan", High : "Nan", Low : "Nan"}
            }
            self.table.rows.push([
                obj.name, 
                obj.currency, 
                ticker.Sell, 
                ticker.Buy, 
                ticker.Last, 
                {
                    'type': 'button',
                    'cmd': "LogStatus" + "_" + obj.index + "_" + "Buy",                              
                    'name': 'buy'
                },
                {
                    'type': 'button',
                    'cmd': "LogStatus" + "_" + obj.index + "_" + "Sell",    
                    'class': 'btn btn-xs btn-danger',                          
                    'name': 'sell'
                }, 
                (new Date().getTime() - obj.tickerPreTime),
            ])
        })
        
        self.runCount++
        LogStatus("Time:", _D(), "Number of Runs:", self.runCount, " ", "\n", '`' + JSON.stringify(self.table) + '`')
    }   

    exs.Chart = function(chartObj, chartCfg){
        var self = this

        _.each(self.ex_objs, function(obj){
            if(typeof(obj.records) !== "undefined" && obj.records){
                if(obj.recordsPreBarTime == 0){                            // Initialize
                    for(var i = 0; i < obj.records.length; i++){
                        chartObj.add(obj.index, [obj.records[i].Time, obj.records[i].Open, obj.records[i].High, obj.records[i].Low, obj.records[i].Close])
                    }
                    obj.recordsPreBarTime = obj.records[obj.records.length - 1].Time
                } else {
                    if(obj.records[obj.records.length - 1].Time !== obj.recordsPreBarTime){
                        chartObj.add(obj.index, [obj.records[obj.records.length - 1].Time, obj.records[obj.records.length - 1].Open, obj.records[obj.records.length - 1].High, obj.records[obj.records.length - 1].Low, obj.records[obj.records.length - 1].Close])
                        obj.recordsPreBarTime = obj.records[obj.records.length - 1].Time
                    } else {
                        chartObj.add(obj.index, [obj.records[obj.records.length - 1].Time, obj.records[obj.records.length - 1].Open, obj.records[obj.records.length - 1].High, obj.records[obj.records.length - 1].Low, obj.records[obj.records.length - 1].Close], -1)
                    }
                }
            }
        })
        chartObj.update(chartCfg)
    } 

    exs.Trade = function(){

    }

    exs.GetTicker = function(){
        var self = this
        self.Go("GetTicker", self.tickerInterval)
        _.each(self.ex_objs, function(obj){
            if(typeof(obj.ticker) !== "undefined" && obj.ticker){
                obj.tickerPre = obj.ticker
            }
        })
    }

    exs.GetRecords = function(){
        var self = this
        self.Go("GetRecords", self.recordsInterval)
        _.each(self.ex_objs, function(obj){
            if(typeof(obj.records) !== "undefined" && obj.records){
                obj.recordsPre = obj.records
            }
        })
    }


    return exs
}

function main(){
    // Initialize the exchange collection object
    var exs = CreateExchanges()

    // Chart initialization
    var arrCfg = []
    for(var i = 0 ; i < exchanges.length ; i++){
        var cfg = {
            title: {
                text: exchanges[i].GetName() + "-" + exchanges[i].GetCurrency()
            },
            xAxis: {
                type: 'datetime'
            },
            series: [{
                type: 'candlestick',
                name: 'KLine',
                id: "" + i,
                data: [] 
            }]
        }
        arrCfg.push(cfg)
    }
    var chart = Chart(arrCfg)
    chart.reset()

    while(true){
        // Handle Interaction
        var cmd = GetCommand()
        if(cmd){
            Log("cmd:", cmd)  // Test
            
            var arr = cmd.split("_")
            if(arr.length == 3){
                var idx = parseInt(arr[1])
                var type = arr[2]
                if(type == "Buy"){
                    $.Buy(exchanges[idx], Amount)
                } else if(type == "Sell"){
                    $.Sell(exchanges[idx], Amount)
                } else {
                    Log("Wrong command,type:", type, "#FF0000")    
                }
            } else if(arr.length == 1) {
                var amount = arr[0].split(":")[1]
                Amount = parseInt(amount)
            }else {
                Log("Wrong command", "#FF0000")
            }
        }
        
        // Obtain records Data
        exs.GetRecords()
        // Obtain ticker Data
        exs.GetTicker()

        // Processing Interface
        exs.TableUpdate()
        exs.Chart(chart, arrCfg)

        Sleep(Interval)
    }
}
```

> Detail

https://www.fmz.com/strategy/125569

> Last Modified

2019-07-19 11:44:04
