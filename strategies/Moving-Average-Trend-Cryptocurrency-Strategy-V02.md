
> Name

Moving-Average-Trend-Cryptocurrency-Strategy-V02

> Author

太极

> Strategy Description

@Tai Chi   QQ7650371
#moving average/Trend Strategy
#By judging how much it rebounds after a death cross bottom to buy
#Sell by how much the golden cross falls after it rises to the top

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|FastPeriod|2|Opening fast line period|
|SlowPeriod|4|Opening slow line period|
|EnterPeriod|true|open position observation period|
|x|------------------------------------------------------------------------------|Separator symbol|
|ExitFastPeriod|2|Closing fast line period|
|ExitSlowPeriod|4|Closing slow line period|
|ExitPeriod|2|Closing Observation Period|
|xx|------------------------------------------------------------------------------|Separator symbol|
|PositionRatio|0.5|Position ratio|
|Interval|10|Polling interval (seconds))|
|xxx|------------------------------------------------------------------------------|Separator symbol|
|MAType|0|Moving average type: TA.EMA|TA.MA|


> Source (python)

``` python
#!/usr/local/bin/python
#-*- coding: UTF-8 -*-
#moving average/Trend Strategy
#By judging how much it rebounds after a death cross bottom to buy
#Sell by how much the golden cross falls after it rises to the top


# FastPeriod=3 #Opening fast line period
# SlowPeriod=7 #Opening slow line period
# EnterPeriod=1       #open position observation period
# ExitFastPeriod=3 #Closing Line Cycle
# ExitSlowPeriod=7 #Closing slow line period
# ExitPeriod=2        #Closing Observation Period
# PositionRatio=0.5 #Position ratio
# Interval=10 #Polling Interval
# MAType=0 #Moving average type TA.EMA|TA.MA


import types
array = [TA.EMA,TA.MA]
_MACalcMethod = array[MAType]
def Cross(a,b):   #Calculate moving average method
    crossNum = 0
    arr1 = []
    arr2 = []
    if(type(a) == types.ListType and type(b) == types.ListType):
        arr1 = a
        arr2 = b
    else:
        records = null
        while True:
            records = exchange.GetRecords()
            if(records and len(records) > a and len(records) > b):
                break
            Sleep(Interval)
        arr1 = _MACalcMethod(records,a)
        arr2 = _MACalcMethod(records,b)
    if(len(arr1) != len(arr2)):
        raise Exception("array length not equal")
    for i in range(len(arr1) - 1,-1,-1):
        if((type(arr1[i]) != types.IntType and type(arr1[i]) != types.FloatType) or (type(arr2[i]) != types.IntType and type(arr2[i]) != types.FloatType) ):
            break
        if(arr1[i] < arr2[i]):
            if(crossNum > 0):
                break
            crossNum -= 1
        elif(arr1[i] > arr2[i]):
            if(crossNum < 0):
                break
            crossNum += 1
        else:
            break
    return crossNum

import datetime
def Caltime(date1,date2):
    try:
        date1=time.strptime(date1,"%Y-%m-%d %H:%M:%S")
        date2=time.strptime(date2,"%Y-%m-%d %H:%M:%S")
        date1=datetime.datetime(date1[0],date1[1],date1[2],date1[3],date1[4],date1[5])
        date2=datetime.datetime(date2[0],date2[1],date2[2],date2[3],date2[4],date2[5])
        return date2-date1
    except Exception,ex:
        Log('except Exception Caltime:',ex)
        return "except Exception"

import time
start_timexx =time.localtime(time.time()) #time.clock()
start_time=time.strftime("%Y-%m-%d %H:%M:%S",start_timexx)
buy_price=0 #Buy price
buy_qty=0  #Buy quantity
gains=0  #Profit

def my_buy(): #Open Position
    try:
        global buy_price,buy_qty
        initAccount = ext.GetAccount()  #Export function of the trading template to obtain account status and save the initial account state before the strategy was run
        opAmount=1
        #Before opening a position, check whether you have the coin, if not, buy first
        if int(initAccount.Stocks)>1:
            if buy_price<1:
                buy_price=_C(exchange.GetTicker).Last
                buy_qty=initAccount.Stocks
            Log('Open position information1 There are more games in the warehouse:',initAccount.Stocks,'Clear','--Open position details:',initAccount)
            return 1
        if int(initAccount.Stocks)<1:
            if int(str(initAccount.Stocks).replace('0.',''))>=1:
                if buy_price<1:
                    buy_price=_C(exchange.GetTicker).Last
                    buy_qty=initAccount.Stocks
                Log('Open position information2 There are more games in the warehouse:',initAccount.Stocks,'Clear','--Open position details:',initAccount)
                return 1

        #if int(initAccount.Stocks)<1:
        if int(str(initAccount.Stocks).replace('0.',''))==0:
            #opAmount=1
            opAmount = _N(initAccount.Balance*PositionRatio,3)  #Buy quantity
            Log("If opening a position without coins, first buy to open%selement"%(str(opAmount)))   #GenerateLOGLog
        #     else:
        #         opAmount = _N(initAccount.Stocks * PositionRatio,3)  #Get trading quantity
        # else:
        #     opAmount = _N(initAccount.Stocks * PositionRatio,3)  #Get trading quantity
        Dict = ext.Buy(opAmount)  #buyext.Buy
        if(Dict):#Confirm successful opening of position
            buy_price=Dict['price'] #Buy price   #{'price': 4046.446, 'amount': 1.5}
            buy_qty=Dict['amount']  #Buy quantity
            print_log(1,initAccount,Dict)
            return 1
        return 0

    except Exception,ex:
        Log('except Exception my_buy:',ex)
        return 0

outAccount = ext.GetAccount()  #Initialization information
def print_log(k_p,Account,Dict):
    try:
        global outAccount
        name=""
        if k_p:
            LogProfit(_N(gains,4),'Position opening information Money:',Account.Balance,'--Coin:',Account.Stocks,'--Opening details:',Dict)
            name="Open Position"
        else:
            LogProfit(_N(gains,4),'Liquidation information Money:',Account.Balance,'--Coins:',Account.Stocks,'--Close details:',Dict)
            name="Close Position"
        endAccount = ext.GetAccount()  #Initialization information
        date1=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))
        LogStatus("Initial investment 2016/9/16 Invested 2,000 yuan\r\n",
                  "This initialization status:",outAccount,
                  "\r\nCurrent Running Status:",endAccount,
                  "\r\nStart running time this session: %s Already running:%s\r\n"%(start_time,Caltime(start_time,date1)),
                  "This profit:%s\r\n"%(str(gains)),
                  "Current status: %s -- Money: %s -- Coin:%s\r\n"%(str(name),str(Account.Balance),str(Account.Stocks)),
                  "Update Time:%s"%(date1)
                  ) # Test
    except Exception,ex:
        Log('except Exception print_log:',ex)


def my_sell(): #Close Position
    try:
        global buy_price,buy_qty,gains,start_time
        nowAccount = ext.GetAccount()  #Export function of trading template Get account information
        if _C(exchange.GetTicker).Last>buy_price+4:   #The current price must be greater than the opening price
            Dict = ext.Sell(nowAccount.Stocks)
            if(Dict):
                sell_gains=(Dict['price']-buy_price)*Dict['amount']
                gains=gains+sell_gains
                buy_price=0 #Buy price
                buy_qty=0  #Buy quantity
                print_log(0,nowAccount,Dict)
                return 1
        return 0
    except Exception,ex:
        Log('except Exception my_sell:',ex)
        return 0

def main():
    global outAccount
    STATE_IDLE = -1  #Idle state
    state = STATE_IDLE  #Initialize state as idle

    Log("run  ",outAccount)  #Output initial account information
    SetErrorFilter("GetAccount|GetRecords|GetTicker")  #Mask error content

    b=0  #Open Position
    b1=0  #Number of checks
    a=0  #Close Position
    a1=0  #Number of checks
    while True:
        if(state == STATE_IDLE):   #Check if status is 'idle' to trigger opening a position
            #Open Position
            n = Cross(FastPeriod,SlowPeriod) #The template function obtains the cross results of the fast and slow lines of the EMA indicator
            if n<0:  #Determine that it is currently a death cross
                b1+=1
                if b>=int(n): #Indicates that it is still in a downtrend/uptrend
                    b=int(n)
                else: #Start falling, open position
                    if(int(n)>=int(b)+int(EnterPeriod)):  #Confirm the upward trend to the point defined by yourself
                        if my_buy():  #Open Position
                            b=0
                            b1=0
                            state = PD_SHORT
                            # if(b1>=10):#Small fluctuation operation to open a position
                            #     b1=0
                            #     if my_buy():
                            #         b=0
                            #         state = PD_SHORT
        else:#Close Position
            n = Cross(ExitFastPeriod,ExitSlowPeriod) #The template function obtains the cross results of the fast and slow lines of the EMA indicator
            if n>0:  #Determine that it is currently a golden cross
                a1+=1
                if a<=int(n): #Indicates that the upward trend is still in progress
                    a=int(n)
                else: #Start falling, close position
                    if(int(n)<=int(a)-int(ExitPeriod)):  #Confirm the downward trend to the point defined by yourself
                        if my_sell(): #Close Position
                            a=0
                            a1=0
                            state = STATE_IDLE   #Change status to idle to trigger position opening
                            # if(a1>=10): #Close positions on small fluctuations
                            #     a1=0
                            #     if my_sell():
                            #         a=0
                            #         state = STATE_IDLE   #Change status to idle to trigger position opening
        Sleep(Interval * 1000)


```

> Detail

https://www.fmz.com/strategy/21369

> Last Modified

2016-09-19 18:05:01
