
> Name

Spot-Balancing-Strategy-001v

> Author

XMaxZone

> Strategy Description

We select four mainstream currencies BTC, ETH, LTC, and XRP, allocate 25% of the market value respectively, and balance every 1% deviation.

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|symbols|BTC,ETH,BCH,LTC|trading pair|
|Interval|2|Dormant Times|
|LogInterval|600|Profit update times|


> Source (python)

``` python


import time
import requests
import math

account = 0          #Save user assets
updateProfitTime = 0   #Update the interval time for return rate
tradeInfo = {}         #save trading pair information
accountAssets = {}
ticker = {}
runtimeData = {}
Funding = 0   #Automatically retrieve when the account balance is 0
Version = '0.0.1'
sbs = list(symbols.split(','))


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
    if _G('Funding') is None:
        Funding = account['Balance']
        Log('Funding:',Funding)
        _G('Funding',Funding)
    else:
        Funding = _G('Funding')

    if account is None:
        Log('Update account timeout!!!')
        return

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

def Trade(symbol,direction,price,amount):
    if amount < tradeInfo[symbol]['minQty']:
        Log(symbol,'The contract value deviates or the iceberg order setting is too small, the minimum transaction amount cannot be reached, and the minimum required:', _N(tradeInfo[symbol]['minQty'] * price,4) + 1)
    else:
        para = ''
        url = '/api/v3/order'
        para += 'symbol='+ symbol +'USDT'
        para += '&side='+ direction
        para += '&type=LIMIT&timeInForce=IOC'
        para += '&quantity='+ str(amount)
        para += '&price='+ str(price)
        para += '&timestamp='+str(time.time() * 1000);
        go = exchange.Go("IO", "api", "POST", url, para)
        ret = go.wait()
        if ret  is not None:
            logType = LOG_TYPE_SELL
            if direction == 'BUY':
                logType =LOG_TYPE_BUY
            exchange.Log(logType,price,amount,symbol)

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

    retData = runtimeData['str'] + '\n' + "Last Update: " + _D() + '\n' + 'Version:' + Version  + '\n'
    LogStatus(retData+ '`' + json.dumps(accountTable) + '`\n'+ '`' + json.dumps(table) + '`\n')


    if int(time.time()*1000) - updateProfitTime > LogInterval * 1000:
        balance = account - Funding
        LogProfit(_N(balance, 3))
        updateProfitTime = int(time.time()*1000)

def Process():

    # Log('Real-time funds:',account)
    for symbol in sbs:

        pct = float(ticker[symbol]['value']) / float(account)
        # Log(symbol,'amount:',amount,1 / len(sbs))
        if pct > (1 / len(sbs) + 0.015):
            # Log('SELL',pct)
            Log(symbol ,'Funding:',Funding,'value:',ticker[symbol]['value'])
            amount = _N( ( (pct-1/len(sbs) ) * account / float(ticker[symbol]['price'])),tradeInfo[symbol]['amountSize'])
            Trade(symbol,'SELL',_N(float(ticker[symbol]['askPrice']), int(tradeInfo[symbol]['priceSize'])),  amount)
        if pct < (1 / len(sbs) - 0.015):
            # Log('Buy', pct)
            Log(symbol ,'Funding:',Funding,'value:',ticker[symbol]['value'])
            amount = _N( ( (1/len(sbs)-pct ) * account / float(ticker[symbol]['price'])),tradeInfo[symbol]['amountSize'])
            Trade(symbol,'BUY',_N(float(ticker[symbol]['bidPrice']), tradeInfo[symbol]['priceSize']),  amount)



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

https://www.fmz.com/strategy/322357

> Last Modified

2021-10-10 20:50:05
