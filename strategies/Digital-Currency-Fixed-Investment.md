
> Name

Digital-Currency-Fixed-Investment

> Author

ankye

> Strategy Description

Universal fixed investment strategy for digital currencies, supporting simultaneous fixed investment on multiple exchanges

# Parameter description
orderAmount #Fixed investment amount: BTCCNY and BCCCNY in CNY, BCCBTC in BTC, etc.

accountLimitMoney #Account limit: keep some money. When the account reaches the minimum limit, stop fixed investment


orderTimeInterval #Regular casting interval, in seconds, per minute = 60 Per hour = 3600 per day = 86400 per week=604800

maxBidPrice  #Maximum trading price. Skip if exceeded, wait for the next trading opportunity

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|orderAmount|true|order amount|
|maxBidPrice|false|max bid price|
|accountLimitMoney|false|account limit money|
|orderTimeInterval|60|Order Time Interval|


> Source (python)

``` python
def onTick():
	
	exchange_count = len(exchanges)
	for i in range(exchange_count):
		account = exchanges[i].GetAccount()

		marketName = exchanges[i].GetName()
		depth = exchanges[i].GetDepth()
		Log("Market ",marketName,exchanges[i].GetCurrency(),"Account Balance [",account["Balance"],"] Stocks[",account["Stocks"],"]")
		if account and depth and account["Balance"] > accountLimitMoney :
			bidPrice = depth["Asks"][0]["Price"] 
			if bidPrice <  maxBidPrice :
				amount = orderAmount
				if amount <= account["Balance"]:
					exchanges[i].Buy(amount)
				else:
					Log("Account Balance is less than bid Amount")
			else:
				Log("Bid Price >= maxBidPrice, not process")
		else:
			Log("Account Balance <= accountLimitMoney")
def main() :
	while 1:
		
		onTick()
		time.sleep(orderTimeInterval)
```

> Detail

https://www.fmz.com/strategy/54256

> Last Modified

2017-09-08 14:43:38
