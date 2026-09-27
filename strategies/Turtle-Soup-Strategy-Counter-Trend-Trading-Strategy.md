
> Name

Turtle-Soup-Strategy-Counter-Trend-Trading-Strategy

> Author

coin989

> Strategy Description

Turtle Soup, referred to as "Turtle Soup", is a trading strategy that is contrary to the Turtle trading rules. It takes advantage of the shortcomings of trend trading (especially the Turtle method) in many false breakthroughs to make profits (making turtles into soup and eating them).

In the early 1980s, there was a very famous group of traders called the "Turtles". Richard Dennis, the market guru who created the trading legend, came up with this interesting name when he was training a group of new traders. Because Richard believes that training traders is actually like Singaporeans raising turtles. This trading method is called the Turtle Method. This simple trend following technique has made their mentor Richard achieve great success.

More than twenty years later, the Turtle Method is no longer a secret and many people understand it. Despite this, why aren't many people trading successfully with it? That's because trend following strategies often need to endure large and prolonged retracements. Many investors or traders do not have the capital or the willingness to hold on to these long-term losses. Usually most people get out before the trade turns in their favor.

Linda Warski and Larry Connaugh named this "Turtle Soup" trading rule, which is the opposite of the "Turtle" trading rule, in their book "Wall Street Wizards-Tried and Tried Short-term Trading Strategies" (Street Smarts). The reason most strategies fail to remain profitable is that their profitability degrades once many market participants use them. This is the method the market uses to balance those imbalances. Huasky found more successful and profitable results by trading the opposite of the Turtle method. Because the Turtle Method requires a lot of losing trades and waiting for bad trades to become profitable. Usually when it makes a profit, it offsets all those losses before making a profit, and this happens over and over again. Obviously, the name of the strategy "Turtle Soup" created by Waskey is a kind of American humor. It uses the costs of turtle traders to make profits (making turtles into soup and eating them).).

The original "Turtle" trading rules were at least swing trading or longer, with time spans between a week and a month. Ms. Huaski uses the "turtle soup" strategy to do shorter-term intraday or swing trading, taking advantage of the high-frequency occurrence of false breakthroughs. Generally speaking, the "turtle" method uses a 20-day cycle breakout: buy if it breaks the 20-day high, and sell if it falls below the 20-day low. The "Turtle Soup" trading rule takes the exact opposite approach.

Strategy Features:
Supports Trend Following on Any Timeframe (Minute, Hourly, Daily, Weekly, etc.))
Supports any trading pair (ETH/BTC, BSV/BTC, etc.))
Supports Any Exchange
Detailed Strategy Report (Including Strategy Status, Trading History, etc.))
Supports nearly 10 custom personalized parameters

Dependency: download botvs_tools template library: 
https://www.pcclean.io/9o7u



> Source (javascript)

