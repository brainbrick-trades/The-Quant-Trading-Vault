
> Name

Keltner-Channel-Breakout-Stop-Loss-Plus-Profit-10-I.e.-Long-Term-Holding-Strategy-V23-Dev-Multi-Cycle

> Author

nanpian

> Strategy Description

A long strategy to buy Btc spot, the original amount is 1000 usdt in cash.
Check every hour to see if it breaks through the keltner channel. If it breaks through, go long.
Launch Strategy:
1,If you lose 6%, stop the loss directly;
2,If it falls below the MA moving average, sell directly;
3,If you make a profit of 10%, use it as a protective cushion and go long directly. If you encounter a continuous drop of 10% in the past 24 hours, it means there is an emergency, so you can stop the loss directly.

Using this strategy in live trading myself, the backtest results are pretty good.
In fact, the essence is to lose less and make more.



> Source (python)

``` python
'''
start: 2020-01-01 00:00:00
end: 2020-04-24 00:00:00
period: 1h
exchanges: [{"eid":"huobi","currency":"BTC_USDT","stocks":0,"meta":{"AccessKey":"7yngd7gh5g-a7ed9b1a-c05064c3-bab33","SecretKey":"553c2cd1-e229e1d2-25a536cb-db7d3"}}]
'''

import talib as ta
import pandas as pd
from datetime import datetime
from datetime import timedelta
import math
#coding:utf8
import sys

eid = -1
last_price = -1

def main():
    global eid
    global last_price
    global ma

    while True:

        records = exchange.GetRecords(1*60*60)
        e = exchange
        kline1 = pd.DataFrame(records)
        kline1['Time'] = kline1['Time'].map(lambda x: datetime.utcfromtimestamp(x/1000)+timedelta(hours=8))
        kline1.columns = ['time','open','high','low','close','volume','oi']
       
        r = kline1
        #Log('LatestkLine Time',r.iloc[-1].time, ' Latest price closing price', r.iloc[-1].close)
    
        leadLine1 = ta.EMA(r.close, 30)
        leadLine2 = ta.SMA(r.close, 30)
        UT=leadLine2 < leadLine1
        DT=leadLine2 > leadLine1
    
        # keltner channel
        ma  = ta.EMA(kline1.close, 80)
        # Real range function
        range1 = ta.TRANGE(kline1.high, kline1.low, kline1.close)
        rangema = ta.EMA(range1, 80)
        upper = ma + 3*rangema
        lower = ma - 3*rangema
       
        # minus and plus of adx/dmi
        minus = ta.MINUS_DI(kline1.high,kline1.low, kline1.close,14) 
        plus = ta.PLUS_DI(kline1.high, kline1.low, kline1.close ,14)
                   
        volume0 = r.iloc[-1].volume
        volume1 = r.iloc[-2].volume
        rn = r.iloc[-1]
       
        entry_long = rn.close > upper.iloc[-1] and (r.iloc[-1].volume+ r.iloc[-2].volume) >1.5 *(r.iloc[-4].volume+ r.iloc[-5].volume)
        long = entry_long
        exit_long = (rn.close < ma.iloc[-1] )
        account = exchange.GetAccount()
        amount = account.Stocks
        #Log('Balance is ', account['Balance'], ' Btc amount is ', amount)
        # If in short position status
        if (account['Balance'] >= 600 and amount < 0.001):
            if long==True and account['Balance'] < 400 and amount<0.01:
                Log('balance is ', account['Balance'], ' Insufficient Balance400,Exit!')
                return
            elif long== True  and account['Balance'] >= 600: #First long position open
                Log('balance is ', account['Balance'])
                Log('Multi position time: ', rn.time, ' open is ', rn.open , ' close is ', rn.close, ' upper is ', upper.iloc[-1], ' volume 0\1 is', volume0 , 'volume 1 is ', volume1 , 
                ' plus is ',plus.iloc[-1], ' minus is ', minus.iloc[-1], '@')
                exchange.Buy(-1,600)
                last_price = rn.close + 10
                Sleep(1000*60*15)
        # If the position is open
        if  amount>0.001 :
            if  amount > 0.0001 and rn.close <= last_price*0.94: 
                Log('Stop-loss close event: ','balance is ', account['Balance'], rn.time, ' rn.close is ', rn.close, ' @')
                id = exchange.Sell(-1, amount);
                account = exchange.GetAccount()
                amount = account.Stocks
                Log('Balance is ', account['Balance'], ' Btc amount is ', amount)
                eid = -1
       #Only sell if in a continuous holding and sharp drop situation
            elif  amount > 0.0001 and rn.close >= last_price * 1.1 and rn.close <= r.iloc[-24].close*0.9:
                Log('Stop-loss closing event during a major drop in the holding period: ', rn.time, ' rn.close is ', rn.close, ' @')
                id = exchange.Sell(-1, amount);
                eid = -1
                account = exchange.GetAccount()
                amount = account.Stocks
                Log('Balance is ', account['Balance'], ' Btc amount is ', amount)
            elif amount > 0.0001 and exit_long == True :
                if rn.close <= last_price:
                    Log('Position trailing stop event,Loss:  amount is ',amount ,' time is ', rn.time, ' Price is:',rn.close,' ma is ', ma.iloc[-1], ' Opening price',last_price,' Loss Range:',100*(last_price -rn.close)/last_price ,'% @')
                    eid = exchange.Sell(-1, amount)
#                print(r.tail(10))
#                print('ma is ' ,ma)
                    account = exchange.GetAccount()
                    amount = account.Stocks
                    Log('Balance is ', account['Balance'], ' Btc amount is ', amount)
                elif rn.close > last_price*1.1 :
                    Log('Exceed10%Profit continue holding')
                    account = exchange.GetAccount()
                    amount = account.Stocks
                    Log('Balance is ', account['Balance'], ' Btc amount is ', amount)
                    return 
                elif rn.close > last_price  and rn.close <=last_price*1.1:
                    eid = exchange.Sell(-1, amount);
                    account = exchange.GetAccount()
                    amount = account.Stocks
                    Log('Balance is ', account['Balance'], ' Btc amount is ', amount)
                    Log('Position trailing stop event,Making money: amount is ',amount, ' time is ', rn.time, ' Price is: ',rn.close,' ma is ', ma.iloc[-1],' Opening price',last_price,' Profit Range:',100*(rn.close-last_price )/last_price ,'% @' )
                else:
                    id = exchange.Sell(-1, amount);
                    Log('The final position fell and the position was closed.,Making money: amount is ',amount, ' time is ', rn.time, ' Price is: ',rn.close,' ma is ', ma.iloc[-1],' Opening price',last_price,' Profit Range:',100*(rn.close-last_price )/last_price ,'% @' )
                    eid = -1
                    account = exchange.GetAccount()
                    amount = account.Stocks
                    Log('Balance is ', account['Balance'], ' Btc amount is ', amount)
            Sleep(1000*60*15)

```

> Detail

https://www.fmz.com/strategy/313041

> Last Modified

2021-09-02 12:04:56
