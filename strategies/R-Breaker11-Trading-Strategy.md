
> Name

R-Breaker11-Trading-Strategy

> Author

太极

> Strategy Description

R-Breaker  Trading strategy



> Source (python)

``` python
# botvs@f976b25629baf8373e73da860a54030d
#!/usr/local/bin/python
#-*- coding: UTF-8 -*-
#Delete reversal stop loss
import math
import talib
def adjustFloat(v):
    v =math.floor(v*1000)
    return v/1000

def GetAccount():
    account = _C(exchange.GetAccount)
    while account == null:
        account = _C(exchange.GetAccount)
        Sleep(1000)
    return account

def GetTicker():
    ticker = exchange.GetTicker()
    while ticker ==null:
        ticker = exchange.GetTicker()
        Sleep(1000)
    return ticker
# def updateProfit(accountInit, accountNow, ticker):
#     netNow = accountNow.Balance + accountNow.FrozenBalance + ((accountNow.Stocks + accountNow.FrozenStocks) * ticker.Buy)
#     netInit = accountInit.Balance + accountInit.FrozenBalance + ((accountInit.Stocks + accountInit.FrozenStocks) * ticker.Buy)
#     LogProfit(adjustFloat(netNow - netInit), accountNow)

#Get the current account total
def GetNowamount():
    account =GetAccount()
    ticker = exchange.GetTicker()
    return account.Balance + account.FrozenBalance + ((account.Stocks + account.FrozenStocks) * ticker.Buy)
#Get the current account market value
def GetStockcap():
    account=GetAccount()
    ticker = GetTicker()
    return (account.Stocks + account.FrozenStocks) * ticker.Buy



#type 0 Total position ratio 1 Percentage of buyable coins
def my_buy(ratio,type):
    try:
        global InitAccount
        account = GetAccount()
        ticker=_C(exchange.GetTicker)
        #Calculate Purchase Amount
        if type == 0:
            unit =(GetNowamount()/ticker.Buy)*ratio - account.Stocks - account.FrozenStocks
        else:
            unit =((GetNowamount()/ticker.Buy) - account.Stocks - account.FrozenStocks)*ratio
        
        #Exit the buying operation if the minimum transaction is insufficient
        if unit < exchange.GetMinStock():
            return 0
        Dict = ext.Buy(unit)  #buyext.Buy
        if(Dict):#Confirm successful opening of position
            #buy_price=Dict['price'] #Buy price   #{'price': 4046.446, 'amount': 1.5}
            #buy_qty=Dict['amount']  #Buy quantity
            #LogProfit(_N(gains,4),'Position opening information Money:',initAccount.Balance,'--Coin:',initAccount.Stocks,'--Opening details:',Dict)
            #updateProfit(InitAccount, GetAccount(), GetTicker())
            Balance_log() #Profit Calculation
            print_log(1,InitAccount)
            return 1
        return 0
    except Exception,ex:
        Log('except Exception my_buy:',ex)
        return 0

def my_sell(ratio,type):
    try:
        global InitAccount
        account = GetAccount()
        if type == 0:
            unit = 1
        else:
            unit =(account.Stocks + account.FrozenStocks)*ratio

        if unit<exchange.GetMinStock():
            return 0

        Dict = ext.Sell(unit)
            #Dict ={"price":_C(exchange.GetTicker).Last}
        if(Dict):
            #updateProfit(InitAccount, GetAccount(), GetTicker())
            Balance_log() #Profit Calculation
            print_log(0,GetAccount())
            return 1
    except Exception,ex:
        Log('except Exception my_sell:',ex)
        return 0


########################################################
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

beng_Account = ext.GetAccount()  #Initialization information
beng_ticker = _C(exchange.GetTicker).Last#Ticker 	Market conditions Last transaction price
beng_Balance=(beng_Account.Stocks*beng_ticker)+beng_Account.Balance #Initialize account funds

def Balance_log(): #Profit Calculation
    try:
        end_Account = ext.GetAccount()  #Current account information
        end_ticker = _C(exchange.GetTicker).Last#Ticker 	Market conditions Last transaction price
        end_Balance=(end_Account.Stocks*end_ticker)+end_Account.Balance #Current amount of money on the account
        LogProfit(end_Balance-beng_Balance) 	#Record Profit Value
    except Exception,ex:
        Log('except Exception Balance_log:',ex)

def print_log(k_p,data=""):  #output
    try:
        name=""
        if k_p:
            name="Open Position"
        else:
            name="Close Position"
        global beng_Account,beng_ticker,beng_Balance
        global R1,R2,R3,S1,S2,S3
        global gains
        end_Account = ext.GetAccount()  #Current account information
        end_ticker = _C(exchange.GetTicker).Last#Ticker 	Market conditions Last transaction price
        #################################################
        date1=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))
        msg_data0=("This time the start of running time: %s has been run:%s\r\n"%(start_time,Caltime(start_time,date1)))
        #################################################
        msg_data1=("This initialization state: %s

Current running state:%s\r\n"%(beng_Account,end_Account))
        #################################################
        end_Balance=(end_Account.Stocks*end_ticker)+end_Account.Balance #Current amount of money on the account
        msg_data2=("Initialization money: %s Current money: %s profit and loss:%s\r\n"%(str(beng_Balance),str(end_Balance),str(end_Balance-beng_Balance)))
        #################################################
        total = end_Account.Balance+end_Account.Stocks*_C(exchange.GetTicker).Last #Account total
        roi = ((total/beng_Balance) -1)*100
        msg_data3=("Current status: %s -- money: %s -- coins: %s -- total value approximately:%.2f\r\n"%(str(name),str(end_Account.Balance),str(end_Account.Stocks),roi))
        #################################################
        income = total - beng_Account['Balance'] - beng_Account['Stocks']*beng_ticker #total profit and loss
        msg_data4=("This profit/loss: %s(RMB)	Total profit/loss:%.2f(RMB) %.2f\r\n"%(str(gains),income,roi))
        #################################################
        #Profit calculation method
        #Profit calculation method: Floating profit: based on (current coin - initial coins)x Current price + (Current money - Initial money)
        diff_stocks=end_Account.Stocks-beng_Account.Stocks    #Difference in ratio
        diff_balance=end_Account.Balance-beng_Account.Balance   #Difference in money
        new_end_balance=diff_stocks*end_ticker+diff_balance #Realize profit and loss # current profit
        #Profit calculation method: Book profit: (current coin x Current Price+current money) - (initial coins x Initial price + initial money)
        new_end_balance2=(end_Account.Stocks*end_ticker+end_Account.Balance)-(beng_Account.Stocks*beng_ticker+beng_Account.Balance)
        msg_data5=("Floating profit: %s(RMB)

Book profit:%s(RMB)\r\n"%(str(_N(new_end_balance,3)),str(_N(new_end_balance2,3))))
        msg_data6 ='R1',R1,'R2',R2,'R3',R3,'\r\n'
        msg_data7 ='S1',S1,'S2',S2,'S3',S3,'\r\n'
        msg_data8 ="Current Price:",end_ticker,'\r\n'
        #################################################
        LogStatus("Initial investment 2016/9/24 Investment 0.2 coins = equivalent market price800RMB\r\n",
                  msg_data0,msg_data1,msg_data2,msg_data3,msg_data4,msg_data5,msg_data6,msg_data7,msg_data8,
                  "Update Time:%s\r\n"%(date1),
                  "%s"%(data)
                  )
        #################################################
        #################################################
        #################################################
    except Exception,ex:
        Log('except Exception print_log:',ex)




def _GetCommand():
    get_command=GetCommand()
    if get_command:
        global K1,K2,N
        arr =get_command.split(":")
        if arr[0] == 'K1':
            K1 = float(arr[-1])
        if arr[0] =='K2':
            K2 = float(arr[-1])
        if arr[0] =='N':
            N = int(arr[-1])


N=2

LastDeal = 0 #Last trading time
def onTick(exchange):
    try:
        global R1,R2,R3,S1,S2,S3,short_state_buy,short_state_sell,LastDeal,task_state,buy_count,sell_count
        amount = GetAccount() # Get account status
        records =exchange.GetRecords() #Default5Minute
        To = records[-1]['Open'] #Today's opening price
        Th = records[-1]['High'] #Today's highest price
        Tl = records[-1]['Low'] #Today's Low
        time = records[-1].Time
        if LastDeal == time:
            return 0
        else:
            LastDeal = 0

        
        records1 =exchange.GetRecords(PERIOD_M30) #Monitoring Period
        #time =(records1[-2].Time - records1[-1].Time)/(60*1000)
        #Log(time);
        records.pop()
        records1.pop()
        ma5 = TA.MA(records1,5)
        ma10 = TA.MA(records1,10)
     


        # HH = records[-2]['High'] #Highest of the day
        # LC = records[-2]['Low']  #Yesterday's lowest
        HC = records[-1]['Close'] #Yesterday's close
        # LL = records[-2]['Low']  #Yesterday's lowest
        HH = TA.Highest(records,N,'High') #NdayhighHighest Price
            #lc = records[-2]['Low']
        #HC = TA.Lowest(records,N,'Close') #//NdaycloseLowest Price
            #hc = records[-2]['Close']
        #HH = TA.Highest(records,N,'Close') #NdaycloseHighest Price
            #ll = records[-2]['Low']
        LC = TA.Lowest(records,N,'Low') #//NdaylowLowest Price
        #HC = TA.Highest(records,N,'Close')
        if ma5[-1] <ma10[-1]:
            HC = records[-1]['Open']

        Pivot = (HH+HC+LC)/3 #Pivot Point
        Pivot = Pivot
        R1 = 2*Pivot-LC #resistance1W
        R2 = Pivot+(HH-LC) #resistance2
        R3 = HH +2*(Pivot-LC) #resistance3

        S1 = 2*Pivot-HH
        S2 = Pivot - (HH-LC)
        S3 = LC-2*(HH-Pivot)
        # Log('r1',R1,"R2",R2,'R3',R3)
        # Log('S1',S1,"S2",S2,'S3',S3)
        
        current_price = _C(exchange.GetTicker).Last #Current Price
        capratio = (amount.Stocks + amount.FrozenStocks)/GetNowamount()
        #Break through the upper band and the half-hour moving average is upward, with funds greater100 then buy
        if ma5[-1] >ma10[-1] :
            if current_price > R3 and amount.Balance > 100 and ma5[-1] >ma10[-1] and capratio <0.8 and buy_count <3 :
               # Log(ma5[-1],ma10[-1])
                Log('open long')
                if my_buy(0.4,1):
                    LastDeal = time
                    sell_count = 0
                    buy_count+=1
                    return
            #Break through the lower track and sell short. If you have currency, enter the selling operation.
            if current_price < S3 and amount.Stocks > 0.03 :
                Log('close all positions')
                if my_sell(1,0):
                    sell_count+=1
                    buy_count = 0
                    LastDeal = time
                    return
            if Th >R2 and Th <R3 and current_price <R1 and current_price >S1   and amount.Stocks > 0.003 and buy_count <3:
                Log('Sell on Trend Reversal')
                if my_sell(0.5,1):
                    LastDeal = time
                    buy_count = 0
                    sell_count+=1
                    return
            if Tl <S2 and Tl >S3 and current_price <S1  and current_price < R1 and capratio <0.6 and ma5[-1] >ma10[-1] and buy_count <3 :
                #Log(ma5[-1],ma10[-1])
                Log('Buy on Trend Reversal')
                if my_buy(0.2,1):
                    buy_count+=1
                    sell_count = 0
                    LastDeal = time
                    return
        else :
            if(current_price > R3 and amount.Stocks > 0.03):
                if my_sell(0.5,1):
                    Log('test buy')
                    LastDeal = time
                    return

            if (current_price < S3 and ma5[-1] >ma5[-5]):
                if my_buy(0.05,1):
                    Log('Test Buy')
                    LastDeal = time
                    buy_count = 0
                    return






        


    except Exception,ex:
        Log('except Exception onTick:',ex)
        return 0


def main():
    global outAccount,init_price,InitAccount,short_state_buy,short_state_sell,task_state,buy_count,sell_count
    init_price = _C(exchange.GetTicker).Last
    InitAccount = GetAccount()
    Log(init_price)
    short_state_buy =short_state_sell = 0
    task_state =0
    buy_count = 0
    sell_count = 0
    while True:
            onTick(exchange)
            nowAccount = ext.GetAccount()  #Export function of trading template Get account information
            print_log(0,nowAccount)
            Sleep(1000) 
```

> Detail

https://www.fmz.com/strategy/23874

> Last Modified

2017-02-13 11:58:17
