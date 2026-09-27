
> Name

Ported-OKCoin-Leek-Harvester-Commented-Python-Version

> Author

去者伯仁



> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|BurstThresholdPct|5e-05|burst.threshold.pct|
|BurstThresholdVol|10|burst.threshold.vol|
|MinStock|0.1|Minimum transaction volume|
|CalcNetInterval|60|Net value calculation period (seconds)|
|BalanceTimeout|10000|Balance waiting time (milliseconds))|
|TickInterval|280|polling cycle (milliseconds))|


> Source (python)

``` python
'''backtest
start: 2019-09-05 00:00:00
end: 2019-09-05 22:00:00
period: 1h
basePeriod: 1h
exchanges: [{"eid":"Binance","currency":"BTC_USDT","stocks":0,"fee":[0,0]}]
mode: 1
'''

import time
class LeeksReaper():  
    def __init__(self):                                      #Create constructorLeeksReaper                                          #Construct an empty object
        self.numTick = 0
        self.lastTradeId = 0
        self.vol = 0
        self.askPrice = 0
        self.bidPrice = 0
        self.orderBook = {}
        self.prices = []
        self.tradeOrderId = 0
        self.p = 0.5
        self.account = None
        self.preCalc = 0
        self.preNet = 0

        self.sgnum = 0
        # self.cny = 0
        # self.btc = 0
        #All of the aboveselfobject properties

    #Create a method
    def updateTrades(self):

        trades = _C(exchange.GetTrades)                     #Create a variabletradesUsed to Receive_CValue returned by the function, the passed-in parameters are:exchange.GetTrades
        if (len(self.prices)== 0):                       #Ifself.pricesLength equals0
            while (len(trades) == 0):                      #IftradesEqual to0Execute the following statement when
                trades = _C(exchange.GetTrades) #Use array concatenation methods to_Cthe value returned by the function andtradesPerform concatenation, passing in the parameter as:exchange.GetTrades

            for i in range(15):                      #Loop, ending condition is i=15, increase i by 1 each loop1
                self.prices.append(trades[-1].Price)#In each looptradesAssign the last value of the array toselfOf the objectpriceson the array, looped together15times

        tradesvol = 0
        for trade in trades:
            if ((trade.Id > self.lastTradeId) or (trade.Id == 0 and trade.Time > self.lastTradeId)):
                #The right side of the equal sign is a ternary operation, iftrade.Id=0Just returntrade.Time,Otherwise returntrade.Id, self.lastTradeId.And compared to return the maximum value, finally assign the returned maximum value toself.lastTradeId
                temp = trade.Time if trade.Id == 0 else trade.Id
                self.lastTradeId = max(temp, self.lastTradeId)
                tradesvol = tradesvol + trade.Amount


        #self.volThe value equals itself multiplied by 0.7 plus the trading volume during this period*0.3
        self.vol = 0.7 * self.vol + 0.3 * tradesvol


    #selfa method of the object
    def updateOrderBook(self):

        # Create a variable orderBook to receive values returned by _C functions, passing in the following parameters:exchange.GetDepth
        orderBook = _C(exchange.GetDepth)
        self.orderBook = orderBook                              #self.orderBook Value EqualsorderBook
        if (len(orderBook.Bids)< 3 or len(orderBook.Asks) < 3):#The first half is a condition checkorderBook.Bidswhether the length is less than3,The second half is a condition checkorderBook.Askswhether the length is less than3,if both sides are less than3Then execute the following statement
            #Returnundefined
            return
        
        #self.bidPriceThe value equals the first value of the orderBook.Bids array multiplied by 0.618 plus the first value of the orderBook.Asks array multiplied by 0.382 plus0.01
        self.bidPrice = orderBook.Bids[0].Price * 0.618 + orderBook.Asks[0].Price * 0.382 + 0.01
        #Same as above
        self.askPrice = orderBook.Bids[0].Price * 0.382 + orderBook.Asks[0].Price * 0.618 - 0.01
        #DeletepriceThe first value of the array and returns the first value
        del(self.prices[0])
        #pricesAdd value to the end of the array; the value is the return of function _N
        self.prices.append(_N((orderBook.Bids[0].Price + orderBook.Asks[0].Price) * 0.35 +
            (orderBook.Bids[1].Price + orderBook.Asks[1].Price) * 0.1 +
            (orderBook.Bids[2].Price + orderBook.Asks[2].Price) * 0.05))

    #selfa method of the object
    def balanceAccount(self):
        # Create a variable `account` to receive the value returned by the GetAccount function.
        account = _C(exchange.GetAccount)
        #JudgmentaccountCheck if empty, if so returnundefined
        if account is None:
            return

        #Assignment
        self.account = account
        #Get the timestamp data of the current time
        now = time.time()
        #Judgmentself.orderBook.Bidswhether the length is greater than0andnow - self.preCalcWhether the value is greater than(CalcNetInterval * 1000),Execute the following statement if all are greater
        if (len(self.orderBook.Bids) > 0 and now - self.preCalc > (CalcNetInterval)):
            #Assignment
            self.preCalc = now
            #Create a variablenetUsed to Receive_NThe return value of the function
            net = _N(account.Balance + account.FrozenBalance + self.orderBook.Bids[0].Price * (account.Stocks + account.FrozenStocks))
            #JudgmentnetWhether not equalself.preNet,If so, execute the statement below
            if (net != self.preNet):
                #Assignment
                self.preNet = net
                #Call FunctionLogProfitAnd pass innet
                LogProfit(net-10000)

        #Assignment
        self.btc = account.Stocks
        self.cny = account.Balance
        self.p = self.btc * self.prices[-1] / (self.btc * self.prices[-1] + self.cny)
        balanced = False
        #Judgmentself.pWhether the value is less than0.48
        # Log(self.p)
        if (self.p < 0.48):
            #CallLogFunction and pass in parameters"Start balancing", self.p
            Log("Start balancing", self.p)
            #self.cny =self.cny-300
            self.cny -= 300
            #Judgmentself.orderBook.Bidswhether the length is greater than0,If so, execute the statement below
            if (len(self.orderBook.Bids) > 0):
                #CallbuyFunction and pass in the corresponding parameters
                exchange.Buy(self.orderBook.Bids[0].Price + 0.00, 0.01)
                exchange.Buy(self.orderBook.Bids[0].Price + 0.01, 0.01)
                exchange.Buy(self.orderBook.Bids[0].Price + 0.02, 0.01)

                Log("Number of Coins Held:",self.btc,"Amount of Cash:",self.cny)

            #Ifself.pGreater than0.52Then execute the following statement
        elif (self.p > 0.52):
            #CallLogFunction and pass in parameters"Start balancing", self.p
            Log("Start balancing", self.p)
            #self.btc=self.btc-0.03
            self.btc -= 0.03
            #Judgmentself.orderBook.Bidswhether the length is greater than0,If so, execute the statement below
            if (len(self.orderBook.Asks) > 0):
                #CallSellFunction and pass in the corresponding parameters
                exchange.Sell(self.orderBook.Asks[0].Price - 0.00, 0.01)
                exchange.Sell(self.orderBook.Asks[0].Price - 0.01, 0.01)
                exchange.Sell(self.orderBook.Asks[0].Price - 0.02, 0.01)

                Log("Number of Coins Held:",self.btc,"Amount of Cash:",self.cny)

        #Call FunctionSleepAnd pass parametersBalanceTimeout
        Sleep(BalanceTimeout)
        #Create ScalarorderTo receiveGetOrdersThe value returned by the function
        orders = _C(exchange.GetOrders)
        #JudgmentordersIs True
        if (orders):
            #Iterateorders
            Log(orders)
            for i in range(len(orders)):
                #JudgmentordersofidWhether not equalself.tradeOrderId
                if (orders[i].Id != self.tradeOrderId):
                    #If it is, then callCancelOrderFunction and pass in parametersorders[i].Id
                    Log(orders[i].Id)
                    exchange.CancelOrder(orders[i].Id)





    #selfA method of <<#1#>>
    def poll(self):

        #self.numTickAdded by itself1
        self.numTick +=1
        #Execute the three methods created aboveupdateTrades,updateOrderBook,updateOrderBook
        self.updateTrades()
        self.updateOrderBook()
        self.balanceAccount()
        #burstPriceThe value equals the last value of the self.prices array multiplied byBurstThresholdPct
        burstPrice = self.prices[-1] * BurstThresholdPct
        #Create a variable and assign a value
        bull = False
        bear = False
        tradeAmount = 0
        #Judgmentself.accountIs True
        if (self.account):
            #If true, then callLogStatusFunction and pass in the corresponding parameters
            LogStatus(self.account, 'Tick:', self.numTick, ', lastPrice:', self.prices[-1], ', burstPrice: ', burstPrice,",Current number of times the harvester has started:",self.sgnum)

        #The first half is a condition checkself.numTickWhether the value is greater than2,If it is greater than2Then Execute||The following statement, if not then judge&&The statement after the operator, iffalesReturn Directlyfales,ExecuteelseSentence of
        if (self.numTick > 2 and (self.prices[-1] - max(self.prices[-6:-1]) > burstPrice or self.prices[-1] - max(self.prices[-6:-2]) > burstPrice and self.prices[-1] > self.prices[-2])):
            #VariablesbullAssign value astrue,tradeAmountAssign value asself.cnyv/self.bidPriceMultiply by0.99
            bull = True
            tradeAmount = self.cny / self.bidPrice * 0.99

        #Same as aboveif
        elif (self.numTick > 2 and (self.prices[-1] - min(self.prices[-6:-1]) < -burstPrice or self.prices[-1] - min(self.prices[-6:-2]) < -burstPrice and self.prices[-1] < self.prices[-2])):
            bear = True
            #Assignment
            tradeAmount = self.btc

        #Judgmentself.volIs Less ThanBurstThresholdVol,If it is, then executeifCode within the statement
        if (self.vol < BurstThresholdVol):
            tradeAmount *= self.vol / BurstThresholdVol

        #Judgmentself.numTickIs Less Than5,If it is, then executeifCode within the statement
        if (self.numTick < 5):
            #tradeAmount=tradeAmount*0.8
            tradeAmount *= 0.8

        #Judgmentself.numTickIs Less Than10
        if (self.numTick < 10):
            tradeAmount *= 0.8

        #The first half is a condition check!bulland!bearWhich one is true, the latter part is a judgmenttradeAmountIs Less ThanMinStock,Execute when both sides are trueifCode within the statement
        if (((not bull) and (not bear)) or tradeAmount < MinStock):
            return

        #IfbullReturn if trueself.bidPriceThe value, otherwise returnself.askPricevalue
        tradePrice = self.bidPrice if bull else self.askPrice
        #tradeAmountCheck whether it is greater than or equal to MinStock; if it is, execute a while loop statement.
        while (tradeAmount >= MinStock):
            #whenbullReturn when trueBuyThe return value of the function, otherwise returnSellThe return value of the function
            orderId = exchange.Buy(self.bidPrice, tradeAmount) if bull else exchange.Sell(self.askPrice, tradeAmount)
            self.sgnum+=1
            Log("Harvester After",self.sgnum,"Next launch")
            #CallSleepParameters passed to the function400,0.4Seconds Execute
            Sleep(400)
            #JudgmentorderIdIs ittrue
            if (orderId):
                #Assignment
                self.tradeOrderId = orderId
                #Assignment
                order = None
                while (True):
                    #rderThe value equals the return value of the GetOrder function
                    order = exchange.GetOrder(orderId)
                    #JudgmentorderIs ittrue
                    if (order):
                        #Check whether the values on both sides are equal
                        if (order.Status == ORDER_STATE_PENDING):
                            #CallCancelOrderFunction
                            exchange.CancelOrder(orderId)
                            #0.2Seconds Execute
                            Sleep(200)
                        else:
                            #Break loop
                            break


                #Assignment
                self.tradeOrderId = 0
                tradeAmount -= order.DealAmount
                tradeAmount *= 0.9
                #Check if both sides are equal
                if (order.Status == ORDER_STATE_CANCELED):
                    #CallselfofupdateOrderBookMethod
                    self.updateOrderBook()
                    #Determine whether it istrue,If yes, then loop
                    while (bull and self.bidPrice - tradePrice > 0.1):
                        #Assignment
                        tradeAmount *= 0.99
                        tradePrice += 0.1

                    #Determine whether it istrue,If yes, then loop
                    while (bear and self.askPrice - tradePrice < -0.1):
                        tradeAmount *= 0.99
                        tradePrice -= 0.1
        #Assignment
        self.numTick = 0




#Functionmain
def main():
    #reaper Is Instance of Constructor
    reaper = LeeksReaper()
    while (True):
        #Call through instancepollMethod
        reaper.poll()
        Sleep(TickInterval)

```

> Detail

https://www.fmz.com/strategy/265827

> Last Modified

2021-04-16 11:34:07
