
> Name

Dynamic-Balancing-Strategy-Python-Version

> Author

teddy





> Source (python)

``` python

# !usr/bin/ python3
# *_* coding:utf-8 *_*
#LearnpythonThe first dynamic balance strategy written later
# QQ:5325049 Comments on shortcomings are welcome

import time

#Define functions to get market data and account information
def nowinfo(): 
    global NowTicker,NowAsset,NowCoinValue,AssetDiff
    NowTicker = exchange.GetTicker() #Get market information
    NowAsset = exchange.GetAccount() # Get account information
    NowCoinValue =NowTicker.Last * NowAsset.Stocks #Calculate coin asset net value
    AssetDiff = NowCoinValue-NowAsset.Balance #Calculate the difference between crypto assets and cash

# Define trade execution function
def trade():
    if AssetDiff > NowAsset.Balance*0.05: # Determine if the coin value exceeds funds5%
        Log("The trade will be executed to",NowTicker.Buy,"sell",AssetDiff/2/NowTicker.Buy,"Currency")
        exchange.SetPrecision(5,5) #Set pricing precision
        exchange.Sell(NowTicker.Buy,AssetDiff/2/NowTicker.Buy) #Execute coin sell trade
    elif AssetDiff < NowAsset.Balance*(-0.05): #Determine if the coin value is below funds5%
        Log("The trade will be executed to",NowTicker.Sell,"buy",AssetDiff/-2/NowTicker.Sell,"Currency")
        exchange.SetPrecision(5,5) #Set pricing precision
        exchange.Buy(NowTicker.Sell,AssetDiff/-2/NowTicker.Sell) #Execute coin buy trade
    else:
        Log("Trading conditions not triggered")

# Entry function, as long as it is defined, the system will automatically execute the function, no need to call it
def main():
    i = 0
    while i < 1000: #Set total execution count
        nowinfo() # Call function to get market asset data
        Log(NowTicker) # Print market information
        Log(NowAsset) # Print account information
        Log("Current coin balance:",NowAsset.Stocks)
        Log("Current account balance:",NowAsset.Balance)
        Log("Current coin market value:", NowCoinValue)
        Log("Difference between coin market value and funds:",AssetDiff)
        trade() #Call transaction execution function
        i+=1 # Conditional Iteration
        Log("No.", i, "End of loop")
        time.sleep(60) # Wait60second


```

> Detail

https://www.fmz.com/strategy/152830

> Last Modified

2019-06-22 18:35:30
