
> Name

bollmaboll

> Author

3piggy

> Strategy Description

Bollinger Bands breakout and retracement combined strategy
Signal for opening a position: The upper moving average of the Bollinger Band is golden cross, the Bollinger Band is enlarged, the middle track is upward, open long. Otherwise open short
Close position signal: Bollinger Bands narrowing, upper band moving average death cross
Reverse signal: Bollinger Band retracement

The signal is still being filtered

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|ma|13|matimeframe|
|bo|25|botimeframe|
|ma2|7|ma2timeframe|
|period|true|period|


> Source (python)

``` python
import numpy as np
import talib
import time
if period == 1:
	per = PERIOD_M1
if period == 2:
	per = PERIOD_M3
if period == 3:
	per = PERIOD_M5
if period == 4:
	per = PERIOD_M15
if period == 5:
	per = PERIOD_M30
if period == 6:
	per = PERIOD_H1
	
status=0 #Long: 1 Short:2

position = 0

def ontick():
	global position
	records = exchange.GetRecords(per)
	#------------Indicator calculation---------
	#rsi = TA.RSI(records,14)
	#if rsi[-1] > 65 or rsi[-1] < 35:
	#    return
	bb = talib.BBANDS(records.Close,timeperiod=bo, nbdevup=2, nbdevdn=2, matype=0) #CalculationBB
	rsi = talib.RSI(records.Close,timeperiod=12)
	cmi = talib.CMO(records.Close,timeperiod=12)
	print(cmi[-1])
	move = talib.SMA(records.Close,ma2)#Closing pricema
	mabt = talib.SMA(bb[0],ma)#Upper railma
	mabd = talib.SMA(bb[2],ma)#Kneelma
	account = exchange.GetAccount()

	

	if bb[0][-1] > mabt[-1] and bb[0][-2] < mabt[-2] and bb[2][-1] < bb[2][-2] and bb[1][-1] > bb[1][-2] and records.Close[-1] > move[-1] and rsi[-1]>60:
		position += 1
		exchange.Buy(-1,account.Balance*0.1)
		#log('Break Upward to Open Long '+ str(close[-1]))
	
	if bb[2][-1] < mabd[-1] and bb[2][-2] > mabd[-2] and bb[0][-1] > bb[0][-2] and bb[1][-1] < bb[1][-2] and records.Close[-1] < move[-1] and rsi[-1]<40:
		position -= 1
		exchange.Sell(-1,account.Stocks*0.1)
		#log('Break Downward to Open Short '+ str(close[-1]))
	
	if bb[0][-1]-bb[2][-1] < bb[0][-2]-bb[2][-2]:
		if bb[0][-1] < mabt[-1] and bb[0][-2] > mabt[-2] and position> 0:
			position -= 1
			exchange.Sell(-1,account.Stocks*0.1)
			#log('Close long positions '+ str(close[-1]))

		if bb[2][-1] > mabd[-1] and bb[2][-2] < mabd[-2] and position < 0:
			position += 1
			exchange.Buy(-1,account.Balance*0.1)
			#log('Close short position '+ str(close[-1]))

def main():
	while True:
		ontick()
		Sleep(30000)
```

> Detail

https://www.fmz.com/strategy/146391

> Last Modified

2020-04-23 16:46:09
