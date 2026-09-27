
> Name

RSI-Statistical-Arbitrage-Strategy

> Author

quant777

> Strategy Description

This strategy is a statistical arbitrage strategy based on the RSI indicator. According to actual measurements, it can also have a high winning rate in a bear market. The strategy will conduct RSI data analysis on the market, and once the predefined candlestick pattern is captured, short-term arbitrage will be carried out.

RSIIndicator Description:
RSIIt was first used in futures trading. Later, people found that using this indicator to guide stock market investment was also very effective, and the characteristics of this indicator were continuously summarized and summarized. Now, RSI has become one of the most widely used technical indicators by investors. The general principle of investment is that investors' buying and selling behavior is a reflection of the comprehensive results of various factors. Changes in the market ultimately depend on the relationship between supply and demand. The RSI indicator is based on the principle of supply and demand balance. It evaluates the strength of long and short forces by measuring the total increase in stock price in a certain period as a percentage of the average total change in stock price, and then prompts specific operations.

Strategy Features:
Supports Trend Following on Any Timeframe (Minute, Hourly, Daily, Weekly, etc.))
Supports any trading pair (ETH/BTC, BSV/BTC, etc.))
Supports Any Exchange
Detailed Strategy Report (Including Strategy Status, Trading History, etc.))
Supports nearly 10 custom personalized parameters

Strategy parameter description:
https://www.pcclean.io/8cut



> Source (javascript)

