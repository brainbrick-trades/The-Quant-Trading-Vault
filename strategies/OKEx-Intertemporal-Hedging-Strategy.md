
> Name

OKEx-Intertemporal-Hedging-Strategy

> Author

reboting

> Strategy Description

What is cross-period hedging?
The so-called intertemporal arbitrage is to establish trading positions of equal quantity and opposite direction on different month contracts of the same futures variety, and finally end the transaction through hedging or delivery to obtain profits. The simplest intertemporal arbitrage is to buy the near-term futures variety and sell the forward futures variety. For example, Okex's BTC next week and current week contracts. The delivery period is different, with a maximum difference of 3 months. When a contract price difference occurs, investors can buy one contract and sell another contract at the same time. After the price difference returns, they can then perform the corresponding reverse closing, and then use the reasonable return of the price difference to obtain profits.

How to conduct cross-period hedging on Okex?
okexThere are often price differences between the prices of the previous week, next week and quarterly contracts. If the price difference reaches or exceeds a certain threshold, intertemporal hedging can be carried out, and then the reverse position can be closed when the price difference disappears, and then the reasonable return of the price difference can be used to obtain profits. For example, there is a price difference between BTC's current week contract and the next week's contract and the current week's contract is lower than the next week's contract price. When the price difference reaches the set threshold, investors can go long the current week's contract and short the next week's contract (the same quantity) to hedge, and wait until the price difference between the current week's contract and the next week's contract returns to the normal value to perform the corresponding reverse closing to obtain profits.

Risks of cross-period hedging:
Because the two contracts have different delivery times, when the contract is forced to close in the near term, if the price difference does not reverse, losses may occur.

Functions and features of strategy implementation:
Supports Okex cross-period hedging
Supports Okex's weekly, next-week, and quarterly contracts
Supports all Okex contract trading instruments (BTC, BCH, EOS, BSV, ETH, etc.))

Special Note: This strategy requires relying on the Botvstools template library to run!
Please download the template library here:
https://www.pcclean.io/45gd 
(After downloading the zip file and extracting it, there will be two js files: one is the policy and the other is the template library. Please distinguish between them)

Strategy parameter description:
https://www.pcclean.io/45gd



> Source (javascript)

