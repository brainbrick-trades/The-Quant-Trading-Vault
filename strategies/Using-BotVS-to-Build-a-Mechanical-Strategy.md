
> Name

Using-BotVS-to-Build-a-Mechanical-Strategy

> Author

发明者量化-小小梦

> Strategy Description

Zhihu column article with strategy
Use BotVS to build a mechanical strategy



> Source (javascript)

``` javascript
// Parameters
var ContractType = "rb1710";
var PointAmount = 1;
var NetSize = 30;
var Interval = 500;
var SumPoints = 10;
var CoverRatio = 2;

// Global Variables
var Controller = {
    symbol : null,
    Amount : 0,
    Size : 0,
    BeginPrice : 0,
    SumPoints : 0,
    CoverRatio : 0,
    Net_Long : [],
    Net_Short : [],
    ContractInfo : null,
    isUpdateNetShow : false,     // Whether to update display
};
var perBar = null;

function loop(){
    var records = exchange.GetRecords();
    var ticker = exchange.GetTicker();
    if(!records || records.length == 0 || !ticker){
        return;
    }
    
    if(records[records.length - 1].Time !== perBar.Time){  // New Bar Generate
        UpdateNet(ticker.Last);
        perBar = records[records.length - 1];
    }

    // Draw lines
    $.PlotRecords(records, 'KLine');
    
    for(var i = 0; (i < Controller.Net_Long.length && Controller.isUpdateNetShow == true); i++){   // Update display
        $.PlotHLine(Controller.Net_Long[i].open, 'long' + i);
        if(i == Controller.Net_Long.length - 1){
            for(var j = 0; j < Controller.Net_Short.length; j++){
                $.PlotHLine(Controller.Net_Short[j].open, 'short' + j, "green");
            }
            $.PlotHLine(Controller.BeginPrice, 'begin', "black", "dash");  // Initial line
            Controller.isUpdateNetShow = false;
            Log("Update display!"); // ceshi
        }
    }
    // throw "stop"; // ceshi
    // Log(Controller.Net_Long); // cehsi
}

function init(){
    Controller.symbol = ContractType;
    Controller.Amount = PointAmount;
    Controller.Size = NetSize;
    Controller.SumPoints = SumPoints;
    Controller.CoverRatio = 2;
    
    // Set Contract
    while(exchange.IO("status") == false || Controller.ContractInfo == null){
        Controller.ContractInfo = exchange.SetContractType(Controller.symbol);
        LogStatus("Time: ", new Date(), "Wait for the connection server initialization.".");
        Sleep(Interval);
    }

    var ticker = _C(exchange.GetTicker);
    var records = _C(exchange.GetRecords);
    perBar = records[records.length - 1];
    // Initial update grid
    UpdateNet(ticker.Last);
}

function UpdateNet(price){
    // Check if the grid has no positions
    for(var n = 0; n < Controller.Net_Long.length; n++){
        if(Controller.Net_Long[n].hold !== 0){
            Log("Net_Long The grid still has positions! Cannot update.");
            return false;
        }
    }

    for(var m = 0; m < Controller.Net_Short.length; m++){
        if(Controller.Net_Short[m].hold !== 0){
            Log("Net_Short The grid still has positions! Cannot update.");
            return false;
        }
    }
    
    Controller.isUpdateNetShow = true;

    Controller.Net_Long = [];
    Controller.Net_Short = [];
    Controller.BeginPrice = price;
    for(var i = 0; i < Controller.SumPoints; i++){
        var Long_point = {
            open : _N(Controller.BeginPrice + (i + 1) * Controller.Size, 0),
            cover : _N(Controller.BeginPrice + (i + 1) * Controller.Size + Controller.CoverRatio * Controller.Size, 0),
            hold : 0,
        }
        Controller.Net_Long.push(Long_point);
    }
    for(var j = 0; j < Controller.SumPoints; j++){
        var Short_point = {
            open : _N(Controller.BeginPrice - (j + 1) * Controller.Size, 0),
            cover : _N(Controller.BeginPrice - (j + 1) * Controller.Size + Controller.CoverRatio * Controller.Size, 0),
            hold : 0,
        }
        Controller.Net_Short.push(Short_point);
    }
}

function main(){
    // Entry function initialization

    // Main loop, which runs after the program initializes until manually closed.
    var LoginState = null;
    var nowTimeStamp = 0;
    while(true){
        nowTimeStamp = new Date().getTime();
        if(exchange.IO("status") == true){
            LoginState = true;
            loop();
        }else{
            LoginState = false;
        }
        LogStatus("Time: ", _D(nowTimeStamp), LoginState ? "Connected to server" : "Not connected to server! "/*, some information to be displayed can be written here, such as account information, real-time market conditions, and program status*/)
        Sleep(Interval);     //  Pause for 0.5 seconds to avoid excessive polling frequency and problems caused by accessing the exchange server too frequently.
    }
}
```

> Detail

https://www.fmz.com/strategy/40357

> Last Modified

2017-09-21 09:16:02