``` javascript
/*
RSIStrategy: For Learning Purposes Only, Use at Your Own Risk in Live Trading
*/

var ExchangProcessor={
	createNew: function(exc_obj){
		//Strategy Arguments
		var manage_assets=1;//bch
		var max_positions=4;//max=4N
		var price_n={BTC_BCH:8,ETH_BCH:8,XRP_BCH:8,EOS_BCH:8,LTC_BCH:8,DASH_BCH:8,CET_BCH:8}; //Price Precision
		var num_n={BTC_BCH:8,ETH_BCH:8,XRP_BCH:8,EOS_BCH:8,LTC_BCH:8,DASH_BCH:8,CET_BCH:8}; //Quantity Precision
		var minest_buy={BTC_BCH:0.001,ETH_BCH:0.01,XRP_BCH:1,EOS_BCH:1,LTC_BCH:0.1,DASH_BCH:0.01,CET_BCH:1};//Minimum purchase quantity
		var minest_sell={BTC_BCH:0.001,ETH_BCH:0.01,XRP_BCH:1,EOS_BCH:1,LTC_BCH:0.1,DASH_BCH:0.01,CET_BCH:1};//Minimum sell quantity
		var order_wait_secs=120000; //Maximum waiting time for orders in milliseconds
		var wait_ms=1000;//default wait in milliseconds
		var sxf=0.0005;//Used to calculate commission consumption
		
		
		//global state variables
		var positions=[];//Record Position
		var init_asset=0; //Initial Assets
		var trades=[];//All transactions
		var trades_recorder=true;//record all trades
		var pre_time=null; //Record polling interval time
		var approximate_profit=0;//Approximate profit and loss
		var add_already=0;//Number of times already added to position
		
		var processor={};
		//Retry the purchase until successful return
		processor.retryBuy=function(ex,price,num)
		{
			var currency=ex.GetCurrency();
			var r=ex.Buy(_N(price,price_n[currency]), _N(num,num_n[currency]));
			while (!r){
				Log("BuyFailed, currentlyretry.");
				Sleep(wait_ms);
				var account=_C(ex.GetAccount);
				var ticker=_C(ex.GetTicker);
				var last=ticker.Last;
				var fixedAmount=(price===-1?Math.min(account.Balance*0.95,num):Math.min(account.Balance/last*0.95,num));
				r=ex.Buy(_N(price,price_n[currency]), _N(fixedAmount,num_n[currency]));
			}
			return r;
		}
		
		//Retry selling until successful
		processor.retrySell=function(ex,price,num){
			var currency=ex.GetCurrency();
			var r=ex.Sell(_N(price,price_n[currency]), _N(num,num_n[currency]));
			while (!r){
				Log("SellFailed, currentlyretry.");
				Sleep(wait_ms);
				var account=_C(ex.GetAccount);
				var fixedAmount=Math.min(account.Stocks,num);
				r=ex.Sell(_N(price,price_n[currency]), _N(fixedAmount,num_n[currency]));
			}
			return r;
		}
		
		
		processor.get_ChinaTimeString=function(){
			var date = new Date(); 
			var now_utc =  Date.UTC(date.getUTCFullYear(), date.getUTCMonth(), date.getUTCDate(),
					date.getUTCHours(), date.getUTCMinutes(), date.getUTCSeconds());
			var cdate=new Date(now_utc);
			cdate.setHours(cdate.getHours()+8);
			var localstring=cdate.getFullYear()+'/'+(cdate.getMonth()+1)+'/'+cdate.getDate()+' '+cdate.getHours()+':'+cdate.getMinutes()+':'+cdate.getSeconds();
			return localstring;
		}
		
		processor.init_obj=function(){
			_CDelay(wait_ms);
			pre_time = new Date();
			
			//init
			{
				var account=_C(exc_obj.GetAccount);
				var ticker=_C(exc_obj.GetTicker);
				var last=ticker.Last;
				init_asset=(account.Balance+account.FrozenBalance)+(account.Stocks+account.FrozenStocks)*last;
				Sleep(wait_ms);
			}
		}
		
		
		processor.work=function(){
			var cur_time = new Date();
			var passedtime=cur_time-pre_time;
			pre_time=cur_time;
			
			//Calculationn,Position
			var exname=exc_obj.GetName();
			var currency=exc_obj.GetCurrency();
			var account=_C(exc_obj.GetAccount);
			var ticker=_C(exc_obj.GetTicker);
			var depth = _C(exc_obj.GetDepth);
			var last=ticker.Last;
			var ask1=depth.Asks[0].Price;
			var bid1=depth.Bids[0].Price;
			var bestprice=bid1+(Math.abs(ask1-bid1)/2);
			var records = _C(exc_obj.GetRecords);
			if (records.length<=50){
				Log("records.length is not valid.");
				Sleep(wait_ms);
				return;
			}
			var atr = TA.ATR(records, 20);
			if (atr.length<=1){
				Log("atr.length is not valid.");
				Sleep(wait_ms);
				return;
			}
			var N=atr[atr.length-1];
			var position_unit=Math.min(manage_assets*0.01/N,account.Balance/last*0.95);//cet
			//Log("N="+N+",  Position Unit="+position_unit+"CET");
			var highest=TA.Highest(records, 20, 'High');
			var Lowest=TA.Lowest(records, 10, 'Low');
			var cur_asset=(account.Balance+account.FrozenBalance)+(account.Stocks+account.FrozenStocks)*last;
			var rsi6 = TA.RSI(records, 6);
			var rsi12 = TA.RSI(records, 12);
			if (rsi6.length<=5 || rsi12.length<=5){
				Log("rsi is not valid.");
				Sleep(wait_ms);
				return;
			}
			var rsi_in=false;
			if (rsi6[rsi6.length-1]-rsi6[rsi6.length-2]>1 && rsi6[rsi6.length-2]<=65){
					//Log("rsi_in=true");
					rsi_in=true;
				}
			var rsi_out=false;
			if (rsi6[rsi6.length-1]>=60){
				//Log("rsi_out=true");
				rsi_out=true;
			}
			
			//Open a position
			if (positions.length==0 && position_unit>minest_buy[currency]){
				if (rsi_in)
				{
					var buyID = processor.retryBuy(exc_obj,last,position_unit);
					Sleep(order_wait_secs);
					var buyOrder=_C(exc_obj.GetOrder,buyID);
					if (buyOrder.Status!=ORDER_STATE_CLOSED){
						exc_obj.CancelOrder(buyID);
					}
					if (buyOrder.DealAmount>0){
						var postion = {
							amount:buyOrder.DealAmount, 
							buy_price:buyOrder.AvgPrice, 
							stoploss_price:buyOrder.AvgPrice-N};
						positions.push(postion);
						
						var details={
							type:"Open a position",
							time:processor.get_ChinaTimeString(),
							RealAmount:buyOrder.DealAmount,
							WantAmount:position_unit,
							RealPrice:buyOrder.AvgPrice,
							WantPrice:buyOrder.Price,
							Memo:""
							};
						if (trades_recorder){
							trades.push(details);
						}
						
						add_already=1;
					}
				}
			}
			
			//add to position
			if (positions.length>0 && position_unit>minest_buy[currency]){
				var last_buy_price=positions[positions.length-1].buy_price;
				if (add_already<max_positions){
					if (last-last_buy_price>=0.5*N){
						var buyID = processor.retryBuy(exc_obj,last,position_unit);
						Sleep(order_wait_secs);
						var buyOrder=_C(exc_obj.GetOrder,buyID);
						if (buyOrder.Status!=ORDER_STATE_CLOSED){
							exc_obj.CancelOrder(buyID);
						}
						if (buyOrder.DealAmount>0){
							var postion = {
								amount:buyOrder.DealAmount, 
								buy_price:buyOrder.AvgPrice, 
								stoploss_price:buyOrder.AvgPrice-N};
							positions.push(postion);
							
							var details={
								type:"add to position",
								time:processor.get_ChinaTimeString(),
								RealAmount:buyOrder.DealAmount,
								WantAmount:position_unit,
								RealPrice:buyOrder.AvgPrice,
								WantPrice:last,
								Memo:""
								};
							if (trades_recorder){
								trades.push(details);
							}
							
							add_already=add_already+1;
						}
					}
				}
			}
			
			//stop loss
			if (positions.length>0){
				var positions_new=[];
				for (var i=0; i < positions.length; i++){
					if (last<=positions[i].stoploss_price){
						account=_C(exc_obj.GetAccount);
						var fixedAmount=Math.min(account.Stocks,positions[i].amount);
						if (fixedAmount>minest_sell[currency]){
							var sellID = processor.retrySell(exc_obj, last, fixedAmount);
							Sleep(order_wait_secs);
							var sellOrder=_C(exc_obj.GetOrder,sellID);
							approximate_profit+=(sellOrder.AvgPrice*sellOrder.DealAmount*(1-sxf)-positions[i].buy_price*sellOrder.DealAmount*(1+sxf));
							Log("Limit Sell: Quantity-"+sellOrder.DealAmount+",approximate_profit="+approximate_profit);
							if (sellOrder.Status!=ORDER_STATE_CLOSED){
								exc_obj.CancelOrder(sellID);
								if (Math.min(account.Stocks,fixedAmount-sellOrder.DealAmount)>minest_sell[currency]){
									var marketsellOrderID=processor.retrySell(exc_obj, -1, fixedAmount-sellOrder.DealAmount);
									Sleep(order_wait_secs);
									var marketsellOrderData=_C(exc_obj.GetOrder,marketsellOrderID);
									approximate_profit+=(marketsellOrderData.AvgPrice*marketsellOrderData.DealAmount*(1-sxf)-positions[i].buy_price*marketsellOrderData.DealAmount*(1+sxf));
									Log("Market Sell: Quantity-"+marketsellOrderData.DealAmount+",approximate_profit="+approximate_profit);
								}
							}
							
							var details={
								type:"stop loss",
								time:processor.get_ChinaTimeString(),
								RealAmount:-1,
								WantAmount:fixedAmount,
								RealPrice:-1,
								WantPrice:last,
								Memo:(last>positions[i].buy_price?"Profit : Loss")
								};
							if (trades_recorder){
								trades.push(details);
							}
						}
					}else{
						positions_new.push(positions[i]);
					}
				}
				positions=positions_new;
			}
			
			//close all positions
			if (positions.length>0){
				if (rsi_out){
					var positions_new=[];
					for (var i=0; i < positions.length; i++){
						account=_C(exc_obj.GetAccount);
						var fixedAmount=Math.min(account.Stocks,positions[i].amount);
						if (fixedAmount>minest_sell[currency]){
							var sellID = processor.retrySell(exc_obj, last, fixedAmount);
							Sleep(order_wait_secs);
							var sellOrder=_C(exc_obj.GetOrder,sellID);
							approximate_profit+=(sellOrder.AvgPrice*sellOrder.DealAmount*(1-sxf)-positions[i].buy_price*sellOrder.DealAmount*(1+sxf));
							Log("Limit Sell: Quantity-"+sellOrder.DealAmount+",approximate_profit="+approximate_profit);
							if (sellOrder.Status!=ORDER_STATE_CLOSED){
								exc_obj.CancelOrder(sellID);
								if (Math.min(account.Stocks,fixedAmount-sellOrder.DealAmount)>minest_sell[currency]){
									var marketsellOrderID=processor.retrySell(exc_obj, -1, fixedAmount-sellOrder.DealAmount);
									Sleep(order_wait_secs);
									var marketsellOrderData=_C(exc_obj.GetOrder,marketsellOrderID);
									approximate_profit+=(marketsellOrderData.AvgPrice*marketsellOrderData.DealAmount*(1-sxf)-positions[i].buy_price*marketsellOrderData.DealAmount*(1+sxf));
									Log("Market Sell: Quantity-"+marketsellOrderData.DealAmount+",approximate_profit="+approximate_profit);
								}
							}
							
							var details={
								type:"close all positions",
								time:processor.get_ChinaTimeString(),
								RealAmount:-1,
								WantAmount:fixedAmount,
								RealPrice:-1,
								WantPrice:last,
								Memo:(last>positions[i].buy_price?"Profit : Loss")
								};
							if (trades_recorder){
								trades.push(details);
							}
						}
					}
					positions=positions_new;
				}
			}
			
			
			//Display Status
			var table1 = {type: 'table', title: 'position-'+exname+'('+currency+')', cols: ['Quantity', 'transaction price','Stop loss price'], rows: []};
			var table2 = {type: 'table', title: 'Status-'+exname+'('+currency+')', cols: ['Average true range(N)','Position Unit','Initial Assets','Current Assets','Polling time','Latest price','Highest','Lowest','Number of positions added','[Approximate Profit and Loss]'], rows: []};
			var table3 = {type: 'table', title: 'Transaction History-'+exname+'('+currency+')', cols: ['Date','Type', 'Transaction quantity','Order quantity','transaction price','order price','Notes'], rows: []};
			for (var i=0; i < positions.length; i++){
				table1.rows.push([positions[i].amount,positions[i].buy_price,positions[i].stoploss_price]);
			}
			table2.rows.push([N,position_unit,init_asset,cur_asset,passedtime+'ms',last,highest,Lowest,add_already,approximate_profit]);
			for (i=0; i < trades.length; i++){
				table3.rows.push([trades[i].time,trades[i].type,trades[i].RealAmount,trades[i].WantAmount,trades[i].RealPrice,trades[i].WantPrice,trades[i].Memo]);
			}
			processor.logstatus=('`' + JSON.stringify([table1, table2, table3])+'`'+'\n');
			
			//Record Profit
			processor.logprofit=approximate_profit;
			
			//rest
			Sleep(wait_ms);
		}
		
		return processor;
	}
};



//Main Function
function main(){
	var exchange_num=exchanges.length;
	var processors=[];
	for (var i=0; i<exchange_num; ++i){
		var p=ExchangProcessor.createNew(exchanges[i]);
		processors.push(p);
	}
	for (i=0; i<exchange_num; ++i){
		processors[i].init_obj();
	}
	var pre_profit=Number(_G("pre_profit"));
	Log('Previous income accumulation:'+pre_profit);
	var lastprofit=0;
	while(true){
		var allstatus='For customized strategies, please contact WeChat: alinwo (Verification message:botvsquantitative)#0000ff'+'\n';
		var allprofit=0;
		for (i=0; i<exchange_num; ++i){
			processors[i].work();
			allstatus+=processors[i].logstatus;
			allprofit+=processors[i].logprofit;
		}
		allstatus+=('For customized strategies, please contact WeChat: alinwo (Verification message:botvsquantitative)#0000ff'+'\n');
		LogStatus(allstatus);
		if (lastprofit!==allprofit){
			LogProfit(pre_profit+allprofit);
			_G("pre_profit", pre_profit+allprofit);
			lastprofit=allprofit;
		}
	}
}
```

> Detail

https://www.fmz.com/strategy/157366

> Last Modified

2019-07-16 14:28:24
