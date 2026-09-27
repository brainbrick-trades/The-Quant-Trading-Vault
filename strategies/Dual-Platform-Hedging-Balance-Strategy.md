
> Name

Dual-Platform-Hedging-Balance-Strategy

> Author

ianzeng123

> Strategy Description

Reference master strategies for inspiration, please critique and point out mistakes.



> Source (python)

``` python
'''backtest
start: 2024-11-19 00:00:00
end: 2024-12-18 08:00:00
period: 1d
basePeriod: 1d
exchanges: [{"eid":"Binance","currency":"TRB_USDT"},{"eid":"OKX","currency":"TRB_USDT"}]
'''

import time
import json

# Global variable definition
depthA = depthB = None
timeBegin = timeEnd = None
askPriceA = bidPriceA = askAmountA = bidAmountA = 0
askPriceB = bidPriceB = askAmountB = bidAmountB = 0
minAmount = 20  # Minimum order quantity
feeA = 0.0020  # Huobi trading fee   
feeB = 0.0010  # Binance trading fee
fees = None
minProfit = 0.0002  # Minimum Profit
notDealAmountA = notDealAmountB = None
accountA = accountB = None
initAccountA = initAccountB = None
maxDeltaAmount = 100  # Maximum tolerable currency deviation
dealAmountA = 0
dealAmountB = 0
safeAmount = 800  # Safe maximum trading volume
profit = None
maxTime = 150  # Maximum delay filtering
accountBNB = None
reload = False

# Initialization function
def init():
    global fees, initAccountA, initAccountB, accountA, accountB

    try:
        fees = feeA + feeB

        initAccountA = _G("initAccountA")
        initAccountB = _G("initAccountB")
        
        if initAccountA is None or initAccountB is None:
            initAccountA = _C(exchanges[0].GetAccount)
            initAccountB = _C(exchanges[1].GetAccount)
            _G("initAccountA", initAccountA)
            _G("initAccountB", initAccountB)
            Log("Account initial value initialized successfully")
        else:
            Log("Successfully inherited initial value data")
        
        accountA = initAccountA
        accountB = initAccountB

    except Exception as e:
        Log("Initialization failed, please restart:", e)

# Normalized depth data
def legalize_depth(depthA, depthB):
    global askPriceA, bidPriceA, askAmountA, bidAmountA
    global askPriceB, bidPriceB, askAmountB, bidAmountB

    askPriceA = bidPriceA = askAmountA = bidAmountA = 0
    askPriceB = bidPriceB = askAmountB = bidAmountB = 0

    for ask in depthA[0]["Asks"]:
        askPriceA = ask["Price"]
        askAmountA += ask["Amount"]
        if askAmountA >= minAmount:
            break

    for bid in depthA[0]["Bids"]:
        bidPriceA = bid["Price"]
        bidAmountA += bid["Amount"]
        if bidAmountA >= minAmount:
            break

    for ask in depthB[0]["Asks"]:
        askPriceB = ask["Price"]
        askAmountB += ask["Amount"]
        if askAmountB >= minAmount:
            break

    for bid in depthB[0]["Bids"]:
        bidPriceB = bid["Price"]
        bidAmountB += bid["Amount"]
        if bidAmountB >= minAmount:
            break

# Cancel all pending orders
def cancel_all_orders():
    global dealAmountA, dealAmountB

    orders = _C(exchanges[0].GetOrders)
    for order in orders:
        exchanges[0].CancelOrder(order["Id"])
        Log("Transaction:", order["DealAmount"], "unfilled:", order["Amount"] - order["DealAmount"])
        dealAmountA -= order["Amount"] - order["DealAmount"]

    orders = _C(exchanges[1].GetOrders)
    for order in orders:
        exchanges[1].CancelOrder(order["Id"])
        Log("Transaction:", order["DealAmount"], "unfilled:", order["Amount"] - order["DealAmount"])
        dealAmountB -= order["Amount"] - order["DealAmount"]

# Check balance
def check_balance():
    global accountA, accountB, dealAmountA, dealAmountB

    cancel_all_orders()
    deltaStocks = (initAccountA["Stocks"] + initAccountA["FrozenStocks"] + initAccountB["Stocks"] + initAccountB["FrozenStocks"]
        - accountA["Stocks"] - accountA["FrozenStocks"] - accountB["Stocks"] - accountB["FrozenStocks"])

    deltaStocks = round(deltaStocks, 0)

    if deltaStocks < -maxDeltaAmount:  # Position is too heavy
        if askPriceA > askPriceB and accountA["Stocks"] > -deltaStocks:
            exchanges[0].Sell(askPriceA, -deltaStocks)
            dealAmountA += -deltaStocks
        else:
            exchanges[1].Sell(askPriceB, -deltaStocks)
            dealAmountB += -deltaStocks
        return True

    if deltaStocks > maxDeltaAmount:  # Position is too light
        if bidPriceA < bidPriceB and accountA["Balance"] * 0.999 / bidPriceA > deltaStocks:
            exchanges[0].Buy(bidPriceA, deltaStocks)
            dealAmountA += deltaStocks
        else:
            exchanges[1].Buy(bidPriceB, deltaStocks)
            dealAmountB += deltaStocks
        return True

    return False

# Update profit
def update_profit():
    global profit

    profit = (
        accountA["Balance"] + accountB["Balance"] + accountA["FrozenBalance"] + accountB["FrozenBalance"]
        + (accountA["Stocks"] + accountA["FrozenStocks"] + accountB["Stocks"] + accountB["FrozenStocks"]
        - initAccountA["Stocks"] - initAccountA["FrozenStocks"] - initAccountB["Stocks"] - initAccountB["FrozenStocks"]) * askPriceA
        - (initAccountA["Balance"] + initAccountA["FrozenBalance"] + initAccountB["Balance"] + initAccountB["FrozenBalance"]))

    return profit

# Check for arbitrage opportunities
def check_opportunity():
    global dealAmountA, dealAmountB, accountA, accountB, diff_A, diff_B 

    diff_A = bidPriceB - askPriceA  # ABuy on Exchange -> Sell on Exchange B
    diff_B = bidPriceA - askPriceB  # BBuy on Exchange -> Sell on Exchange A

    if diff_A > 0 and diff_A > (minProfit + fees) * askPriceA:
        maxBuyAmount = min(accountA["Balance"] / askPriceA * 0.98, askAmountA)
        maxSellAmount = min(accountB["Stocks"], bidAmountB)
        amount = min(maxBuyAmount, maxSellAmount, safeAmount)
        amount = round(amount, 0)

        if amount >= minAmount:
            Log("huobi -> binance", amount)
            exchanges[0].Buy(askPriceA, amount)
            exchanges[1].Sell(bidPriceB, amount)
            time.sleep(3)
            dealAmountA += amount
            dealAmountB += amount
            accountA = _C(exchanges[0].GetAccount)
            accountB = _C(exchanges[1].GetAccount)
            Log("Profit Update:", update_profit())

    if diff_B > 0 and diff_B > (minProfit + fees) * askPriceB:
        maxBuyAmount = min(accountB["Balance"] / askPriceB * 0.98, askAmountB)
        maxSellAmount = min(accountA["Stocks"], bidAmountA)
        amount = min(maxBuyAmount, maxSellAmount, safeAmount)
        amount = round(amount, 0)

        if amount >= minAmount:
            Log("binance -> huobi", amount)
            exchanges[1].Buy(askPriceB, amount)
            exchanges[0].Sell(bidPriceA, amount)
            time.sleep(3)
            dealAmountA += amount
            dealAmountB += amount
            accountA = _C(exchanges[0].GetAccount)
            accountB = _C(exchanges[1].GetAccount)
            Log("Profit Update:", update_profit())

def main():
    global initAccountA, initAccountB
    if reload == True:
        initAccountA = _C(exchanges[0].GetAccount)
        initAccountB = _C(exchanges[1].GetAccount)
        _G("initAccountA", initAccountA)
        _G("initAccountB", initAccountB)

    init()

    checkBalanceCount = 60
    
    while True:
        accountA = exchanges[0].GetAccount()
        accountB = exchanges[1].GetAccount()
        timeBegin = int(time.time() * 1000)
        depthA = exchanges[0].Go("GetDepth")
        depthB = exchanges[1].Go("GetDepth")
        depthA = depthA.wait()
        depthB = depthB.wait()
        
        timeEnd = int(time.time() * 1000)
        # Real trading, remove comments at lines 205-208
        #if timeEnd - timeBegin > maxTime:
        #    continue  # Abandon the current data set if the delay exceeds maxTime milliseconds
        #if depthA is None or depthB is None or accountA is None or accountB is None:
        #    continue

        legalize_depth(depthA, depthB)

        if checkBalanceCount >= 60:
            checkBalanceCount = 0
            if check_balance():
                continue
        else:
            checkBalanceCount += 1
        
        check_opportunity()
        
        # Data visualization operation
        table = {
            'type': 'table',
            'title': 'Position operation',
            'cols': ['Exchange', 'Initial balance', 'Initial number of coins', 'Current balance', 'Current number of coins', 'Trading volume'],
            'rows': [
                ['huobi', initAccountA.Balance + initAccountA.FrozenBalance, initAccountA.Stocks + initAccountA.FrozenStocks,
                    accountA.Balance + accountA.FrozenBalance, accountA.Stocks + accountA.FrozenStocks, dealAmountA],
                ['binance', initAccountB.Balance + initAccountB.FrozenBalance, initAccountB.Stocks + initAccountB.FrozenStocks,
                    accountB.Balance + accountB.FrozenBalance, accountB.Stocks + accountB.FrozenStocks, dealAmountB],
                ['Total', initAccountA.Balance + initAccountB.Balance, initAccountA.Stocks + initAccountB.Stocks,
                    accountA.Balance + accountA.FrozenBalance + accountB.Balance + accountB.FrozenBalance,
                    accountA.Stocks + accountA.FrozenStocks + accountB.Stocks + accountB.FrozenStocks, dealAmountA + dealAmountB],
                ['huobiMarket Depth', askPriceA, askAmountA, bidPriceA, bidAmountA, ''],
                ['binanceMarket Depth', askPriceB, askAmountB, bidPriceB, bidAmountB, ''],
                ['Revenue:', str(_N(update_profit(), 8)) + '#FF0000',  '', '', ''],
                ['Yield', str(_N(100 * profit / (initAccountA.Balance + initAccountA.FrozenBalance + initAccountB.Balance + initAccountB.FrozenBalance), 6)) + '%' + '#FF0000', '', '', '', ''],
                ['Total Delay', timeEnd - timeBegin, '', '', '', ''],
                ['Last update time', _D(), '', '', '', ''],
            ]
        }
        LogStatus('`' + json.dumps(table) + '`')

        time.sleep(10)
        

```

> Detail

https://www.fmz.com/strategy/472020

> Last Modified

2024-12-20 16:29:13
