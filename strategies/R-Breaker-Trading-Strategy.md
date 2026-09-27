
> Name

R-Breaker-Trading-Strategy

> Author

太极

> Strategy Description

R-Breaker  Trading strategy



> Source (python)

``` python
#!/usr/local/bin/python
#-*- coding: UTF-8 -*-
#R-Breaker Trading strategy
#Strategy provider @FJK   QQ:171938416
#Improve  @Tai Chi  QQ:7650371

def my_buy(): #Open Position
    try:
        global buy_price,buy_qty
        initAccount = ext.GetAccount()  #Export function of the trading template to obtain account status and save the initial account state before the strategy was run
        opAmount=1
        PositionRatio =1
        #Before opening a position, check whether you have the coin, if not, buy first
        if int(initAccount.Stocks)>1:
            if buy_price<1:
                buy_price=_C(exchange.GetTicker).Last
                buy_qty=initAccount.Stocks
            #Log('Open position information1 There are more games in the warehouse:',initAccount.Stocks,'Clear','--Open position details:',initAccount)
            return 1
        if int(initAccount.Stocks)<1:
            if int(str(initAccount.Stocks).replace('0.',''))>=3:
                if buy_price<1:
                    buy_price=_C(exchange.GetTicker).Last
                    buy_qty=initAccount.Stocks
                #Log('Open position information2 There are more games in the warehouse:',initAccount.Stocks,'Clear','--Open position details:',initAccount)
                return 1

        #if int(str(initAccount.Stocks).replace('0.',''))==0:
        opAmount = _N(initAccount.Balance*PositionRatio,3)  #Buy quantity
        Log("If opening a position without coins, first buy to open%selement"%(str(opAmount)))   #GenerateLOGLog

        Dict = ext.Buy(opAmount)  #buyext.Buy
        if(Dict):#Confirm successful opening of position
            buy_price=Dict['price'] #Buy price   #{'price': 4046.446, 'amount': 1.5}
            buy_qty=Dict['amount']  #Buy quantity
            #LogProfit(_N(gains,4),'Position opening information Money:',initAccount.Balance,'--Coin:',initAccount.Stocks,'--Opening details:',Dict)
            print_log(1,initAccount)
            return 1
        return 0

    except Exception,ex:
        Log('except Exception my_buy:',ex)
        return 0


import time
import datetime
def Caltime(date1,date2):   #Calculate running days
    try:
        date1=time.strptime(date1,"%Y-%m-%d %H:%M:%S")
        date2=time.strptime(date2,"%Y-%m-%d %H:%M:%S")
        date1=datetime.datetime(date1[0],date1[1],date1[2],date1[3],date1[4],date1[5])
        date2=datetime.datetime(date2[0],date2[1],date2[2],date2[3],date2[4],date2[5])
        return date2-date1
    except Exception,ex:
        Log('except Exception Caltime:',ex)
        return "except Exception"

start_timexx =time.localtime(time.time()) #time.clock()
start_time=time.strftime("%Y-%m-%d %H:%M:%S",start_timexx)
buy_price=0 #Buy price
buy_qty=0  #Buy quantity
gains=0  #Profit

beng_Account = ext.GetAccount()  #Initialization information
beng_ticker = _C(exchange.GetTicker).Last#Ticker 	Market conditions Last transaction price
beng_Balance=(beng_Account.Stocks*beng_ticker)+beng_Account.Balance #Initialize account funds
def print_log(k_p,data=""):  #output
    try:
        name=""
        if k_p:
            name="Open Position"
        else:
            name="Close Position"
        global beng_Account,beng_ticker,beng_Balance
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
        #################################################
        LogStatus("Initial investment 2016/9/24 Investment 0.2 coins = equivalent market price800RMB\r\n",
                  msg_data0,msg_data1,msg_data2,msg_data3,msg_data4,msg_data5,
                  "Update Time:%s\r\n"%(date1),
                  "%s"%(data)
                  )
        #################################################
        #################################################
        #################################################
    except Exception,ex:
        Log('except Exception print_log:',ex)

def my_sell(): #Close Position
    try:
        global buy_price,buy_qty,gains,ExitPeriod
        ExitPeriod = 0
        nowAccount = ext.GetAccount()  #Export function of trading template Get account information
        if nowAccount.Stocks<=0.002:  #Guaranteed to meet transaction volume
            #Log('Does not meet minimum trading volume:',nowAccount.Stocks)
            return 1

        #history_Last=_N(Volume_averages(Ticker_list),2)    #Historical average price
        #cur_last = _N(_C(exchange.GetTicker).Last,2)

        #if _N(_C(exchange.GetTicker).Last,2)>buy_price+ExitPeriod :   #The current price must be greater than the opening price
        if True:
            #if _N(_C(exchange.GetTicker).Last,2)>buy_price+ExitPeriod and  history_Last - cur_last >0 and  history_Last - cur_last < 2 :   #The current price must be greater than the opening price
            #Log('Historical spread:',history_Last - cur_last)
            Dict = ext.Sell(nowAccount.Stocks)
            #Dict ={"price":_C(exchange.GetTicker).Last}
            if(Dict):
                #sell_count+=1
                sell_gains=(Dict['price']-buy_price)*Dict['amount']
                gains=gains+sell_gains
                buy_price=0 #Buy price
                buy_qty=0  #Buy quantity
                LogProfit(_N(gains,4),'Position closing information Money:',nowAccount.Balance,'--Coins:',nowAccount.Stocks,'--Closing details:',Dict)#yield curve
                print_log(0,nowAccount)
                return 1
        else:
            current_Last = _N(_C(exchange.GetTicker).Last,2)    ##Current Price
            data="Does not meet the conditions for closing the position: Buy-Current=Difference:%s-%s=%s"%(buy_price,current_Last,_N(buy_price-current_Last,2))
            print_log(0,nowAccount,data)
        return 0
    except Exception,ex:
        Log('except Exception my_sell:',ex)
        return 0

########################################################
def onTick():
    try:
        records =exchange.GetRecords()  #Data returned by the number of cycles you set
        HH = records[-2]['High'] #Highest of the day
        LC = records[-2]['Low']  #Yesterday's lowest
        HC = records[-2]['Close'] #Yesterday's close
        LL = records[-2]['Low']  #Yesterday's lowest
        Pivot = (HH+HC+LC)/3 #Pivot Point
        R1 = 2*Pivot-LC #resistance1
        R2 = Pivot+(HH-LC) #resistance2
        R3 = HH +2*(Pivot-LC) #resistance3

        S1 = 2*Pivot-HH  #support level1
        S2 = Pivot - (HH-LC)  #support level2
        S3 = LC-2*(HH-Pivot)  #support level3
        #Log('r1',R1,"R2",R2,'R3',R3)
        #Log('S1',S1,"S2",S2,'S3',S3)
        To = records[-1]['Open'] #Today's opening price
        Th = records[-1]['High'] #Today's highest price
        Tl = records[-1]['Low'] #Today's Lowest Price
        current_price = _C(exchange.GetTicker).Last #Current Price

        #Current Price>resistance3   Open Position
        if current_price > R3: #Break above upper band to go long
            if my_buy(): #Log('Many')
                return

        #Current Price<support level3  Close Position
        if current_price < S3: #Break below lower band to go short
            if my_sell(): #Log('Empty')
                return

        # Condition 1 Today's highest price>Resistance2
        # Condition 2 Today's highest price <resistance3
        # Condition 3: current price < resistance1
        # Close position when all three conditions are met
        if Th >R2 and Th <R3 and current_price <R1: #Trend reversal sell
            if my_sell(): #Log('Empty')
                return

        # Condition 1 Today's lowest price <support level2
        # Condition 2 Today's lowest price>Support level3
        # Condition 3 Current price <support level1
        # Open position when all three conditions are met
        if Tl <S2 and Tl >S3 and current_price <S1: #support level1
            if my_buy(): #Log('Many')
                return
                # Log(records[-1])#TodayK
                # Log(records[-2])#YesterdayK
                # Log(exchange.GetTicker())#Current

    except Exception,ex:
        Log('except Exception onTick:',ex)



def main():
    global outAccount
    outAccount = ext.GetAccount()  #Initialization information
    Log("run  ",outAccount)  #Output initial account information
    while True:
        onTick()
        Sleep(1000)


```

> Detail

https://www.fmz.com/strategy/23531

> Last Modified

2016-10-28 19:37:57
