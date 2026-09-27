
> Name

Triangular-Arbitrage-Strategy-Trial-Version

> Author

shoujing



> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|Q3|0.5|Number of bricks moved|


> Source (javascript)

``` javascript
/*backtest
start: 2019-04-24 00:00:00
end: 2019-05-24 00:00:00
period: 1h
exchanges: [{"eid":"OKEX","currency":"BTC_USDT","balance":10000,"stocks":3},{"eid":"OKEX","currency":"LTC_USDT","balance":10000,"stocks":3},{"eid":"OKEX","currency":"LTC_BTC","balance":10000,"stocks":3}]
*/

var initAccount={//Initial account
	BTC:0.009,
	LTC:0.7,
	USDT:55,
}

var doAccount={//Operation account initialization
	BTC:0.009,
	LTC:0.7,
	USDT:55,
}

var tax = 0.0015;//Transaction rate,0.15%

function getBaseData(){
	var P1,P2,P3;//Basic price data,respectivelybtc_usdt,ltc_usdt,ltc_btctrading pair
	P1 = exchanges[0].GetTicker();
	P2 = exchanges[1].GetTicker();
	P3 = exchanges[2].GetTicker();
	return [P1,P2,P3];
}

function main() {
	Log(initAccount);
	var xunhuan  = true;//Whether the program continues execution is used to determine whether the account balance satisfies the operation. It is not considered here.
	while(xunhuan){
		var baseData =  getBaseData();//Get basic data
		if((baseData[1].Buy-baseData[0].Sell*baseData[2].Sell)*Q3>Q3*tax*(2*baseData[1].Buy+baseData[0].Sell*baseData[2].Sell)){//Taking into account the arbitrage conditions of handling fees (P2-P1*P3)*Q3>Q3*tax*(2*P2+P1*P3), note that in order to ensure that all orders can be completed, the counterparty price is used for judgment. In actual operations, the depth of transaction also needs to be considered.
			if(xunhuan){
				doAccount.LTC = doAccount.LTC + Q3*(1-tax);
				doAccount.BTC = doAccount.BTC - baseData[2].Sell*Q3;//Buy LTC, sellBTC
				doAccount.LTC = doAccount.LTC - Q3;
				doAccount.USDT = doAccount.USDT + baseData[1].Buy*Q3*(1-tax);//Sell LTC, receiveUSDT
				doAccount.BTC = doAccount.BTC + baseData[2].Sell*Q3*(1-tax);
				doAccount.USDT = doAccount.USDT - baseData[0].Sell*baseData[2].Sell*Q3;//Buy BTC, receiveUSDT
				Log('UsdtRevenue:',doAccount.USDT-initAccount.USDT,'usdt','Positive cycle arbitrage','#FF0000');
				Log('Real income:',doAccount.USDT-initAccount.USDT-(initAccount.LTC-doAccount.LTC)*baseData[1].Buy-(initAccount.BTC-doAccount.BTC)*baseData[2].Sell,'#0000FF')//Real income after deducting handling fees
			    Log(doAccount.USDT-initAccount.USDT-(initAccount.LTC-doAccount.LTC)*baseData[1].Buy-(initAccount.BTC-doAccount.BTC)*baseData[2].Sell,'#0000FF')
            }else{
				xunhuan = false;
			}
		}else if(baseData[0].Buy*baseData[2].Buy-baseData[1].Sell>(2*baseData[0].Buy*baseData[2].Buy+baseData[1].Sell)*tax){//Reverse circular arbitrage considering handling fees
			if(xunhuan){
				doAccount.LTC = doAccount.LTC - Q3;
				doAccount.BTC = doAccount.BTC + baseData[2].Buy*Q3*(1-tax);
				doAccount.LTC = doAccount.LTC + Q3*(1-tax);
				doAccount.USDT = doAccount.USDT - baseData[1].Sell*Q3;
				doAccount.BTC = doAccount.BTC - baseData[2].Buy*Q3;
				doAccount.USDT = doAccount.USDT + baseData[0].Buy*baseData[2].Buy*Q3*(1-tax);
				Log('UsdtRevenue:',doAccount.USDT-initAccount.USDT,'usdt,Reverse cycle arbitrage','#FF0000');
				Log('Real income:',doAccount.USDT-initAccount.USDT-(initAccount.LTC-doAccount.LTC)*baseData[1].Sell-(initAccount.BTC-doAccount.BTC)*baseData[2].Buy,'#0000FF')
			    Log(doAccount.USDT-initAccount.USDT-(initAccount.LTC-doAccount.LTC)*baseData[1].Buy-(initAccount.BTC-doAccount.BTC)*baseData[2].Sell,'#0000FF')
            }else{
				xunhuan = false;
			}
		}
		Sleep(1000);//Program sleeps for 1 second
	}
}

```

> Detail

https://www.fmz.com/strategy/149489

> Last Modified

2019-05-25 18:11:32
