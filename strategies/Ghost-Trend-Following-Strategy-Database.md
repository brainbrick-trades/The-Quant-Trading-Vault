
> Name

Ghost-Trend-Following-Strategy-Database

> Author

陈皮





> Source (python)

``` python
#!/usr/bin/python
# -*- coding: utf-8 -*-
import time,datetime
import json
from collections import Counter
IFLAGE = 0
class Account(object):
    #Binance account information entity, encapsulates common account information
    #totalWalletBalance:Wallet Balance
    #totalMarginBalance:Margin balance
    #totalPositionInitialMargin:Position margin
    #totalOpenOrderInitialMargin:Current pending order margin
    #availableBalance: Available balance (only calculate USDT assets))
    def __init__(self, totalWalletBalance, totalMarginBalance, totalPositionInitialMargin, totalOpenOrderInitialMargin, availableBalance):
        self.totalWalletBalance = totalWalletBalance
        self.totalMarginBalance = totalMarginBalance
        self.totalPositionInitialMargin = totalPositionInitialMargin
        self.totalOpenOrderInitialMargin = totalOpenOrderInitialMargin 
        self.availableBalance = availableBalance
        
class Position(object):
    #Binance trading pair entity, encapsulates common trading pair information
    #entryPrice:Position cost price
    #leverage:Leverage Ratio
    #liquidationPrice:Forced liquidation price
    #marginType:Isolated margin mode or cross margin mode
    #markPrice:Mark price
    #positionAmt:Position Quantity
    #symbol:trading pair
    #unRealizedProfit:Unrealized P&L of positions
    #positionSide:Position Direction
    def __init__(self, entryPrice, leverage, liquidationPrice, marginType, markPrice, positionAmt, symbol, unRealizedProfit, positionSide):
        self.entryPrice = entryPrice
        self.leverage = leverage
        self.liquidationPrice = liquidationPrice
        self.marginType = marginType 
        self.markPrice = markPrice
        self.positionAmt = positionAmt
        self.symbol = symbol
        self.unRealizedProfit = unRealizedProfit
        self.positionSide = positionSide

class Ticker(object):
    #sell: Sell one price
    #buy: Buy one price
    #last: Last transaction price
    def __init__(self, sell, buy, last):
        self.sell = sell 
        self.buy = buy 
        self.last = last 
        
        
        
class Order(object):
    #id:Order unique identifier 
    #price:Order price 
    #amount:Order quantity 
    #status:Order Status -- 0: Incomplete; 1: Completed; 2: Canceled; 3: Unknown Status.
    def __init__(self, id, price, amount, status):
        self.id = id 
        self.price = price 
        self.amount = amount 
        self.status = status 
        
        
#Get account information        
def GetAccountDao():
    account = _C(exchange.GetAccount)
    assets = account.Info.assets
    busd = {}
    usdt = {}
    for asset in assets:
        symbol = asset["asset"]
        if symbol == "BUSD":
            busd = asset 
        if symbol == "USDT":
            usdt = asset
            
    bTotalWalletBalance = float(busd["walletBalance"])
    bTotalMarginBalance = float(busd["marginBalance"])
    bTotalPositionInitialMargin = float(busd["positionInitialMargin"])
    bTotalOpenOrderInitialMargin = float(busd["openOrderInitialMargin"])
    bAvailableBalance = float(busd["availableBalance"])
    uTotalWalletBalance = float(usdt["walletBalance"])
    uTotalMarginBalance = float(usdt["marginBalance"])
    uTotalPositionInitialMargin = float(usdt["positionInitialMargin"])
    uTotalOpenOrderInitialMargin = float(usdt["openOrderInitialMargin"])
    uAvailableBalance = float(usdt["availableBalance"])
    totalWalletBalance = _N(uTotalWalletBalance+bTotalWalletBalance,2)
    totalMarginBalance = _N(uTotalMarginBalance+bTotalMarginBalance,2)
    totalPositionInitialMargin = _N(uTotalPositionInitialMargin+bTotalPositionInitialMargin,2)
    totalOpenOrderInitialMargin = _N(uTotalOpenOrderInitialMargin+bTotalOpenOrderInitialMargin,2)
    availableBalance = _N(uAvailableBalance+bAvailableBalance,2)
    account = Account(totalWalletBalance, totalMarginBalance, totalPositionInitialMargin, totalOpenOrderInitialMargin, availableBalance)
    return account

#Get all trading pairs of the account
def GetPositionsDao():
    positions = [] 
    num2 = _G("num2")
    for i in _C(exchange.GetPosition):
        entryPrice = _N(float(i.Info.entryPrice),num2)
        leverage = i.Info.leverage 
        liquidationPrice = _N(float(i.Info.liquidationPrice),num2)
        marginType = i.Info.marginType 
        markPrice = _N(float(i.Info.markPrice),num2) 
        positionAmt = i.Info.positionAmt 
        symbol = i.Info.symbol 
        unRealizedProfit = _N(float(i.Info.unRealizedProfit),3)  
        positionSide = i.Info.positionSide 
        
        position = Position(entryPrice, leverage, liquidationPrice, marginType, markPrice,
                            positionAmt, symbol, unRealizedProfit, positionSide)
        positions.append(position)
    return positions

#Obtainticklevel market data
def GetTickerDao(i):
    ticker = _C(exchanges[i].GetTicker)
    sell = ticker.Sell 
    buy = ticker.Buy 
    last = ticker.Last
    newTicker = Ticker(sell,buy,last)
    return newTicker

#Create Order
def CreateOrderDao(price,amount,flag):
    #price: Price
    #amount: Number of contracts
    #flag: 0(Buy to open a long position); 1 (Buy to close a short position); 2 (Sell to open a short position); 3 (Sell to close a long position.))
    num2 = _G("num2")
    price = _N(price,num2)
    id = 0
    if flag == 0:
        exchange.SetDirection("buy")
        id = exchange.Buy(price,amount)
    elif  flag == 1:
        exchange.SetDirection("closesell")
        id = exchange.Buy(price,amount)
    elif  flag == 2:
        exchange.SetDirection("sell")
        id = exchange.Sell(price,amount) 
    elif  flag == 3:
        exchange.SetDirection("closebuy")
        id = exchange.Sell(price,amount)
    return id

#Close at market price
def CreateOrderDao2(amount,flag,message):
    id = 0
    #flag: 0(Buy to open a long position); 1 (Buy to close a short position); 2 (Sell to open a short position); 3 (Sell to close a long position.))
    if flag == 0:
        exchange.SetDirection("buy")
        id = exchange.Buy(-1,amount,message)
    elif  flag == 1:
        exchange.SetDirection("closesell")
        id = exchange.Buy(-1,amount,message)
    elif  flag == 2:
        exchange.SetDirection("sell")
        id = exchange.Sell(-1,amount,message)
    elif flag == 3:
        exchange.SetDirection("closebuy")
        id = exchange.Sell(-1,amount,message)
    return id 


#Get the number of decimal places of the contract
def GetNumByAmountDao():
    depth = _C(exchange.GetDepth)
    nums = []
    num2s = []
    for ask in depth["Asks"]:
        i = ask["Amount"]
        num = 0
        if str(i).count('.') == 1:
            num = len(str(i).split(".")[1])
        nums.append(num)
        
        j = ask["Price"]
        num2 = 0
        if str(j).count('.') == 1:
            num2 = len(str(j).split(".")[1])
        num2s.append(num2)
    num = max(nums)    
    _G("num",num)
    num2 = Counter(num2s).most_common(1)[0][0]
    _G("num2",num2)
    
    
    
#Return aKLine History
def GetRecordsDao(period,i):
    if period == -1:
        return _C(exchanges[i].GetRecords)
    else:
        return _C(exchanges[i].GetRecords,period)

#Set currency
def SetCurrencyDao(symbol,i):
    exchanges[i].SetCurrency(symbol)

#Transfer funds
def SetTransferDao(amount, typeEnum, symbol):
    exchange.SetBase("https://api.binance.com")
    params = "amount=" + str(amount) + "&type=" + typeEnum + "&asset=" + symbol
    ret = exchange.IO("api", "POST", "/sapi/v1/asset/transfer", params)
    Log("Fund transfer: transfer quantity is{}".format(amount))
    exchange.SetBase("https://fapi.binance.com")
    return ret


#Get all currently uncompleted orders
def GetPendingOrdersDao():
    orders = []
    for order in _C(exchange.GetOrders):
        id = order.Id
        price = order.Price
        amount = order.Amount
        status = order.Status
        newOrder = Order(id, price, amount, status)
        orders.append(newOrder)
    return orders 

#According to orderIDGet order details
def GetOrderByIdDao(id):
    order = _C(exchange.GetOrder,id)
    id = order.Id
    price = order.Price
    amount = order.Amount
    status = order.Status
    newOrder = Order(id, price, amount, status)
    return newOrder    

#Cancel an order
def CancelOrderDao(id):
    if id == 0:
        return True
    flag = exchange.CancelOrder(id)
    if flag == True:
        return flag 
    else:
        order =_C(exchange.GetOrder,id)
        if order["Status"] == 0:
            flag = exchange.CancelOrder(id)
        else:
            flag = True
        return flag    

#Cancel all unfinished orders
def AllCanelOrderDao():
    orders = GetPendingOrdersDao()
    for order in orders:
        _C(CancelOrderDao,order.id)

#Timer
def TimerDao(m,key):
    value = _G(key)
    if value is None:
        value = time.time()
        _G(key,value)
        return True
    now = time.time()
    dnow = datetime.datetime.fromtimestamp(now)
    dvalue = datetime.datetime.fromtimestamp(int(value))
    c = (dnow - dvalue).total_seconds()
    if c - m > 0:
        _G(key,now)
        return True
    return False    

#ObtainPeriod
def GetPeriodDao():
    return exchange.GetPeriod()

#ObtainCurrency 
def GetCurrencyDao():
    return exchange.GetCurrency()

#Get Signal 
def GetStopDao():
    i = IFLAGE
    return i

#Set flag1
def SetIFlageDao():
    global IFLAGE 
    IFLAGE = 1  

#Timer
def TimerDao(m,key):
    value = _G(key)
    if value is None:
        value = time.time()
        _G(key,value)
        return True
    now = time.time()
    dnow = datetime.datetime.fromtimestamp(now)
    dvalue = datetime.datetime.fromtimestamp(int(value))
    c = (dnow - dvalue).total_seconds()
    if c - m > 0:
        _G(key,now)
        return True
    return False        
#Set up two-way positions
def SetDualDao():
    dual = _C(exchange.IO,"api", "GET", "/fapi/v1/positionSide/dual", "")
    if dual.dualSidePosition:
        Log("The current account is in two-way position mode, and there is no need to switch the position mode.")
    else:
        Log("The current account is in one-way holding mode and is ready to switch to two-way holding mode.")
        _C(exchange.IO,"api", "POST", "/fapi/v1/positionSide/dual", "dualSidePosition=true")
        Log("Has been switched to hedge mode")    

ext.GetAccountDao = GetAccountDao
ext.GetPositionsDao = GetPositionsDao
ext.GetTickerDao = GetTickerDao
ext.CreateOrderDao = CreateOrderDao
ext.CreateOrderDao2 = CreateOrderDao2
ext.GetNumByAmountDao = GetNumByAmountDao
ext.GetRecordsDao = GetRecordsDao
ext.SetTransferDao = SetTransferDao
ext.GetPendingOrdersDao = GetPendingOrdersDao
ext.GetOrderByIdDao = GetOrderByIdDao
ext.CancelOrderDao = CancelOrderDao
ext.TimerDao = TimerDao
ext.AllCanelOrderDao = AllCanelOrderDao
ext.GetPeriodDao = GetPeriodDao
ext.GetCurrencyDao = GetCurrencyDao
ext.GetStopDao = GetStopDao
ext.SetIFlageDao = SetIFlageDao
ext.TimerDao = TimerDao
ext.SetDualDao = SetDualDao
ext.SetCurrencyDao = SetCurrencyDao
```

> Detail

https://www.fmz.com/strategy/363411

> Last Modified

2022-06-10 22:41:54
