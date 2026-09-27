
> Name

EMA-Trend-Tracking-Current-Week-Week-Quarter

> Author

crypto_future

> Strategy Description

This strategy is based on the EMA trend tracking. When the EMA golden cross is formed, a position is opened and when the EMA death cross is formed, the position is closed. Earn profits from trends. This strategy supports long and short two-way opening of OKEX contracts.

Additional explanation: EMA (Exponential Moving Average) is the exponential moving average. Also called EXPMA indicator, it is also a trend indicator. The exponential moving average is an exponentially decreasing weighted moving average.

EMAThe trend following method is developed based on the trading philosophy of cutting off losses and letting profits run. The trend following method believes that due to the greed and fear of human nature in the market and the influence of the economic cycle, the market trend will continue to rise or fall, thereby forming a trend. By capturing the main trend of the market, market average or profits exceeding the market average can be obtained.

Note: This strategy is only for learning and debugging, using it in live trading is at your own risk.

Instructions for use:
https://www.pcclean.io/%e6%95%b0%e5%ad%97%e8%b4%a7%e5%b8%81ema%e8%b6%8b%e5%8a%bf%e8%b7%9f%e8%b8%aa%e7%ad%96%e7%95%a5%e5%88%86%e4%ba%abokex%e7%89%88/




> Source (javascript)

