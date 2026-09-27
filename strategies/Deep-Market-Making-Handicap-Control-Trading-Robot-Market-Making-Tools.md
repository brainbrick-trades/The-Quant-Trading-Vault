
> Name

Deep-Market-Making-Handicap-Control-Trading-Robot-Market-Making-Tools

> Author

3piggy

> Strategy Description

The strategy for the exchange. The general strategy is to obtain the current price and at the same time place buy and sell orders to increase depth. You can copy other market trends and refer to other trends.



> Source (python)

``` python
# -*- coding: UTF-8 -*-
import requests
import time
import random
import hashlib
import sys
import threading
from api import *

symbol = sys.argv[1]
gap= float(sys.argv[2]) #Density/price difference
baseamount = float(sys.argv[3])
basebuy = float(sys.argv[4])
amount_add	= float(sys.argv[5]) 	#Pending order increment (numeric)(number)
amount_add2 = float(sys.argv[6]) 	#Pending order increment (numeric)(number)
longperoidlimit = int(sys.argv[7])
bigbase = float(sys.argv[8])				#Large order base quantity
orderlimit = int(sys.argv[9])   #total order volume
api_key = sys.argv[10]
secret_key = sys.argv[11]

shortperoidlimit = 3	#High-frequency order volume

pre_short_id = []	#High flat id marker
pre_long_id = []	#Low frequency id marker
pre_big_id = 0

requests.packages.urllib3.disable_warnings()

def GetTicker():

def GetPV():

def GetDepth():

def GetSign(sign_str):


def GetOrders():

def create_order(side,price,amount):

def CancelOrder(order_id):

def Buy(price,amount):

def Sell(price,amount):

def GetRecords(symbol,period):

def GetPrecision():

def getrr():

def ordersend_shortperoid():

def ordersend_longperoid():

def send_big_order():

def cancel():


if __name__ == '__main__':
	precision = GetPrecision()
	print(precision)
	i = 0
	for x in precision:
		if precision[i]['symbol'] == symbol:
			pricedot = precision[i]['price_precision']
			amountdot = precision[i]['amount_precision']
		i += 1
	pricegap =  max(gap,pow(10,-pricedot))
	threading_list = [ordersend_shortperoid,ordersend_longperoid,send_big_order,cancel]
	threadingList = []
	threadingDict = {}
	for x in threading_list:
		th = threading.Thread(target=x)
		threadingList.append(th)
		threadingDict[th.__dict__['_name']] = th.__dict__['_target']
		th.start()

	while True:
		try:
			time.sleep(200)
			for i in threadingList:
				if i.is_alive() is False:
					threadingList.remove(i)
					result = threadingDict.pop(i.name)
					th = threading.Thread(target=result)
					threadingList.append(th)
					threadingDict[th.__dict__['_name']] = th.__dict__['_target']
					th.start()
		except Exception as e:
			print('check error',e)
```

> Detail

https://www.fmz.com/strategy/146238

> Last Modified

2019-12-10 13:39:07
