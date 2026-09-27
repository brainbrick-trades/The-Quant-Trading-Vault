
> Name

Ghost-Trend-Following-Strategy-Business-Library

> Author

陈皮





> Source (python)

``` python
#!/usr/bin/python
# -*- coding: utf-8 -*-
import time,datetime
import json
import math
import urllib.request
RECORDS = None
FLAGE = 0
#Account information tabled, for display in status information
def TableAccountService(account):
    
    clos = [] #Header
    clos.append("Initial Balance")
    clos.append("Wallet Balance")
    clos.append("Margin balance")
    clos.append("Available balance")
    clos.append("Used margin")
    clos.append("Current Leverage")
    clos.append("Total income(Yield)")
    
    initialTotalMarginBalance = "$" + str(_G("initialTotalMarginBalance")) #Initial Balance
    totalWalletBalance = "$" + str(account.totalWalletBalance) #Wallet Balance
    totalMarginBalance = "$" + str(account.totalMarginBalance) #Margin balance
    availableBalance = "$" + str(account.availableBalance) #Available balance
    totalPositionInitialMargin = account.totalPositionInitialMargin#Position margin
    totalOpenOrderInitialMargin = account.totalOpenOrderInitialMargin#Current pending order margin
    #_C(FilterHandlService)
    drawOut = _N(_G("drawOut"),2) #Transferred funds
    if account.totalMarginBalance==0 :
        marginRate = "0"
        lever = 0
        Revenue = "$0"
    else :
        marginRate = (totalPositionInitialMargin+totalOpenOrderInitialMargin)/account.totalMarginBalance
        marginRate = "("+str(_N(marginRate,2)) + ")"#Margin Rate
        leverage = _G("leverage")#leverage 
        lever = _N(totalPositionInitialMargin*leverage/account.totalMarginBalance,2)#Current Leverage
        drawIn = _G("drawIn")
        drawOut = _G("drawOut")
        totalRevenue = account.totalMarginBalance-_G("initialTotalMarginBalance") + drawOut - drawIn#Total income
        initialTotalMarginBalance = _G("initialTotalMarginBalance")
        totalYield = 0
        if initialTotalMarginBalance != 0:
            totalYield = totalRevenue/initialTotalMarginBalance
        totalYield = "(" + str(_N(totalYield,2)) + ")"#Total Return Rate
        Revenue = "$" + str(_N(totalRevenue,2)) + totalYield
        #Record current total profit
        _G("totalRevenue",totalRevenue)
    totalInitialMargin = "$" + str(_N(totalPositionInitialMargin+totalOpenOrderInitialMargin,2))#Used margin
    
    rows = [] #Table content
    row =[]
    row.append(initialTotalMarginBalance)
    row.append(totalWalletBalance)
    row.append(totalMarginBalance)
    row.append(availableBalance)
    row.append(totalInitialMargin+marginRate)
    row.append(lever)
    row.append(Revenue)
    rows.append(row)
    
    table = {
        "type" : "table",
        "title" : "Account Information",
        "cols" : clos,
        "rows" : rows
    }
    
    
    return table
    
#Trading pairs are tabulated for display in the status information    
def TablePositionsService(positions):
    clos = [] #Header
    clos.append("Currency")
    clos.append("Direction")
    clos.append("Quantity")
    clos.append("Opening price")
    clos.append("Forced liquidation price")
    clos.append("Current price")
    clos.append("Unrealized profit and loss")
    rows = [] #Table content
    for position in positions:
        row = []
        symbol = position.symbol
        leverage = position.leverage
        row.append(symbol + "[" + leverage + "X]")
        
        positionAmt = position.positionAmt
        if float(positionAmt)>0:
            row.append("go long")
        else:
            row.append("go short")
        row.append(math.fabs(float(positionAmt)))
        row.append(position.entryPrice)
        row.append(position.liquidationPrice)
        row.append(position.markPrice)
        row.append(position.unRealizedProfit)
        rows.append(row)  
    table = {
        "type" : "table",
        "title" : "Trading pair information",
        "cols" : clos,
        "rows" : rows
    }
    return table 



#Update status information
def UpdateLogStatusService():
    account = ext.GetAccountDao()
    positions = ext.GetPositionsDao()
    LogStatus("`" + json.dumps(TableAccountService(account)) + "`\n" +  "`" + json.dumps(TablePositionsService(positions)) +  "`")

            
#Convert the current price and order value into the number of contracts            
def GetAmountByOrderValueService(price):
    ext.GetNumByAmountService()
    num = _G("num")
    orderValue = _G("orderValue")
    leverage = _G("leverage")
    account = ext.GetAccountDao()
    totalMarginBalance = account.totalMarginBalance
    orderValue = orderValue*totalMarginBalance*leverage*0.99/100
    amount = orderValue/price
    if orderValue < 5:
        amount = 5/price + 1
    amount = _N(amount,num)
    if price*amount > orderValue:
        amount = orderValue*0.99/price
        amount = _N(amount,num)
    exchange.SetMarginLevel(leverage)
    return amount   

#Close Position
def ClearanceService():
    positions = ext.GetPositionsDao()
    for position in positions:
        positionAmt = position.positionAmt
        amt = math.fabs(float(positionAmt))
        totalRevenue = _G("totalRevenue")
        ticker = ext.GetTickerDao(0)
        price = ticker.last
        symbol = position.symbol
        symbol = symbol.replace("USDT","_USDT")
        if float(positionAmt)>0:
            #Hold long position,--Sell to Close
            ext.CreateOrderDao2(amt,3,"{}Current transaction price of currency long position:{}".format(symbol,price))
            LogProfit(_N(totalRevenue,2))
        else:
            #Hold short position,--Buy to Close
            ext.CreateOrderDao2(amt,1,"{}Current transaction price of currency short order:{}".format(symbol,price))
            LogProfit(_N(totalRevenue,2))
            
#Get the number of decimal places of the contract
def GetNumByAmountService():
    ext.GetNumByAmountDao()            

#Calculate the minimum order size for the trading pair
def GetMinOrderCountService():
    minCount = 1
    num = _G("num")
    if num != 0:
        minCount = 1/(10**num)
    return minCount
 
#Get Signal 
def GetStopService():
    return ext.GetStopDao()

#Get trading pair information    
def GetPositionsService():
    return ext.GetPositionsDao()

#ObtaintickPrice
def GetPriceService(i):
    ticker = ext.GetTickerDao(i)
    price = ticker.last
    return price 

#Select the coins with the largest price changes
def GetSymbolService():
    global RECORDS 
    #First time obtaining all coinsrecordData, cached 
    R = _G("RECORDS")
    r = RECORDS
    if r is None:
        if R is None:
            SetSymbolsRecordsService()
        else:
            RECORDS = R
        return
    #Regularly fetch the latest data of one cryptocurrencyrecorddata, compare with the cached data, if they are the same, record the data update identifier as0and skip
    #If different, update the cache for all currenciesrecordData,And record the data update identifier as1
    isUpdate = UpdateRecordService()
    if isUpdate:
        return 
    #Calculate the absolute value of the price change for all currencies and select the currency with the largest value
    #Based on the latest price of the selected currency andbfCountofkCompare the opening price of the line, determine the order direction and record it
    GetMaxSymbolService()
    _G("RECORDS",RECORDS)

#Order Signal
def FirstSignalService():
    global FLAGE
    symbolRecord = _G("symbolRecord")
    #Check whether the currency has been filtered, if not, exit 
    if symbolRecord is None:
        return
    #Check whether the data update identifier is1,If not, jump out 
    isUpdate = _G("isUpdate")
    if isUpdate == 0:
        return
    symbol = symbolRecord["symbol"] 
    #Check if there is a current position 
    positions = ext.GetPositionsDao()
    if len(positions) == 0:
        #If not, use the filtered currency to place an order.
        ext.SetCurrencyDao(symbol,0)
        leverage = _G("leverage")
        exchange.SetMarginLevel(leverage)
        side = symbolRecord["side"]  
        if side == 1:#go long 
            price = symbolRecord["close"]
            amount = GetAmountByOrderValueService(price)
            ext.CreateOrderDao2(amount,0,"{}Current transaction price of multiple orders of currency:{}".format(symbol,price))
            _G("initPrice",price)
            _G("initSide",side)
        else:#go short
            price = symbolRecord["close"]                      
            amount = GetAmountByOrderValueService(price)
            ext.CreateOrderDao2(amount,2,"{}The current transaction price of the short order of the currency:{}".format(symbol,price))
            _G("initPrice",price)
            _G("initSide",side)
    elif len(positions) == 1:
        position = positions[0]
        positionAmt = float(position.positionAmt)
        nSymbol = position.symbol
        nSymbol = nSymbol.replace("USDT","_USDT")
        #Determine whether the filtered currency is the same as the currency currently placed.
        if symbol == nSymbol:
            #Determine whether the current currency has unrealized losses; if so, liquidate the position and place a reverse order
            isFlag = _G("isFlag")
            if isFlag == 0:#Use reversal signals; if isFlag=0, do not use reversal signals and do not process the current position.
                firstPrice = _G("initPrice")
                side = _G("initSide")
                price = symbolRecord["close"]
                if side == 1 and price <= firstPrice:#After exchanging coins, the first order direction is long, but the current price is lower than the initial order price (floating loss), so a reverse order is needed
                    Log("After currency exchange, the current position direction is long, but the current price{}Less than or equal to the initial order price{}(floating loss), so you need to reverse the order".format(price,firstPrice))
                    ClearanceService()
                    amount = GetAmountByOrderValueService(price)
                    if positionAmt > 0:#If you hold a long order, clear the long order and then place a short order.
                        ext.CreateOrderDao2(amount,2,"{}The current transaction price of the short order of the currency:{}".format(symbol,price))
                    else:
                        ext.CreateOrderDao2(amount,0,"{}Current transaction price of multiple orders of currency:{}".format(symbol,price))
                    _G("initSide",0)
                    FLAGE = 0
                elif side == 0 and price >= firstPrice:#After exchanging coins, the first order direction is short, but the current price is higher than the initial order price (floating loss), so a reverse order is needed
                    Log("After currency exchange, the current position direction is short, but the current price{}Greater than or equal to the initial order price{}(floating loss), so you need to reverse the order".format(price,firstPrice))
                    #Clear Positions, Then Place Long Order
                    ClearanceService()
                    amount = GetAmountByOrderValueService(price)
                    if positionAmt < 0:
                        ext.CreateOrderDao2(amount,0,"{}Current transaction price of multiple orders of currency:{}".format(symbol,price))
                    else:
                        ext.CreateOrderDao2(amount,2,"{}The current transaction price of the short order of the currency:{}".format(symbol,price))
                    _G("initSide",1)
                    FLAGE = 0
                else:
                    Log("Current Price{},First order price{},No need to reverse order".format(price,firstPrice))
            else:
                Log("Strategy parameters have blocked the reversal signal function")
        else:
            #Clear the current position and replace it with the selected currency to place an order.
            ClearanceService()
            ext.SetCurrencyDao(symbol,0)
            side = symbolRecord["side"]  
            if side == 1:#go long 
                ticker = ext.GetTickerDao(0)
                price = ticker.last                          
                amount = GetAmountByOrderValueService(price)
                ext.CreateOrderDao2(amount,0,"{}Current transaction price of multiple orders of currency:{}".format(symbol,price))
                _G("initPrice",price)
                _G("initSide",side)
                FLAGE = 0
            else:#go short
                ticker = ext.GetTickerDao(0)
                price = ticker.last                          
                amount = GetAmountByOrderValueService(price)
                ext.CreateOrderDao2(amount,2,"{}The current transaction price of the short order of the currency:{}".format(symbol,price))
                _G("initPrice",price)
                _G("initSide",side)
                FLAGE = 0
        
    
    
#Cacherecord
def SetSymbolsRecordsService():
    global RECORDS 
    symbols = _G("symbols")
    recordss = {}
    for symbol in symbols:
        #Log("symbol:",symbol)
        ext.SetCurrencyDao(symbol,1)
        if RECORDS is None:
            records =  ext.GetRecordsDao(-1,1)
            recordss[symbol] = records
        else:
            oldRecords = RECORDS[symbol]
            _CDelay(250)
            records = _C(CheckRecordService,oldRecords)
            recordss[symbol] = records
    RECORDS = recordss

#Check RecordsrecordWhether data is updated
def CheckRecordService(oldRecords):
    oldTime = oldRecords[-1]["Time"]
    records = ext.GetRecordsDao(-1,1)
    newTime = records[-1]["Time"]
    if oldTime == newTime:
        #Sleep(100)
        return False
    else:
        return records

#Update Allsymbolofrecord    
def UpdateRecordService():
    global RECORDS 
    symbols = _G("symbols")
    symbol = symbols[0]
    ext.SetCurrencyDao(symbol,1)
    newRecords = ext.GetRecordsDao(-1,1)
    newTime = newRecords[-1]["Time"]
    oldRecords = RECORDS[symbol]
    oldTime = oldRecords[-1]["Time"]
    if newTime == oldTime:
        _G("isUpdate",0)
        return True
    else:
        Sleep(500)
        SetSymbolsRecordsService()
        _G("isUpdate",1)
        Log("Market data has been updated")
        return False

#Calculate the coin with the largest price change
def GetMaxSymbolService():
    symbols = _G("symbols")
    bfCount = _G("bfCount") + 1
    chgs = []
    symbolList = []
    tests = []
    tests2 = []
    for symbol in symbols:
        records = RECORDS[symbol]
        record = records[-1]
        close = record["Open"]
        bfRecord = []
        if len(records) < bfCount:
            bfRecord = records[-len(records)]
            Log("{}Insufficient Data{}".format(symbol,len(records)))
        else:
            bfRecord = records[-bfCount]
        bfOpen = bfRecord["Open"]
        chg = 0
        if close >= bfOpen:
            chg = (close - bfOpen)/bfOpen 
        else:
            chg = (bfOpen - close)/bfOpen
        chgs.append(chg)
        symbolList.append(symbol)
        tests.append([symbol,chg])
        tests2.append([symbol,bfOpen,close])
    Log(tests)
    Log(tests2)
    maxChg = max(chgs)
    maxSymbol = symbolList[chgs.index(maxChg)]
    maxRecords = RECORDS[maxSymbol]
    maxRecord = maxRecords[-1]
    maxClose = maxRecord["Open"]
    maxBfRecord = maxRecords[-bfCount]
    maxBfOpen = maxBfRecord["Open"] 
    maxSide = GetSideService(maxSymbol,maxClose,maxBfOpen)
    symbolRecord = {}
    symbolRecord["symbol"] = maxSymbol 
    symbolRecord["initPrice"] = maxBfOpen 
    #symbolRecord["firstPrice"] = price 
    symbolRecord["close"] = maxClose 
    symbolRecord["side"] = maxSide 
    symbolRecord["chg"] = maxChg
    _G("symbolRecord",symbolRecord)
    Log("NewsymbolRecord:",symbolRecord)
    #Log("The currency with the largest price change is:{},Price Change is:{}".format(maxSymbol,maxChg))

#Calculate order direction    
def GetSideService(maxSymbol,maxClose,maxBfOpen):
    symbol = ext.GetCurrencyDao()
    records = RECORDS[symbol]
    price = records[-1]["Open"]
    #Check if there is a current position 
    positions = ext.GetPositionsDao()
    if len(positions) == 0:#If there is no position, do not use the inheritance module 
        Log("First order, no inheritance module is used")
        _G("oldClose",maxClose)
        _G("oldBfOpen",maxBfOpen)
        if maxClose > maxBfOpen:
            return 1 #Long Direction
        else:
            return 0 #Short Direction
    else:
        position = positions[0]
        nSymbol = position.symbol
        nSymbol = nSymbol.replace("USDT","_USDT")
        initPrice = _G("initPrice")
        if nSymbol == maxSymbol:#No need to switch coins for the same currency
            Log("The filtered coins are the same as the currently held coins,No need to change currency")
            if price >= initPrice:
                return 1 #Long Direction
            else:
                return 0 #Short Direction
        #Use inherited module
        Log("The filtered coins are different from the currently held coins,Need to change currency,{}Currency changed to{}Currency".format(nSymbol,maxSymbol))
        oldClose = _G("oldClose")
        oldBfOpen =_G("oldBfOpen")
        if (maxClose >= maxBfOpen and oldClose > oldBfOpen) or (maxClose <= maxBfOpen and oldClose < oldBfOpen):#Inherit the order direction of the previous coin 
            _G("oldClose",maxClose)
            _G("oldBfOpen",maxBfOpen)
            Log("{}Currency Inheritance{}Order direction of currency".format(maxSymbol,nSymbol))
            position =  positions[0]
            positionAmt = float(position.positionAmt)
            if positionAmt < 0:
                return 0
            else:
                return 1
        else:#Do not use inheritance
            Log("Do not use inherited modules")
            _G("oldClose",maxClose)
            _G("oldBfOpen",maxBfOpen)
            if maxClose >= maxBfOpen:
                return 1 #Long Direction
            else:
                return 0 #Short Direction 
#close all positions
def ClearAllService():
    symbols = _G("symbols")
    for symbol in symbols:
        ext.SetCurrencyDao(symbol,0)
        positions = ext.GetPositionsDao()
        if len(positions) != 0:
            Log("Clear existing positions")
            ClearanceService()
    
        
#Strategy Interaction
def GetCommandService():
    cmd = GetCommand()
    if cmd: 
        arr = cmd.split(":")
        if arr[0] == "One-click liquidation: #Clear all trading pair positions
            ClearanceService()
            Log("Close all positions")
        elif arr[0] == "Spot=="Contract": #Transfer USDT from spot account to contract account
            accountFunds = float(arr[1])
            ret = ext.SetTransferDao(accountFunds,"MAIN_UMFUTURE","USDT")
            if ret is None:
                Log("spot=="contract,Error in transferring funds")  
        elif arr[0] == "Contract=="Spot": #Transfer USDT from contract account to spot account
            accountFunds = float(arr[1])
            ret = ext.SetTransferDao(accountFunds,"UMFUTURE_MAIN","USDT")
            if ret is None:
                Log("contract=="spot,Error in transferring funds")
            drawOut = _G("drawOut")
            _G("drawOut",accountFunds + drawOut)

#Reduce Position Signal
def StopSurplusService():
    global FLAGE
    if FLAGE == 1:
        return 
    positions = ext.GetPositionsDao() 
    if len(positions) == 0:
        return 
    position = positions[0]
    positionAmt = float(position.positionAmt)
    entryPrice = float(position.entryPrice)
    ticker = ext.GetTickerDao(0)
    price = ticker.last
    stopSurplus = _G("stopSurplus")/100
    stopSurplusCount = _G("stopSurplusCount")
    stopSurplusCount = float(stopSurplusCount)/100
    if positionAmt > 0:
        if (price - entryPrice)/entryPrice < stopSurplus:
            return 
        positionAmt = stopSurplusCount*positionAmt
        num = _G("num")
        positionAmt = _N(positionAmt,num)
        Log("Reduce long positions")
        ext.CreateOrderDao2(positionAmt,3,"Current transaction price:{}".format(price))
        totalRevenue = _G("totalRevenue")
        LogProfit(_N(totalRevenue,2))
        FLAGE = 1
    else:
        if (entryPrice - price)/entryPrice  < stopSurplus:
            return 
        positionAmt = -positionAmt 
        positionAmt = stopSurplusCount*positionAmt
        num = _G("num")
        positionAmt = _N(positionAmt,num)
        Log("Reduce short positions")
        ext.CreateOrderDao2(positionAmt,1,"Current transaction price:{}".format(price))
        totalRevenue = _G("totalRevenue")
        LogProfit(_N(totalRevenue,2))
        FLAGE = 1
    
#Set up two-way positions           
def SetDualService():
    ext.SetDualDao()
            
ext.TableAccountService = TableAccountService
ext.TablePositionsService = TablePositionsService
ext.UpdateLogStatusService = UpdateLogStatusService
ext.ClearanceService = ClearanceService
ext.GetNumByAmountService = GetNumByAmountService
ext.GetAmountByOrderValueService = GetAmountByOrderValueService
ext.GetStopService = GetStopService
ext.GetPositionsService = GetPositionsService
ext.GetPriceService = GetPriceService 
ext.GetSymbolService = GetSymbolService
ext.FirstSignalService = FirstSignalService
ext.GetCommandService = GetCommandService
ext.SetDualService = SetDualService
ext.GetSymbolService = GetSymbolService
ext.ClearAllService = ClearAllService
ext.StopSurplusService = StopSurplusService
```

> Detail

https://www.fmz.com/strategy/363410

> Last Modified

2022-10-01 01:50:24
