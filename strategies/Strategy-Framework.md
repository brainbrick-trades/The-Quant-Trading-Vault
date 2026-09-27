
> Name

Strategy-Framework

> Author

发明者量化-小小梦

> Strategy Description

Strategy Framework

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|isLogReset|true|Whether to clear logs at startup|




|Button|Default|Description|
|----|----|----|
|upDateAmount|true|Update position size button|
|cmdOpen|__button__|Position opening command|
|cmdCover|__button__|Closing order|


> Source (javascript)

``` javascript
var Interval = 500;
var _long = 1;
var free = 0;
var state = free; //Reset every time a position is opened or closed 
var buyInfo = null; //Reset every time a position is closed
var sellInfo = null; //Reset every time a position is opened
var initAccount = null; //Reset every time a position is closed
var beginAccount = null; //Do not reset
var Profit = 0; //Realized profit and loss
var prefloatProfit = 0;//Last floating profit and loss, sliding take profit update
var openBalance = 0;//Opening volume
var isCover = false;

var tiaojian = 0; //Here you can set trigger conditions, such as a custom indicator function that sends a position opening signal (for example, a value is returned  1 ), For example 0 'Time' is wait, equal to 2 Close position when
                  //It is also possible that the closing condition was triggered
var Amount = 1;   //Here, the transaction volume (number of coins) can be written in the program for automatic control (for example, based on the handicap volume), or it can be set on the interface as parameters on the interface, and passed in when the program is running.

var NowPositionInfo = {//Position information, updated every time a position is closed
    avgPrice: 0,
    amount: 0 ,
    floatProfit: 0
};

function openUpdate(){//Updates after position opening
    state = _long;
    sellInfo = null;
    tiaojian = 0;//Reset conditions
}
function closeUpdate(){//Update after position closing
    state = free;
    addLevel = 0;
    buyInfo = null;
    initAccount = _C(exchange.GetAccount);
    NowPositionInfo.avgPrice = 0;
    NowPositionInfo.amount = 0;
    NowPositionInfo.floatProfit = 0;
    isCover = true;
    tiaojian = 0;//Reset conditions
}

function Calculate(nowAccount,nowDepth){//Calculate and update income, floating income, calculate average position price, and position volume
    if(typeof(nowAccount) === 'undefined' ){
        nowAccount = _C(exchange.GetAccount);
        nowDepth = _C(exchange.GetDepth);
    }
    var diff_stocks = nowAccount.Stocks - initAccount.Stocks;//Difference in coins
    var diff_balance = nowAccount.Balance - initAccount.Balance;//Difference in money
    NowPositionInfo.avgPrice = Math.abs(diff_balance) / Math.abs(diff_stocks);
    NowPositionInfo.amount = Math.abs(diff_stocks);
    NowPositionInfo.floatProfit = diff_balance + diff_stocks * nowDepth.Bids[0].Price; //Floating profit and loss of this trade
    Profit = (initAccount.Stocks - beginAccount.Stocks) * nowDepth.Bids[0].Price + (initAccount.Balance - beginAccount.Balance); //Realize profit and loss

    //Update entry interface
}

function get_Command(){//is a function responsible for interactions, updating relevant values in real time, and users familiar with the process can extend it themselves
    var keyValue = 0;// Parameter value passed by command
    var way = null; //Routing
    var cmd = GetCommand(); //Get interaction commandsAPI
    if (cmd) {
        Log("Pressed the button:",cmd);//Log display
        arrStr = cmd.split(":"); // GetCommand The function returns a string. I have trouble processing it here because I want to get familiar with it.JSON ,So first process the string, and take the function return as a string : is divided into2A string. Stored in a string array.

        if(arrStr.length === 2){//What is accepted is not numerical value, but button type.
            jsonObjStr = '{' + '"' + arrStr[0] + '"' + ':' + arrStr[1] + '}'; // Reassemble the elements in the string array, concatenating them into JSON String, used for conversion toJSON Object.
            jsonObj = JSON.parse(jsonObjStr); // Convert toJSON Object
            
            for(var key in jsonObj){ // Iterate through the member names in the object
                keyValue = jsonObj[key]; //Extract the value corresponding to the member name, which is the value of the interactive button
            }
            
            if(arrStr[0] == "upDateAmount"){// This is a digital type. The processing here is divided into buttons and numbers. For details, see Interactive Settings under the Policy Parameters Settings Interface.
                way = 1;
            }
            if(arrStr[0] == "Extend1"){
                way = 2;
            }
            if(arrStr[0] == "Extend2"){
                way = 3;
            }
            if(arrStr[0] == "Extend3"){
                way = 4;
            }
        }else if(arrStr.length === 1){// Here is the button type  
            //Routing
            if(cmd == "cmdOpen"){ 
                way = 0;
            }
            if(cmd == "cmdCover"){
                way = 5;
            }
        }else{
            throw "error:" + cmd + "--" + arrStr;
        }
        switch(way){ // Branch selection operation
            case 0://Handle issuing open position signal
                tiaojian = 1;
                break;
            case 1://Process
                Amount = keyValue;//Pass the value set by the interactive interface to Amount
                Log("Modify opening volume to:",Amount);//Prompt Information
                break;
            case 2://Process
                
                break;
            case 3://Process
                
                break;
            case 4://Process
                
                break;
            case 5://Handle issuing close position signal
                tiaojian = 2;
                break;
            default: break;
        }
    }
}

function Loop(){//Loop body
    //Get market, account, and other information
    var account = _C(exchange.GetAccount);
    var records = _C(exchange.GetRecords);
    var depth = _C(exchange.GetDepth);
    var len = records.length - 1;
    
    //Apply fault tolerance to the obtained data
    if(records.length < 10 ){//Here you can API Data fault-tolerant handling, here is an example: data retrievalKLine length must be greater than10,Less Than10If done, then return without processing and display a prompt message on the interface.
        //Output to the status bar table and displayKLine length insufficient
        msg = "KLine length insufficient, fetching...";
        return;
    }
    msg = "K line `s length:" + (len + 1);

    //Use of chart templates---------------
    $.Draw(records);
    //---------------------------
    
    
    //Content to be processed on the first launch---------
    if(isFirst === true){
        $.SignOP((new Date()).getTime(),null,null,3,"Chart display starts!");// Test mark custom information onto the chart
        Log("Program Start!");
        isFirst = false;
    }
    //--------------------------
    
    //Display data on the status bar table when the strategy is running table.b1 Just towards b1 Enter in this cell "stock:" + account.Stocks + "#ff00ff"; These data can be compared with screenshots; try it yourself.
    table.b1 = "stock:" + account.Stocks + "#ff00ff";
    table.c1 = "Fstock:" + account.FrozenStocks + "#ff00ff";
    table.d1 = "balance:" + account.Balance + "#ff00ff";
    table.e1 = "Fbalance:" + account.FrozenBalance + "#ff00ff";
    table.b2 = "open:" + records[len].Open;
    table.c2 = "high:" + records[len].High;
    table.d2 = "low:" + records[len].Low;
    table.e2 = "close:" + records[len].Close;
    table.b3 = "bids[0].price:" + depth.Bids[0].Price;
    table.c3 = "bids[0].amount:" + depth.Bids[0].Amount;
    table.d3 = "asks[0].price:" + depth.Asks[0].Price;
    table.e3 = "asks[0].amount:" + depth.Asks[0].Amount;
    table.c4 = "avgPrice:" + NowPositionInfo.avgPrice;
    table.d4 = "amount:" + NowPositionInfo.amount;
    table.e4 = "floatProfit:" + NowPositionInfo.floatProfit;
    //-------------------------------------------------------------------------
    
    //Handle strategy interaction
    get_Command();//Get and process interaction


    //Here you can customize the code that triggers actions, for example, if an indicator crosses (of course, this is your customization), you can give... tiaojian Assign value to this variable 1, That is: tiaojian = 1; In this way, if the following conditions are met, the corresponding operation will be executed.
    
    
    if(state === free && tiaojian === 1 ){//Opening conditions can be expanded freely, including indicator patterns, price differences, trading volume, etc
        //Triggered the aboveifThe conditions in brackets are used to perform specific position opening operations. For example, the digital currency transaction library template is used to handle opening positions.
        buyInfo = $.Buy(Amount);
        if(buyInfo === null){// $.BuyThis function returns null Indicates that there is a reason why the purchase was not made (that is, the position was not opened successfully. There are multiple possible reasons.)
            return;
        }
        $.SignOP((new Date()).getTime(),buyInfo.price,buyInfo.amount,1);// Mark the operation on the chart . Chart template usage can be seen in the posts on the forum
        openUpdate();
    }else if(state === _long && tiaojian === 2 ){
        sellInfo = $.Sell(NowPositionInfo.amount);
        if(buyInfo === null){
            return;
        }
        $.SignOP((new Date()).getTime(),sellInfo.price,sellInfo.amount,0);// Mark the operation on the chart
        closeUpdate();
    }
    
    
    //Update profit if closed-----------------------
    Calculate();//Calculate profit and update position status
    if(isCover === true){
        LogProfit(Profit);
        isCover = false;
    }
    //----------------------------------------
    
    //Update chart---------------------------
    $.UpDateChart(records);
    //---------------------------------
}

