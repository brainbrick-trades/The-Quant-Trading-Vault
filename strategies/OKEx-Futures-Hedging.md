
> Name

OKEx-Futures-Hedging

> Author

larry_super

> Strategy Description

Futures and spot hedging is arbitrage using the price difference between futures and spot. Because on the delivery day, futures will be traded according to the spot price. Once there is a price difference between futures and spot, you can obtain risk-free price difference income by shorting futures and going long on spot (or going long on futures and selling spot).

For example, the current price of BTC is 20,000 knives per unit, and the futures price is 25,000 knives per unit. At this time, I bought 1 spot BTC and shorted one futures BTC. When the delivery time comes, I will get a risk-free profit of $5,000.

The risk of futures hedging is very low. According to the current market situation of OKEX, it can roughly achieve an annualized return of 40%-50%. In extreme bullish and bearish market conditions, returns will be higher.

Strategy logic: This strategy will automatically detect the price difference between spot and futures on OKEX. When the price difference reaches the expected profit threshold, profits will be obtained through equal amount of hedging.

Strategy Features: 
Supports all futures products on OKEX (BTC, EOS, BCH, ETH, etc.))
Supports custom leverage multiples and contract types (current week, next week, etc.))
Supports custom profit expectations (for example, 40% annualized profit))
Detailed reports (including detailed strategy status, transaction history, profit tracking, etc.)
Fully automatic hedging, no manual operation needed

Risks to be faced: Risk of exchange failure

Supported Platforms: Botvs/FMZ

Detailed explanation of strategy parameters:https://www.pcclean.io/7w0e



> Source (javascript)

