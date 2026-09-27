
> Name

Porting-OKCoin-Leek-Harvesting-Bot-Annotated

> Author

lkk91297

> Strategy Description

Transplanted from: https://github.com/richox/okcoin-leeks-reaper

The original author said the service becomes invalid after charging fees. I only did the port, no real market testing. If interested, you can learn
Because the strategy uses GetTrades, this function is simulated in the backtest system, so the backtest is meaningless and can only be tested directly on the real market. !

The following is the original description


OKCoinLeek harvester
================

This is a high-frequency trading robot program on the OKCoin Bitcoin trading platform. From June 2016, the strategy was basically finalized. By mid-January 2017, this strategy successfully increased the initial investment of 6,000 yuan to 250,000. Due to the recent central bank's high-pressure policy on Bitcoin, major platforms have stopped allocating funds and begun to collect transaction fees. This strategy has actually become ineffective.

 ![image](https://dn-filebox.qbox.me/707cd47e69d21b06f3815b933b471390a8d2cedd.png)

This robot program is based on two main strategies:

1. Trend strategy: place orders promptly when the price experiences trend movements, i.e., the so-called **follow the rise, sell at the fall****.
2. Balance strategy: When the position deviates from 50%, place small orders to gradually return the position to 50% to prevent the reversal at the end of the trend from causing a retracement, that is, the maximum profit will be pocketed, and no fish tail will be eaten.**.

This procedure requires balancing positions, that is (principal + financing = currency financing), so that the net assets of the position do not fluctuate with the price when the position is 50%, and also ensures that when trend fluctuations occur, you can make money regardless of the ups and downs.**.

Thanks to the following two projects:

* https://github.com/sutra/okcoin-client
* https://github.com/timmolter/xchange

thanksOKCoin:

* https://www.okcoin.cn

BTC: 3QFn1qfZMhMQ4FhgENR7fha3T8ZVw1bEeU

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|BurstThresholdPct|5e-05|burst.threshold.pct|
|BurstThresholdVol|10|burst.threshold.vol|
|MinStock|0.1|Minimum transaction volume|
|CalcNetInterval|60|Net value calculation period (seconds)|
|BalanceTimeout|10000|Balance waiting time (milliseconds))|
|TickInterval|280|polling cycle (milliseconds))|


> Source (javascript)