var table = null;
var msg = "";//Message displayed at the head of the status bar table
var isFirst = true;

function main(){
    //Initialize
    if(isLogReset === true){
        LogReset();
    }
    beginAccount = _C(exchange.GetAccount);//Initial account information when the program starts running
    initAccount = beginAccount;//Account information before each position opening
    table = $.TableInit(5,6);
    //Initialize table 5,Represents table generation5Columns are a b c d e    , 6Represents table generation 6Rows are  0  1  2  3  4  5  6    . This way, the coordinates of the top-left cell of the table are a0 ,  table.a0 = 3; At this time, it will be displayed in the corresponding table
    
    //Write the unchangeable content into the table------------------
    table.a1 = "account:" + "#ff00ff";
    table.a2 = "records[length-1]:";
    table.a3 = "depth.Bids[0]/Asks[0]:";
    table.a0 = "beginAccount:";
    table.b0 = "stock:" + beginAccount.Stocks;
    table.c0 = "Fstock:" + beginAccount.FrozenStocks;
    table.d0 = "balance:" + beginAccount.Balance;
    table.e0 = "Fbalance:" + beginAccount.FrozenBalance;
    //----------------------------------------------------

    while(true){
        Loop();//Loop Function
        $.UpDateLogStatus(msg);//Update table data
        msg = "";
        Sleep(Interval);
    }
}

```

> Detail

https://www.fmz.com/strategy/20663

> Last Modified

2019-02-18 16:44:55