``` javascript
var strategy_version="1.2.0.7(adjust parameters)";

/*
Instructions for use:
1. Please first set the strategy parameters for the exchange and trading pairs before running this strategy.
2. fmzAdd exchange here: okex futures exchange
3. The parameters contract_min represent the value of a single contract; do not change it arbitrarily
4. It is recommended to set the full position mode in okex to avoid insufficient margin.
5. Try to useokex api v1
6. This strategy is for learning and sharing only, live trading risk is your own responsibility.
*/

/********************************************Strategy Arguments**********************************/
var price_n={Futures_OKCoin_BSV_USD:2};//Price precision setting
var num_n={Futures_OKCoin_BSV_USD:0};//Quantity precision setting
var minestbuy={Futures_OKCoin_BSV_USD:1};//Minimum purchase quantity
var price_step={Futures_OKCoin_BSV_USD:0.05};//Order adjustment amount
var contract_min={Futures_OKCoin_BSV_USD:10};//Minimum contract amount
var wait_ms=3000;//Retry waiting time(ms)
var max_wait_order=10000;//Order waiting time(ms)
var margin_lv=10;//Leverage multiple
var jiacha_monitor={tw_nw:0.02,tw_qt:0.02,nw_qt:0.02};//Opening price difference
var hulie_monitor={tw_nw:0.003,tw_qt:0.003,nw_qt:0.003};//Ignored spread
var ok_future_target='bsv';//Target Contract
var keep_risk_rate=10;//Margin Rate
var trade_unit=100;//How many lots per trade
var push_notification=true;//WeChat notification for trading opportunities
/********************************************Strategy Arguments**********************************/


//Global Variables
var total_loop=0;

//Main Function
function main(){
	Log("strategy_version="+strategy_version);
	$.set_params(price_n,num_n,minestbuy,price_step,wait_ms,max_wait_order);
	
	if (push_notification){
		Log("Strategy has started running! Notifications enabled.@");
	}
	
	while(true){
		exchange.SetMarginLevel(margin_lv);
		var exname=exchange.GetName();
		var currency=exchange.GetCurrency();
		var account=$.retry_get_account(exchange);
		var f_orders=_C(exchange.GetOrders);
		
		exchange.SetContractType("this_week");
		var tw_depth=_C(exchange.GetDepth);
		var tw_sell1=tw_depth.Asks[0].Price;
		var tw_buy1=tw_depth.Bids[0].Price;
		var tw_records=_C(exchange.GetRecords,PERIOD_H1);
		if (tw_records.length<=50){
			Log("tw_records.lengthInvalid,Skip this execution...");
			Sleep(wait_ms);
			continue;
		}
		
		exchange.SetContractType("next_week");
		var nw_depth=_C(exchange.GetDepth);
		var nw_sell1=nw_depth.Asks[0].Price;
		var nw_buy1=nw_depth.Bids[0].Price;
		var nw_records=_C(exchange.GetRecords,PERIOD_H1);
		if (nw_records.length<=50){
			Log("nw_records.lengthInvalid,Skip this execution...");
			Sleep(wait_ms);
			continue;
		}
		
		exchange.SetContractType("quarter");
		var qt_depth=_C(exchange.GetDepth);
		var qt_sell1=qt_depth.Asks[0].Price;
		var qt_buy1=qt_depth.Bids[0].Price;
		var qt_records=_C(exchange.GetRecords,PERIOD_H1);
		if (qt_records.length<=50){
			Log("qt_records.lengthInvalid,Skip this execution...");
			Sleep(wait_ms);
			continue;
		}
		
		var tw_price_ma = TA.MA(tw_records, 30).slice(-1)[0];
		var nw_price_ma = TA.MA(nw_records, 30).slice(-1)[0];
		var qt_price_ma = TA.MA(qt_records, 30).slice(-1)[0];
		
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
		var risk_rate=account.Info.info[ok_future_target].risk_rate;//Margin Rate  10Leverage multiple, when margin rate is less than or equal to10%,Will trigger liquidation line only;20Leverage multiple, when margin rate is less than or equal to20%,Only then will the liquidation line be triggered. This means if you open10timesLTCContract, when your loss reaches the initial margin of the position90%, the liquidation line will be triggered; if open20For leveraged contracts, when your loss reaches the opening margin80%will trigger the liquidation line. 

		
		var tw_buy1_fixed=tw_buy1;
		var tw_sell1_fixed=tw_sell1;
		var nw_buy1_fixed=nw_buy1-(nw_price_ma-tw_price_ma);
		var nw_sell1_fixed=nw_sell1-(nw_price_ma-tw_price_ma);
		var qt_buy1_fixed=qt_buy1-(qt_price_ma-tw_price_ma);
		var qt_sell1_fixed=qt_sell1-(qt_price_ma-tw_price_ma);

		//this week - next week - kaichang
		if (tw_sell1_fixed<nw_buy1_fixed && (nw_buy1_fixed-tw_sell1_fixed)/tw_sell1_fixed>jiacha_monitor['tw_nw']){
			if (push_notification){
				Log("Next Week_Current Week_Arbitrage opportunities:"+exname+" "+((nw_buy1_fixed-tw_sell1_fixed)/tw_sell1_fixed)+"@");
			}
			if (risk_rate>keep_risk_rate && account.Stocks>0){
				exchange.SetContractType("this_week");
				exchange.SetDirection("buy");
				var dealamount=$.perform_limited_order("buy",exchange,tw_sell1,trade_unit,false,"futures","buy");
				if (dealamount>0){
					exchange.SetContractType("next_week");
					exchange.SetDirection("sell");
					$.perform_limited_order("buy",exchange,nw_buy1,dealamount,true,"futures","sell");
				}
			}
		}
		else if (nw_sell1_fixed<tw_buy1_fixed && (tw_buy1_fixed-nw_sell1_fixed)/nw_sell1_fixed>jiacha_monitor['tw_nw']){
			if (push_notification){
				Log("Current Week_Next Week_Arbitrage opportunities:"+exname+" "+((tw_buy1_fixed-nw_sell1_fixed)/nw_sell1_fixed)+"@");
			}
			if (risk_rate>keep_risk_rate && account.Stocks>0){
				exchange.SetContractType("next_week");
				exchange.SetDirection("buy");
				var dealamount=$.perform_limited_order("buy",exchange,nw_sell1,trade_unit,false,"futures","buy");
				if (dealamount>0){
					exchange.SetContractType("this_week");
					exchange.SetDirection("sell");
					$.perform_limited_order("buy",exchange,tw_buy1,dealamount,true,"futures","sell");
				}
			}
		}
		//this week - quarter - kaichang
		else if (tw_sell1_fixed<qt_buy1_fixed && (qt_buy1_fixed-tw_sell1_fixed)/tw_sell1_fixed>jiacha_monitor['tw_qt']){
			if (push_notification){
				Log("Quarter_Current Week_Arbitrage opportunities:"+exname+" "+((qt_buy1_fixed-tw_sell1_fixed)/tw_sell1_fixed)+"@");
			}
			if (risk_rate>keep_risk_rate && account.Stocks>0){
				exchange.SetContractType("this_week");
				exchange.SetDirection("buy");
				var dealamount=$.perform_limited_order("buy",exchange,tw_sell1,trade_unit,false,"futures","buy");
				if (dealamount>0){
					exchange.SetContractType("quarter");
					exchange.SetDirection("sell");
					$.perform_limited_order("buy",exchange,qt_buy1,dealamount,true,"futures","sell");
				}
			}
		}
		else if (qt_sell1_fixed<tw_buy1_fixed && (tw_buy1_fixed-qt_sell1_fixed)/qt_sell1_fixed>jiacha_monitor['tw_qt']){
			if (push_notification){
				Log("Current Week_Quarter_Arbitrage opportunities:"+exname+" "+((tw_buy1_fixed-qt_sell1_fixed)/qt_sell1_fixed)+"@");
			}
			if (risk_rate>keep_risk_rate && account.Stocks>0){
				exchange.SetContractType("quarter");
				exchange.SetDirection("buy");
				var dealamount=$.perform_limited_order("buy",exchange,qt_sell1,trade_unit,false,"futures","buy");
				if (dealamount>0){
					exchange.SetContractType("this_week");
					exchange.SetDirection("sell");
					$.perform_limited_order("buy",exchange,tw_buy1,dealamount,true,"futures","sell");
				}
			}
		}
		//next week - quarter - kaichang
		else if (nw_sell1_fixed<qt_buy1_fixed && (qt_buy1_fixed-nw_sell1_fixed)/nw_sell1_fixed>jiacha_monitor['nw_qt']){
			if (push_notification){
				Log("Quarter_Next Week_Arbitrage opportunities:"+exname+" "+((qt_buy1_fixed-nw_sell1_fixed)/nw_sell1_fixed)+"@");
			}
			if (risk_rate>keep_risk_rate && account.Stocks>0){
				exchange.SetContractType("next_week");
				exchange.SetDirection("buy");
				var dealamount=$.perform_limited_order("buy",exchange,nw_sell1,trade_unit,false,"futures","buy");
				if (dealamount>0){
					exchange.SetContractType("quarter");
					exchange.SetDirection("sell");
					$.perform_limited_order("buy",exchange,qt_buy1,dealamount,true,"futures","sell");
				}
			}
		}
		else if (qt_sell1_fixed<nw_buy1_fixed && (nw_buy1_fixed-qt_sell1_fixed)/qt_sell1_fixed>jiacha_monitor['nw_qt']){
			if (push_notification){
				Log("Next Week_Quarter_Arbitrage opportunities:"+exname+" "+((nw_buy1_fixed-qt_sell1_fixed)/qt_sell1_fixed)+"@");
			}
			if (risk_rate>keep_risk_rate && account.Stocks>0){
				exchange.SetContractType("quarter");
				exchange.SetDirection("buy");
				var dealamount=$.perform_limited_order("buy",exchange,qt_sell1,trade_unit,false,"futures","buy");
				if (dealamount>0){
					exchange.SetContractType("next_week");
					exchange.SetDirection("sell");
					$.perform_limited_order("buy",exchange,nw_buy1,dealamount,true,"futures","sell");
				}
			}
		}
		//this week - next week - pingchang
		else if (Math.abs((nw_sell1_fixed-tw_buy1_fixed)/tw_buy1_fixed)<hulie_monitor['tw_nw'] && tw_zuoduo_zhangshu>0 && nw_zuokong_zhangshu>0){
			var pingchang_zhangshu=Math.min(tw_zuoduo_zhangshu,nw_zuokong_zhangshu);
			exchange.SetContractType("this_week");
			exchange.SetDirection("closebuy");
			var dealamount=$.perform_limited_order("sell",exchange,tw_buy1,pingchang_zhangshu,false,"futures","closebuy");
			if (dealamount>0){
				exchange.SetContractType("next_week");
				exchange.SetDirection("closesell");
				$.perform_limited_order("sell",exchange,nw_sell1,dealamount,true,"futures","closesell");
			}
		}
		else if (Math.abs((tw_sell1_fixed-nw_buy1_fixed)/nw_buy1_fixed)<hulie_monitor['tw_nw'] && tw_zuokong_zhangshu>0 && nw_zuoduo_zhangshu>0){
			var pingchang_zhangshu=Math.min(tw_zuokong_zhangshu,nw_zuoduo_zhangshu);
			exchange.SetContractType("next_week");
			exchange.SetDirection("closebuy");
			var dealamount=$.perform_limited_order("sell",exchange,nw_buy1,pingchang_zhangshu,false,"futures","closebuy");
			if (dealamount>0){
				exchange.SetContractType("this_week");
				exchange.SetDirection("closesell");
				$.perform_limited_order("sell",exchange,tw_sell1,dealamount,true,"futures","closesell");
			}
		}
		//this week - quarter - pingchang
		else if (Math.abs((qt_sell1_fixed-tw_buy1_fixed)/tw_buy1_fixed)<hulie_monitor['tw_qt'] && tw_zuoduo_zhangshu>0 && qt_zuokong_zhangshu>0){
			var pingchang_zhangshu=Math.min(tw_zuoduo_zhangshu,qt_zuokong_zhangshu);
			exchange.SetContractType("this_week");
			exchange.SetDirection("closebuy");
			var dealamount=$.perform_limited_order("sell",exchange,tw_buy1,pingchang_zhangshu,false,"futures","closebuy");
			if (dealamount>0){
				exchange.SetContractType("quarter");
				exchange.SetDirection("closesell");
				$.perform_limited_order("sell",exchange,qt_sell1,dealamount,true,"futures","closesell");
			}
		}
		else if (Math.abs((tw_sell1_fixed-qt_buy1_fixed)/qt_buy1_fixed)<hulie_monitor['tw_qt'] && tw_zuokong_zhangshu>0 && qt_zuoduo_zhangshu>0){
			var pingchang_zhangshu=Math.min(tw_zuokong_zhangshu,qt_zuoduo_zhangshu);
			exchange.SetContractType("quarter");
			exchange.SetDirection("closebuy");
			var dealamount=$.perform_limited_order("sell",exchange,qt_buy1,pingchang_zhangshu,false,"futures","closebuy");
			if (dealamount>0){
				exchange.SetContractType("this_week");
				exchange.SetDirection("closesell");
				$.perform_limited_order("sell",exchange,tw_sell1,dealamount,true,"futures","closesell");
			}
		}
		//next week - quarter - pingchang
		else if (Math.abs((qt_sell1_fixed-nw_buy1_fixed)/nw_buy1_fixed)<hulie_monitor['nw_qt'] && nw_zuoduo_zhangshu>0 && qt_zuokong_zhangshu>0){
			var pingchang_zhangshu=Math.min(nw_zuoduo_zhangshu,qt_zuokong_zhangshu);
			exchange.SetContractType("next_week");
			exchange.SetDirection("closebuy");
			var dealamount=$.perform_limited_order("sell",exchange,nw_buy1,pingchang_zhangshu,false,"futures","closebuy");
			if (dealamount>0){
				exchange.SetContractType("quarter");
				exchange.SetDirection("closesell");
				$.perform_limited_order("sell",exchange,qt_sell1,dealamount,true,"futures","closesell");
			}
		}
		else if (Math.abs((nw_sell1_fixed-qt_buy1_fixed)/qt_buy1_fixed)<hulie_monitor['nw_qt'] && nw_zuokong_zhangshu>0 && qt_zuoduo_zhangshu>0){
			var pingchang_zhangshu=Math.min(nw_zuokong_zhangshu,qt_zuoduo_zhangshu);
			exchange.SetContractType("quarter");
			exchange.SetDirection("closebuy");
			var dealamount=$.perform_limited_order("sell",exchange,qt_buy1,pingchang_zhangshu,false,"futures","closebuy");
			if (dealamount>0){
				exchange.SetContractType("next_week");
				exchange.SetDirection("closesell");
				$.perform_limited_order("sell",exchange,nw_sell1,dealamount,true,"futures","closesell");
			}
		}
		else{
			//Process delivery
			var total_zuoduo=tw_zuoduo_zhangshu+nw_zuoduo_zhangshu+qt_zuoduo_zhangshu;
			var total_zuokong=tw_zuokong_zhangshu+nw_zuokong_zhangshu+qt_zuokong_zhangshu;
			if (total_zuoduo!==total_zuokong){
				if (total_zuoduo>total_zuokong){
					var diff_num=total_zuoduo-total_zuokong;
					
					//Forced draw
					Log("Start forced long liquidation:"+diff_num+'@');
					if (qt_zuoduo_zhangshu>=diff_num){
						exchange.SetContractType("quarter");
						exchange.SetDirection("closebuy");
						$.perform_limited_order("sell",exchange,qt_buy1,diff_num,true,"futures","closebuy");
					}else{
						exchange.SetContractType("quarter");
						exchange.SetDirection("closebuy");
						$.perform_limited_order("sell",exchange,qt_buy1,qt_zuoduo_zhangshu,true,"futures","closebuy");
						var diff2=diff_num-qt_zuoduo_zhangshu;
						if (nw_zuoduo_zhangshu>=diff2){
							exchange.SetContractType("next_week");
							exchange.SetDirection("closebuy");
							$.perform_limited_order("sell",exchange,nw_buy1,diff2,true,"futures","closebuy");
						}else{
							exchange.SetContractType("next_week");
							exchange.SetDirection("closebuy");
							$.perform_limited_order("sell",exchange,nw_buy1,nw_zuoduo_zhangshu,true,"futures","closebuy");
							var diff3=diff2-nw_zuoduo_zhangshu;
							if (tw_zuoduo_zhangshu>=diff3){
								exchange.SetContractType("this_week");
								exchange.SetDirection("closebuy");
								$.perform_limited_order("sell",exchange,tw_buy1,diff3,true,"futures","closebuy");
							}else{
								exchange.SetContractType("this_week");
								exchange.SetDirection("closebuy");
								$.perform_limited_order("sell",exchange,tw_buy1,tw_zuoduo_zhangshu,true,"futures","closebuy");
							}
						}
					}
				}
				else if (total_zuokong>total_zuoduo){
					var diff_num=total_zuokong-total_zuoduo;
					
					//Forced closing
					Log("Start forced short liquidation:"+diff_num+'@');
					if (qt_zuokong_zhangshu>=diff_num){
						exchange.SetContractType("quarter");
						exchange.SetDirection("closesell");
						$.perform_limited_order("sell",exchange,qt_sell1,diff_num,true,"futures","closesell");
					}else{
						exchange.SetContractType("quarter");
						exchange.SetDirection("closesell");
						$.perform_limited_order("sell",exchange,qt_sell1,qt_zuokong_zhangshu,true,"futures","closesell");
						var diff2=diff_num-qt_zuokong_zhangshu;
						if (nw_zuokong_zhangshu>=diff2){
							exchange.SetContractType("next_week");
							exchange.SetDirection("closesell");
							$.perform_limited_order("sell",exchange,nw_sell1,diff2,true,"futures","closesell");
						}else{
							exchange.SetContractType("next_week");
							exchange.SetDirection("closesell");
							$.perform_limited_order("sell",exchange,nw_sell1,nw_zuokong_zhangshu,true,"futures","closesell");
							var diff3=diff2-nw_zuokong_zhangshu;
							if (tw_zuokong_zhangshu>=diff3){
								exchange.SetContractType("this_week");
								exchange.SetDirection("closesell");
								$.perform_limited_order("sell",exchange,tw_sell1,diff3,true,"futures","closesell");
							}else{
								exchange.SetContractType("this_week");
								exchange.SetDirection("closesell");
								$.perform_limited_order("sell",exchange,tw_sell1,tw_zuokong_zhangshu,true,"futures","closesell");
							}
						}
					}
				}
			}
		}

		

		LogStatus(
		"Recent average contract price="+tw_price_ma+'/'+nw_price_ma+'/'+qt_price_ma+"\n"+
		'-----------------------------------------------------------\n'+
		'Next week_Current week_Open position spread='+(nw_buy1_fixed-tw_sell1_fixed)/tw_sell1_fixed+'/'+jiacha_monitor['tw_nw']+"\n"+
		'Current week_Next week_Open position spread='+(tw_buy1_fixed-nw_sell1_fixed)/nw_sell1_fixed+'/'+jiacha_monitor['tw_nw']+"\n"+
		'Quarter_Current week_Open position spread='+(qt_buy1_fixed-tw_sell1_fixed)/tw_sell1_fixed+'/'+jiacha_monitor['tw_qt']+"\n"+
		'Current week_Quarter_Open position spread='+(tw_buy1_fixed-qt_sell1_fixed)/qt_sell1_fixed+'/'+jiacha_monitor['tw_qt']+"\n"+
		'Quarter_Next week_Open position spread='+(qt_buy1_fixed-nw_sell1_fixed)/nw_sell1_fixed+'/'+jiacha_monitor['nw_qt']+"\n"+
		'Next week_Quarter_Open position spread='+(nw_buy1_fixed-qt_sell1_fixed)/qt_sell1_fixed+'/'+jiacha_monitor['nw_qt']+"\n"+
		'-----------------------------------------------------------\n'+
		'Next Week_Current Week_Close the difference='+Math.abs((nw_sell1_fixed-tw_buy1_fixed)/tw_buy1_fixed)+'/'+hulie_monitor['tw_nw']+"\n"+
		'Current Week_Next Week_Close the difference='+Math.abs((tw_sell1_fixed-nw_buy1_fixed)/nw_buy1_fixed)+'/'+hulie_monitor['tw_nw']+"\n"+
		'Quarter_Current Week_Close the difference='+Math.abs((qt_sell1_fixed-tw_buy1_fixed)/tw_buy1_fixed)+'/'+hulie_monitor['tw_qt']+"\n"+
		'Current Week_Quarter_Close the difference='+Math.abs((tw_sell1_fixed-qt_buy1_fixed)/qt_buy1_fixed)+'/'+hulie_monitor['tw_qt']+"\n"+
		'Quarter_Next Week_Close the difference='+Math.abs((qt_sell1_fixed-nw_buy1_fixed)/nw_buy1_fixed)+'/'+hulie_monitor['nw_qt']+"\n"+
		'Next Week_Quarter_Close the difference='+Math.abs((nw_sell1_fixed-qt_buy1_fixed)/qt_buy1_fixed)+'/'+hulie_monitor['nw_qt']+"\n"+
		'-----------------------------------------------------------\n'+
		'Account Equity='+account_rights+'\n'+
		'Used margin='+keep_deposit+'\n'+
		'Available Margin='+account.Stocks+'\n'+
		'Margin Rate='+risk_rate+'\n'+
		'Number of long/short positions for the week='+tw_zuoduo_zhangshu+'/'+tw_zuokong_zhangshu+'\n'+
		'Number of long/short positions in the next week='+nw_zuoduo_zhangshu+'/'+nw_zuokong_zhangshu+'\n'+
		'Quarterly number of long/short contracts='+qt_zuoduo_zhangshu+'/'+qt_zuokong_zhangshu+'\n'+
		'Futures Position='+position.length+'\n'+
		'Pending orders='+f_orders.length+'\n'+
		'Average price of long/short for the week='+tw_zuoduo_avg_price+'/'+tw_zuokong_avg_price+'\n'+
		'Long/short average price for the next week='+nw_zuoduo_avg_price+'/'+nw_zuokong_avg_price+'\n'+
		'Quarterly long/short average price='+qt_zuoduo_avg_price+'/'+qt_zuokong_avg_price+'\n'+
		'♜Polling Times: '+total_loop+'\n'+
		'♜Update Time: '+$.get_ChinaTimeString()+'\n'+
		'♜WeChat: alinwo (verification message:botvs) #0000ff'+'\n'+
		'♜Linlin Quant - Live Trading Strategy: http://www.pcclean.io/quant  #ff0000'+'\n'
		);
		
		if (total_loop%200===0){
			LogProfit(account_rights);
		}
		
		total_loop++;
		Sleep(wait_ms);
		
	}//while end
}

```

> Detail

https://www.fmz.com/strategy/157635

> Last Modified

2019-07-17 22:39:05
