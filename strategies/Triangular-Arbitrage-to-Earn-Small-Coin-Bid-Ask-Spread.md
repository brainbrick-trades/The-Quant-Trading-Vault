
> Name

Triangular-Arbitrage-to-Earn-Small-Coin-Bid-Ask-Spread

> Author

@cqz



> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|maxElapse|60|Maximum delay|
|pricePrecisions|1,1,1|Price decimal precision|
|amountPrecisions|1,1,1|Quantity decimal precision|
|runMode|0|Operation mode: Test|Buy only|Sell only|Buy and sell|
|placePriceRatio|0.8|Order Price Ratio|
|cancelPriceRatio|0.2|Cancel Order Price Ratio|
|minTakerAmount|true|Minimum quantity per arbitrage|
|maxTakerAmount|true|Maximum quantity per arbitrage|
|buyMaxTakerAmount|1000|Maximum Buy Order Quantity|
|sellMaxTakerAmount|1000|Maximum Sell Order Quantity|
|restoreData|false|Re-archive|


> Source (javascript)

``` javascript
function getAccounts() {
	var accounts = [];
	while (true) {
		for (var i = 0; i < exchanges.length; i++) {
			if (accounts[i] == null) {
				// Create Asynchronous Operation
				accounts[i] = exchanges[i].Go("GetAccount");
			}
		}
		var failed = 0;
		for (var i = 0; i < exchanges.length; i++) {
			if (typeof(accounts[i].wait) != "undefined") {
				// Waiting for results
				var account = accounts[i].wait(5);
				if (typeof(account) != "undefined") {
					if (account) {
						accounts[i] = account;
					} else {
						// Try again
						accounts[i] = null;
						failed++;
					}
				} else {
					failed++;
				}
			}
		}
		if (failed == 0) {
			break;
		}
	}
	return accounts;
}

function getDepthInfo() {
	var beginTime = new Date().getTime();
	var depths = [];
	var elapses = [];
	// for (var i = 0; i < exchanges.length; i++) {
	// 	var startTime = new Date().getTime();
	// 	depths[i] = _C(exchanges[i].GetDepth);
	// 	var endTime = new Date().getTime();
	// 	elapses[i] = endTime - startTime;
	// }
	while (true) {
		for (var i = 0; i < exchanges.length; i++) {
			if (depths[i] == null && (elapses[i] == null || elapses[i] <= maxElapse)) {
				// Create Asynchronous Operation
				depths[i] = exchanges[i].Go("GetDepth");
			}
		}
		var failed = 0;
		for (var i = 0; i < exchanges.length; i++) {
			if (depths[i] == null) {
				continue;
			}
			if (typeof(depths[i].wait) != "undefined") {
				var waitStartTime = new Date().getTime();
				// Waiting for results
				var depth = depths[i].wait(5);
				if (typeof(depth) != "undefined") {
					if (depth) {
						depths[i] = depth;
					} else {
						// Try again
						depths[i] = null;
						failed++;
					}
				} else {
					failed++;
				}
				var waitEndTime = new Date().getTime();
				if (elapses[i] == null) {
					elapses[i] = waitEndTime - waitStartTime;
				} else {
					elapses[i] = elapses[i] + waitEndTime - waitStartTime;
				}
			}
		}
		if (failed == 0) {
			break;
		}
	}
	var finishTime = new Date().getTime();
	return {
		"totalElapse": finishTime - beginTime,
		"elapses": elapses,
		"depths": depths
	};
}

function getExchangeTariff(index) {
	var exchangeName = exchanges[index].GetName();
	if (exchangeName == "Huobi") {
		return 0.09 / 100;
	} else if (exchangeName == "Binance") {
		return 0.075 / 100;
	} else if (exchangeName == "GateIO") {
		return 0.03 / 100;
	} else if (exchangeName == "OKEX") {
		return 0.15 / 100;
	} else {
		return 0.1 / 100;
	}
}
var pricesChart = Chart([{ // this chart At/InJS In the language, it is an object, in useChart Before the function, we need to declare an object variable to configure the chartchart.
	__isStock: true, // Mark whether it is a general chart. If interested, you can change it to false and run it.
	tooltip: {
		xDateFormat: '%Y-%m-%d %H:%M:%S, %A'
	}, // Zoom tool
	title: {
		text: 'Spread analysis chart'
	}, // Title
	rangeSelector: { // Selection range
		buttons: [{
			type: 'hour',
			count: 1,
			text: '1h'
		}, {
			type: 'hour',
			count: 3,
			text: '3h'
		}, {
			type: 'hour',
			count: 8,
			text: '8h'
		}, {
			type: 'all',
			text: 'All'
		}],
		selected: 0,
		inputEnabled: false
	},
	xAxis: {
		type: 'datetime'
	}, // Horizontal axis of the coordinate system, i.e., x-axis. The currently set type is: Time
	yAxis: { // coordinate axis vertical axis i.e., y-axis, default value adjusts with data size.
		title: {
			text: 'Spread'
		}, // Title
		opposite: false, // Whether to enable the right vertical axis
	},
	series: [ // Data series, this attribute saves each data series (line, candlestick chart, label, etc...)
		{
			name: "Entrusted purchase price",
			id: "Entrusted purchase price,bidPrice",
			data: []
		}, {
			name: "Entrusted selling price",
			id: "Entrusted selling price,askPrice",
			data: []
		}, {
			name: "Arbitrage purchase price",
			id: "Arbitrage purchase price,arbitrageBidPrice",
			data: []
		}, {
			name: "Arbitrage selling price",
			id: "Arbitrage selling price,arbitrageAskPrice",
			data: []
		}, {
			name: "Buy Order Price",
			id: "Buy Order Price,placeOrderPrice",
			dashStyle: 'shortdash',
			data: []
		}, {
			name: "Buy Cancel Price",
			id: "Buy Cancel Price,cancelOrderPrice",
			dashStyle: 'shortdash',
			data: []
		},
	]
}]);

function updatePriceChart(bidPrice, askPrice, arbitrageBidRealPrice, arbitrageAskRealPrice, placeOrderDiffPriceRatio, cancelOrderDiffPriceRatio) {
	var nowTime = new Date().getTime();
	pricesChart.add([0, [nowTime, bidPrice.RealPrice]]);
	pricesChart.add([1, [nowTime, askPrice.RealPrice]]);
	pricesChart.add([2, [nowTime, arbitrageBidRealPrice]]);
	pricesChart.add([3, [nowTime, arbitrageAskRealPrice]]);
	pricesChart.add([4, [nowTime, bidPrice.RealPrice * (1 + placeOrderDiffPriceRatio)]]);
	pricesChart.add([5, [nowTime, bidPrice.RealPrice * (1 + cancelOrderDiffPriceRatio)]]);
}

var CurrencyOverturn = false;

var BidOrder = {
	"DealAmount": 0,
	"Amount": 0,
	"Price": 0,
	"RealPrice": 0,
	"OrderId": 0,
}
var AskOrder = {
	"DealAmount": 0,
	"Amount": 0,
	"Price": 0,
	"RealPrice": 0,
	"OrderId": 0,
}

var RunningInfo = {
	"OpenOrders": [],
	"Profit": 0,
	"FeeCost": 0,
	"CoinProfit": 0,
	"CoinFeeCost": 0,
	"Profit_hedge": 0,
	"FeeCost_hedge": 0,
	"Changed": false
};

var AccountInfo = {
	"CurBalance": 0,
	"CurStocks": 0,
	"LastUpdateTime": 0,
}

function updateAccountInfo(flush) {
	if (!flush && new Date().getTime() - AccountInfo.LastUpdateTime < 60 * 1000) {
		return
	}
	var exAccount = _C(exchanges[0].GetAccount);
	AccountInfo.CurBalance = exAccount.Balance;
	AccountInfo.CurStocks = exAccount.Stocks;
	AccountInfo.LastUpdateTime = new Date().getTime();
}

function getOrder(ex, orderId) {
	order = ex.GetOrder(orderId);
	if (order != null) {
		fixOrder(ex, order);
	}
	return order;
}

function fixOrder(ex, order) {
	var exName = ex.GetName();
	if (exName == "GateIO") {
		order.DealAmount = parseFloat(order.Info.filledAmount);
		order.AvgPrice = parseFloat(order.Info.filledRate);
	} else if (exName == "Binance") {
		order.AvgPrice = parseFloat(order.Info.cummulativeQuoteQty) / order.DealAmount;
	}
}

function mergeDepth(askOrBids, mergeAmount) {
	var askOrBid = {
		"Amout": 0,
		"Price": 0
	};
	for (var i = 0; i < askOrBids.length; i++) {
		if (askOrBid.Amout > mergeAmount) {
			break;
		}
		askOrBid.Amout += askOrBids[i].Amount;
		askOrBid.Price = askOrBids[i].Price;
	}
	return askOrBid;
}

function getArbitrageBidRealPrice(depths) {
	var askPrice1 = mergeDepth(depths[1].Asks, maxTakerAmount).Price
	var askMoney1 = askPrice1 * maxTakerAmount;
	if (CurrencyOverturn) {
		return (askPrice1 * (1 + getExchangeTariff(1))) * (mergeDepth(depths[2].Asks, askMoney1).Price * (1 + getExchangeTariff(2)));
	} else {
		return (askPrice1 * (1 + getExchangeTariff(1))) / (mergeDepth(depths[2].Bids, askMoney1 / depths[2].Bids[0].Price).Price * (1 - getExchangeTariff(2)));
	}
}

function getArbitrageAskRealPrice(depths) {
	var bidPrice1 = mergeDepth(depths[1].Bids, maxTakerAmount).Price;
	var bidMoney1 = bidPrice1 * maxTakerAmount;
	if (CurrencyOverturn) {
		return (bidPrice1 * (1 - getExchangeTariff(1))) * (mergeDepth(depths[2].Bids, bidMoney1).Price * (1 - getExchangeTariff(2)));
	} else {
		return (bidPrice1 * (1 - getExchangeTariff(1))) / (mergeDepth(depths[2].Asks, bidMoney1 / depths[2].Asks[0].Price).Price * (1 + getExchangeTariff(2)));
	}
}

function getOpenOrdersAmount() {
	var amount = 0;
	for (var i = 0; i < RunningInfo.OpenOrders.length; i++) {
		amount += RunningInfo.OpenOrders[i].Amout;
	}
	return amount;
}

function getOpenOrdersAvgRealPrice() {
	var amount = 0;
	var realMoney = 0;
	for (var i = 0; i < RunningInfo.OpenOrders.length; i++) {
		amount += RunningInfo.OpenOrders[i].Amout;
		realMoney += RunningInfo.OpenOrders[i].RealPrice * RunningInfo.OpenOrders[i].Amout;
	}
	if (amount > 0) {
		return realMoney / amount;
	} else {
		return 0;
	}
}

function mergeOpenOrders() {
	var buyOpenOrders = [];
	var sellOpenOrders = [];
	for (var i = 0; i < RunningInfo.OpenOrders.length; i++) {
		if (RunningInfo.OpenOrders[i].Amout > 0) {
			var contain = false;
			for (var j = 0; j < buyOpenOrders.length; j++) {
				if (buyOpenOrders[j].Price == RunningInfo.OpenOrders[i].Price) {
					buyOpenOrders[j].Amout += RunningInfo.OpenOrders[i].Amout;
					contain = true;
					break;
				}
			}
			if (!contain && RunningInfo.OpenOrders[i].Amout != 0) {
				buyOpenOrders.push(RunningInfo.OpenOrders[i]);
			}
		} else {
			var contain = false;
			for (var j = 0; j < sellOpenOrders.length; j++) {
				if (sellOpenOrders[j].Price == RunningInfo.OpenOrders[i].Price) {
					sellOpenOrders[j].Amout += RunningInfo.OpenOrders[i].Amout;
					contain = true;
					break;
				}
			}
			if (!contain && RunningInfo.OpenOrders[i].Amout != 0) {
				sellOpenOrders.push(RunningInfo.OpenOrders[i]);
			}
		}
	}

	var profitChange = false;
	for (var i = 0; i < buyOpenOrders.length; i++) {
		var buyOpenOrder = buyOpenOrders[i];
		if (buyOpenOrder.Amout == 0) {
			continue;
		}
		for (var j = 0; j < sellOpenOrders.length; j++) {
			var sellOpenOrder = sellOpenOrders[j];
			if (sellOpenOrder.Amout == 0) {
				continue;
			}
			if (RunningInfo.Profit_hedge == null) {
				RunningInfo.Profit_hedge = 0;
			}
			if (RunningInfo.FeeCost_hedge == null) {
				RunningInfo.FeeCost_hedge = 0;
			}
			if (buyOpenOrder.Amout + sellOpenOrder.Amout > 0) {
				RunningInfo.Profit_hedge += (-sellOpenOrder.Amout) * (sellOpenOrder.RealPrice - buyOpenOrder.RealPrice);
				RunningInfo.FeeCost_hedge += (-sellOpenOrder.Amout * sellOpenOrder.Price * getExchangeTariff(0)) + (-sellOpenOrder.Amout * buyOpenOrder.Price * getExchangeTariff(0))
				buyOpenOrder.Amout += sellOpenOrder.Amout;
				sellOpenOrder.Amout = 0;
			} else {
				RunningInfo.Profit_hedge += (buyOpenOrder.Amout) * (sellOpenOrder.RealPrice - buyOpenOrder.RealPrice);
				RunningInfo.FeeCost_hedge += (buyOpenOrder.Amout * sellOpenOrder.Price * getExchangeTariff(0)) + (buyOpenOrder.Amout * buyOpenOrder.Price * getExchangeTariff(0))
				sellOpenOrder.Amout += buyOpenOrder.Amout;
				buyOpenOrder.Amout = 0;
			}
			profitChange = true;
		}
	}
	if (profitChange) {
		RunningInfo.Changed = true;
		// LogProfit(RunningInfo.Profit + RunningInfo.CoinProfit * RunningInfo.OpenOrders[i].Price);
	}
	var nowOpenOrders = [];
	var fixOpenOrders = [];
	for (var i = 0; i < buyOpenOrders.length; i++) {
		if (buyOpenOrders[i].Amout == 0) {
			continue;
		}
		if (buyOpenOrders[i].TransactionTime != null && new Date().getTime() - buyOpenOrders[i].TransactionTime < 5 * 60 * 1000) {
			nowOpenOrders.push(buyOpenOrders[i])
			continue;
		}
		if (fixOpenOrders.length == 0 || fixOpenOrders[fixOpenOrders.length - 1].Amout < 0) {
			fixOpenOrders.push(buyOpenOrders[i]);
			continue;
		}
		var mergeOpenOrder = fixOpenOrders[fixOpenOrders.length - 1];
		var mergeAmount = buyOpenOrders[i].Amout + mergeOpenOrder.Amout;
		var mergeMoney = buyOpenOrders[i].Amout * buyOpenOrders[i].Price + mergeOpenOrder.Amout * mergeOpenOrder.Price;
		var mergeRealMoney = buyOpenOrders[i].Amout * buyOpenOrders[i].RealPrice + mergeOpenOrder.Amout * mergeOpenOrder.RealPrice;
		mergeOpenOrder.Amout = mergeAmount;
		mergeOpenOrder.Price = mergeMoney / mergeAmount;
		mergeOpenOrder.RealPrice = mergeRealMoney / mergeAmount;
	}
	for (var i = 0; i < sellOpenOrders.length; i++) {
		if (sellOpenOrders[i].Amout == 0) {
			continue;
		}
		if (sellOpenOrders[i].TransactionTime != null && new Date().getTime() - sellOpenOrders[i].TransactionTime < 5 * 60 * 1000) {
			nowOpenOrders.push(sellOpenOrders[i]);
			continue;
		}
		if (fixOpenOrders.length == 0 || fixOpenOrders[fixOpenOrders.length - 1].Amout > 0) {
			fixOpenOrders.push(sellOpenOrders[i]);
			continue;
		}
		var mergeOpenOrder = fixOpenOrders[fixOpenOrders.length - 1];
		var mergeAmount = sellOpenOrders[i].Amout + mergeOpenOrder.Amout;
		var mergeMoney = sellOpenOrders[i].Amout * sellOpenOrders[i].Price + mergeOpenOrder.Amout * mergeOpenOrder.Price;
		var mergeRealMoney = sellOpenOrders[i].Amout * sellOpenOrders[i].RealPrice + mergeOpenOrder.Amout * mergeOpenOrder.RealPrice;
		mergeOpenOrder.Amout = mergeAmount;
		mergeOpenOrder.Price = mergeMoney / mergeAmount;
		mergeOpenOrder.RealPrice = mergeRealMoney / mergeAmount;

	}
	for (var i = 0; i < nowOpenOrders.length; i++) {
		fixOpenOrders.push(nowOpenOrders[i]);
	}
	RunningInfo.OpenOrders = fixOpenOrders;
}

function marketSell(exIndex, amount, bidPrice) {
	var orderId = null;
	var ex = exchanges[exIndex];
	if (ex.GetName() == "GateIO") {
		orderId = ex.Sell(bidPrice * 0.8, amount, ex.GetCurrency());
		if (orderId == null) {
			Sleep(500);
			orderId = ex.Sell(bidPrice * 0.8, amount, ex.GetCurrency());
		}
	} else {
		orderId = ex.Sell(-1, amount, ex.GetCurrency());
		if (orderId == null) {
			Sleep(500);
			orderId = ex.Sell(-1, amount, ex.GetCurrency());
		}
	}
	if (orderId == null) {
		return null;
	}
	var order = null;
	while (true) {
		order = getOrder(ex, orderId);
		if (order != null && order.Status != ORDER_STATE_PENDING) {
			break;
		} else {
			Sleep(50);
		}
	}
	return order
}

function marketBuy(exIndex, amount, askPrice) {
	var orderId = null;
	var ex = exchanges[exIndex];
	if (ex.GetName() == "GateIO") {
		orderId = ex.Buy(askPrice * 1.2, amount, ex.GetCurrency())
		if (orderId == null) {
			Sleep(500);
			orderId = ex.Buy(askPrice * 1.2, amount, ex.GetCurrency())
		}
	} else {
		orderId = ex.Buy(-1, amount, ex.GetCurrency())
		if (orderId == null) {
			Sleep(500);
			orderId = ex.Buy(-1, amount, ex.GetCurrency())
		}
	}
	if (orderId == null) {
		return null;
	}
	var order = null;
	while (true) {
		order = getOrder(ex, orderId);
		if (order != null && order.Status != ORDER_STATE_PENDING) {
			break;
		} else {
			Sleep(50);
		}
	}
	return order
}

function isBuyAmount(exIndex) {
	return exchanges[exIndex].GetName() == "Binance" || exchanges[exIndex].GetName() == "GateIO";
}


function handleOpenOrders(arbitrageBidRealPrice, arbitrageAskRealPrice, cancelOrderDiffPriceRatio, depths) {
	if (RunningInfo.OpenOrders.length == 0) {
		return false;
	}
	mergeOpenOrders();
	for (var i = 0; i < RunningInfo.OpenOrders.length; i++) {
		var doTransaction = false;
		if (RunningInfo.OpenOrders[i].Amout >= minTakerAmount && arbitrageAskRealPrice > RunningInfo.OpenOrders[i].RealPrice * (1 + cancelOrderDiffPriceRatio)) {
			if (runMode == 1 && (AskOrder.OrderId != 0 && AskOrder.OrderId != null) && getOpenOrdersAmount() - (AskOrder.Amount + AskOrder.DealAmount) < math.min(maxTakerAmount, RunningInfo.OpenOrders[i].Amout)) {
				exchanges[0].CancelOrder(AskOrder.OrderId, "Sell: ", AskOrder," current one-sided quantity:", getOpenOrdersAmount());
				return false;
			}
			Log("Arbitrage path: [buy->sell], Buying price" + RunningInfo.OpenOrders[i].Price + ", Start======");
			//Small Coin to Buy
			var takerAmount = math.min(maxTakerAmount, RunningInfo.OpenOrders[i].Amout); //Small currency
			var takerMoney = takerAmount * RunningInfo.OpenOrders[i].Price; //Large currencies
			var takerFeeCost = takerMoney * getExchangeTariff(0); //Major Coin Fee
			//Sell the small currency to get the middle currency
			var order = marketSell(1, takerAmount, mergeDepth(depths[1].Bids, takerAmount).Price);
			if (order == null) {
				continue;
			}
			//The intermediate currency obtained
			var swapCoinPrice = order.AvgPrice;
			var swapCoinAmount = order.DealAmount * order.AvgPrice;
			var swapCoinFeeCost = swapCoinAmount * getExchangeTariff(1); //Intermediate currency handling fee
			if (CurrencyOverturn) {
				//Third exchange reversal: CoinC/CoinB, CoinCIs the intermediate currency
				order = marketSell(2, swapCoinAmount, mergeDepth(depths[2].Bids, swapCoinAmount).Price)
			} else {
				//Buy large currencies through intermediate currencies: CoinB/CoinC
				if (isBuyAmount(2)) {
					//Set purchase quantity on Binance
					var hedgeMoney = (RunningInfo.Profit_hedge + RunningInfo.FeeCost_hedge)
					var compensateMoney = 0;
					if (hedgeMoney < -takerMoney) {
						compensateMoney = takerMoney / 4
					} else if (hedgeMoney < 0) {
						compensateMoney = -hedgeMoney
					}
					order = marketBuy(2, takerMoney + compensateMoney, mergeDepth(depths[2].Asks, takerMoney + compensateMoney).Price)
				} else {
					//Other setting of purchase amount
					order = marketBuy(2, swapCoinAmount, 0)
				}
			}

			if (order == null) {
				RunningInfo.OpenOrders[i].Amout -= takerAmount;
				return true;
			}
			var feeCost = 0;
			var profit = 0;
			if (CurrencyOverturn) {
				feeCost = takerFeeCost + swapCoinFeeCost * order.AvgPrice + order.DealAmount * order.AvgPrice * getExchangeTariff(2);
				profit = order.DealAmount * order.AvgPrice - takerMoney - feeCost;
			} else {
				if (isBuyAmount(2)) { //Binance earns the intermediate currency
					feeCost = takerFeeCost * order.AvgPrice + swapCoinFeeCost + order.DealAmount * order.AvgPrice * getExchangeTariff(2);
					profit = swapCoinAmount - order.DealAmount * order.AvgPrice - feeCost;
					RunningInfo.Profit_hedge += (order.DealAmount - takerMoney)
					if (RunningInfo.FeeCost_hedge > 0) {
						feeCost += RunningInfo.FeeCost_hedge * order.AvgPrice
						profit -= RunningInfo.FeeCost_hedge * order.AvgPrice
						RunningInfo.Profit_hedge += RunningInfo.FeeCost_hedge;
						RunningInfo.FeeCost_hedge = 0;
					}
				} else { //Others earn major currencies
					feeCost = takerFeeCost + swapCoinFeeCost / order.AvgPrice + order.DealAmount * getExchangeTariff(2);
					profit = order.DealAmount - takerMoney - feeCost;
				}
			}
			RunningInfo.Profit += profit;
			RunningInfo.FeeCost += feeCost;
			RunningInfo.Changed = true;
			Log("Arbitrage methods: [buy->sell], Selling price", CurrencyOverturn ? swapCoinPrice * order.AvgPrice : swapCoinPrice / order.AvgPrice, ", Quantity", takerAmount, ", trading fee", feeCost, ", Profit", profit);
			LogProfit(RunningInfo.Profit + (RunningInfo.CoinProfit - RunningInfo.CoinFeeCost) * RunningInfo.OpenOrders[i].Price);
			RunningInfo.OpenOrders[i].Amout -= takerAmount;
			doTransaction = true;
		} else if (RunningInfo.OpenOrders[i].Amout <= -minTakerAmount && arbitrageBidRealPrice < RunningInfo.OpenOrders[i].RealPrice * (1 - cancelOrderDiffPriceRatio)) {
			if (runMode == 2 && (BidOrder.OrderId != 0 && BidOrder.OrderId != null) && getOpenOrdersAmount() + (BidOrder.Amount - BidOrder.DealAmount) > -math.min(maxTakerAmount, -RunningInfo.OpenOrders[i].Amout)) {
				exchanges[0].CancelOrder(BidOrder.OrderId, "Buy: ", BidOrder, "Current one-sided quantity.":", getOpenOrdersAmount());
				return false;
			}
			Log("Arbitrage path: [sell->buy], Selling price" + RunningInfo.OpenOrders[i].Price + ", Start======");
			//Small Coin to Sell
			var takerAmount = math.min(maxTakerAmount, -RunningInfo.OpenOrders[i].Amout);
			var takerMoney = takerAmount * RunningInfo.OpenOrders[i].Price; //Large currencies
			var takerFeeCost = takerMoney * getExchangeTariff(0); //Major Coin Fee
			//Sell the big currency to get the middle currency
			//todo: The third trading pair flip was not handled
			var order = marketSell(2, takerMoney, mergeDepth(depths[2].Bids, takerMoney).Price)
			if (order == null) {
				continue;
			}
			//The intermediate currency obtained
			var swapCoinPrice = order.AvgPrice;
			var swapCoinAmount = order.DealAmount * order.AvgPrice;
			var swapCoinFeeCost = swapCoinAmount * getExchangeTariff(2); //Intermediate currency handling fee
			var bigSwapPrice = order.AvgPrice;
			//Buy small coins through an intermediate currency
			if (isBuyAmount(1)) {
				//Set purchase quantity on Binance
				order = marketBuy(1, takerAmount, mergeDepth(depths[1].Asks, takerAmount).Price)
			} else {
				//Other setting of purchase amount
				order = marketBuy(1, swapCoinAmount, 0)
			}
			if (order == null) {
				RunningInfo.OpenOrders[i].Amout += takerAmount;
				return true;
			}
			var feeCost = 0;
			var profit = 0;
			var coinProfit = 0;
			var coinFeeCost = 0;
			if (isBuyAmount(1)) { //Binance earns the intermediate currency
				feeCost = takerFeeCost * bigSwapPrice + swapCoinFeeCost + order.DealAmount * order.AvgPrice * getExchangeTariff(2);
				profit = swapCoinAmount - order.DealAmount * order.AvgPrice - feeCost;
			} else { //Others earn minor currencies
				feeCost = takerFeeCost + swapCoinFeeCost / bigSwapPrice + order.DealAmount * order.AvgPrice / bigSwapPrice * getExchangeTariff(2);
				coinProfit = order.DealAmount - takerAmount;
				coinFeeCost = order.DealAmount * getExchangeTariff(1);
			}
			RunningInfo.FeeCost += feeCost;
			RunningInfo.Profit += profit;
			RunningInfo.CoinProfit += coinProfit;
			RunningInfo.CoinFeeCost += coinFeeCost;
			RunningInfo.Changed = true;
			if (isBuyAmount(1)) {
				Log("Arbitrage methods: [sell->buy], Buying price", CurrencyOverturn ? swapCoinPrice * order.AvgPrice : order.AvgPrice / swapCoinPrice, ", Quantity", takerAmount, ", trading fee", feeCost, ", Profit", profit);
			} else {
				Log("Arbitrage methods: [sell->buy], Buying price", CurrencyOverturn ? swapCoinPrice * order.AvgPrice : order.AvgPrice / swapCoinPrice, ", Quantity", takerAmount, ", trading fee", feeCost, ", Get currency", coinProfit);
			}
			LogProfit(RunningInfo.Profit + (RunningInfo.CoinProfit - RunningInfo.CoinFeeCost) * RunningInfo.OpenOrders[i].Price);
			RunningInfo.OpenOrders[i].Amout += takerAmount;
			doTransaction = true;
		}
		if (doTransaction) {
			return true;
		}
	}
	return false;
}

function loop(bidPrice, askPrice, arbitrageBidRealPrice, arbitrageAskRealPrice, placeOrderDiffPriceRatio, cancelOrderDiffPriceRatio) {
	if ((arbitrageAskRealPrice > bidPrice.RealPrice * (1 + placeOrderDiffPriceRatio) && (runMode == 3 || runMode == 1)) ||
		(runMode == 2 && getOpenOrdersAmount() < -minTakerAmount &&
			(getOpenOrdersAvgRealPrice() > bidPrice.RealPrice ||
				(arbitrageAskRealPrice > bidPrice.RealPrice * (1 - cancelOrderDiffPriceRatio) &&
					arbitrageBidRealPrice > bidPrice.RealPrice * (1 + (placeOrderDiffPriceRatio + cancelOrderDiffPriceRatio) * 1.5)
				)
			)
		)
	) {
		if (BidOrder.OrderId == 0 || BidOrder.OrderId == null) {
			var buyAmount = math.min(AccountInfo.CurBalance / bidPrice.Price, buyMaxTakerAmount);
			if (buyAmount > minTakerAmount) {
				BidOrder.OrderId = exchanges[0].Buy(bidPrice.Price, buyAmount);
				BidOrder.Price = bidPrice.Price;
				BidOrder.RealPrice = bidPrice.RealPrice;
				BidOrder.Amount = buyAmount;
			}
		} else {
			var order = _C(exchanges[0].GetOrder, BidOrder.OrderId);
			fixOrder(exchanges[0], order);
			if (order.Status != ORDER_STATE_PENDING) {
				if (order.DealAmount > BidOrder.DealAmount) {
					RunningInfo.OpenOrders.push({
						"Amout": order.DealAmount - BidOrder.DealAmount,
						"Price": order.Price,
						"RealPrice": order.Price * (1 + getExchangeTariff(0)),
						"TransactionTime": new Date().getTime(),
					});
					if (order.DealAmount - BidOrder.DealAmount > minTakerAmount) {
						Log("Buy transaction, Quantity", order.DealAmount - BidOrder.DealAmount, ", Price", order.Price, "#ff0000@");
					}
				}
				BidOrder.OrderId = 0;
				BidOrder.DealAmount = 0;
			} else if (bidPrice.Price > BidOrder.Price) {
				exchanges[0].CancelOrder(BidOrder.OrderId, "buy:", BidOrder);
			} else {
				if (order.DealAmount > BidOrder.DealAmount) {
					RunningInfo.OpenOrders.push({
						"Amout": order.DealAmount - BidOrder.DealAmount,
						"Price": order.Price,
						"RealPrice": order.Price * (1 + getExchangeTariff(0)),
						"TransactionTime": new Date().getTime(),
					});
					if (order.DealAmount - BidOrder.DealAmount > minTakerAmount) {
						Log("Buy transaction, Quantity", order.DealAmount - BidOrder.DealAmount, ", Price", order.Price, "#ff0000@");
					}
					BidOrder.DealAmount = order.DealAmount;
				}
			}
		}
	} else if (BidOrder.OrderId != 0 && BidOrder.OrderId != null) {
		var order = _C(exchanges[0].GetOrder, BidOrder.OrderId);
		fixOrder(exchanges[0], order);
		if (order.Status != ORDER_STATE_PENDING) {
			if (order.DealAmount > BidOrder.DealAmount) {
				RunningInfo.OpenOrders.push({
					"Amout": order.DealAmount - BidOrder.DealAmount,
					"Price": order.Price,
					"RealPrice": order.Price * (1 + getExchangeTariff(0)),
					"TransactionTime": new Date().getTime(),
				});
				if (order.DealAmount - BidOrder.DealAmount > minTakerAmount) {
					Log("Buy transaction, Quantity", order.DealAmount - BidOrder.DealAmount, ", Price", order.Price, "#ff0000@");
				}
			}
			BidOrder.OrderId = 0;
			BidOrder.DealAmount = 0;
		} else if ((arbitrageAskRealPrice < bidPrice.RealPrice * (1 + cancelOrderDiffPriceRatio) && bidPrice.Price <= BidOrder.Price && (runMode == 3 || runMode == 1)) ||
			(runMode == 2 && getOpenOrdersAvgRealPrice() <= BidOrder.RealPrice && bidPrice.Price <= BidOrder.Price &&
				(arbitrageAskRealPrice < bidPrice.RealPrice * (1 - placeOrderDiffPriceRatio) ||
					arbitrageBidRealPrice < bidPrice.RealPrice * (1 + (placeOrderDiffPriceRatio + cancelOrderDiffPriceRatio))
				)
			)
		) {
			exchanges[0].CancelOrder(BidOrder.OrderId, "buy:", BidOrder);
		} else {
			if (order.DealAmount > BidOrder.DealAmount) {
				RunningInfo.OpenOrders.push({
					"Amout": order.DealAmount - BidOrder.DealAmount,
					"Price": order.Price,
					"RealPrice": order.Price * (1 + getExchangeTariff(0)),
					"TransactionTime": new Date().getTime(),
				});
				if (order.DealAmount - BidOrder.DealAmount > minTakerAmount) {
					Log("Buy transaction, Quantity", order.DealAmount - BidOrder.DealAmount, ", Price", order.Price, "#ff0000@");
				}
				BidOrder.DealAmount = order.DealAmount;
			}
		}

	}


	if ((arbitrageBidRealPrice < askPrice.RealPrice * (1 - placeOrderDiffPriceRatio) && (runMode == 3 || runMode == 2)) ||
		(runMode == 1 && getOpenOrdersAmount() > minTakerAmount &&
			(getOpenOrdersAvgRealPrice() < askPrice.RealPrice ||
				(arbitrageBidRealPrice < askPrice.RealPrice * (1 + cancelOrderDiffPriceRatio) &&
					arbitrageAskRealPrice < askPrice.RealPrice * (1 - (placeOrderDiffPriceRatio + cancelOrderDiffPriceRatio) * 1.5)
				)
			)
		)
	) {
		if (AskOrder.OrderId == 0 || AskOrder.OrderId == null) {
			var sellAmount = math.min(AccountInfo.CurStocks, sellMaxTakerAmount);
			if (sellAmount > minTakerAmount) {
				AskOrder.OrderId = exchanges[0].Sell(askPrice.Price, sellAmount);
				AskOrder.Price = askPrice.Price;
				AskOrder.RealPrice = askPrice.RealPrice;
				AskOrder.Amount = sellAmount;
			}
		} else {
			var order = _C(exchanges[0].GetOrder, AskOrder.OrderId);
			fixOrder(exchanges[0], order);
			if (order.Status != ORDER_STATE_PENDING) {
				if (order.DealAmount > -AskOrder.DealAmount) {
					RunningInfo.OpenOrders.push({
						"Amout": -(order.DealAmount + AskOrder.DealAmount),
						"Price": order.Price,
						"RealPrice": order.Price * (1 - getExchangeTariff(0)),
						"TransactionTime": new Date().getTime(),
					});
					if (order.DealAmount + AskOrder.DealAmount > minTakerAmount) {
						Log("Sell transaction, Quantity", order.DealAmount + AskOrder.DealAmount, ", Price", order.Price, "#ff0000@");
					}
				}
				AskOrder.OrderId = 0;
				AskOrder.DealAmount = 0;
			} else if (askPrice.Price < AskOrder.Price) {
				exchanges[0].CancelOrder(AskOrder.OrderId, "sell:", AskOrder);
			} else {
				if (order.DealAmount > -AskOrder.DealAmount) {
					RunningInfo.OpenOrders.push({
						"Amout": -(order.DealAmount + AskOrder.DealAmount),
						"Price": order.Price,
						"RealPrice": order.Price * (1 - getExchangeTariff(0)),
						"TransactionTime": new Date().getTime(),
					});
					if (order.DealAmount + AskOrder.DealAmount > minTakerAmount) {
						Log("Sell transaction, Quantity", order.DealAmount + AskOrder.DealAmount, ", Price", order.Price, "#ff0000@");
					}
					AskOrder.DealAmount = -order.DealAmount;
				}
			}
		}
	} else if (AskOrder.OrderId != 0 && AskOrder.OrderId != null) {
		var order = _C(exchanges[0].GetOrder, AskOrder.OrderId);
		fixOrder(exchanges[0], order);
		if (order.Status != ORDER_STATE_PENDING) {
			if (order.DealAmount > -AskOrder.DealAmount) {
				RunningInfo.OpenOrders.push({
					"Amout": -(order.DealAmount + AskOrder.DealAmount),
					"Price": order.Price,
					"RealPrice": order.Price * (1 - getExchangeTariff(0)),
					"TransactionTime": new Date().getTime(),
				});
				if (order.DealAmount + AskOrder.DealAmount > minTakerAmount) {
					Log("Sell transaction, Quantity", order.DealAmount + AskOrder.DealAmount, ", Price", order.Price, "#ff0000@");
				}
			}
			AskOrder.OrderId = 0;
			AskOrder.DealAmount = 0;
		} else if ((arbitrageBidRealPrice > askPrice.RealPrice * (1 - cancelOrderDiffPriceRatio) && askPrice.Price >= AskOrder.Price && (runMode == 3 || runMode == 2)) ||
			(runMode == 1 && getOpenOrdersAvgRealPrice() >= AskOrder.RealPrice && askPrice.Price >= AskOrder.Price &&
				(arbitrageBidRealPrice > askPrice.RealPrice * (1 + placeOrderDiffPriceRatio) ||
					arbitrageAskRealPrice > askPrice.RealPrice * (1 - (placeOrderDiffPriceRatio + cancelOrderDiffPriceRatio))
				)
			)
		) {
			exchanges[0].CancelOrder(AskOrder.OrderId, "sell:", AskOrder);
		} else {
			if (order.DealAmount > -AskOrder.DealAmount) {
				RunningInfo.OpenOrders.push({
					"Amout": -(order.DealAmount + AskOrder.DealAmount),
					"Price": order.Price,
					"RealPrice": order.Price * (1 - getExchangeTariff(0)),
					"TransactionTime": new Date().getTime(),
				});
				if (order.DealAmount + AskOrder.DealAmount > minTakerAmount) {
					Log("Sell transaction, Quantity", order.DealAmount + AskOrder.DealAmount, ", Price", order.Price, "#ff0000@");
				}
				AskOrder.DealAmount = -order.DealAmount;
			}
		}

	}
}

function checkArgs() {
	Log("Detection parameters...");
	if (exchanges.length != 3) {
		throw "There must be three trading pairs to hedge";
	}
	if (exchanges[0].GetName() != exchanges[1].GetName() || exchanges[0].GetName() != exchanges[2].GetName()) {
		throw "The trading pairs are not on the same exchange";
	}
	var coinA = exchanges[0].GetCurrency().split("_")[0];
	var coinB = exchanges[0].GetCurrency().split("_")[1];
	if (exchanges[1].GetCurrency().split("_")[0] != coinA) {
		throw "Second Trading Pair" + exchanges[1].GetCurrency() + "Currency is not equal to" + coinA;
	}
	var coinC = exchanges[1].GetCurrency().split("_")[1];
	if (exchanges[2].GetCurrency() == coinB + "_" + coinC) {
		CurrencyOverturn = false;
	} else if (exchanges[2].GetCurrency() == coinC + "_" + coinB) {
		CurrencyOverturn = true;
	} else {
		throw "Third Trading Pair" + exchanges[2].GetCurrency() + "Unable to Hedge";
	}
	if (placePriceRatio < 0.5) {
		throw "Order Price Ratio:" + placePriceRatio + " Less Than0.5";
	}
	if (cancelPriceRatio > placePriceRatio) {
		throw "Cancel Order Price Ratio:" + cancelPriceRatio + " Greater than" + placePriceRatio;
	}
	Log("Start Triangular Arbitrage CoinA:", coinA, ", CoinB:", coinB, ", CoinC:", coinC, ", Third trading pair reversal:", CurrencyOverturn);
}


function updateStatus(totalElapse) {
	var coinA = exchanges[0].GetCurrency().split("_")[0];
	var coinB = exchanges[0].GetCurrency().split("_")[1];
	var coinC = exchanges[1].GetCurrency().split("_")[1];
	var makeCoin = !CurrencyOverturn && isBuyAmount(2) ? coinC : coinB;
	var profitPrecisions = !CurrencyOverturn && isBuyAmount(2) ? parseInt(pricePrecisions.split(",")[1]) : parseInt(pricePrecisions.split(",")[0]);
	var statusTable = [{
		type: 'table',
		title: 'Position information',
		cols: [],
		rows: []
	}, {
		type: 'table',
		title: 'Current Order',
		cols: ['Order Number', 'Quantity', 'Completed Quantity', 'Price.''],
		rows: []
	}, {
		type: 'table',
		title: 'Unilateral transaction',
		cols: ['Quantity', 'Price'],
		rows: []
	}];
	if (makeCoin != coinB) {
		statusTable[0].cols = ['Exchange', 'Fee%', 'Delay', 'Current balance', 'Current number of coins',
			'Revenue' + makeCoin, 'Revenue' + coinA, 'trading fee' + makeCoin, "Hedging income" + coinB, "Hedging fee" + coinB, 'Operation'
		];
		statusTable[0].rows[0] = [
			exchanges[0].GetName(),
			getExchangeTariff(0) * 100,
			totalElapse,
			_N(AccountInfo.CurBalance, parseInt(pricePrecisions.split(",")[0])),
			_N(AccountInfo.CurStocks, parseInt(amountPrecisions.split(",")[0])),
			_N(RunningInfo.Profit, profitPrecisions),
			_N(RunningInfo.CoinProfit, parseInt(amountPrecisions.split(",")[0])),
			_N(RunningInfo.FeeCost, profitPrecisions),
			_N(RunningInfo.Profit_hedge, parseInt(pricePrecisions.split(",")[0])),
			_N(RunningInfo.FeeCost_hedge, parseInt(pricePrecisions.split(",")[0])),
		]
	} else {
		statusTable[0].cols = ['Exchange', 'Fee%', 'Delay', 'Current balance', 'Current number of coins',
			'Revenue' + makeCoin, 'Revenue' + coinA, 'trading fee' + makeCoin, 'Operation'
		];
		RunningInfo.Profit += RunningInfo.Profit_hedge;
		RunningInfo.Profit_hedge = 0;
		RunningInfo.FeeCost += RunningInfo.FeeCost_hedge;
		RunningInfo.FeeCost_hedge = 0;
		statusTable[0].rows[0] = [
			exchanges[0].GetName(),
			getExchangeTariff(0) * 100,
			totalElapse,
			_N(AccountInfo.CurBalance, parseInt(pricePrecisions.split(",")[0])),
			_N(AccountInfo.CurStocks, parseInt(amountPrecisions.split(",")[0])),
			_N(RunningInfo.Profit, profitPrecisions),
			_N(RunningInfo.CoinProfit, parseInt(amountPrecisions.split(",")[0])),
			_N(RunningInfo.FeeCost, profitPrecisions),
		]
	}
	if (AskOrder.OrderId != 0 && AskOrder.OrderId != null) {
		statusTable[1].rows[statusTable[1].rows.length] = [AskOrder.OrderId, AskOrder.Amount, AskOrder.DealAmount, AskOrder.Price];
	}
	if (BidOrder.OrderId != 0 && BidOrder.OrderId != null) {
		statusTable[1].rows[statusTable[1].rows.length] = [BidOrder.OrderId, BidOrder.Amount, BidOrder.DealAmount, BidOrder.Price];
	}
	for (var i = 0; i < RunningInfo.OpenOrders.length; i++) {
		statusTable[2].rows[i] = [RunningInfo.OpenOrders[i].Amout, RunningInfo.OpenOrders[i].Price];
	}
	LogStatus('`' + JSON.stringify(statusTable) + '`' +
		"\nUpdate Time: " + _D(new Date().getTime())
	);
}


function main() {
	_CDelay(100);
	checkArgs();
	if (restoreData) {
		LogProfitReset();
		LogReset(1);
		LogVacuum();
		pricesChart.reset();
		_G(null);
	}
	SetErrorFilter("500:|502:|GetAccount: Failed to load data|Unknown order sent|Incorrect order state|timeout|network is unreachable|The request could not be satisfied|Too many requests; current limit is 1200 requests per minute|Request Timeout|timeout awaiting response headers|request canceled|GetOrder[\\w\\W]*?429 Too Many Requests|GetOrder[\\w\\W]*?Order does not exist|The order \\d* cancelled or not found");
	for (var i = 0; i < exchanges.length; i++) {
		exchanges[i].SetPrecision(parseInt(pricePrecisions.split(",")[i]), parseInt(amountPrecisions.split(",")[i]));
	}
	var runningInfo = _G("runningInfo");
	if (runningInfo != null) {
		RunningInfo = runningInfo;
		if (RunningInfo.CoinFeeCost == null) {
			RunningInfo.CoinFeeCost = 0;
		}
		if (RunningInfo.FeeCost_hedge == null) {
			RunningInfo.FeeCost_hedge = 0;
		}
		if (RunningInfo.Profit_hedge == null) {
			RunningInfo.Profit_hedge = 0;
		}
	}
	updateAccountInfo(true);
	Log(AccountInfo);

	while (true) {
		var sleepMillis = 500;
		var depthInfo = getDepthInfo();
		var reloop = false;
		for (var i = 0; i < depthInfo.elapses.length; i++) {
			if (depthInfo.elapses[i] > maxElapse) {
				reloop = true;
				break
			}
		}
		if (reloop) {
			Sleep(sleepMillis);
			continue;
		}
		var depths = depthInfo.depths;
		var bidPrice = {
			"Price": depths[0].Bids[0].Price,
			"RealPrice": depths[0].Bids[0].Price * (1 + getExchangeTariff(0))
		};
		var askPrice = {
			"Price": depths[0].Asks[0].Price,
			"RealPrice": depths[0].Asks[0].Price * (1 - getExchangeTariff(0))
		};
		var arbitrageBidRealPrice = getArbitrageBidRealPrice(depths);
		var arbitrageAskRealPrice = getArbitrageAskRealPrice(depths);
		var diffPriceRatio = (askPrice.RealPrice - bidPrice.RealPrice) / askPrice.RealPrice;
		if (diffPriceRatio < 0.5 / 100) {
			throw "The ratio of trading pair price difference is too small"
		}
		var placeOrderDiffPriceRatio = placePriceRatio * (diffPriceRatio / 2);
		var cancelOrderDiffPriceRatio = math.max(cancelPriceRatio * (diffPriceRatio / 2), 0.1 / 100);
		var bidOrderId = BidOrder.OrderId;
		var askOrderId = AskOrder.OrderId;
		var openOrdersAmount = getOpenOrdersAmount();
		if (runMode != 0) {
			if (handleOpenOrders(arbitrageBidRealPrice, arbitrageAskRealPrice, cancelOrderDiffPriceRatio, depths)) {
				sleepMillis = 50
			} else {
				loop(bidPrice, askPrice, arbitrageBidRealPrice, arbitrageAskRealPrice, placeOrderDiffPriceRatio, cancelOrderDiffPriceRatio);
			}
			_G("runningInfo", RunningInfo);
		}
		flushAccountInfo = BidOrder.OrderId != bidOrderId || AskOrder.OrderId != askOrderId || openOrdersAmount != getOpenOrdersAmount();
		updateAccountInfo(flushAccountInfo);
		updatePriceChart(bidPrice, askPrice, arbitrageBidRealPrice, arbitrageAskRealPrice, placeOrderDiffPriceRatio, cancelOrderDiffPriceRatio);
		updateStatus(depthInfo.totalElapse);
		Sleep(sleepMillis);
	}
}

function onexit() {
	cancelAllOrders();
}

function onerror() {
	cancelAllOrders();
}

function cancelAllOrders() {
	Log("Cancel All Orders...")
	var orders = _C(exchanges[0].GetOrders);
	for (var i = 0; i < orders.length; i++) {
		exchanges[0].CancelOrder(orders[i].Id, orders[i]);
	}
}
```

> Detail

https://www.fmz.com/strategy/365407

> Last Modified

2022-05-24 17:40:35