``` javascript
//[OKEXExplanation of futures-spot hedging
//==============================================================================================================================
/*

NOTE:
	Confirm that the ok futures operation is "full position mode""
	Confirm the contract type to operate is 'This Week'"
	Add exchanges strictly in order of two groups BCH/USDC, BCH/USD A: spot B: futures
	Strategies will adjust spot prices using the USDT/USD exchange rate!

Version History:
	9:51 2018/1/9  			first release
	14:57 2018/1/13 		officially starts running
	15:12 2018/11/15 		Automatically handle forced liquidation and improve profit targets. The report supports displaying futures positions, canceling the display of transaction history, and only displaying icons.stocks
	23:12 2019/02/15		Support button to clear all revenue logs
	16:09 2019/06/16		Support button updates the yield chart, correcting the spot price with the USDT/USD exchange rate

*/




var ExchangProcessor={
	
	createNew: function(exA,exB){
		//Strategy Arguments
		//==============================================================================================================================
		var contract_type		="this_week";		//Contract Type
		var margin_level		=10;				//Leverage multiple
		var want_profit			=0.01;				//Extra income desired(+Exchange Rate Loss)
		var ignore_range		=0.001;				//For ExampleUSDTvsUSD, Safe fluctuation range during the hedging period; the strategy will ignore fluctuations in this range
		var max_wait_order		=10000;				//Order Waiting
		var wait_ms				=3000;				//default wait in milliseconds
		var traders_recorder	=false;				//record all trades
		
		var handfee=	 {OKEX:0.001,	Futures_OKCoin:0.001};				//trading fee
		var trade_amount={ETH_USD:0.5,	BCH_USD:0.5,	BTC_USD:0.05};		//Quantity per transaction e.g.0.5Individual/Unitbch
		var contract_min={ETH_USD:10,	BCH_USD:10,		BTC_USD:100};		//How many US dollars is a contract worth? USD,Use this to calculate the number of tickets bought
		
		var price_n		={ETH_USDT:4,		ETH_USD:3,		BCH_USDT:4,		BCH_USD:3,		BTC_USDT:4,		BTC_USD:2}; 	//Price Precision
		var num_n		={ETH_USDT:3,		ETH_USD:0,		BCH_USDT:3,		BCH_USD:0,		BTC_USDT:3,		BTC_USD:0}; 	//Quantity Precision
		var minestbuy	={ETH_USDT:0.001,	ETH_USD:1,		BCH_USDT:0.001,	BCH_USD:1,		BTC_USDT:0.001,	BTC_USD:1}; 	//Minimum purchase quantity
		var price_step	={ETH_USDT:0.03,	ETH_USD:0.03,	BCH_USDT:0.05,	BCH_USD:0.05,	BTC_USDT:0.65,	BTC_USD:0.65}; 	//Unit for adjusting prices in the price list(Ten thousand per adjustment1, is roughly equal to25Minute adjustment%1)
		
		
		
		
		
		//global state variables
		//==============================================================================================================================
		var pre_time=null; 		//Record polling interval time
		var limit_orders=[];	//Limit order
		var trades=[];			//All transactions
		var pending_pos=[];		//Unfinished hedging positions
		var hedging_op=0;		//Hedging opportunities
		var hedging_real=0;		//real hedge count
		var hedging_complete=0;	//hedge completion count
		
		
		
		
		
		
		//Build processor
		var processor={};
		
		//Utility function
		//==============================================================================================================================		
		//Retry the purchase until successful return
		processor.retryBuy=function(ex,price,num,mode)
		{
			var currency=ex.GetCurrency();
			var r=ex.Buy(_N(price,price_n[currency]), _N(num,num_n[currency]));
			var tempnum=num;
			while (!r){
				Log("BuyFailed, retrying.");
				Sleep(wait_ms);
				if (mode==="spot"){
					var account=_C(ex.GetAccount);
					var ticker=_C(ex.GetTicker);
					var last=ticker.Last;
					var fixedAmount=Math.min(account.Balance*0.95/last,num);
					r=ex.Buy(_N(price,price_n[currency]), _N(fixedAmount,num_n[currency]));
				}else if(mode==="futures"){
					//tempnum=tempnum-1;
					if (tempnum===0){
						break;
					}
					r=ex.Buy(_N(price,price_n[currency]), _N(tempnum,num_n[currency]));
				}
			}
			return r;
		}
		//Retry selling until successful
		processor.retrySell=function(ex,price,num,mode){
			var currency=ex.GetCurrency();
			var r=ex.Sell(_N(price,price_n[currency]), _N(num,num_n[currency]));
			var tempnum=num;
			while (!r){
				Log("SellFailed, retrying.");
				Sleep(wait_ms);
				if (mode==="spot"){
					var account=_C(ex.GetAccount);
					var fixedAmount=Math.min(account.Stocks,num);
					r=ex.Sell(_N(price,price_n[currency]), _N(fixedAmount,num_n[currency]));
				}else if(mode==="futures"){
					//tempnum=tempnum-1;
					var position=_C(ex.GetPosition);
					if (tempnum===0 || position.length===0){
						break;
					}
					r=ex.Sell(_N(price,price_n[currency]), _N(tempnum,num_n[currency]));

				}
			}
			return r;
		}
		//get the USD exchange rate
		processor.getUSDTratio=function(){
			var r = _C(HttpQuery,"https://api.coinmarketcap.com/v2/ticker/825/");
			var o = JSON.parse(r);
			return o.data.quotes.USD.price;
		}
		//get China time
		processor.get_ChinaTimeString=function(){
			var date = new Date(); 
			var now_utc =  Date.UTC(date.getUTCFullYear(), date.getUTCMonth(), date.getUTCDate(),date.getUTCHours(), date.getUTCMinutes(), date.getUTCSeconds());
			var cdate=new Date(now_utc);
			cdate.setHours(cdate.getHours()+8);
			var localstring=cdate.getFullYear()+'/'+(cdate.getMonth()+1)+'/'+cdate.getDate()+' '+cdate.getHours()+':'+cdate.getMinutes()+':'+cdate.getSeconds();
			return localstring;
		}
		//Process pricing list
		processor.process_limiteorders=function(){
			var cur_time=new Date();
			var limit_orders_new=[];
			for (var i=0; i<limit_orders.length; ++i){
				var create_time=limit_orders[i].create_time;
				var passedtime=cur_time-create_time;
				if (passedtime>max_wait_order){
					var exchange_c=limit_orders[i].exchange;
					var order_ID=limit_orders[i].ID;
					var ordermode=limit_orders[i].mode;
					var exname=exchange_c.GetName();
					var account=_C(exchange_c.GetAccount);
					var ticker=_C(exchange_c.GetTicker);
					var last=ticker.Last;
					var orderdata=_C(exchange_c.GetOrder,order_ID);
					var type=orderdata.Type;
					var currency=exchange_c.GetCurrency();
					
					if (orderdata.Status!=ORDER_STATE_CLOSED){
						var notcompleted=orderdata.Amount-orderdata.DealAmount;
						exchange_c.CancelOrder(order_ID);
						if (type===ORDER_TYPE_BUY){
							var allowbuy=notcompleted;
							if (allowbuy>=minestbuy[currency]){
								var limited_order_ID=processor.retryBuy(exchange_c,orderdata.Price+price_step[currency],allowbuy,ordermode);
								Log("Buy at increased price."+orderdata.Price+"|"+(orderdata.Price+price_step[currency]));
								var limited_order_data={
									exchange:exchange_c,
									ID:limited_order_ID,
									create_time:new Date(),
									utcdate:processor.get_ChinaTimeString(),
									mode:ordermode
								};
								limit_orders_new.push(limited_order_data);
							}
						}else if (type===ORDER_TYPE_SELL){
							var allowsell=notcompleted;
							if (allowsell>=minestbuy[currency]){
								var limited_order_ID=processor.retrySell(exchange_c,orderdata.Price-price_step[currency],allowsell,ordermode);
								Log("Sell at reduced price."+orderdata.Price+"|"+(orderdata.Price-price_step[currency]));
								var limited_order_data={
									exchange:exchange_c,
									ID:limited_order_ID,
									create_time:new Date(),
									utcdate:processor.get_ChinaTimeString(),
									mode:ordermode
								};
								limit_orders_new.push(limited_order_data);
							}
						}
						
						//Save transaction information
						if (type===ORDER_TYPE_BUY){
							var details={
								type:"limit buy",
								time:limit_orders[i].utcdate,
								RealAmount:orderdata.DealAmount,
								WantAmount:orderdata.Amount,
								RealPrice:orderdata.Price,
								WantPrice:orderdata.Price,
								Memo:"Partially completed",
								exname:exname
								};
							if (traders_recorder){
								trades.push(details);
							}
						}else if (type===ORDER_TYPE_SELL){
							var details={
								type:"limit sell",
								time:limit_orders[i].utcdate,
								RealAmount:orderdata.DealAmount,
								WantAmount:orderdata.Amount,
								RealPrice:orderdata.Price,
								WantPrice:orderdata.Price,
								Memo:"Partially completed",
								exname:exname
								};
							if (traders_recorder){
								trades.push(details);
							}
						}
					}else{
						//Save transaction information
						if (type===ORDER_TYPE_BUY){
							var details={
								type:"limit buy",
								time:limit_orders[i].utcdate,
								RealAmount:orderdata.DealAmount,
								WantAmount:orderdata.Amount,
								RealPrice:orderdata.Price,
								WantPrice:orderdata.Price,
								Memo:"completed",
								exname:exname
								};
							if (traders_recorder){
								trades.push(details);
							}
						}else if (type===ORDER_TYPE_SELL){
							var details={
								type:"limit sell",
								time:limit_orders[i].utcdate,
								RealAmount:orderdata.DealAmount,
								WantAmount:orderdata.Amount,
								RealPrice:orderdata.Price,
								WantPrice:orderdata.Price,
								Memo:"completed",
								exname:exname
								};
							if (traders_recorder){
								trades.push(details);
							}
						}
					}
				}else{
					limit_orders_new.push(limit_orders[i]);
				}
			}
			limit_orders=limit_orders_new;
		}
		//Forcing limit order
		processor.force_limited_order=function(type,ex,price,num,mode){
			if (type==="buy"){
				var buyID=processor.retryBuy(ex,price,num,mode);
				var order1={
					exchange:ex,
					ID:buyID,
					create_time:new Date(),
					utcdate:processor.get_ChinaTimeString(),
					mode:mode
				};
				limit_orders.push(order1);
			}
			if (type==="sell"){
				var sellID=processor.retrySell(ex,price,num,mode);
				var order1={
					exchange:ex,
					ID:sellID,
					create_time:new Date(),
					utcdate:processor.get_ChinaTimeString(),
					mode:mode
				};
				limit_orders.push(order1);
			}
			
			while(limit_orders.length!==0){
				//process limited orders
				processor.process_limiteorders();
				Sleep(wait_ms);
			}
		}
		
		
		
		
		
		
		
		
		//Initialize
		//==============================================================================================================================
		processor.init_obj=function(){
			_CDelay(wait_ms);
			pre_time = new Date();
		}
		
		
		
		
		
		
		
		
		//Process transactions
		//==============================================================================================================================
		processor.work=function(){
			var cur_time = new Date();
			var passedtime=cur_time-pre_time;
			pre_time=cur_time;
			
			var USDT_r=processor.getUSDTratio();
			
			//get information
			var A_account=_C(exA.GetAccount);
			var A_exname=exA.GetName();
			var A_currency=exA.GetCurrency();
			var A_quotecurrency=exA.GetQuoteCurrency();
			var A_ticker=_C(exA.GetTicker);
			var A_last=A_ticker.Last;
			var A_last_fixed=A_last*USDT_r;	//Fixed price: ETH/USD
			var A_depth=_C(exA.GetDepth);
			var A_orders=_C(exA.GetOrders);
			var A_buy1=A_depth.Bids[0].Price;
			var A_sell1=A_depth.Asks[0].Price;
			
			exB.SetContractType(contract_type);
			exB.SetMarginLevel(margin_level);
			var B_account=_C(exB.GetAccount);
			var B_exname=exB.GetName();
			var B_currency=exB.GetCurrency();
			var B_quotecurrency=exB.GetQuoteCurrency();
			var B_ticker=_C(exB.GetTicker);
			var B_last=B_ticker.Last;
			var B_depth=_C(exB.GetDepth);
			var B_orders=_C(exB.GetOrders);
			var B_buy1=B_depth.Bids[0].Price;
			var B_sell1=B_depth.Asks[0].Price;
			
			var cdiff=Math.abs(B_last-A_last_fixed)/A_last_fixed;
			var cdiff2=(B_last-A_last_fixed)/A_last_fixed;
			var target_bofu=want_profit+handfee[A_exname]*2+handfee[B_exname]*2+ignore_range;
			
			
			//Start hedging
			if (limit_orders.length===0 && A_last_fixed>B_last && cdiff>target_bofu){
				
				hedging_op++;
				
				var heyuefenshu_B=_N(trade_amount[B_currency]*B_last/contract_min[B_currency],0);
				var exact_amount=heyuefenshu_B*contract_min[B_currency]/B_last;
				
				if (A_account.Stocks*0.9>exact_amount && B_account.Stocks*0.9>exact_amount){
					
					hedging_real++;
					
					//sell 1 bch from A
					processor.force_limited_order("sell",exA,A_buy1,exact_amount,"spot");
					//buy 1 bch from B
					exB.SetDirection("buy");
					processor.force_limited_order("buy",exB,B_sell1,heyuefenshu_B,"futures");
					
					var posA={
						type:'spot-sell',
						exchange:exA,
						price:A_buy1,
						amount:exact_amount,
						starttime:processor.get_ChinaTimeString()
					};
					pending_pos.push(posA);
					var posB={
						type:'futures-buyup',
						exchange:exB,
						price:B_sell1,
						amount:heyuefenshu_B,
						starttime:processor.get_ChinaTimeString()
					};
					pending_pos.push(posB);

				}
				
			}
			if (limit_orders.length===0 && A_last_fixed<B_last && cdiff>target_bofu){
				
				hedging_op++;
				
				var heyuefenshu_B=_N(trade_amount[B_currency]*B_last/contract_min[B_currency],0);
				var exact_amount=heyuefenshu_B*contract_min[B_currency]/B_last;
				
				if (A_account.Balance*0.9>exact_amount*A_last && B_account.Stocks*0.9>exact_amount){
					
					hedging_real++;
					
					//buy 1 bch from A
					processor.force_limited_order("buy",exA,A_sell1,exact_amount,"spot");
					//sell 1 bch from B
					exB.SetDirection("sell");
					processor.force_limited_order("buy",exB,B_sell1,heyuefenshu_B,"futures");
					
					var posA={
						type:'spot-buy',
						exchange:exA,
						price:A_sell1,
						amount:exact_amount,
						starttime:processor.get_ChinaTimeString()
					};
					pending_pos.push(posA);
					var posB={
						type:'futures-buydown',
						exchange:exB,
						price:B_sell1,
						amount:heyuefenshu_B,
						starttime:processor.get_ChinaTimeString()
					};
					pending_pos.push(posB);

				}
			}
			
			//End hedging
			if (limit_orders.length===0 && cdiff<=ignore_range && A_orders.length===0 && B_orders.length===0 && pending_pos.length>0){
				
				hedging_complete++;
				
				for (var thidx=0; thidx<pending_pos.length; ++thidx){
					var posinfo=pending_pos[thidx];
					var ticker=_C(posinfo.exchange.GetTicker);
					var last=ticker.Last;
					var depth=_C(posinfo.exchange.GetDepth);
					var buy1=depth.Bids[0].Price;
					var sell1=depth.Asks[0].Price;
					var account=_C(posinfo.exchange.GetAccount);
					if (posinfo.type==='futures-buydown'){
						posinfo.exchange.SetDirection("closesell");
						processor.force_limited_order("sell",posinfo.exchange,buy1,posinfo.amount,"futures");
					}
					if (posinfo.type==='futures-buyup'){
						posinfo.exchange.SetDirection("closebuy");
						processor.force_limited_order("sell",posinfo.exchange,buy1,posinfo.amount,"futures");
					}
					
					if (posinfo.type==='spot-buy'){
						processor.force_limited_order("sell",posinfo.exchange,buy1,Math.min(account.Stocks,posinfo.amount),"spot");
					}
					if (posinfo.type==='spot-sell'){
						processor.force_limited_order("buy",posinfo.exchange,sell1,Math.min(account.Balance/last,posinfo.amount),"spot");
					}
				}
				
				pending_pos=[];
			}
			
			//Automatically release hedging positions
			var B_position=_C(exB.GetPosition);
			if (B_position.length===0 && pending_pos.length>0 && limit_orders.length===0 && A_orders.length===0 && B_orders.length===0){
				Log('detectedOkexPosition has been forcibly liquidated, automatically releasing hedging positions.');
				
				hedging_complete++;
				
				for (var thidx=0; thidx<pending_pos.length; ++thidx){
					var posinfo=pending_pos[thidx];
					var ticker=_C(posinfo.exchange.GetTicker);
					var last=ticker.Last;
					var depth=_C(posinfo.exchange.GetDepth);
					var buy1=depth.Bids[0].Price;
					var sell1=depth.Asks[0].Price;
					var account=_C(posinfo.exchange.GetAccount);
					
					if (posinfo.type==='spot-buy'){
						processor.force_limited_order("sell",posinfo.exchange,buy1,Math.min(account.Stocks,posinfo.amount),"spot");
					}
					if (posinfo.type==='spot-sell'){
						processor.force_limited_order("buy",posinfo.exchange,sell1,Math.min(account.Balance/last,posinfo.amount),"spot");
					}
				}
				
				pending_pos=[];
			}
			
			
			//status
			var table1 = {type: 'table', title: 'exchange', cols: ['exchange','trading pair','Latest price','Money','Currency','Pending orders','Buy one','Sell one'], rows: []};
			var table2 = {type: 'table', title: 'Statistics', cols: ['Polling time','Current spread','Target spread','Hedging opportunities/Actual number of hedges/hedge completion count','USDT/USD','Ignore fluctuation range'], rows: []};
			var table3 = {type: 'table', title: 'Unfinished hedging positions', cols: ['exchange','Type','Price','Quantity','Position opening time'], rows: []};
			var table4 = {type: 'table', title: 'Uncompleted pricing orders', cols: ['exchange','OrderID','Date of issue'], rows: []};
			var table5 = {type: 'table', title: 'Transaction History', cols: ['exchange','Date','Type', 'Transaction quantity','Order quantity','transaction price','order price','Notes'], rows: []};
			var table6 = {type: 'table', title: 'Futures Position', cols: ['exchange','Position','frozen amount','Average position price','Achieve profitability','Type','Contract Code'], rows: []};
			table1.rows.push([A_exname,A_currency,A_last+'(corrected price:'+A_last_fixed+')',A_account.Balance,A_account.Stocks,A_orders.length,A_depth.Bids[0].Price,A_depth.Asks[0].Price]);
			table1.rows.push([B_exname,B_currency,B_last,B_account.Balance,B_account.Stocks,B_orders.length,B_depth.Bids[0].Price,B_depth.Asks[0].Price]);
			table2.rows.push([passedtime+'Millisecond',cdiff2,target_bofu,hedging_op+'/'+hedging_real+'/'+hedging_complete,USDT_r,ignore_range]);
			for (var thidx=0; thidx<pending_pos.length; ++thidx){
				var posinfo=pending_pos[thidx];
				table3.rows.push([posinfo.exchange.GetName(),posinfo.type,posinfo.price,posinfo.amount,posinfo.starttime]);
			}
			for (var idx2=0; idx2<limit_orders.length; ++idx2){
				var info=limit_orders[idx2];
				table4.rows.push([info.exchange.GetName(),info.ID,info.utcdate]);
			}
			for (var i=0; i < trades.length; i++){
				table5.rows.push([trades[i].exname,trades[i].time,trades[i].type,trades[i].RealAmount,trades[i].WantAmount,trades[i].RealPrice,trades[i].WantPrice,trades[i].Memo]);
			}
			for (var i=0; i < B_position.length; i++){
				table6.rows.push([B_exname,B_position[i].Amount,B_position[i].FrozenAmount,B_position[i].Price,B_position[i].Profit,B_position[i].Type,B_position[i].ContractType]);
			}

			processor.logstatus=('`' + JSON.stringify([table1,table2,table3,table4,table6,table5])+'`'+'\n');
			processor.stocksbalance=A_account.Stocks+B_account.Stocks;
			
			//sleep
			Sleep(wait_ms);
		}
		
		return processor;
	}
};









//Main Function
//==============================================================================================================================
function main(){
	var processors=[];
	for (var i=0; i<exchanges.length; i+=2){
		var p=ExchangProcessor.createNew(exchanges[i],exchanges[i+1]);
		processors.push(p);
	}
	for (i=0; i<processors.length; ++i){
		processors[i].init_obj();
	}
	
	var pre_profit=Number(_G("pre_profit"));
	Log('Previous income accumulation:'+pre_profit);
	var lastprofit=-1;
	var total_loop=0;
	var beginrunning=processors[0].get_ChinaTimeString();

	while(true){
		
		//running processors
		total_loop++;
		var allstatus='';
		allstatus+=('♞Strategy start time: '+beginrunning+'#0000ff\n');
		var mybalance=0;
		for (i=0; i<processors.length; ++i){
			processors[i].work();
			allstatus+=processors[i].logstatus;
			mybalance+=processors[i].stocksbalance;
		}
		allstatus+=('♜Polling Times: '+total_loop+'\n');
		allstatus+=('♜Update Time: '+processors[0].get_ChinaTimeString()+'\n');
		allstatus+=('♜Strategy is for learning and communication purposes only!Real trading risk borne by oneself!#0000ff'+'\n');
        allstatus+=('♜WeChat:alinwo (Verification message: botvs)'+'\n');
		allstatus+=('`'+JSON.stringify({'type':'button', 'cmd': 'clearprofitchart', 'name': 'Clear profit chart'})+'`'+'\n');
		allstatus+=('`'+JSON.stringify({'type':'button', 'cmd': 'logprofit', 'name': 'Update profit chart'})+'`'+'\n');
		LogStatus(allstatus);
		
		if (lastprofit!==mybalance && total_loop%300===0){
			LogProfit(mybalance);
			_G("pre_profit", mybalance);
			lastprofit=mybalance;
		}
		
		//process button commands
		var cmd=GetCommand();
        if (cmd!==null && cmd==='clearprofitchart') { 
			LogProfitReset();
            Log("All revenue logs have been cleared!");
        } 
		if (cmd!==null && cmd==='logprofit') { 
			LogProfit(mybalance);
			_G("pre_profit", mybalance);
			Log("Earnings chart updated!");
        } 
	}
}
```

> Detail

https://www.fmz.com/strategy/157269

> Last Modified

2019-07-16 14:06:39