``` javascript
var strategy_version="1.62.EMA"; //test

/*
Instructions for use:
- okex's account is set to 10 times leverage
- Use full position mode
- UseAPI v1
*/

/********************************************Strategy Arguments**********************************/
var price_n={Futures_OKCoin_BSV_USD:2};//Price precision setting
var num_n={Futures_OKCoin_BSV_USD:0};//Quantity precision setting
var minestbuy={Futures_OKCoin_BSV_USD:1};//Minimum purchase quantity
var price_step={Futures_OKCoin_BSV_USD:0.2};//Order adjustment amount
var contract_min={Futures_OKCoin_BSV_USD:10};//Minimum contract amount
var wait_ms=3000;//Retry waiting time(ms)
var max_wait_order=6000;//Order waiting time(ms)
var margin_lv=10;//Leverage multiple
var ok_future_target='bsv';//Target Contract
var keep_risk_rate=2;//Margin Rate  (Total Equity/Available)
var trade_unit_div=4;//Percentage of assets per trade
var push_notification=true;//WeChat notification for trading opportunities
var N_mult=3;//NMultiplier of(Used to calculate high-level stop loss)
var k_type=PERIOD_M15;//kLine Type
var N_knumber=50;//Take50Individual/UnitbarUsed for Calculationn
/********************************************Strategy Arguments**********************************/


//Global Variables
var total_loop=0;
var tw_sell1_lowest=100000;
var tw_buy1_highest=0;
var nw_sell1_lowest=100000;
var nw_buy1_highest=0;
var qt_sell1_lowest=100000;
var qt_buy1_highest=0;
var total_trade_num=0;
var success_trade_num=0;
var failed_trade_num=0;

//Main Function
function main(){
	Log("strategy_version="+strategy_version);
	$.set_params(price_n,num_n,minestbuy,price_step,wait_ms,max_wait_order);
	
	if (push_notification){
		Log("Strategy has started running! Notifications enabled.@");
	}
	
	//restore data
	total_trade_num=Number(_G("total_trade_num"));
	success_trade_num=Number(_G("success_trade_num"));
	failed_trade_num=Number(_G("failed_trade_num"));
	
	while(true){
		
		try{
			exchange.SetMarginLevel(margin_lv);
			var exname=exchange.GetName();
			var currency=exchange.GetCurrency();
			var account=$.retry_get_account(exchange);
			var f_orders=_C(exchange.GetOrders);
			
			exchange.SetContractType("this_week");
			var tw_depth=_C(exchange.GetDepth);
			var tw_sell1=tw_depth.Asks[0].Price;
			var tw_buy1=tw_depth.Bids[0].Price;
			var tw_records=_C(exchange.GetRecords,k_type);
			if (tw_records.length<=60){
				Log("tw_records.lengthInvalid,Skip this execution...");
				Sleep(wait_ms);
				continue;
			}
			
			exchange.SetContractType("next_week");
			var nw_depth=_C(exchange.GetDepth);
			var nw_sell1=nw_depth.Asks[0].Price;
			var nw_buy1=nw_depth.Bids[0].Price;
			var nw_records=_C(exchange.GetRecords,k_type);
			if (nw_records.length<=60){
				Log("nw_records.lengthInvalid,Skip this execution...");
				Sleep(wait_ms);
				continue;
			}
			
			exchange.SetContractType("quarter");
			var qt_depth=_C(exchange.GetDepth);
			var qt_sell1=qt_depth.Asks[0].Price;
			var qt_buy1=qt_depth.Bids[0].Price;
			var qt_records=_C(exchange.GetRecords,k_type);
			if (qt_records.length<=60){
				Log("qt_records.lengthInvalid,Skip this execution...");
				Sleep(wait_ms);
				continue;
			}
			
		
			var position=_C(exchange.GetPosition);
			
			var tw_zuoduo_zhangshu=0;
			var tw_zuoduo_avg_price=0;
			var tw_zuoduo_amount=0;
			var tw_zuokong_zhangshu=0;
			var tw_zuokong_avg_price=0;	
			var tw_zuokong_amount=0;
			
			var nw_zuoduo_zhangshu=0;
			var nw_zuoduo_avg_price=0;
			var nw_zuoduo_amount=0;
			var nw_zuokong_zhangshu=0;
			var nw_zuokong_avg_price=0;
			var nw_zuokong_amount=0;
			
			var qt_zuoduo_zhangshu=0;
			var qt_zuoduo_avg_price=0;
			var qt_zuoduo_amount=0;
			var qt_zuokong_zhangshu=0;
			var qt_zuokong_avg_price=0;
			var qt_zuokong_amount=0;

			
			for (var i=0; i < position.length; i++){
				if (position[i].ContractType==="this_week"){
					if (position[i].Type===PD_LONG){
						tw_zuoduo_zhangshu=position[i].Amount;
						tw_zuoduo_avg_price=position[i].Price;
						tw_zuoduo_amount=tw_zuoduo_zhangshu*contract_min[$.get_exchange_id(exchange)]*(1/tw_zuoduo_avg_price-1/tw_buy1+1/tw_zuoduo_avg_price);
					}
					if (position[i].Type===PD_SHORT){
						tw_zuokong_zhangshu=position[i].Amount;
						tw_zuokong_avg_price=position[i].Price;
						tw_zuokong_amount=tw_zuokong_zhangshu*contract_min[$.get_exchange_id(exchange)]*(1/tw_sell1-1/tw_zuokong_avg_price+1/tw_zuokong_avg_price);
					}
				}
				if (position[i].ContractType==="next_week"){
					if (position[i].Type===PD_LONG){
						nw_zuoduo_zhangshu=position[i].Amount;
						nw_zuoduo_avg_price=position[i].Price;
						nw_zuoduo_amount=nw_zuoduo_zhangshu*contract_min[$.get_exchange_id(exchange)]*(1/nw_zuoduo_avg_price-1/nw_buy1+1/nw_zuoduo_avg_price);
					}
					if (position[i].Type===PD_SHORT){
						nw_zuokong_zhangshu=position[i].Amount;
						nw_zuokong_avg_price=position[i].Price;
						nw_zuokong_amount=nw_zuokong_zhangshu*contract_min[$.get_exchange_id(exchange)]*(1/nw_sell1-1/nw_zuokong_avg_price+1/nw_zuokong_avg_price);
					}
				}
				if (position[i].ContractType==="quarter"){
					if (position[i].Type===PD_LONG){
						qt_zuoduo_zhangshu=position[i].Amount;
						qt_zuoduo_avg_price=position[i].Price;
						qt_zuoduo_amount=qt_zuoduo_zhangshu*contract_min[$.get_exchange_id(exchange)]*(1/qt_zuoduo_avg_price-1/qt_buy1+1/qt_zuoduo_avg_price);
					}
					if (position[i].Type===PD_SHORT){
						qt_zuokong_zhangshu=position[i].Amount;
						qt_zuokong_avg_price=position[i].Price;
						qt_zuokong_amount=qt_zuokong_zhangshu*contract_min[$.get_exchange_id(exchange)]*(1/qt_sell1-1/qt_zuokong_avg_price+1/qt_zuokong_avg_price);
					}
				}
			}
			
			var account_rights=account.Info.info[ok_future_target].account_rights;//Account Equity
			var keep_deposit=account.Info.info[ok_future_target].keep_deposit;//Margin
			var profit_real=account.Info.info[ok_future_target].profit_real;//Realized profit and loss
			var profit_unreal=account.Info.info[ok_future_target].profit_unreal;//Unrealized profit and loss
			var risk_rate=(keep_deposit===0?1000000:(account_rights/keep_deposit));//account.Info.info[ok_future_target].risk_rate;//Margin Rate  10Leverage multiple, when margin rate is less than or equal to10%,Will trigger liquidation line only;20Leverage multiple, when margin rate is less than or equal to20%,Only then will the liquidation line be triggered. This means if you open10timesLTCContract, when your loss reaches the initial margin of the position90%, the liquidation line will be triggered; if open20For leveraged contracts, when your loss reaches the opening margin80%will trigger the liquidation line. 

			var tw_atr = TA.ATR(tw_records, N_knumber);
			var nw_atr = TA.ATR(nw_records, N_knumber);
			var qt_atr = TA.ATR(qt_records, N_knumber);
			if (tw_atr.length<=1 || nw_atr.length<=1 || qt_atr.length<=1){
				Log("atr.lengthInvalid,Skip this execution...");
				Sleep(wait_ms);
				continue;
			}
			
			var tw_N=tw_atr[tw_atr.length-1];
			var nw_N=nw_atr[nw_atr.length-1];
			var qt_N=tw_atr[qt_atr.length-1];
			
			var tw_ema7=TA.EMA(tw_records,7);
			var nw_ema7=TA.EMA(nw_records,7);
			var qt_ema7=TA.EMA(qt_records,7);
			
			var tw_ema30=TA.EMA(tw_records,30);
			var nw_ema30=TA.EMA(nw_records,30);
			var qt_ema30=TA.EMA(qt_records,30);
			
			if (tw_ema7.length<=5||tw_ema30.length<=5||nw_ema7.length<=5||nw_ema30.length<=5||qt_ema7.length<=5||qt_ema30.length<=5){
				Log("emaInvalid,Skip this execution...");
				Sleep(wait_ms);
				continue;
			}
			
			var tw_ema_buyduo=false;
			var tw_ema_sellduo=false;
			if (tw_ema7[tw_ema7.length-2]>tw_ema30[tw_ema30.length-2] &&
				tw_ema7[tw_ema7.length-3]<=tw_ema30[tw_ema30.length-3]){
					tw_ema_buyduo=true;
			}
			if (tw_ema7[tw_ema7.length-2]<tw_ema30[tw_ema30.length-2] &&
				tw_ema7[tw_ema7.length-3]>=tw_ema30[tw_ema30.length-3]){
				tw_ema_sellduo=true;
			}
			var nw_ema_buyduo=false;
			var nw_ema_sellduo=false;
			if (nw_ema7[nw_ema7.length-2]>nw_ema30[nw_ema30.length-2] &&
				nw_ema7[nw_ema7.length-3]<=nw_ema30[nw_ema30.length-3]){
					nw_ema_buyduo=true;
			}
			if (nw_ema7[nw_ema7.length-2]<nw_ema30[nw_ema30.length-2] &&
				nw_ema7[nw_ema7.length-3]>=nw_ema30[nw_ema30.length-3]){
				nw_ema_sellduo=true;
			}
			var qt_ema_buyduo=false;
			var qt_ema_sellduo=false;
			if (qt_ema7[qt_ema7.length-2]>qt_ema30[qt_ema30.length-2] &&
				qt_ema7[qt_ema7.length-3]<=qt_ema30[qt_ema30.length-3]){
					qt_ema_buyduo=true;
			}
			if (qt_ema7[qt_ema7.length-2]<qt_ema30[qt_ema30.length-2] &&
				qt_ema7[qt_ema7.length-3]>=qt_ema30[qt_ema30.length-3]){
				qt_ema_sellduo=true;
			}
			
			
			var tw_ema_buykong=false;
			var tw_ema_sellkong=false;
			if (tw_ema7[tw_ema7.length-2]<tw_ema30[tw_ema30.length-2] &&
				tw_ema7[tw_ema7.length-3]>=tw_ema30[tw_ema30.length-3]){
					tw_ema_buykong=true;
			}
			if (tw_ema7[tw_ema7.length-2]>tw_ema30[tw_ema30.length-2] &&
				tw_ema7[tw_ema7.length-3]<=tw_ema30[tw_ema30.length-3]){
				tw_ema_sellkong=true;
			}
			var nw_ema_buykong=false;
			var nw_ema_sellkong=false;
			if (nw_ema7[nw_ema7.length-2]<nw_ema30[nw_ema30.length-2] &&
				nw_ema7[nw_ema7.length-3]>=nw_ema30[nw_ema30.length-3]){
					nw_ema_buykong=true;
			}
			if (nw_ema7[nw_ema7.length-2]>nw_ema30[nw_ema30.length-2] &&
				nw_ema7[nw_ema7.length-3]<=nw_ema30[nw_ema30.length-3]){
				nw_ema_sellkong=true;
			}
			var qt_ema_buykong=false;
			var qt_ema_sellkong=false;
			if (qt_ema7[qt_ema7.length-2]<qt_ema30[qt_ema30.length-2] &&
				qt_ema7[qt_ema7.length-3]>=qt_ema30[qt_ema30.length-3]){
					qt_ema_buykong=true;
			}
			if (qt_ema7[qt_ema7.length-2]>qt_ema30[qt_ema30.length-2] &&
				qt_ema7[qt_ema7.length-3]<=qt_ema30[qt_ema30.length-3]){
				qt_ema_sellkong=true;
			}
			
			//update lowest and highest
			if (tw_zuoduo_zhangshu>0 && tw_buy1>tw_buy1_highest){
				tw_buy1_highest=tw_buy1;
			}
			if (tw_zuokong_zhangshu>0 && tw_sell1<tw_sell1_lowest){
				tw_sell1_lowest=tw_sell1;
			}
			if (nw_zuoduo_zhangshu>0 && nw_buy1>nw_buy1_highest){
				nw_buy1_highest=nw_buy1;
			}
			if (nw_zuokong_zhangshu>0 && nw_sell1<nw_sell1_lowest){
				nw_sell1_lowest=nw_sell1;
			}
			if (qt_zuoduo_zhangshu>0 && qt_buy1>qt_buy1_highest){
				qt_buy1_highest=qt_buy1;
			}
			if (qt_zuokong_zhangshu>0 && qt_sell1<qt_sell1_lowest){
				qt_sell1_lowest=qt_sell1;
			}
			if (tw_zuoduo_zhangshu===0){
				tw_buy1_highest=0;
			}
			if (tw_zuokong_zhangshu===0){
				tw_sell1_lowest=100000;
			}
			if (nw_zuoduo_zhangshu===0){
				nw_buy1_highest=0;
			}
			if (nw_zuokong_zhangshu===0){
				nw_sell1_lowest=100000;
			}
			if (qt_zuoduo_zhangshu===0){
				qt_buy1_highest=0;
			}
			if (qt_zuokong_zhangshu===0){
				qt_sell1_lowest=100000;
			}
			
			var trade_unit=(account_rights*(10/keep_risk_rate)/trade_unit_div)*((tw_buy1+tw_sell1+nw_buy1+nw_sell1+qt_buy1+qt_sell1)/6)/contract_min[$.get_exchange_id(exchange)];
			
			//Open Position
			if (tw_zuoduo_zhangshu===0 && tw_ema_buyduo && risk_rate>keep_risk_rate && account.Stocks>0){
				exchange.SetContractType("this_week");
				exchange.SetDirection("buy");
				var dealamount=$.perform_limited_order("buy",exchange,tw_sell1,trade_unit,false,"futures","buy");
				tw_buy1_highest=tw_buy1;
				if (push_notification){
					Log("Completed long positions for the week"+trade_unit+'Zhang'+'@');
				}
			}
			else if (tw_zuokong_zhangshu===0 && tw_ema_buykong && risk_rate>keep_risk_rate && account.Stocks>0){
				exchange.SetContractType("this_week");
				exchange.SetDirection("sell");
				var dealamount=$.perform_limited_order("sell",exchange,tw_buy1,trade_unit,false,"futures","sell");
				tw_sell1_lowest=tw_sell1;
				if (push_notification){
					Log("Completed short positions for the week"+trade_unit+'Zhang'+'@');
				}
			}
			else if (nw_zuoduo_zhangshu===0 && nw_ema_buyduo && risk_rate>keep_risk_rate && account.Stocks>0){
				exchange.SetContractType("next_week");
				exchange.SetDirection("buy");
				var dealamount=$.perform_limited_order("buy",exchange,nw_sell1,trade_unit,false,"futures","buy");
				nw_buy1_highest=nw_buy1;
				if (push_notification){
					Log("Completed long positions for the next week"+trade_unit+'Zhang'+'@');
				}
			}
			else if (nw_zuokong_zhangshu===0 && nw_ema_buykong && risk_rate>keep_risk_rate && account.Stocks>0){
				exchange.SetContractType("next_week");
				exchange.SetDirection("sell");
				var dealamount=$.perform_limited_order("sell",exchange,nw_buy1,trade_unit,false,"futures","sell");
				nw_sell1_lowest=nw_sell1;
				if (push_notification){
					Log("Next week short completed"+trade_unit+'Zhang'+'@');
				}
			}
			else if (qt_zuoduo_zhangshu===0 && qt_ema_buyduo && risk_rate>keep_risk_rate && account.Stocks>0){
				exchange.SetContractType("quarter");
				exchange.SetDirection("buy");
				var dealamount=$.perform_limited_order("buy",exchange,qt_sell1,trade_unit,false,"futures","buy");
				qt_buy1_highest=qt_buy1;
				if (push_notification){
					Log("Quarterly long completed"+trade_unit+'Zhang'+'@');
				}
			}
			else if (qt_zuokong_zhangshu===0 && qt_ema_buykong && risk_rate>keep_risk_rate && account.Stocks>0){
				exchange.SetContractType("quarter");
				exchange.SetDirection("sell");
				var dealamount=$.perform_limited_order("sell",exchange,qt_buy1,trade_unit,false,"futures","sell");
				qt_sell1_lowest=qt_sell1;
				if (push_notification){
					Log("Quarterly short completed"+trade_unit+'Zhang'+'@');
				}
			}
			//Close Position
			else if (tw_zuoduo_zhangshu>0 && (tw_buy1_highest-tw_buy1>N_mult*tw_N||tw_ema_sellduo/* ||tw_buy1-tw_zuoduo_avg_price>N_mult*tw_N */)){
				exchange.SetContractType("this_week");
				exchange.SetDirection("closebuy");
				var dealamount=$.perform_limited_order("sell",exchange,tw_buy1,tw_zuoduo_zhangshu,true,"futures","closebuy");
				total_trade_num++;
				if (tw_buy1>tw_zuoduo_avg_price){
					success_trade_num++;
				}else{
					failed_trade_num++;
				}
				if (push_notification){
					Log("This week long closed:"+((tw_buy1>tw_zuoduo_avg_price)?'Profit':'Loss')+'@');
				}
			}
			else if (tw_zuokong_zhangshu>0 && (tw_sell1-tw_sell1_lowest>N_mult*tw_N||tw_ema_sellkong/* ||tw_zuokong_avg_price-tw_sell1>N_mult*tw_N */)){
				exchange.SetContractType("this_week");
				exchange.SetDirection("closesell");
				var dealamount=$.perform_limited_order("buy",exchange,tw_sell1,tw_zuokong_zhangshu,true,"futures","closesell");
				total_trade_num++;
				if (tw_sell1<tw_zuokong_avg_price){
					success_trade_num++;
				}else{
					failed_trade_num++;
				}
				if (push_notification){
					Log("This week short closed:"+((tw_sell1<tw_zuokong_avg_price)?'Profit':'Loss')+'@');
				}
			}
			else if (nw_zuoduo_zhangshu>0 && (nw_buy1_highest-nw_buy1>N_mult*nw_N||nw_ema_sellduo/* ||nw_buy1-nw_zuoduo_avg_price>N_mult*nw_N */)){
				exchange.SetContractType("next_week");
				exchange.SetDirection("closebuy");
				var dealamount=$.perform_limited_order("sell",exchange,nw_buy1,nw_zuoduo_zhangshu,true,"futures","closebuy");
				total_trade_num++;
				if (nw_buy1>nw_zuoduo_avg_price){
					success_trade_num++;
				}else{
					failed_trade_num++;
				}
				if (push_notification){
					Log("Next week long closed:"+((nw_buy1>nw_zuoduo_avg_price)?'Profit':'Loss')+'@');
				}
			}
			else if (nw_zuokong_zhangshu>0 && (nw_sell1-nw_sell1_lowest>N_mult*nw_N||nw_ema_sellkong/* ||nw_zuokong_avg_price-nw_sell1>N_mult*nw_N */)){
				exchange.SetContractType("next_week");
				exchange.SetDirection("closesell");
				var dealamount=$.perform_limited_order("buy",exchange,nw_sell1,nw_zuokong_zhangshu,true,"futures","closesell");
				total_trade_num++;
				if (nw_sell1<nw_zuokong_avg_price){
					success_trade_num++;
				}else{
					failed_trade_num++;
				}
				if (push_notification){
					Log("Next week short closed:"+((nw_sell1<nw_zuokong_avg_price)?'Profit':'Loss')+'@');
				}
			}
			else if (qt_zuoduo_zhangshu>0 && (qt_buy1_highest-qt_buy1>N_mult*qt_N||qt_ema_sellduo/* ||qt_buy1-qt_zuoduo_avg_price>N_mult*qt_N */)){
				exchange.SetContractType("quarter");
				exchange.SetDirection("closebuy");
				var dealamount=$.perform_limited_order("sell",exchange,qt_buy1,qt_zuoduo_zhangshu,true,"futures","closebuy");
				total_trade_num++;
				if (qt_buy1>qt_zuoduo_avg_price){
					success_trade_num++;
				}else{
					failed_trade_num++;
				}
				if (push_notification){
					Log("Quarterly long closed:"+((qt_buy1>qt_zuoduo_avg_price)?'Profit':'Loss')+'@');
				}
			}
			else if (qt_zuokong_zhangshu>0 && (qt_sell1-qt_sell1_lowest>N_mult*qt_N||qt_ema_sellkong/* ||qt_zuokong_avg_price-qt_sell1>N_mult*qt_N */)){
				exchange.SetContractType("quarter");
				exchange.SetDirection("closesell");
				var dealamount=$.perform_limited_order("buy",exchange,qt_sell1,qt_zuokong_zhangshu,true,"futures","closesell");
				total_trade_num++;
				if (qt_sell1<qt_zuokong_avg_price){
					success_trade_num++;
				}else{
					failed_trade_num++;
				}
				if (push_notification){
					Log("Quarterly short closed:"+((qt_sell1<qt_zuokong_avg_price)?'Profit':'Loss')+'@');
				}
			}
			

			LogStatus(
					'-----------------------------------------------------'+'\n'+
					'Number of long contracts/average price/current price/stop-loss price for the current week: '+tw_zuoduo_zhangshu+'/'+_N(tw_zuoduo_avg_price,2)+'/'+_N(tw_buy1,2)+'/'+_N(tw_buy1_highest-N_mult*tw_N,2)+'\n'+
					'Number of long contracts/average price/current price/stop-loss price for the next week: '+nw_zuoduo_zhangshu+'/'+_N(nw_zuoduo_avg_price,2)+'/'+_N(nw_buy1,2)+'/'+_N(nw_buy1_highest-N_mult*nw_N,2)+'\n'+
					'Number of long contracts/average price/current price/stop-loss price for the quarter: '+qt_zuoduo_zhangshu+'/'+_N(qt_zuoduo_avg_price,2)+'/'+_N(qt_buy1,2)+'/'+_N(qt_buy1_highest-N_mult*qt_N,2)+'\n'+
					'-----------------------------------------------------'+'\n'+
					'Number of short contracts/average price/current price/stop-loss price for the current week: '+tw_zuokong_zhangshu+'/'+_N(tw_zuokong_avg_price,2)+'/'+_N(tw_sell1,2)+'/'+_N(tw_sell1_lowest+N_mult*tw_N,2)+'\n'+					
					'Number of short contracts/average price/current price/stop-loss price for the next week: '+nw_zuokong_zhangshu+'/'+_N(nw_zuokong_avg_price,2)+'/'+_N(nw_sell1,2)+'/'+_N(nw_sell1_lowest+N_mult*nw_N,2)+'\n'+					
					'Number of short contracts/average price/current price/stop-loss price for the quarter: '+qt_zuokong_zhangshu+'/'+_N(qt_zuokong_avg_price,2)+'/'+_N(qt_sell1,2)+'/'+_N(qt_sell1_lowest+N_mult*qt_N,2)+'\n'+
					'-----------------------------------------------------'+'\n'+
					'Current WeekN: '+tw_N+'\n'+
					'Next WeekN: '+nw_N+'\n'+
					'QuarterN: '+qt_N+'\n'+
					'-----------------------------------------------------'+'\n'+
					'Account Equity: '+account_rights+'\n'+
					'Used margin: '+keep_deposit+'\n'+
					'Available Margin: '+account.Stocks+'\n'+
					'Risk Ratio: '+risk_rate+'\n'+
					'Futures Position: '+position.length+'\n'+
					'Pending orders: '+f_orders.length+'\n'+
					'Total number of trades / number of profitable trades / number of losing trades: '+total_trade_num+'/'+success_trade_num+'/'+failed_trade_num+'\n'+
					'Transaction Success Rate: '+success_trade_num/total_trade_num+'\n'+
					'Number of contracts per trade: '+trade_unit+'\n'+
					'-----------------------------------------------------'+'\n'+
					('♜Polling Times: '+total_loop+'\n')+
					('♜Update Time: '+$.get_ChinaTimeString()+'\n')+
					('♜VER:'+strategy_version+'\n')+
					('♜Linlin Quantification-Blog: http://www.pcclean.io/category/quantitative trading/  #0000ff'+'\n')+
					('♜Linlin Quant - Live Trading Strategy: http://www.pcclean.io/quant  #ff0000'+'\n')
					);
					
			_G("total_trade_num", total_trade_num);
			_G("success_trade_num", success_trade_num);
			_G("failed_trade_num", failed_trade_num);
			
			if (total_loop%100===0){
				LogProfit(account_rights);
			}		
			total_loop++;
			Sleep(wait_ms);
		
		}catch(err) {
			Log("catch error:"+err.message);
			Sleep(wait_ms);
		}
		
	}//while end
}

```

> Detail

https://www.fmz.com/strategy/203272

> Last Modified

2020-04-29 11:58:29
