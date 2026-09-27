
> Name

Binance-Futures-Grid-Basic-Version-001

> Author

XMaxZone

> Strategy Description

When the strategy is started for the first time, the initial price will be recorded. Later, orders will be placed on this base price. If the price is greater than the base price, the order will be short. If the price is less than the base price, the order will be long.,
This is the basic version. If you have other needs, you can modify it yourself or contact me.

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|value|150|Opening value|
|pct|0.01|Grid interval|
|Show|true|Yes: Display income, No: Display total account|
|Interval|2|Dormant Time|
|LogInterval|600|Update time of profit curve(s)|


> Source (python)

``` python
# I just started learning python, so I apologize for any inaccuracies.!!!
import time
import requests
import math
import pandas as pd

InitPrice = 0
updateProfitTime = 0
assets = {}
tradeInfo = {}
accountAssets = {}
runtimeData = {}
Funding = 0   #Automatically retrieve when the account balance is 0
symbol = ''
Version = '0.0.1'
SuccessColor = '#5cb85c' #Success color
DangerColor = '#ff0000' #Dangerous colors
WrningColor = '#f0ad4e' #Warning color

assets['USDT'] = {'unrealised_profit':0,'margin':0,'margin_balance':0,'total_balance':0,'leverage':0,'update_time':0,'margin_ratio':0,'init_balance':0,'profit':0}


if IsVirtual():
    Log('Cannot perform backtest')
    exit()

if exchange.GetName() != 'Futures_Binance':
    Log('Only supports Binance futures exchange!')
    exit()

def init():
    initData()
    CancelOrder()
    exchangeInfo = requests.get('https://fapi.binance.com/fapi/v1/exchangeInfo').json()
    if exchangeInfo is None:
        Log('Unable to connect to Binance network, requires overseas hosting')
        exit()
    for i in range(len(exchangeInfo['symbols'])):
        if exchangeInfo['symbols'][i]['symbol'] == symbol:
            assets[symbol] = {'amount': 0,'hold_price': 0,'value': 0,'bid_price': 0,'ask_price': 0,'realised_profit': 0,'margin': 0,'unrealised_profit': 0,
            'leverage': 20, 'positionInitialMargin': 0,  'liquidationPrice': 0 }
            tradeInfo[symbol] = {'minQty': float(exchangeInfo['symbols'][i]['filters'][1]['minQty']) ,
            'priceSize': int((math.log10(1.1/float(exchangeInfo['symbols'][i]['filters'][0]['tickSize'])))),'amountSize': int((math.log10(1.1/float(exchangeInfo['symbols'][i]['filters'][1]['stepSize']))))}

def CancelOrder():
    exchange.SetContractType('swap')
    #Cancel all unfilled orders
    orders = exchange.GetOrders()
    for x in range(len(orders)):
        if orders[x]['Info']['symbol'] == symbol :
            exchange.CancelOrder(orders[x]['Id'])

def UpdateStatus():
    global Funding,updateProfitTime
    if Funding == 0 :
        Funding = float(FirstAccount()['Info']['totalWalletBalance'])   #Get initial funds
    # totalProfit = assets['USDT']['total_balance'] - Funding             #Calculate income

    accountTable = {
        'type': "table",
        'title': "Profit statistics",
        'cols': ["Operating days", "Initial funds", "Existing funds", "Margin balance", "Used margin", "Margin ratio", "Total income", "Estimated annualized", "Estimated monthly", "Average daily"],
        'rows': []
    }
    table = {
        'type': 'table',
        'title': 'Trading pair information',
        'cols': ['Number', '[Mode][Multiple]', 'Currency information', 'Opening direction', 'Opening quantity', 'Position price', 'Current price', 'Liquidation price', 'Position value', 'Margin', 'Unrealized profit and loss''],
        'rows': []
    }

    profitColors = DangerColor
    totalProfit = assets['USDT']['total_balance'] - Funding
    runday = runtimeData['dayDiff']
    if runday == 0:
        runday = 1
    if totalProfit > 0:
        profitColors = SuccessColor
    dayProfit = totalProfit / runday
    dayRate = dayProfit / Funding * 100


    accountTable['rows'].append([
        runday,
        '$' + str(_N(Funding, 2)),
        '$' + str(assets['USDT']['total_balance']),
        '$' + str(assets['USDT']['margin_balance']),
        '$' + str(assets['USDT']['margin']),
        str(_N(assets['USDT']['margin_ratio'], 2)) + '%',
        str(_N(totalProfit / Funding * 100, 2)) + "% = $" + str(_N(totalProfit, 2)) + (profitColors),
        str(_N(dayRate * 365, 2)) + "% = $" + str(_N(dayProfit * 365, 2)) + (profitColors),
        str(_N(dayRate * 30, 2)) + "% = $" + str(_N(dayProfit * 30, 2)) + (profitColors),
        str(_N(dayRate, 2)) + "% = $" + str(_N(dayProfit, 2)) + (profitColors)
    ])


    i = 1
    for x in list(symbol.split(',')):
        
        direction = 'Short position'
        margin = direction
        if assets[x]['amount'] != 0:
            direction = 'go long' + SuccessColor if assets[symbol]['amount'] > 0 else 'go short' + DangerColor
            margin = 'Cross position' if assets[symbol]['marginType'] == 'cross' else 'Isolated position'
        unrealised_profit_color = '#000000'
        if assets[symbol]['unrealised_profit'] > 0:
            unrealised_profit_color = SuccessColor
        if assets[symbol]['unrealised_profit'] < 0:
            unrealised_profit_color = DangerColor

        infoList = [
        i,
        '['+margin+']'+'['+str(assets[x]['leverage'])+']',
        x,
        direction,
        assets[x]['amount'],
        assets[x]['hold_price'],
        assets[x]['price'],
        assets[x]['liquidationPrice'],
        float(assets[x]['amount']) * float(assets[x]['price']),
        assets[x]['positionInitialMargin'],
        assets[x]['unrealised_profit'],
        ]
        table['rows'].append(infoList)

        retData = runtimeData['str'] + '\n' + "Last Update: " + _D() + '\n' + 'Version:' + Version  + '\n'
        LogStatus(retData+ '`' + json.dumps(accountTable) + '`\n'+ '`' + json.dumps(table) + '`\n')

    if int(time.time()*1000) - updateProfitTime > LogInterval * 1000:
        balance = assets['USDT']['total_balance']
        key = "initialAccount_" + exchange.GetLabel()
        initialAccount = _G(key)
        #Log('balance:',balance,'Funding:',Funding,'initialAccount:',initialAccount['Info']['totalWalletBalance'])
        if Show:
            balance = assets['USDT']['total_balance'] - Funding
        LogProfit(_N(balance, 3))
        updateProfitTime = int(time.time()*1000)
        Profit = _N(balance,0)


def UpdateAccount():
    # Log('UpdateAccount()')
    global accountAssets
    account = exchange.GetAccount()
    position = exchange.GetPosition()
    if account is None and position is None :
        Log('Update account timeout!!!')
        return
    accountAssets = account['Info']['assets']
    assets['USDT']['update_time'] = int(time.time()) * 1000  #Convert seconds to milliseconds and update account time synchronously
    for  i in range(len(account['Info']['positions'])) :
        if account['Info']['positions'][i]['symbol'] == symbol :
            #Calculate position margin Initial margin                +            Maintenance margin
            assets[symbol]['margin'] = float(account['Info']['positions'][i]['initialMargin']) + float(account['Info']['positions'][i]['maintMargin'])
            #Unrealized gains
            assets[symbol]['unrealised_profit'] = float(account['Info']['positions'][i]['unrealizedProfit'])
            assets[symbol]['positionInitialMargin'] = float(account['Info']['positions'][i]['positionInitialMargin'])
            assets[symbol]['leverage'] = account['Info']['positions'][i]['leverage']

    #Calculate the total margin of positions
    assets['USDT']['margin'] = float(account['Info']['totalInitialMargin']) + float(account['Info']['totalMaintMargin'])
    assets['USDT']['margin_balance'] = float(account['Info']['totalMarginBalance'])
    assets['USDT']['total_balance'] = float(account['Info']['totalWalletBalance'])

    ps = json.loads(exchange.GetRawJSON())
    if len(ps) > 0 :
        for x in range(len(ps)):
            if ps[x]['symbol'] == symbol:
                assets[symbol]['hold_price'] = float(ps[x]['entryPrice'])
                assets[symbol]['amount'] = float(ps[x]['positionAmt'])
                assets[symbol]['unrealised_profit'] = float(ps[x]['unRealizedProfit'])
                assets[symbol]['liquidationPrice'] = float(ps[x]['liquidationPrice'])
                assets[symbol]['marginType'] = ps[x]['marginType']

def UpdateTick():
    global InitPrice
    try:
        res = requests.get(f'https://fapi.binance.com/fapi/v1/ticker/price?symbol={symbol}').json()
    except:
        Log('get ticker time out !')
        return

    if target:
        InitPrice = target_price
        _G('InitPrice',InitPrice)
    else:
        if  _G('InitPrice') is None :
            InitPrice = res['price']
            _G('InitPrice',InitPrice)
        else:
            InitPrice = _G('InitPrice')

    assets[symbol]['price'] = res['price']

def Trade(direction,price,amount):
    if amount < tradeInfo[symbol]['minQty']:
        Log(symbol,'The contract value deviates or the iceberg order setting is too small, the minimum transaction amount cannot be reached, and the minimum required:', _N(tradeInfo[symbol]['minQty'] * price,4) + 1)
    else:
        para = ''
        url = '/fapi/v1/order'
        para += 'symbol='+ symbol
        para += '&side='+ direction
        para += '&type=LIMIT&timeInForce=GTC'
        para += '&quantity='+ str(amount)
        para += '&price='+ str(price)
        para += "&timestamp="+str(time.time() * 1000);
        go = exchange.Go("IO", "api", "POST", url, para)
        ret = go.wait()
        if ret  is not None:
            logType = LOG_TYPE_SELL
            if direction == 'BUY':
                logType =LOG_TYPE_BUY
            exchange.Log(logType,price,amount,symbol)

def batch(buy_price,sell_price):
    exchange.SetContractType('swap')
    #Cancel all unfilled orders
    orders = exchange.GetOrders()
    if len(orders) < 2 :
        return True
    return False

def Process():

    buy_price = (value / pct - value) / ((value / pct) / float(InitPrice) + assets[symbol]['amount'])
    sell_price = (value / pct + value) / ((value / pct) / float(InitPrice) + assets[symbol]['amount'])

    if float(buy_price) > float(assets[symbol]['price']) or float(sell_price) < float(assets[symbol]['price']) or batch(buy_price,sell_price):
        CancelOrder()
        Trade('BUY', _N(buy_price, 5), _N(value / buy_price, 0))
        Trade('SELL', _N(sell_price, 5), _N(value / sell_price, 0))

def FirstAccount():
    key = "initialAccount_" + exchange.GetLabel()
    initialAccount = _G(key)
    if initialAccount is None:
        initialAccount = exchange.GetAccount()
        _G(key, initialAccount)
    return initialAccount

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

def initData():
    global symbol
    if _G('symbol') is None:
        symbol = exchange.GetCurrency().replace('_','')
        _G('symbol',symbol)
        Log('Initialize the currency:',symbol)
    else:
        symbol = _G('symbol')
        Log('Transaction currency:',symbol)

def main():
    exchange.SetContractType('swap')
    exchange.SetMarginLevel(10)
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

        Sleep(1000 * Interval)

```

> Detail

https://www.fmz.com/strategy/322060

> Last Modified

2021-10-09 12:58:38
