
> Name

Spot-Index-Balance-Strategy-V11-Used-to-Run-Live-Trading-for-a-While-But-Now-Suspected-of-a-Bug-Because-Its-No-Longer-Used-and-Im-Too-Lazy-to-Fix-It

> Author

GCC

> Strategy Description

Index balancing strategy Python version

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|symbols|BTC,ETH,BCH,LTC|trading pair|
|slip|0.03|Order slippage|
|percent|0.2,0.2,0.2,0.2|Value proportion of each trading pair|
|delta|0.01|Balance the difference by what level the difference reaches|
|Interval|2|Dormant Times|
|LogInterval|600|Profit update times|
|init_fund|-1|Initial capital|


> Source (python)

``` python

import json
import time
import requests
import math

account = 0  
updateProfitTime = 0 
tradeInfo = {} 
accountAssets = {}
ticker = {}
runtimeData = {}
Funding = 0

sbs = list(symbols.split(','))
pcts = list(percent.split(','))
for i in range(len(pcts)):
    pcts[i] = float(pcts[i])

p_dic = {
            'ETH':[2,4], 'BTC':[2,5], 'XRP':[4,0], 'TRX':[5,1], 'LTC':[1,3], 'BNB':[1,3]
         }    #Price and quantity precision, add as needed


SuccessColor = '#5cb85c' #Success color
DangerColor = '#ff0000' #Dangerous colors
WrningColor = '#f0ad4e' #Warning color

if IsVirtual():
    Log('Cannot perform backtest')
    exit()

if exchange.GetName() != 'Binance':
    Log('Only supports Binance spot exchange!')
    exit()

def init():
    exchangeInfo = requests.get('https://api.binance.com/api/v1/exchangeInfo').json()
    if exchangeInfo is None:
        Log('Unable to connect to Binance network, requires an overseas host!!!')
        exit()
    for x in range(len(exchangeInfo['symbols'])):
        for symbol in sbs:
            if exchangeInfo['symbols'][x]['symbol'] == symbol+'USDT':
                tradeInfo[symbol] = {'minQty': float(exchangeInfo['symbols'][x]['filters'][2]['minQty']) ,
                'priceSize': int((math.log10(1.1/float(exchangeInfo['symbols'][x]['filters'][0]['tickSize'])))),'amountSize': int((math.log10(1.1/float(exchangeInfo['symbols'][x]['filters'][2]['stepSize']))))}
    # Log('tradeInfo:',tradeInfo)

def UpdateAccount():
    global accountAssets,Funding,account
    acc = exchange.GetAccount()

    if acc is None:
        Log('Update account timeout!!!')
        return

    if _G('Funding') is None:
        Funding = acc['Balance']
        Log('Funding:',Funding)
        _G('Funding',Funding)
    else:
        Funding = _G('Funding')
    if init_fund >0:
        Funding = init_fund
    

    for x in range(len(acc['Info']['balances'])):
        for symbol in sbs:
            # Log(account['Info']['balances'])
            if acc['Info']['balances'][x]['asset'] == symbol:
                accountAssets[symbol] = acc['Info']['balances'][x]
                accountAssets[symbol]['amount'] = float(accountAssets[symbol]['free']) + float(accountAssets[symbol]['locked'])
            if acc['Info']['balances'][x]['asset'] == 'USDT':
                # Log('USDT:',acc['Info']['balances'][x])
                account = float(acc['Info']['balances'][x]['free']) + float(acc['Info']['balances'][x]['locked'])

    # Log('accountAssets:',accountAssets)

def UpdateTick():
    global ticker,account
    try:
        res = requests.get('https://api.binance.com/api/v3/ticker/bookTicker').json()
    except:
        Log('Market update timeout')
        return
    for x in range(len(res)):
        for symbol in sbs:
            if res[x]['symbol'] == symbol + 'USDT':
                # Log('res[x]:',res[x])
                ticker[symbol] = res[x]
                ticker[symbol]['price'] = (float(ticker[symbol]['askPrice']) + float(ticker[symbol]['bidPrice'])) / 2
                ticker[symbol]['value'] = accountAssets[symbol]['amount'] * ticker[symbol]['price']
    # Log('ticker:',ticker)
    # account = 0
    for symbol in sbs:
        account += _N(ticker[symbol]['value'],4)

def UpdateStatus():
    global updateProfitTime
    accountTable = {
        'type': "table",
        'title': "Profit statistics",
        'cols': ["Operating days", "Initial capital", "Existing capital", "Total income", "Estimated annualized profit", "Estimated monthly profit", "Average daily profit""],
        'rows': []
    }

    table = {
        'type': 'table',
        'title': 'Trading pair information',
        'cols': [''Number', 'Cryptocurrency Information', 'Proportion %', 'Opening Quantity', 'Current Price', 'Position Value''],
        'rows': []
    }
    totalProfit = account - Funding
    profitColors = DangerColor
    runday = runtimeData['dayDiff']
    if runday == 0:
        runday = 1
    if totalProfit > 0:
        profitColors = SuccessColor
    dayProfit = totalProfit / runday   #Average daily profit
    dayRate = totalProfit / Funding * 100
    accountTable['rows'].append([
    runday,
    Funding,
    account,
    str(_N(totalProfit / Funding * 100, 2)) + "% = $" + str(_N(totalProfit, 2)) + (profitColors),
    str(_N(dayRate * 365, 2)) + "% = $" + str(_N(dayProfit * 365, 2)) + (profitColors),
    str(_N(dayRate * 30, 2)) + "% = $" + str(_N(dayProfit * 30, 2)) + (profitColors),
    str(_N(dayRate, 2)) + "% = $" + str(_N(dayProfit, 2)) + (profitColors)
    ])

    i=1
    for symbol in sbs:
        table['rows'].append([
        i,
        symbol,
        str(_N(ticker[symbol]['value'] / account * 100, 4 )),
        str(_N(accountAssets[symbol]['amount'],tradeInfo[symbol]['amountSize'])),
        str(_N(ticker[symbol]['price'],tradeInfo[symbol]['priceSize'])),
        str(_N(ticker[symbol]['value'],4))
        ])
        i += 1

    retData = runtimeData['str'] + '\n' + "Last Update: " + _D() + '\n' + 'This strategy is adapted fromXMaxZoneExpert's spot balance strategy-0.0.1v,Original strategy URL:https://www.fmz.com/strategy/322357' + '\n'
    LogStatus(retData+ '`' + json.dumps(accountTable) + '`\n'+ '`' + json.dumps(table) + '`\n')

    if int(time.time()*1000) - updateProfitTime > LogInterval * 1000:
        balance = account - Funding
        LogProfit(_N(balance, 3))
        updateProfitTime = int(time.time()*1000)

def Process():
    # Log('Real-time funds:',account)
    for i in range(len(sbs)):
        pct = float(ticker[sbs[i]]['value']) / float(account)
        # Log(symbol,'amount:',amount,1 / len(sbs))
        if pct > (pcts[i] + delta):
            # Log('SELL',pct)
            amount = _N( ( (pct-pcts[i] ) * account / float(ticker[sbs[i]]['price'])),tradeInfo[sbs[i]]['amountSize'])
            if amount >= tradeInfo[sbs[i]]['minQty'] and float(amount)*float(ticker[sbs[i]]['value']) > 10:
                Log(sbs[i] ,'Funding:',Funding,'value:',ticker[sbs[i]]['value'])
                # Trade(sbs[i],'SELL',_N(float(ticker[sbs[i]]['askPrice']), int(tradeInfo[sbs[i]]['priceSize'])),  amount)
                exchange.SetCurrency(sbs[i]+'_USDT')
                exchange.SetPrecision(p_dic[sbs[i]][0], p_dic[sbs[i]][1])
                exchange.Sell(float(ticker[sbs[i]]['bidPrice'])*(1-slip), amount)
        if pct < (pcts[i] - delta):
            # Log('Buy', pct)
            amount = _N( ( (pcts[i]-pct ) * account / float(ticker[sbs[i]]['price'])),tradeInfo[sbs[i]]['amountSize'])
            if amount >= tradeInfo[sbs[i]]['minQty'] and float(amount)*float(ticker[sbs[i]]['value']) > 10:
                Log(sbs[i] ,'Funding:',Funding,'value:',ticker[sbs[i]]['value'])
                # Trade(sbs[i],'BUY',_N(float(ticker[sbs[i]]['bidPrice']), tradeInfo[sbs[i]]['priceSize']),  amount)
                exchange.SetCurrency(sbs[i]+'_USDT')
                exchange.SetPrecision(p_dic[sbs[i]][0], p_dic[sbs[i]][1])
                exchange.Buy(float(ticker[sbs[i]]['bidPrice'])*(1+slip), amount)

def StartTime():
    StartTime = _G('StartTime')
    if StartTime is None:
        StartTime = _D()
        _G('StartTime',StartTime)
    return StartTime

def RunTime():
    ret = {}
    startTime = StartTime()
    nowTime = _D()
    dateDiff = (time.mktime(time.strptime(nowTime,'%Y-%m-%d %H:%M:%S')) - time.mktime(time.strptime(startTime,'%Y-%m-%d %H:%M:%S')) ) * 1000  #Calculate the time difference
    dayDiff = math.floor(dateDiff / (24 * 3600 * 1000))
    lever1 = dateDiff % (24 * 3600 * 1000 )
    hours = math.floor(lever1 / (3600 * 1000))
    lever2 = lever1 % (3600 * 1000)
    minutes = math.floor(lever2 / (60 * 1000))

    ret['dayDiff'] = dayDiff
    ret['hours'] = hours
    ret['minutes'] = minutes
    ret['str'] = 'Running time:' + str(dayDiff) + 'Sky/Heaven' + str(hours) + 'Hour' + str(minutes) + 'Minute'
    return ret

def main():
    SetErrorFilter("502:|503:|tcp|character|unexpected|network|timeout|WSARecv|Connect|GetAddr|no such|reset|http|received|EOF|reused|Unknown")
    global runtimeData

    while True:
        runtimeData = RunTime()
        #Update account and positions
        UpdateAccount()
        #Update Quotes
        UpdateTick()
        #Main logic of strategy
        Process()
        #Update chart
        UpdateStatus()
        #Dormant Time
        Sleep(Interval * 1000)

```

> Detail

https://www.fmz.com/strategy/329093

> Last Modified

2021-12-04 20:53:35