``` javascript
var strategy_version="1.0.0.0(new release For learning and research purposes only, real trading consequences are your own responsibility. Access to real trading strategieshttp://pcclean.io/quant  )";

var price_n={Futures_OKCoin_BSV_USD:2};
var num_n={Futures_OKCoin_BSV_USD:0};
var minestbuy={Futures_OKCoin_BSV_USD:1};
var price_step={Futures_OKCoin_BSV_USD:0.05};
var contract_min={Futures_OKCoin_BSV_USD:10};
var wait_ms=3000;
var max_wait_order=15000;
var max_positions=4;

//gloabl variables
var positions_duo=[];
var positions_kong=[];
var total_loop=0;
var bet_duo=0;
var bet_kong=0;

function main(){
	Log("strategy_version="+strategy_version);
	$.set_params(price_n,num_n,minestbuy,price_step,wait_ms,max_wait_order);
	while(true){
		var exname=exchange.GetName();
		var currency=exchange.GetCurrency();
		var account=_C(exchange.GetAccount);
		var ticker=_C(exchange.GetTicker);
		var depth=_C(exchange.GetDepth);		
		var sell1=depth.Asks[0].Price;
		var buy1=depth.Bids[0].Price;
		var records=_C(exchange.GetRecords);
		if (records.length<=50){
			Log("records.lengthInvalid,Skip this execution...");
			Sleep(wait_ms);
			continue;
		}
		var atr = TA.ATR(records, 20);
		if (atr.length<=1){
			Log("atr.lengthInvalid,Skip this execution...");
			Sleep(wait_ms);
			continue;
		}
		var N=atr[atr.length-1];
		var position_unit=account.Stocks/(max_positions*2);
		var highest20=TA.Highest(records, 20, 'High');
		var lowest20=TA.Lowest(records, 20, 'Low');
		var highest10=TA.Highest(records, 10, 'High');		
		var lowest10=TA.Lowest(records, 10, 'Low');
		
		//Open a position
		if (positions_duo.length===0){
			if (sell1<=lowest20){
				var heyuefenshu=_N(position_unit*sell1/contract_min[$.get_exchange_id(exchange)],0);
				exchange.SetDirection("buy");
				var dealamount=$.perform_limited_order("buy",exchange,sell1,heyuefenshu,false,"futures","buy");
				if (dealamount>0){
					var postion = {
						amount:dealamount, 
						price:sell1,
						stoploss_price:sell1-2.5*N,
						stopwin_price:sell1+2.5*N,
						};
					positions_duo.push(postion);
					bet_duo=1;
				}
			}
		}
		if (positions_kong.length===0){
			if (buy1>=highest20){
				var heyuefenshu=_N(position_unit*buy1/contract_min[$.get_exchange_id(exchange)],0);
				exchange.SetDirection("sell");
				var dealamount=$.perform_limited_order("buy",exchange,buy1,heyuefenshu,false,"futures","sell");
				if (dealamount>0){
					var postion = {
						amount:dealamount, 
						price:buy1,
						stoploss_price:buy1+2.5*N,
						stopwin_price:buy1-2.5*N,
						};
					positions_kong.push(postion);
					bet_kong=1;
				}
			}
		}
		//add to position
		if (positions_duo.length>0){
			var last_price=positions_duo[positions_duo.length-1].price;
			if (bet_duo<max_positions){
				if (last_price-sell1>=0.5*N){
					var heyuefenshu=_N(position_unit*sell1/contract_min[$.get_exchange_id(exchange)],0);
					exchange.SetDirection("buy");
					var dealamount=$.perform_limited_order("buy",exchange,sell1,heyuefenshu,false,"futures","buy");
					if (dealamount>0){
						var postion = {
							amount:dealamount, 
							price:sell1,
							stoploss_price:sell1-2.5*N,
							stopwin_price:sell1+2.5*N,
							};
						positions_duo.push(postion);
						bet_duo+=1;
					}
				}
			}
		}
		if (positions_kong.length>0){
			var last_price=positions_kong[positions_kong.length-1].price;
			if (bet_kong<max_positions){
				if (buy1-last_price>=0.5*N){
					var heyuefenshu=_N(position_unit*buy1/contract_min[$.get_exchange_id(exchange)],0);
					exchange.SetDirection("sell");
					var dealamount=$.perform_limited_order("buy",exchange,buy1,heyuefenshu,false,"futures","sell");
					if (dealamount>0){
						var postion = {
							amount:dealamount, 
							price:buy1,
							stoploss_price:buy1+2.5*N,
							stopwin_price:buy1-2.5*N,
							};
						positions_kong.push(postion);
						bet_kong+=1;
					}
				}
			}
		}
		//stop loss
		if (positions_duo.length>0){
			var positions_duo_new=[];
			for (var i=0; i < positions_duo.length; i++){
				if (buy1<=positions_duo[i].stoploss_price){
					exchange.SetDirection("closebuy");
					$.perform_limited_order("sell",exchange,buy1,positions_duo[i].amount,true,"futures","closebuy");
				}else{
					positions_duo_new.push(positions_duo[i]);
				}
			}
			positions_duo=positions_duo_new;
		}
		if (positions_kong.length>0){
			var positions_kong_new=[];
			for (var i=0; i < positions_kong.length; i++){
				if (sell1>=positions_kong[i].stoploss_price){
					exchange.SetDirection("closesell");
					$.perform_limited_order("sell",exchange,sell1,positions_kong[i].amount,true,"futures","closesell");
				}else{
					positions_kong_new.push(positions_kong[i]);
				}
			}
			positions_kong=positions_kong_new;
		}
		//take profit
		if (positions_duo.length>0){
			var positions_duo_new=[];
			for (var i=0; i < positions_duo.length; i++){
				if (buy1>=positions_duo[i].stopwin_price){
					exchange.SetDirection("closebuy");
					$.perform_limited_order("sell",exchange,buy1,positions_duo[i].amount,true,"futures","closebuy");
				}else{
					positions_duo_new.push(positions_duo[i]);
				}
			}
			positions_duo=positions_duo_new;
		}
		if (positions_kong.length>0){
			var positions_kong_new=[];
			for (var i=0; i < positions_kong.length; i++){
				if (sell1<=positions_kong[i].stopwin_price){
					exchange.SetDirection("closesell");
					$.perform_limited_order("sell",exchange,sell1,positions_kong[i].amount,true,"futures","closesell");
				}else{
					positions_kong_new.push(positions_kong[i]);
				}
			}
			positions_kong=positions_kong_new;
		}
		//close all positions
		if (positions_duo.length>0){
			if (buy1>=highest10){
				for (var i=0; i < positions_duo.length; i++){
					exchange.SetDirection("closebuy");
					$.perform_limited_order("sell",exchange,buy1,positions_duo[i].amount,true,"futures","closebuy");
				}
				positions_duo=[];
			}
		}
		if (positions_kong.length>0){
			if (sell1<=lowest10){
				for (var i=0; i < positions_kong.length; i++){
					exchange.SetDirection("closesell");
					$.perform_limited_order("sell",exchange,sell1,positions_kong[i].amount,true,"futures","closesell");
				}
				positions_kong=[];
			}
		}
		//Exchange forced liquidation
		var current_ok_position=_C(exchange.GetPosition);//must update here
		if (current_ok_position.length===0){
			positions_duo=[];
			positions_kong=[];
		}
		
		//chart
		var table1={type: 'table', title: 'Futures Position', cols: ['exchange','Position','frozen amount','Average position price','Achieve profitability','Type','Contract Code'], rows: []};
		var table2={type: 'table', title: 'Track position', cols: ['exchange','Type','Quantity','Price','Stop loss price','Take-profit price'], rows: []};
		for (var i=0; i < current_ok_position.length; i++){
				table1.rows.push([exname,
				current_ok_position[i].Amount,
				current_ok_position[i].FrozenAmount,
				current_ok_position[i].Price,
				current_ok_position[i].Profit,
				current_ok_position[i].Type,
				current_ok_position[i].ContractType]);
			}
		for (i=0; i<positions_duo.length; ++i){
			table2.rows.push([exname,'go long',positions_duo[i].amount,positions_duo[i].price,
			positions_duo[i].stoploss_price,positions_duo[i].stopwin_price]);
		}
		for (i=0; i<positions_kong.length; ++i){
			table2.rows.push([exname,'go short',positions_kong[i].amount,positions_kong[i].price,
			positions_kong[i].stoploss_price,positions_kong[i].stopwin_price]);
		}
		LogStatus(
					'`' + JSON.stringify([table1,table2])+'`'+'\n'+
					'Long position:'+positions_duo.length+'\n'+
					'Short position:'+positions_kong.length+'\n'+
					'Trading unit: '+position_unit+'\n'+
					'highest20: '+highest20+'\n'+
					'highest10: '+highest10+'\n'+
					'lowest20: '+lowest20+'\n'+
					'lowest10: '+lowest10+'\n'+
					'♜Polling Times: '+total_loop+'\n'+
					'♜Update Time: '+$.get_ChinaTimeString()+'\n'+
					'♜To customize the strategy, contact WeChat: alinwo (verification message: botvs). Real offer strategy access: http://pcclean.io/quant'+'\n'
				  );
		if (total_loop%300===0){
			LogProfit(account.Stocks);
		}
		
		Sleep(wait_ms);
		total_loop++;
	}
}
```

> Detail

https://www.fmz.com/strategy/157372

> Last Modified

2019-07-16 14:57:23
