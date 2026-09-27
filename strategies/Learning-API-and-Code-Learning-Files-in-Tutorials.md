
> Name

Learning-API-and-Code-Learning-Files-in-Tutorials

> Author

中本大料





> Source (javascript)

``` javascript
/*backtest
start: 2018-11-26 00:00:00
end: 2018-12-26 00:00:00
period: 1h
exchanges: [{"eid":"OKCoin_EN","currency":"BTC_USD"}]
*/

//
//
//
var tradeAmount = 0.1;
var wave = 5
var tide = 20
//-------------------------
var bars = null;
var newbar = null;
var Stock = null;
var Balance = null;
var depth = null;
var accountData = null;
var triggerofTrade = null;
var bidPrice = null
var askPrice = null
var oldtime = "oldtime"
var newtime = "newtime"

var next = false

function Data(){        //Data Preprocessing
    depth = _C(exchange.GetDepth);
    accountData = _C(exchange.GetAccount);      //Try to take an array back and split it,Avoid data discrepancies
    Stock = accountData.Stocks;
    Balance = accountData.Balance;
    bars = _C(exchange.GetRecords);
   // newtime = bars[bars.length-1].Time
    // if(newtime == oldtime){
    //     return  next = true
    //     }
    // newbar = bars
    // oldtime = newtime
    Log(bars[bars.length-1])
}


function main() {
    while(true){
        // next = false
        Data()
        // Log(next)
        // Log("!!!" + newbar[newbar.length-1].Time);
        // if(next = true){
        //     continue
        //     // Log("!!!" + newbar[newbar.length-1].Time);
        // }   
    
        // // Log("!!!"+ newbar)
        // //Sleep(1000)
        // Log("!!!" + newbar[newbar.length-1].Time);
        Sleep(10000)
    }
	// var begintime = new Date().getTime()
   
 //    Log("Test1  ^");
 //    var s ="hello "+"world!";
 //    Log(s[0]);
 //    Log(s);
 //    Log(s.length)
 //    Log(exchange.GetAccount());
    
 //    Log("\n");
 //    Log("Test2  ^");
 //    var symbol = "BTC_USDT"
 //        if(symbol.endsWith('USDT')){
 //            Log("The current pricing currency isUSDT")
 //           }
 //    var a = symbol.split('_')[0];   //?!How to get the first one in the array?
 //    Log(a,typeof(a));   
 //    Log(a[0]);
 //    var b = "USDT";                //Test the difference between single quotes and double quotes, there seems to be no difference
 //    var c = 'USDT'; 
 //    Log(b,typeof(b),c,typeof(c));        
    
 //    Log("\n");
 //    Log("Test3  Object Operations1^");
 //    var xiaoming = {name:"Big fool",birth:1990};
 //    var key = "birth";
 //    Log(xiaoming.name);
 //    Log(xiaoming[key]);
 //    xiaoming.score = 80;
 //        if('score' in xiaoming){
 //            Log(xiaoming)
 //        }
    
 //    Log("\n");
 //    Log("Test4  Object Operations2^");
 //    var ticker = exchange.GetTicker();
 //    Log(ticker);
 //    var price = ticker.Last;
 //    Log(price);
 //    Log(ticker.Last);
    
 //    Log("\n");
 //    Log("Test5  Boolean Operation^");
 //    var x = 1.5;
 //    var y = 2;
 //    var z = 3;
 //    if(x > y){
 //        Log("X > Y, That's right");
 //    }
 //    else{
 //        Log("X < Y, Wrong calculation");
 //    }
 //    if(x < y || x == 1){
 //        Log("That's right")                    //==Equal to !=is not equal to &&and
 //    }
    
 //    Log("\n");
 //    Log("^Learn6  Array Operations^");
 //    var arr = [1,2,3.14,"hello",'hello'];
 //    Log(arr.length,"_",arr[5],arr[4].length);
 //    Log(arr.indexOf("hello"));
 //    var records = exchange.GetRecords();
 //    Log(records);
 //    var ma = null
 //    //if(records && records.length > 20 ){
 //    	//Log("KLineBarQuantity Greater Than20,can generate moving averages")
 //    	//var ma10 = TA.MA(records,10)
 //    	//Log("ma10",ma10)
 //    	//var ma20 = TA.MA(records,20)
 //    	//Log("ma20",ma20)
 //    	//Log(ma10[11]);
 //    	//$.PlotLine('MA10', ma[11]);/
 //    //}
 //    //else{
 //    	//Log("KInsufficient number of threads, please get moreKLine or readjust the moving average period")
 //   // }

	// Log("\n");
 //    Log("^Learn7  Common data operations^");
 //    var d;
 //    Log(d);							//?Why didn't it appearundefine
 //    var tom = {name:"tom",age:10};
 //    Log(tom.name,tom.gender);  

	// Log("\n");
 //    Log("^Learn8  Define and call functions^");
 //    function test(a,b){
 //    	Log(a,b,a+b);
 //    	return;
 //    }
 //    test(1);   //null NaNWhat do they mean??

 //    Log("\n");
 //    Log("^Learn9  Conversion between data^");
 //    var xa = 123;
 //    Log(String(xa),typeof(String(xa)));
 //    Log(xa.toString(),typeof(xa.toString()));
 //    var xb = '{"free":1,"frozen":2}';  //Note the single quotes
 //    Log(xb,typeof(xb));
 //    object_xb = JSON.parse(xb);			//WillJSONConvert string to object
 //    Log(object_xb,typeof(object_xb));
 //    var obj ={address:"ABC",name:"123"}
 //    var jsonstr = JSON.stringify(obj);
 //    Log(obj,typeof(obj),jsonstr,typeof(jsonstr));

 //    Log("\n");
 //    Log("^Learn10  Conditional statement judgment^");
 //    var ticker1 = exchange.GetTicker();
 //    Log(ticker1.Last)
 //    if(ticker1.Last < 3000){
 //    	Log("ticker1 Less Than 3000")
 //    }else if(ticker1.Last > 3000 && ticker1.Last<3500){
 //    	Log("ticker1 Greater than3000 Less Than3500")
 //    }else{
 //    	Log("ticker1 Greater than > 3500");
 //    }
 //    var symbol10 = "ETH";
 //    switch(symbol10){				//Useswitch+case+break
 //    	case "ETH":
	// 		Log("The current transaction object isETH")
 //    		break;
 //    	case "BTC":
 //    		Log("The current transaction object isBTC")
 //    		break;
	// 	//case "ETH":
	// 		//Log("The current transaction object isBTC")
 //    		//break;
 //    }

 //    Log("\n");
 //    Log("^Learn11  javaLoop^");
 //    var records11 = exchange.GetRecords();
 //    Log(records11.length)
 //    if(records11){
 //    	for(i=0;i<29;i++){
 //    		Log(records11[i])
 //    	}
 //    }
 //    $.PlotRecords(records11, 'BTC');
 //    Log("vEnd of Studyv");
 //    Log("\n");

 //    Log("\n");
 //    Log("^Learn12  Traverse Object^");
 //    var assets12 ={"BTC":1.2,"BCH":1,"ETH":12};
 //    for(var a12 in assets12){
 //    	Log(a12,assets12[a12])
 //    }
 //    Log("-----------------------------");
 //    var assets121 ={"BTC":1.2,"BCH":1,"ETH":12};
 //    for(var a121 in assets121){
 //    	if(a121 == "ETH"){
 //    		continue				//Skip this loop if conditions are met
 //    	}
 //    	Log(a121,assets121)
 //    }
 //    Log("vEnd of Studyv");
 //    Log("\n");

 //    Log("^Learn13  whileLoop^");
 //    var a13 = 0
 //    while(a13 == 10){				//If Here Is a13 = 0 is not executed even once
 //    	Log("while",a13);
 //    	a13 ++ ;
 //    }
 //    var a131 = 0
 //    do{								//Usedo while The loop will execute at least once
 //    	Log("do",a131);
 //    	a131++;
 //    }while(a131 == 0)
 //    Log("-----------------------------");
 //    var n13 = 0
 //    var sum13 = 0
 //    while(true){
 //    	sum13 += n13
 //    	n13++
 //    	if(n13 > 10){
 //    		Log("My mandate is over,Take a Step First",n13,sum13)
 //    		break
 //    	}
 //    }
 //    Log("vEnd of Studyv");
 //    Log("\n");

 //    Log("^Learn14  Define a function^");
 //    function go1s(){
 //    	var time14 = new Date().getTime()
	//     Log(time14)
	//     Sleep(1000)
	//     var endtime14 =new Date().getTime()
	//     Log(endtime14 - time14)
 //    }
 //    go1s()
 //    function timenow(){
 //    	Log("Current Time:",_D())  //_D()A function encapsulated by the platform
 //    }
 //    timenow()
 //    function lastrecords(){
 //    	var records14 = exchange.GetRecords()			//GetrecordsWhat is passed in is a time period
 //    	var bar14 = records14[records14.length-1]
 //    	Log(bar14.Time)     //.TimeYes/IsbarAn Attribute of
 //    	Log("The last one barThe Time Is",_D(bar14.Time))
 //    }
 //    lastrecords()

 //    Log("vEnd of Studyv");
 //    Log("\n");

 //    Log("^Learn15  Get account information^");
 //    var account15 = exchange.GetAccount()
 //    Log(account15)
 //    exchange.Buy(3700,2)
 //    var accountstate = exchange.GetAccount()
 //    Log(accountstate)
 //    Log(exchange.GetOrders()) //See how order cancellation is done
 //    var trade15 = exchange.GetTrades()
 //    Log(trade15)  //Log(order15)
 //    Log("vEnd of Studyv");
 //    Log("\n");

 //    //LogReset()
 //    Log("^Learn16  Use indicator functions and functions to determine moving average crossovers^");
 //    var records16 = null
 //    while(1){
 //    	records16 = exchange.GetRecords()
 //    	if(records16.length>30){
 //    		break
 //    	}
 //    	Sleep(100)
 //    }
 //    var ma167 = TA.MA(records,7)
 //    var ma1630 = TA.MA(records,30)
 //    var cross16 = _Cross(ma167,ma1630)
 //    Log("crosspoint",cross16,"#FF0000")
	// Log("vEnd of Studyv");
 //    Log("\n");

 //    LogReset()
 //    Log("^Learn17  Visualization^");
 //    var i17 = 0
 //    while(1){
 //    	var random17 = Math.random()
 //    	var num17 = random17 * 10
 //    	LogProfit(num17,_D())
 //    	Sleep(5000)
 //    	i17 ++
 //    	if(i17 > 50){
 //    		break
 //    	}
 //    }
 //    Log(i17,num17)
 //    LogStatus("Current Time:",_D(),"Random value:",num17,"\n","Multiply by10The previous random number:",random17)
 //    Log("vEnd of Studyv");
 //    Log("\n");

 //    LogReset()
 //    Log("^Learn18  Loop Test^");
 //    var i18 =1
 //    while(i18<50){
 //        var orders18 = 1;
 //        // while (!(orders18 - 50 < 0)){
 //        //     Sleep(1000);
 //        //     orders18++
 //        // }
 //        while(orders18<50){
 //            orders18++
 //        }
 //        i18++
 //        //Log(i18)
 //        Log(orders18)
 //    }
 //    Log("vEnd of Studyv");
 //    Log("\n");

 //    LogReset()
 //    Log("^Learn19  ObtainKTime interval of line information^");
 //    for(var i20 = 0; i20 < 10; i20++){
 //        var records20 = exchange.GetRecords();
 //        Log(records20)
 //    }
 //    for(var i21 = 0; i21 < 10; i21++){
 //        var ticker20 = exchange.GetTicker();
 //        Log(ticker20)
 //    }
 //    Log("vEnd of Studyv");
 //    Log("\n");

    // LogReset()
    // Log("^Learn20  Continuously get the array,Prevent fetching too short^");
    //function Data(){
    // var Stock = null;
    // var Balance = null;
    // var tide =65;
    // var accountData = _C(exchange.GetAccount);
    // Stock = accountData.Stocks;
    // Balance = accountData.Balance;
    // bars = _C(exchange.GetRecords);
    // Log(bars);
    // Log(bars.length)
    // var bars = "0"
    // Log(bars.length)
    // bars = _C(exchange.GetRecords)
    // // if (bars.length < tide+1){
    // //     bars = _C(exchange.GetRecords);
    // //     }
    //     // while(bars.length < tide){
    //     //     bars = _C(exchange.GetRecords)
    //     // }
    // Log(bars.length)
        
    //     // while(true){
    //     //     var bars = _C(exchange.GetRecords);
    //     //     if(bars.length < tide + 1){
    //     //         continue
    //     //     }
    //     //     return bars
    // Log(bars,bars.length)
        

    // }
    // for (iii20 = 1; iii20<30; iii20++){
    //     Data()
    //     ;
    //     Sleep(500);
    //}
   
    // Data()
    // Log(bars)
    // Log(bars.length)
    // while(bars.length < tide+1){
    //  bars = _C(exchange.GetRecords);     //can be found atmainAdd another one to the loop if Verify  e.g. if bars.length < 10,msg = "KLine data acquisition failed,Automatic Retry" return 
    //  Sleep(500);
    // }
    //In the moving average strategy, etc., you need to passKIn strategies that judge buying and selling timing and direction based on line patterns, In backtest mode, How to ensure that the latest version is always usedKUse lines to judge indicators?






	   
    










	Log("+++++++++++++++++++++++++++++");
    // var endtime = new Date().getTime()
    // Log("The total time taken to execute the program is:",endtime-begintime,"Millisecond")
	Log("+++++++++++++++++++++++++++++")



}
```

> Detail

https://www.fmz.com/strategy/131864

> Last Modified

2019-01-02 15:41:01
