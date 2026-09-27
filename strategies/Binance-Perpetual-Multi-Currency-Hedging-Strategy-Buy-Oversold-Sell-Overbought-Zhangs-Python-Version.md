
> Name

Binance-Perpetual-Multi-Currency-Hedging-Strategy-Buy-Oversold-Sell-Overbought-Zhangs-Python-Version

> Author

汇链资本



> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|Trade_symbols|IOST,TRX,XLM,QTUM,DASH,ADA,BNB,XMR,ZEC,ATOM,IOTA,NEO,ONT,XRP,BAT,VET,EOS,ETC,LTC|Transaction currency|
|Trade_value|50|Holding value for every 1% deviation from the index|
|Adjust_value|20|Contract value adjustment deviation|
|Ice_value|20|Size of iceberg order|
|Log_profit_interval|600|LogTotal equity intervals|
|Interval|5|Dormant Times|
|Reset|false|Reset historical data|


> Source (python)

``` python
#Just learnedpython,Hope for corrections! Learn together!
import time
import requests
import math
Alpha = 0.001 #The larger the Alpha parameter of the exponential moving average is set, the more sensitive the benchmark price tracking will be, and the final position will be lower, which reduces the leverage, but will reduce the income. You need to weigh it based on the backtest results.
Update_base_price_time_interval = 60 #How often to update the benchmark price, in seconds, related to the Alpha parameter. The smaller the Alpha setting, the smaller the interval can also be set.
#Stop_lossSet to 0.8 means stop-loss, liquidate all positions, and stop the strategy when the funds fall below 80% of the initial amount.
#As the strategy runs,Stop_lossCan set greater than1(Effective after restart), for example from1000Earn1500,Stop_lossSet as1.3,Then draw down to1300Yuan stop loss. If you don't want to stop the loss, you can set this parameter very small.
#The risk is that if everyone uses this stop loss, it will cause a stampede and increase losses.
#Initial funds in the status barinit_balancefield, please note that operations such as withdrawals will be affected. Don't accidentally stop the loss.
#If still afraid of black swan events, for example if a coin returns0Waiting, can manually withdraw.

Stop_loss = 0.8
Max_diff = 0.03 #When the deviation (diff) is greater than 0.4, do not continue adding short positions; set manually.
Min_diff = -0.03 #When diff is less than -0.3, do not continue to add long positions, set it yourself
Version = '0.1.3'
Show = false #The default is false and the accumulated income is displayed as account balance. If it is changed to true, the accumulated income is displayed as income. If the account balance was displayed before, you use LogProfitReset() to clear the chart.
Funding = 0 #Account initial capital: if 0, it will be automatically fetched; if not 0, it is custom
success = '#5cb85c' #Success color
danger = '#ff0000' #Dangerous colors
warning = '#f0ad4e' #Warning color
RunTime = {} #Running time
SelfFee = 0.04 #https:#www.binance.com/cn/fee/futureFee
TotalLong = 0
TotalShort = 0
UpProfit = 0
accountAssets = [] #Save assets
WinRateData = {} #Save the win rate and number of positions opened for all currencies

if IsVirtual():
    Log('Cannot backtest, reference for backtest https://www.fmz.com/digest-topic/5294 ')
    exit()
if exchange.GetName() != 'Futures_Binance':
    Log('Only supports Binance futures exchange, which is different from spot exchange and needs to be added separately with the nameFutures_Binance')
    exit()
trade_symbols = Trade_symbols.split(',')
symbols = trade_symbols + ['BTC']
index = 1 #Index
update_profit_time = 0
update_base_price_time = int(time.time()*1000)
assets = {}
init_prices = {}
trade_info = {}

def init():
    InitRateData()
    exchange_info = requests.get('https://fapi.binance.com/fapi/v1/exchangeInfo').json()
    if exchange_info is None:
        Log('Unable to connect to Binance network, requires overseas hosting')
        exit()    
    for i in range(len(exchange_info['symbols'])):
        if exchange_info['symbols'][i]['baseAsset'] in symbols:            
            assets[exchange_info['symbols'][i]['baseAsset']] = {'amount': 0,'hold_price': 0,'value': 0,'bid_price': 0,'ask_price': 0,'btc_price': 0, 'btc_change': 1,'btc_diff': 0,'realised_profit': 0,'margin': 0,'unrealised_profit': 0,'leverage': 20, 'positionInitialMargin': 0,  'liquidationPrice': 0 }
            trade_info[exchange_info['symbols'][i]['baseAsset']] = {'minQty': float(exchange_info['symbols'][i]['filters'][1]['minQty']) , 'priceSize': int((math.log10(1.1/float(exchange_info['symbols'][i]['filters'][0]['tickSize'])))),'amountSize': int((math.log10(1.1/float(exchange_info['symbols'][i]['filters'][1]['stepSize']))))}

assets['USDT'] = {
    'unrealised_profit': 0,
    'margin': 0,
    'margin_balance': 0,
    'total_balance': 0,
    'leverage': 0,
    'update_time': 0,
    'margin_ratio': 0,
    'init_balance': 0,
    'stop_balance': 0,
    'short_value': 0,
    'long_value': 0,
    'profit': 0
}

def updateAccount() : #Update account and positions
    global accountAssets
    account = exchange.GetAccount()
    pos = exchange.GetPosition()
    if account is None or pos is None:
        Log('update account time out')
        return    
    accountAssets = account['Info']['assets']
    assets['USDT']['update_time'] = int(time.time()*1000)
    for i in range(len(trade_symbols)):
        assets[trade_symbols[i]]['margin'] = 0
        assets[trade_symbols[i]]['unrealised_profit'] = 0
        assets[trade_symbols[i]]['hold_price'] = 0
        assets[trade_symbols[i]]['amount'] = 0
    
    for j in range(len(account['Info']['positions'])):        
        if account['Info']['positions'][j]['positionSide'] == 'BOTH':
            pair = account['Info']['positions'][j]['symbol']
            coin = pair[0:len(pair)-4]
            if coin not in trade_symbols:
                continue
            assets[coin]['margin'] = float(account['Info']['positions'][j]['initialMargin']) + float(account['Info']['positions'][j]['maintMargin'])
            assets[coin]['unrealised_profit'] = float(account['Info']['positions'][j]['unrealizedProfit'])
            assets[coin]['positionInitialMargin'] = float(account['Info']['positions'][j]['positionInitialMargin'])
            assets[coin]['leverage'] = account['Info']['positions'][j]['leverage']

    assets['USDT']['margin'] = _N(float(account['Info']['totalInitialMargin']) + float(account['Info']['totalMaintMargin']), 2)
    assets['USDT']['margin_balance'] = _N(float(account['Info']['totalMarginBalance']), 2)
    assets['USDT']['total_balance'] = _N(float(account['Info']['totalWalletBalance']), 2)
    if assets['USDT']['init_balance'] == 0:
        if _G('init_balance'):
            assets['USDT']['init_balance'] = _N(_G('init_balance'), 2)
        else:
            assets['USDT']['init_balance'] = assets['USDT']['total_balance']
            _G('init_balance', assets['USDT']['init_balance'])
    assets['USDT']['profit'] = _N(assets['USDT']['margin_balance'] - assets['USDT']['init_balance'], 2)
    assets['USDT']['stop_balance'] = _N(Stop_loss * assets['USDT']['init_balance'], 2)
    assets['USDT']['total_balance'] = _N(float(account['Info']['totalWalletBalance']), 2)
    assets['USDT']['unrealised_profit'] = _N(float(account['Info']['totalUnrealizedProfit']), 2)
    assets['USDT']['leverage'] = _N(assets['USDT']['margin'] / assets['USDT']['total_balance'], 2)
    assets['USDT']['margin_ratio'] = float(account['Info']['totalMaintMargin']) / float(account['Info']['totalMarginBalance']) * 100
    pos = json.loads(exchange.GetRawJSON())
    if len(pos) > 0:
        for k in range(len(pos)):
            pair = pos[k]['symbol']
            coin = pair[0:len(pair)-4]
            if coin not in trade_symbols:
                continue            
            if pos[k]['positionSide'] != 'BOTH':
                continue       
            assets[coin]['hold_price'] = float(pos[k]['entryPrice'])
            assets[coin]['amount'] = float(pos[k]['positionAmt'])
            assets[coin]['unrealised_profit'] = float(pos[k]['unRealizedProfit'])
            assets[coin]['liquidationPrice'] = float(pos[k]['liquidationPrice'])
            assets[coin]['marginType'] = pos[k]['marginType']

def updateIndex(): #Update index
    global update_base_price_time,index,init_prices,Reset
    if _G('init_prices') is None or Reset:
        Reset = False
        for i in range(len(trade_symbols)):
            init_prices[trade_symbols[i]] = (assets[trade_symbols[i]]['ask_price'] + assets[trade_symbols[i]]['bid_price']) / (assets['BTC']['ask_price'] + assets['BTC']['bid_price'])
        Log('Save the price at startup')
        _G('init_prices', init_prices)
        _G("StartTime", None) #Reset start time
        _G("initialAccount_" + exchange.GetLabel(), None) #Reset starting funds
        _G('tradeNumber', 0) #Reset number of trades
        _G('tradeVolume', 0) #Reset trading volume
        _G('buyNumber', 0) #Reset number of long positions
        _G('sellNumber', 0) #Reset number of short positions
        _G('totalProfit', 0) #Reset print count
        _G('profitNumber', 0) #Reset number of profitable trades
    else:
        init_prices = _G('init_prices')
        if (int(time.time()*1000) - update_base_price_time > Update_base_price_time_interval * 1000):
            update_base_price_time = int(time.time()*1000)
            for i in range(len(trade_symbols)): #Update initial price
                init_prices[trade_symbols[i]] = init_prices[trade_symbols[i]] * (1 - Alpha) + Alpha * (assets[trade_symbols[i]]['ask_price'] + assets[trade_symbols[i]]['bid_price']) / (assets['BTC']['ask_price'] + assets['BTC']['bid_price'])
            _G('init_prices', init_prices)
        temp = 0
        for i in range(len(trade_symbols)):
            assets[trade_symbols[i]]['btc_price'] = (assets[trade_symbols[i]]['ask_price'] + assets[trade_symbols[i]]['bid_price']) / (assets['BTC']['ask_price'] + assets['BTC']['bid_price'])
            if trade_symbols[i] not in init_prices:
                Log('Add new currency', trade_symbols[i])
                init_prices[trade_symbols[i]] = assets[trade_symbols[i]]['btc_price']
                _G('init_prices', init_prices)
            assets[trade_symbols[i]]['btc_change'] = _N(assets[trade_symbols[i]]['btc_price'] / init_prices[trade_symbols[i]], 4)
            temp += assets[trade_symbols[i]]['btc_change']        
        index = _N(temp / len(trade_symbols), 4)

def updateTick() : #Update Quotes
    try:
        ticker = requests.get('https://fapi.binance.com/fapi/v1/ticker/bookTicker').json()
    except Exception as e:
        Log('get ticker time out:',e)
        return
    assets['USDT']['short_value'] = 0
    assets['USDT']['long_value'] = 0
    for i in range(len(ticker)):
        pair = ticker[i]['symbol']
        coin = pair[0:len(pair)-4]
        if coin not in symbols:
            continue
        assets[coin]['ask_price'] = float(ticker[i]['askPrice'])
        assets[coin]['bid_price'] = float(ticker[i]['bidPrice'])
        assets[coin]['ask_value'] = _N(assets[coin]['amount'] * assets[coin]['ask_price'], 2)
        assets[coin]['bid_value'] = _N(assets[coin]['amount'] * assets[coin]['bid_price'], 2)
        if coin not in trade_symbols:
            continue
        if assets[coin]['amount'] < 0 :
            assets['USDT']['short_value'] += abs((assets[coin]['ask_value'] + assets[coin]['bid_value']) / 2)
        else:
            assets['USDT']['long_value'] += abs((assets[coin]['ask_value'] + assets[coin]['bid_value']) / 2)        
        assets['USDT']['short_value'] = _N(assets['USDT']['short_value'], 0)
        assets['USDT']['long_value'] = _N(assets['USDT']['long_value'], 0)    
    updateIndex()
    for i in range(len(trade_symbols)):
        assets[trade_symbols[i]]['btc_diff'] = _N(assets[trade_symbols[i]]['btc_change'] - index, 4)

def trade(symbol, dirction, value) : #Transaction
    if (int(time.time()*1000) - assets['USDT']['update_time'] > 10 * 1000):
        Log('Update account delay, do not trade')
    else:
        price = assets[symbol]['bid_price'] if dirction == 'sell' else assets[symbol]['ask_price']
        amount = _N(min(value, Ice_value) / price, trade_info[symbol]['amountSize'])
        if amount < trade_info[symbol]['minQty']:
            Log(symbol, 'Contract value deviation or iceberg order size is set too small to meet the minimum transaction., At least needed: ', _N(trade_info[symbol]['minQty'] * price, 0) + 1)
        else:
            exchange.IO("currency", symbol + '_' + 'USDT')
            exchange.SetContractType('swap')
            exchange.SetDirection(dirction)
            #f = 'Buy' if dirction == 'buy' else 'Sell'
            place_order = getattr(exchange,'Buy' if dirction == 'buy' else 'Sell')
            id = place_order(price, amount, symbol)
            if id:
                exchange.CancelOrder(id) #Order will be canceled immediately
            tradingCounter('tradeVolume', price * amount) #Save transaction volume
            tradingCounter('tradeNumber', 1) #Save number of trades
            WinRateData[symbol]['tradeNumber'] += 1
            if dirction == 'buy':
                tradingCounter('buyNumber', 1)
                WinRateData[symbol].buyNumber += 1
            else:
                tradingCounter('sellNumber', 1)
                WinRateData[symbol].sellNumber += 1            
            _G("WinRateData", WinRateData) #Save trading data for each currency
            return id

def InitRateData():
    global WinRateData
    if Reset :
        _G("WinRateData", None)    
    if _G("WinRateData"):
        WinRateData = _G("WinRateData")    
    for i in range(len(symbols)):        
        if symbols[i] not in WinRateData:
            WinRateData[symbols[i]] = {'totalProfit': 0, 'profitNumber': 0,'tradeNumber': 0,'buyNumber': 0, 'sellNumber': 0}
                                            #Count of statistics        #Number of Wins          #Number of Trades       #Number of long trades        #Number of short trades
    _G("WinRateData", WinRateData)

def RunCommand():
    str_cmd = GetCommand()
    if str_cmd:
        arrCmd = str_cmd.split(':')
        symbol = arrCmd[1]
        amount = float(arrCmd[2])
        if amount == 0:
            Log('Dear,Do you still remember Qiao Biluo by Daming Lake??' + danger)
        else:
            #f = 'Buy' if amount < 0 else 'Sell'
            dirction = 'buy' if amount < 0 else 'sell'
            exchange.IO("currency", symbol + '_' + 'USDT')
            exchange.SetContractType('swap')
            exchange.SetDirection(dirction)
            place_order = getattr(exchange,'Buy' if dirction == 'buy' else 'Sell')
            id = place_order(-1, abs(amount), symbol)
            #exchange[f](-1, abs(amount), symbol)

def FirstAccount():
    key = "initialAccount_" + exchange.GetLabel()
    initialAccount = _G(key)
    if initialAccount is None:
        initialAccount = exchange.GetAccount()
        _G(key, initialAccount)    
    return initialAccount

def StartTime():
    StartTime = _G("StartTime")
    if StartTime is None:
        StartTime = _D()
        _G("StartTime", StartTime)    
    return StartTime

def RuningTime():
    ret = {}    
    dateBegin = StartTime()
    dateEnd = _D()
    dateDiff = (time.mktime(time.strptime(dateEnd, '%Y-%m-%d %H:%M:%S')) - time.mktime(time.strptime(dateBegin, '%Y-%m-%d %H:%M:%S'))) * 1000
    dayDiff = math.floor(dateDiff / (24 * 3600 * 1000))
    leave1 = dateDiff % (24 * 3600 * 1000)
    hours = math.floor(leave1 / (3600 * 1000))
    leave2 = leave1 % (3600 * 1000)
    minutes = math.floor(leave2 / (60 * 1000))
    ret['dayDiff'] = dayDiff
    ret['hours'] = hours
    ret['minutes'] = minutes
    ret['str'] = "Running time: " + str(dayDiff) + " Sky/Heaven " + str(hours) + " Hour " + str(minutes) + " Minute"
    return ret

def AppendedStatus():
    global TotalLong , TotalShort,RunTime,Funding, accountAssets
    accountTable = {
        'type': "table",
        'title': "Profit statistics",
        'cols': ["Running days", "Initial funds", "Existing funds", "Margin balance", "Used margin", "Margin ratio", "Stop loss", "Total income", "Estimated annualized", "Estimated monthly", "Average daily"],
        'rows': []
    }
    feeTable = {
        'type': 'table',
        'title': 'Trading statistics',
        'cols': ["Strategy index", 'Number of transactions', 'Number of longs', 'Number of shorts', 'Estimated winning rate', 'Estimated transaction volume', 'Estimated handling fee', "Unrealized profit", 'Total position value', 'Total long value', 'Total short value''],
        'rows': []
    }
    runday = RunTime['dayDiff']
    if runday == 0:
        runday = 1
    if Funding == 0:
        Funding = float(FirstAccount()['Info']['totalWalletBalance'])
    profitColors = danger
    totalProfit = assets['USDT']['total_balance'] - Funding #Total profit
    if totalProfit > 0:
        profitColors = success
    dayProfit = totalProfit / runday #Daily profit
    dayRate = dayProfit / Funding * 100
    accountTable['rows'].append([
        runday,
        '$' + str(_N(Funding, 2)),
        '$' + str(assets['USDT']['total_balance']),
        '$' + str(assets['USDT']['margin_balance']),
        '$' + str(assets['USDT']['margin']),
        str(_N(assets['USDT']['margin_ratio'], 2)) + '%',
        str(_N(assets['USDT']['stop_balance'], 2)) + danger,
        str(_N(totalProfit / Funding * 100, 2)) + "% = $" + str(_N(totalProfit, 2)) + (profitColors),
        str(_N(dayRate * 365, 2)) + "% = $" + str(_N(dayProfit * 365, 2)) + (profitColors),
        str(_N(dayRate * 30, 2)) + "% = $" + str(_N(dayProfit * 30, 2)) + (profitColors),
        str(_N(dayRate, 2)) + "% = $" + str(_N(dayProfit, 2)) + (profitColors)
    ])
    vloume = _G('tradeVolume') if _G('tradeVolume') is not None else 0
    feeTable['rows'].append([
        index, #Index
        _G('tradeNumber') if _G('tradeNumber') is not None else 0, #Number of Trades
        _G('buyNumber') if _G('buyNumber') is not None else 0, #Number of long trades
        _G('sellNumber') if _G('sellNumber') is not None else 0, #Number of short trades
        str(_N(_G('profitNumber') / _G('totalProfit') * 100, 2) if _G('totalProfit') > 0 else 0) + '%', #Win rate
        '$' + str(_N(vloume, 2)) + ' ≈ ฿' + str(_N(vloume / ((assets['BTC']['bid_price'] + assets['BTC']['ask_price']) / 2), 6)), #Transaction amount
        '$' + str(_N(vloume * (SelfFee / 100), 4)), #trading fee
        '$' + str(_N(assets['USDT']['unrealised_profit'], 2)) + (success if assets['USDT']['unrealised_profit'] >= 0 else danger),
        '$' + str(_N(TotalLong + abs(TotalShort), 2)), #Total value of positions
        '$' + str(_N(TotalLong, 2)) + success, #Total value of long trades
        '$' + str(_N(abs(TotalShort), 2)) + danger, #Total value of short trades
    ])
    assetTable = {
        'type': 'table',
        'title': 'Account asset information',
        'cols': ['Number', 'Asset name', 'Initial margin', 'Maintenance margin', 'Margin balance', 'Maximum withdrawal amount', 'Starting margin for pending orders', 'Starting margin for positions', 'Unrealized profit and loss for positions', 'Account balance'],
        'rows': []
    }
    for i in range(len(accountAssets)):
        acc = accountAssets[i]
        assetTable['rows'].append([
            i + 1,
            acc['asset'], acc['initialMargin'], acc['maintMargin'], acc['marginBalance'],
            acc['maxWithdrawAmount'], acc['openOrderInitialMargin'], acc['positionInitialMargin'],
            acc['unrealizedProfit'], acc['walletBalance']
        ])
    indexTable = {
        'type': 'table',
        'title': 'Coin index information',
        'cols': ['Number', 'Currency information', 'Current price', 'BTC pricing', 'BTC pricing change (%)', 'Deviation from average', 'Number of transactions', 'Number of shorts', 'Number of longs', 'Estimated winning rate'],
        'rows': []
    }
    for i in range(len(symbols)) :
        price = _N((assets[symbols[i]]['ask_price'] + assets[symbols[i]]['bid_price']) / 2, trade_info[symbols[i]]['priceSize'])
        if symbols[i] not in symbols:
            indexTable['rows'].append([i + 1, symbols[i], price, assets[symbols[i]]['btc_price'], _N((1 - assets[symbols[i]]['btc_change']) * 100), assets[symbols[i]]['btc_diff']], 0, 0, 0, '0%')
        else:
            rateData = _G("WinRateData")
            winRate = _N(rateData[symbols[i]]['profitNumber'] / rateData[symbols[i]]['totalProfit'] * 100, 2) if rateData[symbols[i]]['totalProfit'] > 0 else 0
            indexTable['rows'].append([
                (i + 1),
                symbols[i] + warning,
                price,
                _N(assets[symbols[i]]['btc_price'], 6),
                _N((1 - assets[symbols[i]]['btc_change']) * 100),
                str(assets[symbols[i]]['btc_diff']) + (success if assets[symbols[i]]['btc_diff'] >= 0 else danger),
                rateData[symbols[i]]['tradeNumber'],
                rateData[symbols[i]]['sellNumber'],
                rateData[symbols[i]]['buyNumber'],
                (str(winRate) if rateData[symbols[i]]['profitNumber'] > 0 and rateData[symbols[i]]['totalProfit'] > 0 else '0') + '%' + (success if winRate >= 50 else danger), #Win rate
            ])    
    retData = {}
    retData['upTable'] = RunTime['str'] + '\n' + "Last Update: " + _D() + '\n' + 'Version:' + Version + '\n' + '`' + json.dumps([accountTable, assetTable]) + '`\n' + '`' + json.dumps(feeTable) + '`\n'
    retData['indexTable'] = indexTable
    return retData


def WinRate():
    global WinRateData
    for i in range(len(symbols)) :
        unrealised = assets[symbols[i]]['unrealised_profit']
        WinRateData[symbols[i]]['totalProfit'] += 1
        if unrealised != 0:
            if unrealised > 0:
                WinRateData[symbols[i]]['profitNumber'] += 1    
    _G("WinRateData", WinRateData)

def tradingCounter(key, newValue):
    value = _G(key)
    if value is None:
        _G(key, newValue)
    else:
        _G(key, value + newValue)

def updateStatus() : #Status bar information
    global TotalLong , TotalShort,Funding,update_profit_time,UpProfit
    TotalLong = 0
    TotalShort = 0
    table = {
        'type': 'table',
        'title': 'Trading pair information',
        'cols': ['Number', '[Mode][Multiple]', 'Currency Information', 'Opening Direction', 'Opening Quantity', 'Position Price', 'Current Price', 'Liquidation Price', 'Liquidation Difference', 'Position Value', 'Margin', 'Unrealized Profit and Loss', 'Surrender'],
        'rows': []
    }
    
    for i in range(len(symbols)):        
        direction = 'Short position'
        margin = direction
        if assets[symbols[i]]['amount'] != 0:
            direction = 'go long' + success if assets[symbols[i]]['amount'] > 0 else 'go short' + danger
            margin = 'Cross position' if assets[symbols[i]]['marginType'] == 'cross' else 'Isolated position'
        price = _N((assets[symbols[i]]['ask_price'] + assets[symbols[i]]['bid_price']) / 2, trade_info[symbols[i]]['priceSize'])
        value = _N((assets[symbols[i]]['ask_value'] + assets[symbols[i]]['bid_value']) / 2, 2)
        if value != 0:
            if value > 0:
                TotalLong += value
            else:
                TotalShort += value
        # rateData = _G("WinRateData")
        infoList = [
            i + 1,
            "[" + margin + "] [" + str(assets[symbols[i]]['leverage']) + 'x] ',
            symbols[i],
            direction,
            abs(assets[symbols[i]]['amount']),
            assets[symbols[i]]['hold_price'],
            price,
            assets[symbols[i]]['liquidationPrice'], #Forced liquidation price
            '0' if assets[symbols[i]]['liquidationPrice'] == 0 else '$' + str(_N(assets[symbols[i]]['liquidationPrice'] - price, 5)) + ' ≈ ' + str(_N(assets[symbols[i]]['liquidationPrice'] / price * 100, 2)) + '%' + warning, #Forced liquidation price
            abs(value),
            _N(assets[symbols[i]]['positionInitialMargin'], 2),
            # assets[symbols[i]]['btc_diff'],
            str(_N(assets[symbols[i]]['unrealised_profit'], 3)) + (success if assets[symbols[i]]['unrealised_profit'] >= 0 else danger),
            # (rateData[symbols[i]]['profit']Number > 0 and rateData[symbols[i]].totalProfit > 0 ? _N(rateData[symbols[i]]['profit']Number / rateData[symbols[i]].totalProfit * 100, 2) : '0') + '%', #Win rate
            {
                'type': 'button',
                'cmd': 'There was supposed to be no retreat???:' + symbols[i] + ':' + str(assets[symbols[i]]['amount']) + ':',
                'name': symbols[i] + ' Surrender'
            }
        ]
        table['rows'].append(infoList)
    #del assets['USDT']['update_time'] #Timestamp is useless, discard it
    logString = json.dumps(assets['USDT']) + '\n'
    StatusData = AppendedStatus()
    LogStatus(StatusData['upTable'] + '`' + json.dumps([table, StatusData['indexTable']]) + '`\n' + logString)

    if int(time.time()*1000) - update_profit_time > Log_profit_interval * 1000:
        balance = assets['USDT']['margin_balance']
        if Show:
            balance = assets['USDT']['margin_balance'] - Funding
        LogProfit(_N(balance, 3), '&')
        update_profit_time = int(time.time()*1000)
        if UpProfit != 0 and (_N(balance, 0) != UpProfit): #The first time will not be calculated, and the winning rate will not be calculated to the decimal point.
            tradingCounter("totalProfit", 1) #Count the number of prints, winning rate = number of profits/number of prints*100
            if _N(balance, 0) > UpProfit:
                tradingCounter('profitNumber', 1) #Number of Wins
            WinRate()
        UpProfit = _N(balance, 0)

def stopLoss() : #Stop-loss function
    while True:
        if assets['USDT']['margin_balance'] < Stop_loss * assets['USDT']['init_balance'] and assets['USDT']['init_balance'] > 0:
            Log('Trigger stop-loss, current funds:', assets['USDT']['margin_balance'], 'Initial capital:', assets['USDT']['init_balance'])
            Ice_value = 200 #Stop loss faster, can be modified
            updateAccount()
            updateTick()
            trading = False #Is it trading
            for i in range(len(trade_symbols)):
                symbol = trade_symbols[i]
                if assets[symbol]['ask_price'] == 0:
                    continue                
                if assets[symbol]['bid_value'] >= trade_info[symbol]['minQty'] * assets[symbol]['bid_price']:
                    trade(symbol, 'sell', assets[symbol]['bid_value'])
                    trading = True
                if assets[symbol]['ask_value'] <= -trade_info[symbol]['minQty'] * assets[symbol]['ask_price']:
                    trade(symbol, 'buy', -assets[symbol]['ask_value'])
                    trading = True
            Sleep(1000)
            if not trading :
                Log('Stop-loss ended,If you need to rerun the strategy, you need to lower the stop loss') 
                exit()
        else : #No need for stop-loss
            return None

def onTick() : #Strategy logic section
    for i in range(len(trade_symbols)) :
        symbol = trade_symbols[i]
        if assets[symbol]['ask_price'] == 0:
            continue        
        aim_value = -Trade_value * _N(assets[symbol]['btc_diff'] / 0.01, 3)        
        if aim_value - assets[symbol]['ask_value'] >= Adjust_value and assets[symbol]['btc_diff'] > Min_diff and assets['USDT']['long_value'] - assets['USDT']['short_value'] <= 1.1 * Trade_value:
            Log('go long',symbol,'   aim_value:',aim_value,'   Deviation from average:',assets[symbol]['btc_diff'])            
            trade(symbol, 'buy', aim_value - assets[symbol]['ask_value'])
        if aim_value - assets[symbol]['bid_value'] <= -Adjust_value and assets[symbol]['btc_diff'] < Max_diff and assets['USDT']['short_value'] - assets['USDT']['long_value'] <= 1.1 * Trade_value:
            Log('go short',symbol,'   aim_value:',aim_value,'   Deviation from average:',assets[symbol]['btc_diff'])            
            trade(symbol, 'sell', -(aim_value - assets[symbol]['bid_value']))

def main():
    global RunTime
    SetErrorFilter("502:|503:|tcp|character|unexpected|network|timeout|WSARecv|Connect|GetAddr|no such|reset|http|received|EOF|reused|Unknown")
    while True:
        RunTime = RuningTime()
        RunCommand() #Capture interactive commands
        updateAccount() #Update account and positions
        updateTick() #Market quotation
        stopLoss() #stop loss
        onTick() #Strategy logic section
        updateStatus() #Output status bar information
        Sleep(Interval * 1000)

```

> Detail

https://www.fmz.com/strategy/201963

> Last Modified

2020-05-02 23:34:14
