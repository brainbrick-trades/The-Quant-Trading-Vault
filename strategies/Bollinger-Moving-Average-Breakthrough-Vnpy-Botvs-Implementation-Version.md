
> Name

Bollinger-Moving-Average-Breakthrough-Vnpy-Botvs-Implementation-Version

> Author

ipqhjjybj

> Strategy Description

This is a simple encapsulation of the botvs' interface using VNPY to facilitate later calls!
           This was originally a futures strategy; just modify the parameters directly to apply to Bitcoin.
           For futures, switch to minute-level, for Bitcoin futures use hourly level
           Parameters need to be adjusted in live trading.
           If you have any strategy improvements, please communicate with me.   250657661

           bar.minute.hour  Represents hourly level 
           bar.minute.minute  Represents minute level

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|ContractTypeIdx|0|Futures type: This week | Next week | Quarter|
|MarginLevelIdx|0|Leverage size: 10|20|
|LoopInterval|true|Polling interval (seconds)|
|minute_use|12|minute level|


> Source (python)

``` python
'''
Strategy name: BollingBreaker Trend Strategy
Strategy Author: ipqhjjybj
Strategy Description:  
           This is a simple encapsulation of the botvs' interface using VNPY to facilitate later calls!
           This was originally a futures strategy; just modify the parameters directly to apply to Bitcoin.
           For futures, switch to minute-level, for Bitcoin futures use hourly level
           Parameters need to be adjusted in live trading.
           If you have any strategy improvements, please communicate with me.   250657661

           bar.minute.hour  Represents hourly level 
           bar.minute.minute  Represents minute level

           
------------------------------------------------------------------

          Currently only supports Bitcoin OKCOIN futures. To use CTP futures, minor adjustments are needed.

Trend-following strategy
'''
import time
from datetime import datetime
import numpy as np
import talib

EMPTY_STRING = ""
EMPTY_INT = 0
EMPTY_FLOAT = 0.0
EMPTY_UNICODE = u''

DIRECTION_LONG = u'long'
DIRECTION_SHORT = u'short'

OFFSET_OPEN = u'kaicang'
OFFSET_CLOSE = u'pingcang'

# CTATypes of trading directions involved in the engine
CTAORDER_BUY = "buy"
CTAORDER_SELL = "closebuy"
CTAORDER_SHORT = "sell"
CTAORDER_COVER = "closesell"


# Local stop order status
STOPORDER_WAITING = u'waiting'
STOPORDER_CANCELLED = u'canceled'
STOPORDER_TRIGGERED = u'touched'

# Local stop order prefix
STOPORDERPREFIX = 'CtaStopOrder'



########################################################################
class VtBarData:
    """KLine Data"""

    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        
        self.vtSymbol = EMPTY_STRING        # vtSystem code
        self.symbol = EMPTY_STRING          # code
        self.exchange = EMPTY_STRING        # exchange
    
        self.open = EMPTY_FLOAT             # OHLC
        self.high = EMPTY_FLOAT
        self.low = EMPTY_FLOAT
        self.close = EMPTY_FLOAT
        
        self.date = EMPTY_STRING            # barStart time, date
        self.time = EMPTY_STRING            # Time
        self.datetime = None                # pythondatetime object
        
        self.volume = EMPTY_INT             # Trading volume
        self.openInterest = EMPTY_INT       # Position    

########################################################################
class VtTickData:
    """TickMarket data class"""

    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        
        # Code related
        self.exchange = EMPTY_STRING            # Exchange code
        self.vtSymbol = EMPTY_STRING            # The unique code of the contract in the VT system, usually in the format contract code.exchange code.
        
        # Transaction data
        self.lastPrice = EMPTY_FLOAT            # Latest transaction price
        self.lastVolume = EMPTY_INT             # Latest Trading Volume
        self.volume = EMPTY_INT                 # Today's total trading volume
        self.openInterest = EMPTY_INT           # Position
        self.time = EMPTY_STRING                # Time 11:20:56.5
        self.date = EMPTY_STRING                # Date 20151009
        self.datetime = None                    # pythondatetime object
        
        # Regular Quotes
        self.openPrice = EMPTY_FLOAT            # Today's opening price
        self.highPrice = EMPTY_FLOAT            # Today's highest price
        self.lowPrice = EMPTY_FLOAT             # Today's Lowest Price
        self.preClosePrice = EMPTY_FLOAT
        
        self.upperLimit = EMPTY_FLOAT           # Price limit
        self.lowerLimit = EMPTY_FLOAT           # Lower limit price
        
        # Five levels of market conditions
        self.bidPrice1 = EMPTY_FLOAT
        self.bidPrice2 = EMPTY_FLOAT
        self.bidPrice3 = EMPTY_FLOAT
        self.bidPrice4 = EMPTY_FLOAT
        self.bidPrice5 = EMPTY_FLOAT
        
        self.askPrice1 = EMPTY_FLOAT
        self.askPrice2 = EMPTY_FLOAT
        self.askPrice3 = EMPTY_FLOAT
        self.askPrice4 = EMPTY_FLOAT
        self.askPrice5 = EMPTY_FLOAT        
        
        self.bidVolume1 = EMPTY_INT
        self.bidVolume2 = EMPTY_INT
        self.bidVolume3 = EMPTY_INT
        self.bidVolume4 = EMPTY_INT
        self.bidVolume5 = EMPTY_INT
        
        self.askVolume1 = EMPTY_INT
        self.askVolume2 = EMPTY_INT
        self.askVolume3 = EMPTY_INT
        self.askVolume4 = EMPTY_INT
        self.askVolume5 = EMPTY_INT         


########################################################################
class StopOrder(object):
    """Local Stop Order"""

    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        self.vtSymbol = EMPTY_STRING
        self.orderType = EMPTY_UNICODE
        self.direction = EMPTY_UNICODE
        self.offset = EMPTY_UNICODE
        self.price = EMPTY_FLOAT
        self.volume = EMPTY_INT
        
        self.strategy = None             # Strategy object for placing stop orders
        self.stopOrderID = EMPTY_STRING  # Local number of the stop order 
        self.status = EMPTY_STRING       # Stop Order Status


class BollingerBreakerStrategy:
    #Variety attributes
    vtSymbol = EMPTY_STRING # What Kind of Product

    # Strategy Arguments
    minute_use = 6              # candlestick of how many minutes

    bar = None                  # 1Minute candlestick object
    fiveBar = None              # 1Minute candlestick object

    # Strategy Arguments
    bollLength = 20         # Number of Channel Windows
    topDev = 1.3            # Position opening deviation
    trailingPrcnt = 2       # Trailing stop percentage
    use_range = 10          # use_rangeBreak the highest price within the day
    N = 10                  # Number of Days to Breakthrough

    bufferSize = 40                     # Size of the data that needs to be cached
    bufferCount = 0                     # Count of data currently cached


    realBuyCond = 0                     # Buy/Sell Status
    realSellCond = 0                    # Buy/Sell Status
    
    bollMid = 0                         # Bollinger Bands Middle Line
    bollStd = 0                         # Bollinger Band Width
    entryUp = 0                         # Open a position and hit the track

    barMinute = EMPTY_STRING            # KCurrent minute of the line

    fixedSize = 1

    stopOrderCount = 0                  # Record the number of stop orders

    pos = 0                             # position

    LastBarTime = None                  # python Previous candleTick

    currency = EMPTY_STRING

    def __init__(self, _exchange , setting ):
        self.exchange = _exchange
        for key in setting.keys():
            if key == "vtSymbol":
                self.vtSymbol = setting[key]
            if key == "currency":
                self.currency = setting[key]
            if key == 'minute_use':
                self.minute_use = setting[key]
            if key == "bollLength":
                self.bollLength = setting[key]
            if key == "topDev":
                self.topDev = setting[key]
            if key == "trailingPrcnt":
                self.trailingPrcnt = setting[key]
            if key == "use_range":
                self.use_range = setting[key]
            if key == "N":
                self.N = setting[key]
        Log(setting)

        self.pos = 0
        self.order_PreUse = {}            # vtPreID , pushDealAmount  Transaction data that has already been pushed
        self.workingStopOrderDict = {}
        self.stopOrderDict = {}
        self.orderList = []               # Save the list of order codes
        self.fixedSize = 1
        ##################
        self.bufferSize = 40
        #################
        self.highArray = np.zeros(self.bufferSize) 
        self.lowArray = np.zeros(self.bufferSize)
        self.closeArray = np.zeros(self.bufferSize)
        
        self.buyValue = np.zeros(self.bufferSize)


    def onCall(self):
        try:
            #self.exchange.IO("currency" , self.currency)
            need_remove = []
            for orderId in self.orderList:
                # Order status, refer to the order status in the constants; below are the constants for this key.
                # ORDER_STATE_PENDING  :not completed
                # ORDER_STATE_CLOSED   :Closed Completed
                # ORDER_STATE_CANCELED :canceled
                # STOPORDERPREFIX Whether it is an internal system stop order
                if orderId != None and type(orderId) != type(1) and STOPORDERPREFIX in orderId:
                    continue
                botvsOrder = self.exchange.GetOrder(orderId)
                preAmount = 0.0
                if botvsOrder != None:
                    if botvsOrder["Status"] in [ORDER_STATE_CLOSED,ORDER_STATE_CANCELED]:
                        try:
                            preAmount = self.order_PreUse[orderId]
                        except Exception,ex:
                            Log("Error in preAmount",ex)
                            preAmount = 0.0
                        Log("preAmount:" , preAmount)
                        incAmount = botvsOrder["DealAmount"] - preAmount
                        if incAmount > 0:
                            self.order_PreUse[orderId] = botvsOrder["DealAmount"]
                            botvsOrder["preAmount"] = preAmount
                            botvsOrder["incAmount"] = incAmount
                            self.onTrade( botvsOrder )


                    if botvsOrder["Status"] == ORDER_STATE_CLOSED:
                        need_remove.append(orderId)
                else:
                    Log("None order!")

            for orderId in need_remove:
                Log("remove order:" , orderId)
                self.orderList.remove(orderId)

            
            # Log("currency",self.currency)
            botvsTick = self.exchange.GetTicker()


            if self.LastBarTime != botvsTick["Time"]:
                newTick = VtTickData()
                newTick.datetime = datetime.fromtimestamp(botvsTick["Time"] / 1000.0)
                newTick.vtSymbol = self.vtSymbol
                newTick.lastPrice = float(botvsTick["Last"])
                newTick.lastVolume = float(botvsTick["Volume"])
                newTick.volume = float(botvsTick["Volume"])
                newTick.highPrice = float(botvsTick["High"])
                newTick.lowPrice = float(botvsTick["Low"])

                newTick.upperLimit = newTick.highPrice * 1.03
                newTick.lowerLimit = newTick.lowPrice * 0.97

                newTick.exchange = self.exchange.GetName()

                newTick.date = newTick.datetime.strftime("%Y%m%d")
                newTick.time = newTick.datetime.strftime("%Y:%m:%d")

                self.onTick(newTick)

                self.processStopOrder(newTick)
        except Exception,ex:
            Log(ex , "error in onCall , maybe getTicker wrong!")

    #----------------------------------------------------------------------
    def onTrade(self, trade):
        # Send a status update event
        #'Type': 0           # Order type, refer to the order type in the constants; below are the constants for this key.
                             # ORDER_TYPE_BUY   :Buy Order
                             # ORDER_TYPE_SELL  :Sell Order
        try:
            Log("trade:",trade)
            newPos = 0.0
            if trade["Type"] == ORDER_TYPE_BUY:
                newPos += trade["incAmount"]
            elif trade["Type"] == ORDER_TYPE_SELL:
                newPos -= trade["incAmount"]
            else:
                Log("What ? trade Type error!")
            self.pos += newPos
        except Exception,ex:
            print ex
    #----------------------------------------------------------------------
    def processStopOrder(self, tick):
        """Process the local stop order after receiving the market price (check whether to issue it immediately)"""
        vtSymbol = tick.vtSymbol
        
        # Traverse pending stop orders and check if they will be triggered
        for so in self.workingStopOrderDict.values():
            if so.vtSymbol == vtSymbol:
                longTriggered = so.direction==DIRECTION_LONG and tick.lastPrice>=so.price        # Long stop order triggered
                shortTriggered = so.direction==DIRECTION_SHORT and tick.lastPrice<=so.price     # Short stop order triggered
                
                if longTriggered or shortTriggered:
                    # Buy and sell orders are issued at the upper limit and lower limit prices respectively (simulated market orders)
                    if so.direction==DIRECTION_LONG:
                        price = tick.upperLimit
                    else:
                        price = tick.lowerLimit
                    
                    so.status = STOPORDER_TRIGGERED
                    orderIDList = self.sendOrder(so.vtSymbol, so.orderType, price, so.volume, False ,so.strategy)
                    for orderID in orderIDList:
                        self.orderList.append(orderID)
                    del self.workingStopOrderDict[so.stopOrderID]
                    so.strategy.onStopOrder(so)

    def onStopOrder(self, vtStopOrder):
        Log("stopOrder Deal ID:", vtStopOrder.stopOrderID , vtStopOrder.status )

    def sendStopOrder(self, vtSymbol, orderType, price, volume, strategy ):
        """Issue stop order (local implementation))"""
        self.stopOrderCount += 1
        stopOrderID = STOPORDERPREFIX + str(self.vtSymbol) + str(self.stopOrderCount)

        so = StopOrder()
        so.vtSymbol = vtSymbol
        so.orderType = orderType
        so.price = price
        so.volume = volume
        so.strategy = strategy
        so.stopOrderID = stopOrderID
        so.status = STOPORDER_WAITING

        if orderType == CTAORDER_BUY:
            so.direction = DIRECTION_LONG
            so.offset = OFFSET_OPEN
        elif orderType == CTAORDER_SELL:
            so.direction = DIRECTION_SHORT
            so.offset = OFFSET_CLOSE
        elif orderType == CTAORDER_SHORT:
            so.direction = DIRECTION_SHORT
            so.offset = OFFSET_OPEN
        elif orderType == CTAORDER_COVER:
            so.direction = DIRECTION_LONG
            so.offset = OFFSET_CLOSE      

        # Save the stopOrder object into the dictionary
        self.stopOrderDict[stopOrderID] = so
        self.workingStopOrderDict[stopOrderID] = so
        
        # Push stop order status
        strategy.onStopOrder(so)
        return stopOrderID

    def sendOrder(self , vtSymbol , orderType , price, volume , stop , strategy ):
        #   id1 = exchange.Buy(4300,1)     # Date Platform Type Price Quantity Information
        #                                  # 2016-10-21 00:00:00  OKCoin  buy  4300     1
        #   id2 = exchange.Buy(-1, 8000)   # The meaning of the second parameter of the market order is the number of coins purchased with an amount of 8000.
        #   id1 = exchange.Sell(4300,1)    #     Date Platform Type Price Quantity Information
        #                                  #     2016-10-21 00:00:00     OKCoin      Sell Market order     1    
        # id2 = exchange.Sell(-1, 1)       #     Date Platform Type Price Quantity Information
                                           #     2016-10-21 00:00:00     OKCoin      sell      4300      1
                                           # Common error prompt: Smaller than the allowed minimum trading unit, most of the time the reason is this (Parameter 1 is 1 RMB instead of 1 coin).).
        if stop == True:
            vtOrderID = self.sendStopOrder(self.vtSymbol, orderType, price, volume, self)
            return vtOrderID
        else:
            ret_order_list = []
            self.exchange.SetDirection( orderType )
            if orderType in [ CTAORDER_BUY , CTAORDER_COVER]:
                ret_order_list.append( self.exchange.Buy( price , volume ))
            elif orderType in [CTAORDER_SELL , CTAORDER_SHORT]:
                ret_order_list.append( self.exchange.Sell( price , volume ))
            return ret_order_list

    def buy(self , price , volume , stop = False):
        Log(CTAORDER_BUY,price,volume)
        return self.sendOrder( self.vtSymbol , CTAORDER_BUY , price , volume , stop , self)
    def sell(self , price , volume , stop = False):
        Log(CTAORDER_SELL,price,volume)
        return self.sendOrder( self.vtSymbol , CTAORDER_SELL , price , volume , stop , self)
    def short(self , price , volume , stop = False):
        Log(CTAORDER_SELL,price,volume)
        return self.sendOrder( self.vtSymbol , CTAORDER_SHORT , price , volume , stop , self)
    def cover(self , price , volume , stop = False):
        Log("cover",price,volume)
        return self.sendOrder( self.vtSymbol , CTAORDER_COVER , price , volume , stop , self)

    #----------------------------------------------------------------------
    def cancelStopOrder(self, stopOrderID):
        """Cancel Stop Order"""
        # Check if the stop order exists
        if stopOrderID in self.workingStopOrderDict:
            so = self.workingStopOrderDict[stopOrderID]
            so.status = STOPORDER_CANCELLED
            del self.workingStopOrderDict[stopOrderID]
            so.strategy.onStopOrder(so)

        if stopOrderID in self.orderList:
            self.orderList.remove(stopOrderID)

    def cancelOrder(self , vtOrderId):
        Log("cancelOrder:",vtOrderId)
        if STOPORDERPREFIX in vtOrderId:
            self.cancelStopOrder(vtOrderId)
        else:
            self.exchange.CancelOrder(vtOrderId)

    def onTick(self, tick):

        # self.orderList = []
        # orderIDList = self.buy(tick.lastPrice , abs(self.fixedSize))
        # #Log( str(self.vtSymbol) + " cover 0 1 " + str(self.fixedSize) +" " +str(','.join(orderIDList))  + "\n")
        # #print str(self.vtSymbol) , "cover 0 1" , self.fixedSize , orderID
        # for orderID in orderIDList:
        #     self.orderList.append(orderID)

        # Aggregate into 1-minute candlestick
        tickMinute = tick.datetime.hour

        if tickMinute != self.barMinute:  
            if self.bar:
                self.onBar(self.bar)

            bar = VtBarData()              
            bar.vtSymbol = tick.vtSymbol
            bar.exchange = tick.exchange

            bar.open = tick.lastPrice
            bar.high = tick.lastPrice
            bar.low = tick.lastPrice
            bar.close = tick.lastPrice

            bar.date = tick.date
            bar.time = tick.time
            bar.datetime = tick.datetime    # KSet the line's time to the time of the first tick

            self.bar = bar                  # This way of writing is to reduce one layer of access and speed up
            self.barMinute = tickMinute     # Update the current minute
        else:                               # Otherwise, continue to accumulate new candlesticks
            bar = self.bar                  # The writing style is also to speed up

            bar.high = max(bar.high, tick.lastPrice)
            bar.low = min(bar.low, tick.lastPrice)
            bar.close = tick.lastPrice

    def onBar(self , bar):
        
        if bar.datetime.hour  % self.minute_use == 0:         # bar.datetime.minute Then switch to minute level
            # If there is already an aggregated 5-minute candlestick
            if self.fiveBar:
                # Update the latest minute data into the current 5-minute chart
                fiveBar = self.fiveBar
                fiveBar.high = max(fiveBar.high, bar.high)
                fiveBar.low = min(fiveBar.low, bar.low)
                fiveBar.close = bar.close
                
                # Push 5-minute candlestick data
                self.onFiveBar(fiveBar)
                
                # Clear 5-minute line data cache
                self.fiveBar = None
        else:
            # Create a new one if not cached
            if not self.fiveBar:
                fiveBar = VtBarData()
                
                fiveBar.vtSymbol = bar.vtSymbol
                fiveBar.symbol = bar.symbol
                fiveBar.exchange = bar.exchange
            
                fiveBar.open = bar.open
                fiveBar.high = bar.high
                fiveBar.low = bar.low
                fiveBar.close = bar.close
            
                fiveBar.date = bar.date
                fiveBar.time = bar.time
                fiveBar.datetime = bar.datetime 
                
                self.fiveBar = fiveBar
            else:
                fiveBar = self.fiveBar
                fiveBar.high = max(fiveBar.high, bar.high)
                fiveBar.low = min(fiveBar.low, bar.low)
                fiveBar.close = bar.close


    def onFiveBar(self , bar):
        #Log( self.currency , bar.close , self.pos , self.orderList)

        for orderID in self.orderList:
            self.cancelOrder(orderID)
        self.orderList = []
    
        # Save candlestick data
        self.closeArray[0:self.bufferSize-1] = self.closeArray[1:self.bufferSize]
        self.highArray[0:self.bufferSize-1] = self.highArray[1:self.bufferSize]
        self.lowArray[0:self.bufferSize-1] = self.lowArray[1:self.bufferSize]
        self.buyValue[0:self.bufferSize-1] = self.buyValue[1:self.bufferSize]

        self.closeArray[-1] = bar.close
        self.highArray[-1] = bar.high
        self.lowArray[-1] = bar.low
    
        # Calculate indicator values
        self.bollMid = talib.MA(self.closeArray, self.bollLength)[-1]
        self.bollStd = talib.STDDEV(self.closeArray, self.bollLength)[-1]
        self.entryUp = self.bollMid + self.bollStd * self.topDev

        self.buyValue[-1] = self.entryUp

        self.bufferCount += 1
        if self.bufferCount < self.bufferSize:
            return

        # Determine whether to trade
        cond1 = 0
        for i in range(1 , self.use_range + 1):
            if self.highArray[-i] > self.buyValue[-i]:
                cond1 = 1
        cond2 = 0

        # newHigh = [float(x) for x in self.highArray]
        # if bar.high >= max(newHigh[-self.N : ]) and self.highArray[-2] >= max(newHigh[-self.N-1 : -1]):
        #     cond2 = 1
        if self.pos == 0 and cond1 > 0:
            self.intraTradeHigh = bar.high
            newHigh = [float(x) for x in self.highArray]
            entryBuyPrice = max(newHigh[-self.N:])
            orderID = self.buy( entryBuyPrice, self.fixedSize , stop=True)
            self.orderList.append(orderID)

        elif self.pos > 0:
            self.intraTradeHigh = max(bar.high , self.intraTradeHigh)
            exitPrice = self.intraTradeHigh * (1 - self.trailingPrcnt / 100.0) 
            orderID = self.sell( exitPrice , self.fixedSize , stop=True)
            self.orderList.append(orderID)

'''
bollLength = 20         # Number of Channel Windows
topDev = 1.3            # Position opening deviation
trailingPrcnt = 2       # Trailing stop percentage
use_range = 10          # use_rangeBreak the highest price within the day
N = 10                  # Number of Days to Breakthrough
'''
running_key = {
    "BTC":{ "bollLength":20 , "topDev":1.3 , "trailingPrcnt": 2 , "use_range": 10 , "N":10 , "minute_use": 6},
    "LTC":{ "bollLength":20 , "topDev":1.3 , "trailingPrcnt": 2 , "use_range": 10 , "N":10 , "minute_use": 6}
}

def main():
    global LoopInterval 

    objs = []
    for e in exchanges:
        if e.GetName() != 'Futures_OKCoin':
            raise Error_noSupport
        e.SetRate(1)
        use_symbol = ["this_week","next_week","quarter"][ContractTypeIdx]
        e.SetContractType(use_symbol) 
        e.SetMarginLevel([10,20][MarginLevelIdx])

        e_currency = e.GetCurrency().upper()
        Log(e_currency)
        st = BollingerBreakerStrategy(e , {
        "vtSymbol":e.GetName() + "_" + use_symbol + "_" + e.GetCurrency(), 
        "currency":e_currency,
        "minute_use":running_key[e_currency]["minute_use"],
        "bollLength":running_key[e_currency]["bollLength"],
        "topDev": running_key[e_currency]["topDev"],
        "trailingPrcnt": running_key[e_currency]["trailingPrcnt"],
        "use_range": running_key[e_currency]["use_range"],
        "N": running_key[e_currency]["N"]
        })

        objs.append(st)

    while True:
        for st in objs:
            st.onCall()
        Sleep(LoopInterval * 1000)
```

> Detail

https://www.fmz.com/strategy/52801

> Last Modified

2017-09-10 21:35:41
