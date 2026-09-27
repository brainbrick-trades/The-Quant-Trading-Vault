
> Name

MACD-Top-Escape-Strategy

> Author

program

> Strategy Description

**Introduction:** MACDSell and hold the currency when volume and price divergence
**Principle Implementation:** At the currentmacdThe value is used to start traversing forward to find one greater than the currentmacdValue index correspondencekLine closing price, lock the correspondingkLine price to current closing linekThe maximum value within the line range. If the current price is greater than the highest price in the area, selling is triggered.
Traverse macd data forward. When the maximum retained length is greater than 15, select the nearest macd maximum value.
 ![IMG](https://www.fmz.com/upload/asset/245a08277f17f12091cf4.png) 
**Backtest Data:** 
 ![IMG](https://www.fmz.com/upload/asset/245180e358693ba791ce0.png) 

**Explanation:** The strategy only supports spot trading and can run multiple currencies simultaneously,The source code is for reference only, please operate with caution during real operation.

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|num|0.1|Sell Quantity|


> Source (python)

``` python
'''backtest
start: 2023-01-01 00:00:00
end: 2023-05-12 00:00:00
period: 1d
basePeriod: 1h
exchanges: [{"eid":"Bitfinex","currency":"BTC_USD","stocks":10}]
'''


# from matplotlib import pyplot as plt
# plt.figure()

class ExitTop(object):
    def __init__(self,index):
        self.index = index 
        self.totestlist = [] # MACDData
        self.klist = [] # kLine Data
        self.toplus = []
        self.tocpn = []
        self.Sell = False
    
    # Get candlestick and MACD data
    def GetRecord(self) -> bool:
        self.totestlist = []
        self.klist = []
        self.toplus = []
        self.tocpn = []
        records = exchanges[self.index].GetRecords()
        macd = TA.MACD(records, 12, 26, 9)
        # Determine if DIF is greater thanDEA
        if not macd[0][-2] > macd[1][-2] and macd[0][-3] < macd[1][-3] or not macd[0][-2] > macd[1][-2] and macd[0][-4] < macd[1][-4]:
            return False
        self.totestlist = macd[0][len(macd[0])-80:]
        # Encapsulate candlestick data
        for get in range(len(records)):
            self.klist.append(records[get]["Close"])
        self.klist = self.klist[len(self.klist)-80:]
        return True
    
    def mepath(self):
        if not self.GetRecord():
            return False
        # Traverse forward to find the maximum value
        maxsign = -1000000000000
        for i in range(len(self.totestlist)-1,-1,-1):
            if self.totestlist[i] > maxsign:
                maxsign = self.totestlist[i]
                self.tocpn.append([1,i])
            else:
                if len(self.tocpn) > 0:
                    self.tocpn[-1][0] = self.tocpn[-1][0]+1
            self.toplus.insert(0,maxsign)
        sign = False
        shorttime = [0,0] # Step size, index
        for i in range(len(self.tocpn)):
            if self.tocpn[i][0] > 15 and sign == False:
                shorttime = [self.tocpn[i][0],self.tocpn[i][1]]
                sign = True
        # If the maximum index is not yourself
        if shorttime[1] < len(self.klist)-4:
            # Lock the highest price in the area
            are = max(self.klist[shorttime[1]:-4])
            # Check if there is a MACD value above the current one, and if the current price is above the highest price in the area
            if self.totestlist[-2]+300 < self.totestlist[shorttime[1]] and self.klist[-2] >= are:
                return True
            return False
        return False
    
    def main(self):
        result = self.mepath()
        if result == True and self.Sell == False:
            exchanges[self.index].Sell(-1, num)
            self.Sell = True
        elif result == False:
            if self.Sell == True:
                self.Sell = False
        # plt.plot(self.totestlist)
        # plt.plot(self.toplus)
        # LogStatus(plt)


def main():
    transaction = []
    for index in range(len(exchanges)):
        transaction.append(ExitTop(index))
    while True:
        for tran in range(len(transaction)):
            transaction[tran].main()
            Sleep(1000*60)
```

> Detail

https://www.fmz.com/strategy/356399

> Last Modified

2023-05-13 21:21:01