``` javascript
function LeeksReaper() {                                        //Create constructorLeeksReaper
    var self = {}                                               //Construct an empty object
    self.numTick = 0
    self.lastTradeId = 0
    self.vol = 0
    self.askPrice = 0
    self.bidPrice = 0
    self.orderBook = { Asks: [], Bids: [] }
    self.prices = []
    self.tradeOrderId = 0
    self.p = 0.5
    self.account = null
    self.preCalc = 0
    self.preNet = 0
    //All of the aboveselfobject properties
    //Create a method
    self.updateTrades = function () {
        var trades = _C(exchange.GetTrades)                     //Create a variabletradesUsed to Receive_CValue returned by the function, the passed-in parameters are:exchange.GetTrades
        if (self.prices.length == 0) {                          //Ifself.pricesLength equals0
            while (trades.length == 0) {                        //IftradesEqual to0Execute the following statement when
                trades = trades.concat(_C(exchange.GetTrades))  //Use array concatenation methods to_Cthe value returned by the function andtradesPerform concatenation, passing in the parameter as:exchange.GetTrades
            }
            for (var i = 0; i < 15; i++) {                      //Loop, with the end condition beingi=15,Each iterationiAll self-increment1
                self.prices[i] = trades[trades.length - 1].Price//In each looptradesAssign the last value of the array toselfOf the objectpriceson the array, looped together15times
            }
        }
        //self.volThe value equals itself multiplied by0.7plus_.reduceThe return value of the function*0.3,among_.reduceThe parameters passed into the function aretradesAnd an anonymous function, and also a0,The parameters of the anonymous function aremen,trade
        self.vol = 0.7 * self.vol + 0.3 * _.reduce(trades, function (mem, trade) {
            // Huobi not support trade.Id
            //The first half is a comparisonrade.IdGreater thanself.lastTradeId,If the result istrueThen execute the following statement, if it isfalesJust look ahead, the latter half AND operator,trade.Id == 0andtrade.Time > self.lastTradeIdWill only return true when both are truetrue,YesfalesThen returnfales
            if ((trade.Id > self.lastTradeId) || (trade.Id == 0 && trade.Time > self.lastTradeId)) {
                //The right side of the equal sign is a ternary operation, iftrade.Id=0Just returntrade.Time,Otherwise returntrade.Id, self.lastTradeId.And compared to return the maximum value, finally assign the returned maximum value toself.lastTradeId
                self.lastTradeId = Math.max(trade.Id == 0 ? trade.Time : trade.Id, self.lastTradeId)
                //mem=trade.Amount+mem 
                mem += trade.Amount
            }
            //Returnmem
            return mem
        }, 0)


    }
    //selfa method of the object
    self.updateOrderBook = function () {
        // Create a variableorderBookUsed to Receive_CValue returned by the function, the passed-in parameters are:exchange.GetDepth
        var orderBook = _C(exchange.GetDepth)
        self.orderBook = orderBook                              //self.orderBook Value EqualsorderBook
        if (orderBook.Bids.length < 3 || orderBook.Asks.length < 3) {//The first half is a condition checkorderBook.Bidswhether the length is less than3,The second half is a condition checkorderBook.Askswhether the length is less than3,if both sides are less than3Then execute the following statement
            //Returnundefined
            return
        }
        //self.bidPriceValue EqualsorderBook.BidsThe first value of the array multiplied by0.618plusorderBook.AsksThe first value of the array multiplied by0.382plus0.01
        self.bidPrice = orderBook.Bids[0].Price * 0.618 + orderBook.Asks[0].Price * 0.382 + 0.01
        //Same as above
        self.askPrice = orderBook.Bids[0].Price * 0.382 + orderBook.Asks[0].Price * 0.618 - 0.01
        //DeletepriceThe first value of the array and returns the first value
        self.prices.shift()
        //pricesAppend value to the array, value is the function_NReturn value of
        self.prices.push(_N((orderBook.Bids[0].Price + orderBook.Asks[0].Price) * 0.35 +
            (orderBook.Bids[1].Price + orderBook.Asks[1].Price) * 0.1 +
            (orderBook.Bids[2].Price + orderBook.Asks[2].Price) * 0.05))
    }
    //selfa method of the object
    self.balanceAccount = function () {
        // Create a variableaccountUsed to ReceiveGetAccountThe value returned by the function
        var account = exchange.GetAccount()
        //JudgmentaccountCheck if empty, if so returnundefined
        if (!account) {
            return
        }
        //Assignment
        self.account = account
        //Get the timestamp data of the current time
        var now = new Date().getTime()
        //Judgmentself.orderBook.Bidswhether the length is greater than0andnow - self.preCalcWhether the value is greater than(CalcNetInterval * 1000),Execute the following statement if all are greater
        if (self.orderBook.Bids.length > 0 && now - self.preCalc > (CalcNetInterval * 1000)) {
            //Assignment
            self.preCalc = now
            //Create a variablenetUsed to Receive_NThe return value of the function
            var net = _N(account.Balance + account.FrozenBalance + self.orderBook.Bids[0].Price * (account.Stocks + account.FrozenStocks))
            //JudgmentnetWhether not equalself.preNet,If so, execute the statement below
            if (net != self.preNet) {
                //Assignment
                self.preNet = net
                //Call FunctionLogProfitAnd pass innet
                LogProfit(net)
            }
        }
        //Assignment
        self.btc = account.Stocks
        self.cny = account.Balance
        self.p = self.btc * self.prices[self.prices.length - 1] / (self.btc * self.prices[self.prices.length - 1] + self.cny)
        var balanced = false
        //Judgmentself.pWhether the value is less than0.48
        if (self.p < 0.48) {
            //CallLogFunction and pass in parameters"Start balancing", self.p
            Log("Start balancing", self.p)
            //self.cny =self.cny-300
            self.cny -= 300
            //Judgmentself.orderBook.Bidswhether the length is greater than0,If so, execute the statement below
            if (self.orderBook.Bids.length > 0) {
                //CallbuyFunction and pass in the corresponding parameters
                exchange.Buy(self.orderBook.Bids[0].Price + 0.00, 0.01)
                exchange.Buy(self.orderBook.Bids[0].Price + 0.01, 0.01)
                exchange.Buy(self.orderBook.Bids[0].Price + 0.02, 0.01)
            }
            //Ifself.pGreater than0.52Then execute the following statement
        } else if (self.p > 0.52) {
            //CallLogFunction and pass in parameters"Start balancing", self.p
            Log("Start balancing", self.p)
            //self.btc=self.btc-0.03
            self.btc -= 0.03
            //Judgmentself.orderBook.Bidswhether the length is greater than0,If so, execute the statement below
            if (self.orderBook.Asks.length > 0) {
                //CallSellFunction and pass in the corresponding parameters
                exchange.Sell(self.orderBook.Asks[0].Price - 0.00, 0.01)
                exchange.Sell(self.orderBook.Asks[0].Price - 0.01, 0.01)
                exchange.Sell(self.orderBook.Asks[0].Price - 0.02, 0.01)
            }
        }
        //Call FunctionSleepAnd pass parametersBalanceTimeout
        Sleep(BalanceTimeout)
        //Create ScalarorderTo receiveGetOrdersThe value returned by the function
        var orders = exchange.GetOrders()
        //JudgmentordersIs True
        if (orders) {
            //Iterateorders
            for (var i = 0; i < orders.length; i++) {
                //JudgmentordersofidWhether not equalself.tradeOrderId
                if (orders[i].Id != self.tradeOrderId) {
                    //If it is, then callCancelOrderFunction and pass in parametersorders[i].Id
                    exchange.CancelOrder(orders[i].Id)
                }
            }
        }
    }

    //selfA method of <<#1#>>
    self.poll = function () {
        //self.numTickAdded by itself1
        self.numTick++
        //Execute the three methods created aboveupdateTrades,updateOrderBook,updateOrderBook
        self.updateTrades()
        self.updateOrderBook()
        self.balanceAccount()
        //burstPriceValue Equalsself.pricesThe last value of the array is multipliedBurstThresholdPct
        var burstPrice = self.prices[self.prices.length - 1] * BurstThresholdPct
        //Create a variable and assign a value
        var bull = false
        var bear = false
        var tradeAmount = 0
        //Judgmentself.accountIs True
        if (self.account) {
            //If true, then callLogStatusFunction and pass in the corresponding parameters
            LogStatus(self.account, 'Tick:', self.numTick, ', lastPrice:', self.prices[self.prices.length - 1], ', burstPrice: ', burstPrice)
        }
        //The first half is a condition checkself.numTickWhether the value is greater than2,If it is greater than2Then Execute||The following statement, if not then judge&&The statement after the operator, iffalesReturn Directlyfales,ExecuteelseSentence of
        if (self.numTick > 2 && (
            self.prices[self.prices.length - 1] - _.max(self.prices.slice(-6, -1)) > burstPrice ||
            self.prices[self.prices.length - 1] - _.max(self.prices.slice(-6, -2)) > burstPrice && self.prices[self.prices.length - 1] > self.prices[self.prices.length - 2]
        )) {
            //VariablesbullAssign value astrue,tradeAmountAssign value asself.cnyv/self.bidPriceMultiply by0.99
            bull = true
            tradeAmount = self.cny / self.bidPrice * 0.99
        }
        //Same as aboveif
        else if (self.numTick > 2 && (
            self.prices[self.prices.length - 1] - _.min(self.prices.slice(-6, -1)) < -burstPrice ||
            self.prices[self.prices.length - 1] - _.min(self.prices.slice(-6, -2)) < -burstPrice && self.prices[self.prices.length - 1] < self.prices[self.prices.length - 2]
        )) {
            bear = true
            //Assignment
            tradeAmount = self.btc
        }
        //Judgmentself.volIs Less ThanBurstThresholdVol,If it is, then executeifCode within the statement
        if (self.vol < BurstThresholdVol) {
            tradeAmount *= self.vol / BurstThresholdVol
        }
        //Judgmentself.numTickIs Less Than5,If it is, then executeifCode within the statement
        if (self.numTick < 5) {
            //tradeAmount=tradeAmount*0.8
            tradeAmount *= 0.8
        }
        //Judgmentself.numTickIs Less Than10
        if (self.numTick < 10) {
            tradeAmount *= 0.8
        }
        //The first half is a condition check!bulland!bearWhich one is true, the latter part is a judgmenttradeAmountIs Less ThanMinStock,Execute when both sides are trueifCode within the statement
        if ((!bull && !bear) || tradeAmount < MinStock) {
            return
        }
        //IfbullReturn if trueself.bidPriceThe value, otherwise returnself.askPricevalue
        var tradePrice = bull ? self.bidPrice : self.askPrice
        //tradeAmountWhether greater than or equal toMinStock,If yes, then loopwhileSentence of
        while (tradeAmount >= MinStock) {
            //whenbullReturn when trueBuyThe return value of the function, otherwise returnSellThe return value of the function
            var orderId = bull ? exchange.Buy(self.bidPrice, tradeAmount) : exchange.Sell(self.askPrice, tradeAmount)
            //CallSleepParameters passed to the function400,0.4Seconds Execute
            Sleep(400)
            //JudgmentorderIdIs ittrue
            if (orderId) {
                //Assignment
                self.tradeOrderId = orderId
                //Assignment
                var order = null
                while (true) {
                    //rderValue EqualsGetOrderThe return value of the function
                    order = exchange.GetOrder(orderId)
                    //JudgmentorderIs ittrue
                    if (order) {
                        //Check whether the values on both sides are equal
                        if (order.Status == ORDER_STATE_PENDING) {
                            //CallCancelOrderFunction
                            exchange.CancelOrder(orderId)
                            //0.2Seconds Execute
                            Sleep(200)
                        } else {
                            //Break loop
                            break
                        }
                    }
                }
                //Assignment
                self.tradeOrderId = 0
                tradeAmount -= order.DealAmount
                tradeAmount *= 0.9
                //Check if both sides are equal
                if (order.Status == ORDER_STATE_CANCELED) {
                    //CallselfofupdateOrderBookMethod
                    self.updateOrderBook()
                    //Determine whether it istrue,If yes, then loop
                    while (bull && self.bidPrice - tradePrice > 0.1) {
                        //Assignment
                        tradeAmount *= 0.99
                        tradePrice += 0.1
                    }
                    //Determine whether it istrue,If yes, then loop
                    while (bear && self.askPrice - tradePrice < -0.1) {
                        tradeAmount *= 0.99
                        tradePrice -= 0.1
                    }
                }
            }
        }
        //Assignment
        self.numTick = 0
    }
    //Returnself
    return self
}

//Functionmain
function main() {
    //reaper Is Instance of Constructor
    var reaper = LeeksReaper()
    while (true) {
        //Call through instancepollMethod
        reaper.poll()
        Sleep(TickInterval)
    }
}
```

> Detail

https://www.fmz.com/strategy/124178

> Last Modified

2018-10-31 13:43:19
