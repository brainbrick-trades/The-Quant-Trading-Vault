
> Name

Platform-Price-Indicator-Monitoring-11

> Author

tfboys

> Strategy Description

1.5---Can be monitoredATR,RSI,BOLL,PRICE
1.4---Add Alarm Cycle Settings
1.3---Add WeChat notification
1.2---Supported futures platforms
1.1---Stable version

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|CType0|0|Currency type 0: RMB | USD|
|ContractType0|0|Contract types for No.0: This Week | Next Week | Current Month | Quarterly|
|MLevel0|0|All leverage sizes: 10x|20x|
|LoopInterval|500|Polling interval (milliseconds)|
|MaxVal|2755|Value upper limit|
|MinVal|2730|Value lower limit|
|AlarmPeriod|2|Alarm cycle (unit: polling time)|
|Interval|500|Function retry interval|
|Period|14|timeframe|
|Index|0|Indicator type: ATR|RSI|BOLL|PRICE|
|RecordsHand|false|Manually collect candlestick|
|CleanLog|true|Clear log charts|




|Button|Default|Description|
|----|----|----|
|Push switching|__button__|WeChat push|


> Source (javascript)

``` javascript
var _ContractType0 = ["this_week", "next_week", "month", "quarter"][ContractType0];
var _MarginLeve0 = [10, 20][MLevel0];
var usdrate0 = 6.35;
var rate0 = 1;
var TS = 0;		//Whether to alert
var _CType0 = [0, 1][CType0];
var _Index 	= [0, 1, 2, 3][Index];	//atr,rsi,boll

var CanAlarm = true;
var LastRcdTime = 0;
var arrValue1 = 0;
var arrValue1Last1 = 0;
var arrValue1Last2 = 0;
var ArrayPrice = null;
var ArrayLen = 0;

//External value
//var MaxRate = 104.2	//maximum value
//var MinVal = 103.2	//Minimum value
//var AlarmPeriod = 120;	//Unit:onetickertime, approximately0.5second
//var Interval = 500;			//Retry interval
//var Period = 12;
//var RecordsHand = true;	//Manually collect candlestick
//var CleanLog = true;		//Clear log charts

//Constant
var RsiMid = 50;

//{Custom interval
function UpArrayNGetAvg(valIn, arr, arrLen) {
	//Variables
	var nowOp = 0;
	var nowHi = 0;
	var nowLo = 0;
	var newLen = 0;
	
	if (valIn) {
		if(arr.length <= 0){
			nowOp = valIn.Last;
			nowHi = valIn.Sell;
			nowLo = valIn.Buy;
		}
		else{
			nowOp = arr[arr.length - 1].Close;
			nowHi = Math.max(arr[arr.length - 1].Close, valIn.Sell, valIn.Last);
			nowLo = Math.min(arr[arr.length - 1].Close, valIn.Buy, valIn.Last);
		}
		
		var rcd = {Time:new Date().getTime(), Open:nowOp, High:nowHi, Low:nowLo, Close:valIn.Last, Volume:valIn.Volume};
		newLen = arr.push(rcd);
		while(newLen > arrLen){
			arr.splice(0, 1);	//Delete the first element
			newLen = arr.length;
		}
	}

	return arr;
}

ARRAY_ZEROS = function(len) {
    var n = [];
    return n;
};
//}

function _N(v, precision) {
    if (typeof(precision) != 'number') {
        precision = 4;
    }
	if(!v)
		return 0;
	
    var d = parseFloat(v.toFixed(Math.max(10, precision+5)));
    s = d.toString().split(".");
    if (s.length < 2 || s[1].length <= precision) {
        return d;
    }

    var b = Math.pow(10, precision);
    return Math.floor(d*b)/b;
}

function GetTicker(e) {
    while (true) {
        var ticker = EnsureCall(e, 'GetTicker');
        if (ticker && ticker.Buy > 0 && ticker.Sell > 0 && ticker.Sell > ticker.Buy) {
            return ticker;
        }
        Sleep(Interval);
    }
}

function EnsureCall(e, method) {
    var r;
    while (!(r = e[method].apply(this, Array.prototype.slice.call(arguments).slice(2)))) {
        Sleep(Interval);
    }
    return r;
}

function sdGetDepth(e) {
	var dpth = null;
	while ( !(dpth = e.GetDepth()) || dpth.Asks.length <= 0 || dpth.Bids.length <= 0) {
		Sleep(Interval);
	}
	return dpth;
}

function getCmd() {
	var cmd = GetCommand();
	if(cmd) {
		//Log(" ------ : ", cmd);
		var strNum = cmd.replace(/[^0-9]/ig,"");
		if(cmd.indexOf("Push switching") >= 0)
		{
			var ms = "Current push status is: ";
			if(TS == 1) {
				TS = 0;
				ms = ms + "without";
			}
			else {
				TS = 1;
				ms = ms + "Yes";
			}

			Log(ms, "#000000ff0000");
		}
	}
}
	
function main()  {
	//Cleanup
	if(CleanLog){
		LogProfitReset();
		LogReset();
	}
	
	//Local variable declaration
	var ticker0 = null;
	var price0 = 0;
	var priceLast = 0;
	var tickerCnt = 0;
	var records = null;
	var name0 = exchanges[0].GetName();
	var coin0 = exchanges[0].GetCurrency();
	
	//Check and Set Exchange
	if(exchanges[0].GetName() == 'Futures_OKCoin') {
		Log(name0, coin0, "Yes/Is:Futures price");
    	exchanges[0].SetContractType(_ContractType0);
    	exchanges[0].SetMarginLevel(_MarginLeve0);
	}
	else
		Log(name0, coin0, "Yes/Is:Spot price");
	
	usdrate0 = exchanges[0].GetUSDCNY();
	rate0 = exchanges[0].GetRate();

	//Set the exchange rate and log,Internal usage value
	if(_CType0 == 1){//Require usage in USD
		if(rate0 == 1)	//Current RMB denomination
			exchanges[0].SetRate(1/usdrate0);
		else
			exchanges[0].SetRate(1);
	}
	else			//Require to use RMB			
	{
		if(rate0 == 1)	//Current RMB denomination
			exchanges[0].SetRate(1);
		else
			exchanges[0].SetRate(usdrate0);
	}
	
    Log(name0, _CType0 == 0 ? "Denominated Currency: RMB" : "Denominated Currency: USD");
    SetErrorFilter("502:|503:|network|timeout|WSARecv|Connect|GetAddr|no such|reset");
	EnableLogLocal(false);
	LoopInterval = Math.max(LoopInterval, 100);

	//Initialize variable
    Log('Current robotID: ', _G(), 'Start Running...');
	Log('Current Alarm Push Status: ', TS==0 ? 'without' : 'Yes', "#0000ff");
	Log('Polling Interval: ', _N(LoopInterval / 1000.0, 1), 'second');
	Log('Alarm cycle: Polling', AlarmPeriod, 'Alarm once every time !');

	//Initialize
	var rcd = exchange.GetRecords();
    while ((_Index != 3) && (!rcd || rcd.length < (Period + 20))) {
		rcd = exchange.GetRecords();
		Sleep(Interval);
    }
	ArrayLen = Math.max(rcd.length, (Period + 20));
	ArrayPrice = ARRAY_ZEROS(ArrayLen);

	while (true) {
		//Get command
		getCmd();

		tickerCnt = tickerCnt + 1;
		//Update alert standards
		if(tickerCnt % (AlarmPeriod+1) == 0) {
			CanAlarm = true;
			tickerCnt = 0;
		}

		//{
		if(_Index == 0 || _Index == 1 || _Index == 2)
		{
			if(RecordsHand == true){
				//Statistics stage
				var ticker0 = GetTicker(exchange);
				records = UpArrayNGetAvg(ticker0, ArrayPrice, ArrayLen);
			}
			else
		    	records = exchanges[0].GetRecords();
			
		    if (!records || records.length < (Period + 5)) {
				Sleep(Interval);
				if(records)
					Log(records[records.length - 1]);
		        continue;
		    }
			
			if(LastRcdTime == records[records.length - 1].Time)
				continue;
			else
				LastRcdTime = records[records.length - 1].Time;
		}
		else if(_Index == 3)
		{
			ticker0 = GetTicker(exchanges[0]);
			price0 = ticker0.Last;
		}

		var arr = null;
		if(_Index == 0)		//atr
			arr = TA.ATR(records, Period);
		else if(_Index == 1)	//rsi
			arr = TA.RSI(records, Period);
		else if(_Index == 2)	//boll
			arr = TA.BOLL(records, Period, 2);

		//Print
		if(_Index == 0){
			arrValue1 = arr[arr.length - 2];
			LogProfit(arrValue1, "Time: ", records[records.length - 1]);
		}
		else if(_Index == 1){
			arrValue1 = arr[arr.length - 2];
			LogProfit(arrValue1, "Time: ", records[records.length - 1].Time);
		}
		else if(_Index == 2){
			arrValue1 = arr[0][arr[0].length - 2] - arr[2][arr[2].length - 2];
			LogProfit(arrValue1, "Time: ", records[records.length - 1].Time, "upValue: ", arr[0][arr[0].length - 2], "downValue: ", arr[2][arr[2].length - 2]);
		}
		else if(_Index == 3){
			arrValue1 = price0;
			//var nowDate = new Date();
			LogProfit(arrValue1, "Time: ", new Date().getTime());
		}
		//}

		//Push
		if(TS) 
		{
			if(_Index == 0) {
				if(arrValue1 >= MaxVal && CanAlarm == true) {
					Log('ATRLow value: ', arrValue1, '! Warning value range:<', MinVal, ', ', MaxVal,'> !@');
					CanAlarm = false;
				}
				if(arrValue1 <= MinVal && CanAlarm == true) {
					Log('ATRHigh value:', arrValue1, '! Warning value range:<', MinVal, ', ', MaxVal,'> !@');
					CanAlarm = false;
				}
			}
			else if(_Index == 1) {
				if(arrValue1 >= RsiMid && arrValue1Last1 <= RsiMid && arrValue1 > arrValue1Last1 && CanAlarm == true) {
					Log('RSITravel through: value ---> ', arrValue1, '! Crossing value range:<', arrValue1Last1, ', ', arrValue1,'> !@');
					CanAlarm = false;
				}
				if(arrValue1 <= RsiMid && arrValue1Last1 >= RsiMid && arrValue1 < arrValue1Last1 && CanAlarm == true) {
					Log('RSINext time travel: value ---> ', arrValue1, '! Warning value range:<', arrValue1Last1, ', ', arrValue1,'> !@');
					CanAlarm = false;
				}
			}
			else if(_Index == 2){
				if(arrValue1Last1 > arrValue1Last2 && arrValue1Last1 > arrValue1 && arrValue1Last2 != 0) {
					Log('BOLLValue peaks:', arrValue1, '! Peaking interval:<', arrValue1Last2, ', ', arrValue1Last1, ', ', arrValue1,'> !@');
					CanAlarm = false;
				}
				if(arrValue1Last1 < arrValue1Last2 && arrValue1Last1 < arrValue1 && arrValue1Last2 != 0) {
					Log('BOLLValue bottoms out:', arrValue1, '! Bottoming range:<', arrValue1Last2, ', ', arrValue1Last1, ', ', arrValue1,'> !@');
					CanAlarm = false;
				}
			}
			else if(_Index == 3){
				if(price0 >= MaxVal && priceLast <= MaxVal && price0 > priceLast && CanAlarm == true) {
					Log('Price rises out of range: ', price0, '! Warning value range:<', MinVal, ', ', MaxVal,'> !@');
					CanAlarm = false;
				}
				if(price0 <= MinVal && priceLast >= MaxVal && price0 < priceLast && CanAlarm == true) {
					Log('Price falls out of range:', price0, '! Warning value range:<', MinVal, ', ', MaxVal,'> !@');
					CanAlarm = false;
				}
			}
		}

		//Update status value
		if(_Index == 0){
			//if(arrValue1Last1 != arrValue1) 		arrValue1Last1 = arrValue1;
			//if(arrValue1Last2 != arrValue1Last1) 	arrValue1Last2 = arrValue1Last1;
		}
		else if(_Index == 1){
			if(arrValue1Last1 != arrValue1) 		arrValue1Last1 = arrValue1;
			//if(arrValue1Last2 != arrValue1Last1) 	arrValue1Last2 = arrValue1Last1;
		}
		else if(_Index == 2){
			if(arrValue1Last2 != arrValue1Last1) 	arrValue1Last2 = arrValue1Last1;// 2 <--- 1
			if(arrValue1Last1 != arrValue1) 		arrValue1Last1 = arrValue1;		// 1 <--- 0
		}
		else if(_Index == 3){
			if(priceLast != price0)					priceLast = price0;
		}

		Sleep(LoopInterval);
	}
}

```

> Detail

https://www.fmz.com/strategy/12442

> Last Modified

2016-04-25 12:56:03
