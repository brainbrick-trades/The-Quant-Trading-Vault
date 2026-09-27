
> Name

Platform-Price-Comparison-10

> Author

tfboys

> Strategy Description

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
|ContractType1|0|Contract types for No.1: This Week | Next Week | Current Month | Quarterly|
|MLevel1|0|All leverage size: 10 times | 20 times|
|LoopInterval|5000|Polling interval (milliseconds)|
|MaxVal|105|Value upper limit|
|MinVal|102|Value lower limit|
|AlarmPeriod|20|Alarm cycle (unit: polling time)|
|CType1|0|Currency type 1: RMB | USD|
|Interval|1000|Function retry interval|
|Price0|0|All 0 price types: Asks[0]|Last|Bids[0]|
|Price1|0|All 1 price types: Asks[0]|Last|Bids[0]|
|Option|0|Comparison type: Sub|Dev|




|Button|Default|Description|
|----|----|----|
|Push switching|__button__|WeChat push|


> Source (javascript)

``` javascript
var _ContractType0 = ["this_week", "next_week", "month", "quarter"][ContractType0];
var _MarginLeve0 = [10, 20][MLevel0];
var _ContractType1 = ["this_week", "next_week", "month", "quarter"][ContractType1];
var _MarginLeve1 = [10, 20][MLevel1];
var usdrate0 = 6.35;
var usdrate1 = 6.35;
var rate0 = 1;
var rate1 = 1;
var TS = 0;		//Whether to alert
var _CType0 = [0, 1][CType0];
var _CType1 = [0, 1][CType1];
var _Price0 = [0, 1, 2][Price0];//Asks[0], Last, Bids[0]
var _Price1 = [0, 1, 2][Price1];//Asks[0], Last, Bids[0]
var _Option = [0, 1][Option];	//Sub, Dev

var CanAlarm = true;

//External value
//var MaxRate = 104.2	//maximum value
//var MinVal = 103.2	//Minimum value
//var AlarmPeriod = 120;	//Unit:onetickertime, approximately0.5second
//var Interval = 500;			//Retry interval

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
	//Local variable declaration
	var ticker0 = null;
	var ticker1 = null;
	var depths0 = null;
	var depths1 = null;
	var price0 = 1;
	var price1 = 1;
	var priceDev = 0.0;
	var tickerCnt = 0;
	var name0 = exchanges[0].GetName();
	var name1 = exchanges[1].GetName();
	var coin0 = exchanges[0].GetCurrency();
	var coin1 = exchanges[1].GetCurrency();
	
	//Check and Set Exchange
	if(exchanges[0].GetName() == 'Futures_OKCoin') {
		Log(name0, coin0, "Yes/Is:Futures price");
    	exchanges[0].SetContractType(_ContractType0);
    	exchanges[0].SetMarginLevel(_MarginLeve0);
	}
	else
		Log(name0, coin0, "Yes/Is:Spot price");
	
	if(exchanges[1].GetName() == 'Futures_OKCoin') {
		Log(name1, coin1, "Yes/Is:Futures price");
    	exchanges[1].SetContractType(_ContractType1);
    	exchanges[1].SetMarginLevel(_MarginLeve1);
	}
	else
		Log(name1, coin1, "Yes/Is:Spot price");
	
	usdrate0 = exchanges[0].GetUSDCNY();
	usdrate1 = exchanges[1].GetUSDCNY();
	rate0 = exchanges[0].GetRate();
	rate1 = exchanges[1].GetRate();

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
	
	if(_CType1 == 1){//Require usage in USD
		if(rate1 == 1)	//Current RMB denomination
			exchanges[1].SetRate(1/usdrate1);
		else
			exchanges[1].SetRate(1);
	}
	else			//Require to use RMB			
	{
		if(rate1 == 1)	//Current RMB denomination
			exchanges[1].SetRate(1);
		else
			exchanges[1].SetRate(usdrate1);
	}
	
    Log(name0, _CType0 == 0 ? "Denominated Currency: RMB" : "Denominated Currency: USD");
	Log(name1, _CType1 == 0 ? "Denominated Currency: RMB" : "Denominated Currency: USD");
    SetErrorFilter("502:|503:|network|timeout|WSARecv|Connect|GetAddr|no such|reset");
	EnableLogLocal(false);
	LoopInterval = Math.max(LoopInterval, 100);

	//Initialize variable
    Log('Current robotID: ', _G(), 'Start Running...');
	Log('Current Alarm Push Status: ', TS==0 ? 'without' : 'Yes', "#0000ff");
	Log('Polling Interval: ', _N(LoopInterval / 1000.0, 1), 'second');
	Log('Alarm cycle: Polling', AlarmPeriod, 'Alarm once every time !');
	Log('Alarm interval: [', MinVal, ', ', MaxVal, ']');

	while (true) {
		//Get command
		getCmd();
		
		//Update market prices and depth
		ticker0 = GetTicker(exchanges[0]);
		ticker1 = GetTicker(exchanges[1]);
		depths0 = sdGetDepth(exchanges[0]);
		depths1 = sdGetDepth(exchanges[1]);
		tickerCnt = tickerCnt + 1;
		//Update alert standards
		if(tickerCnt % (AlarmPeriod+1) == 0) {
			CanAlarm = true;
			tickerCnt = 0;
		}

		if(_Price0 == 0)
			price0 = depths0.Asks[0].Price;
		else if(_Price0 == 1)
			price0 = ticker0.Last;
		else if(_Price0 == 2)
			price0 = depths0.Bids[0].Price;
		
		if(_Price1 == 0)
			price1 = depths1.Asks[0].Price;
		else if(_Price1 == 1)
			price1 = ticker1.Last;
		else if(_Price1 == 2)
			price1 = depths1.Bids[0].Price;

		if(price1 <= 0) {//err
			continue;
		}
		if(_Option == 0)	//Sub
			priceDev = price0 - price1;
		else			//Dev
			priceDev = price0 / price1;
		
		priceDev = _N(priceDev, 4);
		
		LogProfit(priceDev, name0, coin0, "Price: ", _N(price0,4), name1, coin1, "price.": ", _N(price1,4));

		if(TS) {
			if(priceDev >= MaxVal && CanAlarm == true) {
				Log('Upper wear value: ', priceDev, '! Warning value range:<', MinVal, ', ', MaxVal,'> !@');
				CanAlarm = false;
			}
			if(priceDev <= MinVal && CanAlarm == true) {
				Log('penetration value:', priceDev, '! Warning value range:<', MinVal, ', ', MaxVal,'> !@');
				CanAlarm = false;
			}
		}

		Sleep(LoopInterval);
	}
}


```

> Detail

https://www.fmz.com/strategy/8266

> Last Modified

2015-12-10 21:35:13
