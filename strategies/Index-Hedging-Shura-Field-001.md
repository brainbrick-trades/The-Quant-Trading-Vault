
> Name

Index-Hedging-Shura-Field-001

> Author

XMaxZone

> Strategy Description

* hedge

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|TradeSymbols|BTC,ETH,BCH,XRP,EOS,LTC,TRX,ETC,LINK,XLM,ADA,XMR,DASH,ZEC,XTZ,BNB,ATOM,ONT,IOTA,BAT,VET,NEO,QTUM,IOST|Transaction currency|
|TradeValue|50|Holding value for every 1% deviation from the index|
|DeviateValue|20|Contract value adjustment deviation|
|IceValue|20|Iceberg order|
|LogInterval|600|LogTotal equity intervals|
|Interval|5|Dormant Times|
|MockTrading|false|Simulated Trading|
|MockTradingValue|100000|Simulated transaction amount|
|Reset|false|Reset|


> Source (python)

``` python

import time
import requests
import math
import pandas as pd

Alpha = 0.001  #For the MA parameter of the exponential moving average, the larger the setting, the more sensitive the benchmark price tracking will be, and the final position will be lower. This reduces the leverage, but will reduce the income. You can weigh it according to your own needs.
UpdateBasePriceInterval = 60 #How often the base price is updated, in bits per second, related to Alpha. The smaller the Alpha is set, the smaller the interval can also be set.
StopLossRate = 0.8 #means the stop-loss is triggered when the initial capital reaches 80%. The stop-loss strategy can be dynamically set as the strategy becomes profitable
MaxDiff = 0.5  #Stop adding positions when the deviation (diff) is greater than this value
MinDiff = -0.5  #Stop adding positions when the StopLossRate deviation Diff is less than this value
Version = '0.0.1'
Show = True   #Default false shows account balance, true shows cumulative profit
Funding = 0    #Account funds: automatically retrieve if zero, manually set if non-zero
SuccessColor = '#5cb85c' #Success color
DangerColor = '#ff0000' #Dangerous colors
WrningColor = '#f0ad4e' #Warning color
SelfFee = 0.04   #Fee Rate   https:#www.binance.com/cn/fee/futureFee
TotalLong = 0    #Go long the total value
TotalShort = 0   #Total short value
Profit = 0       #Revenue
Account = {}     #Save account information
WinRateData = {}  # Store win rate information
assets = {}
tradeInfo = {}
accountAssets = {}
runtimeData = {}

if IsVirtual():
    Log('Cannot perform backtest')
    exit()

tradeSymbols = list(TradeSymbols.replace(' ','').split(','))
Index = 1   #Index
UpdateBasePriceTime = 0
InitPrice = {}
updateProfitTime = 0


#
assets['USDT'] = {'unrealised_profit':0,'margin':0,'margin_balance':0,'total_balance':0,'leverage':0,'update_time':0,'margin_ratio':0,'init_balance':0,'stop_balance':0,'short_value':0,'long_value':0,'profit':0}

if exchange.GetName() != 'Futures_Binance':
    Log('Only supports Binance futures exchange!')
    exit()

def init():
    InitRateData()
    exchangeInfo = requests.get('https://fapi.binance.com/fapi/v1/exchangeInfo').json()
    if exchangeInfo is None:
        Log('Unable to connect to Binance network, requires overseas hosting')
        exit()
    #Log(exchangeInfo)
    for i in range(len(exchangeInfo['symbols'])):
        if len(exchangeInfo['symbols'][i]['symbol'].split('_')) > 1 :continue
        sp = exchangeInfo['symbols'][i]['symbol'].split('_')[0]
        symbol = sp.replace('USDT','')
        #Log(sp)
        BUSD = sp[-4:len(sp)]
        if 'BUSD' != BUSD or symbol not in exchangeInfo['symbols'][i]['symbol']:   #Exclude BUSD trading pairs
            if symbol in tradeSymbols:
                assets[symbol] = {'amount': 0,'hold_price': 0,'value': 0,'bid_price': 0,'ask_price': 0,'btc_price': 0, 'btc_change': 1,'btc_diff': 0,
                'realised_profit': 0,'margin': 0,'unrealised_profit': 0,'leverage': 20, 'positionInitialMargin': 0,  'liquidationPrice': 0 }
                tradeInfo[symbol] = {'minQty': float(exchangeInfo['symbols'][i]['filters'][1]['minQty']) ,
                'priceSize': int((math.log10(1.1/float(exchangeInfo['symbols'][i]['filters'][0]['tickSize'])))),'amountSize': int((math.log10(1.1/float(exchangeInfo['symbols'][i]['filters'][1]['stepSize']))))}


def UpdateAccount():
    global accountAssets ,StopLoss
    #Determine whether the current transaction is simulated trading or real trading
    if MockTrading:
        Log('Simulate trade to update account')

    else:
        #Log('Live trade updates account')
        account = exchange.GetAccount()
        ps = exchange.GetPosition()
        if account is None:
            Log('Update account timeout!')
            return
        accountAssets = account['Info']['assets']
        assets['USDT']['update_time'] = int(time.time() * 1000)
        #Log(account['Info']['positions'])
        for i in range(len(account['Info']['positions'])):
            symbol = account['Info']['positions'][i]['symbol']
            if len(symbol.split('_')) > 1: continue   #Filter Out, e.g., symbol: ETHUSDT_211231 contract.
            sp = symbol.split('_')[0]
            #ExcludeBUSDTrading pairs and trading pairs not in the trading list
            coin = sp.replace('USDT','')
            BUSD = sp[-4:len(sp)]
            if 'BUSD' == BUSD or coin not in tradeSymbols: continue
            #Filter unidirectional position coins
            if account['Info']['positions'][i]['positionSide'] == 'BOTH':
                # if coin == 'ETH':
                #     Log(coin,account['Info']['positions'][i])
                #Log('symbol:',symbol)
                assets[coin]['margin'] = float(account['Info']['positions'][i]['initialMargin']) + float(account['Info']['positions'][i]['maintMargin'])
                assets[coin]['unrealised_profit'] = float(account['Info']['positions'][i]['unrealizedProfit'])
                assets[coin]['positionInitialMargin'] = float(account['Info']['positions'][i]['positionInitialMargin'])
                assets[coin]['leverage'] = account['Info']['positions'][i]['leverage']
        #Log(assets)
        #Calculate the total margin of positions
        assets['USDT']['margin'] = float(account['Info']['totalInitialMargin']) + float(account['Info']['totalMaintMargin'])
        assets['USDT']['margin_balance'] = float(account['Info']['totalMarginBalance'])
        assets['USDT']['total_balance'] = float(account['Info']['totalWalletBalance'])
        if assets['USDT']['init_balance'] == 0:
            if _G('init_balance'):
                assets['USDT']['init_balance'] = _N(_G('init_balance'),2)
            else:
                assets['USDT']['init_balance'] = assets['USDT']['total_balance']
                _G('init_balance',assets['USDT']['init_balance'])
        #Calculate income
        assets['USDT']['profit'] = _N(float(assets['USDT']['margin_balance']) - float(assets['USDT']['init_balance']),2)
        #Calculate stop-loss position
        assets['USDT']['stop_balance'] = _N(StopLossRate * assets['USDT']['init_balance'], 2)
        #Calculate unrealized profit
        assets['USDT']['unrealised_profit'] = _N(float(account['Info']['totalUnrealizedProfit']),2)
        #Calculate Leverage
        assets['USDT']['leverage'] = _N(assets['USDT']['margin'] / float(assets['USDT']['total_balance']))
        #Calculate margin ratio
        assets['USDT']['margin_ratio'] = _N(float(account['Info']['totalMaintMargin']) / float(account['Info']['totalMarginBalance'])) * 100
        exchange.SetContractType('swap')
        ps = json.loads(exchange.GetRawJSON())
        # Update Positions
        #Log('position:',ps)
        if len(ps) > 0:
            j = 1
            for i in range(len(ps)):
                #Log(ps[i])
                if len(ps[i]['symbol'].split('_')) > 1: continue   #Filter Out, e.g., symbol: ETHUSDT_211231 contract.
                sp = ps[i]['symbol'].split('_')[0]
                BUSD = sp[-4:len(sp)]
                symbol = sp.replace('USDT','')


                if 'BUSD' == BUSD or symbol not in tradeSymbols : continue
                if ps[i]['positionSide'] != 'BOTH': continue
                assets[symbol]['hold_price'] = float(ps[i]['entryPrice'])
                assets[symbol]['amount'] = float(ps[i]['positionAmt'])
                assets[symbol]['unrealised_profit'] = float(ps[i]['unRealizedProfit'])
                assets[symbol]['liquidationPrice'] = float(ps[i]['liquidationPrice'])
                assets[symbol]['marginType'] = ps[i]['marginType']
                #Log(j,assets[symbol])
                #j+=1
        #Log('Live account update completed!')


def UpdateTick():
    try:
        ticker = requests.get('https://fapi.binance.com/fapi/v1/ticker/bookTicker').json()
    except Exception as e:
        Log('get ticker time out !')
        return
    assets['USDT']['long_value'] = 0
    assets['USDT']['short_value'] = 0
    for i in range(len(ticker)):
        sp = ticker[i]['symbol'].split('_')[0]
        if len(ticker[i]['symbol'].split('_')) > 1: continue   #Filter Out, e.g., symbol: ETHUSDT_211231 contract.
        BUSD = sp[-4:len(sp)]
        symbol = sp.replace('USDT','')
        if 'BUSD' == BUSD or symbol not in tradeSymbols: continue
        # if symbol == 'BTCDOM':
        #     Log(symbol,ticker[i])
        #Log(ticker[i])
        assets[symbol]['ask_price'] = float(ticker[i]['askPrice'])
        assets[symbol]['bid_price'] = float(ticker[i]['bidPrice'])
        assets[symbol]['ask_value'] = _N(assets[symbol]['amount'] * assets[symbol]['ask_price'], 2)
        assets[symbol]['bid_value'] = _N(assets[symbol]['amount'] * assets[symbol]['bid_price'], 2)

        # if symbol == 'BTCDOM':
        #     Log(symbol,assets[symbol])
        value = (assets[symbol]['ask_value'] + assets[symbol]['bid_value']) / 2
        if value != 0:
            if value > 0:
                assets['USDT']['long_value'] += value
            else:
                assets['USDT']['short_value'] += value

        # if assets[symbol]['amount'] < 0:
        #     assets['USDT']['short_value'] += abs((assets[symbol]['ask_value'] + assets[symbol]['bid_price']) / 2)
        # else:
        #     assets['USDT']['long_value'] += abs((assets[symbol]['ask_value'] + assets[symbol]['bid_value']) / 2)

        assets['USDT']['short_value']    = _N(assets['USDT']['short_value'], 2)
        assets['USDT']['long_value']     = _N(assets['USDT']['long_value'], 2)

        #Log('UpdateTick:',symbol,assets[symbol])
    #Update index
    UpdateIndex()
    for symbol in  tradeSymbols:
        assets[symbol]['btc_diff'] = _N((assets[symbol]['btc_change'] - Index), 4)


def UpdateIndex():
    global UpdateBasePriceTime,InitPrice,Index,Reset

    if MockTrading:
        Log('Update index in simulated trading mode')
    else:
        #Log('Update index in live trading mode')
        if _G('InitPrice') is None or Reset:
            Reset = False
            for symbol in tradeSymbols:
                InitPrice[symbol] = (assets[symbol]['ask_price'] + assets[symbol]['bid_price']) / (assets['BTC']['ask_price'] + assets['BTC']['bid_price'])
            Log('Save the price at startup')
            _G('InitPrice',InitPrice)
            _G('StartTime',None)
            _G('InitAccount_'+exchange.GetLabel(), None)
            _G('tradeNumber', 0) #Reset number of trades
            _G('tradeVolume', 0) #Reset trading volume
            _G('buyNumber', 0) #Reset number of long positions
            _G('sellNumber', 0) #Reset number of short positions
            _G('totalProfit', 0) #Reset print count
            _G('profitNumber', 0) #Reset number of profitable trades
        else:
            InitPrice = _G('InitPrice')
            if int(time.time()*1000) - UpdateBasePriceTime > UpdateBasePriceInterval:
                UpdateBasePriceTime = int(time.time() * 1000)
                for symbol in tradeSymbols:
                    if symbol not in InitPrice: continue
                    InitPrice[symbol] = InitPrice[symbol] * (1 - Alpha) + Alpha * (assets[symbol]['ask_price'] + assets[symbol]['bid_price']) / (assets['BTC']['ask_price'] + assets['BTC']['bid_price'])
                    _G('InitPrice',InitPrice)
            temp = 0
            for symbol in tradeSymbols:
                assets[symbol]['btc_price'] = (assets[symbol]['ask_price'] + assets[symbol]['bid_price']) / (assets['BTC']['ask_price'] + assets['BTC']['bid_price'])
                if symbol not in InitPrice:
                    Log('Add new currency:',symbol)
                    InitPrice[symbol] = assets[symbol]['btc_price']
                    _G('InitPrice',InitPrice)
                #Log(symbol,assets[symbol]['btc_price'],InitPrice[symbol])
                assets[symbol]['btc_change'] = _N(assets[symbol]['btc_price'] / InitPrice[symbol], 4)
                temp += assets[symbol]['btc_change']
            Index = _N(temp / len(tradeSymbols), 4)
            #Log('Latest Index:',Index)


#Stop-Loss Module
def StopLoss():
    if assets['USDT']['margin_balance'] < StopLossRate * assets['USDT']['init_balance'] and assets['USDT']['init_balance'] != 0:
        Log('Trigger stop loss! Current funds:',assets['USDT']['margin_balance'],'Initial capital:',assets['USDT']['init_balance'])
        UpdateAccount()
        UpdateTick()
        Ice_value = 200 #Stop loss faster, can be modified
        trading = False
        for symbol in tradeSymbols:
            if assets[symbol]['bid_price'] == 0 : continue
            if assets[symbol]['bid_value'] >= tradeInfo[symbol]['minQty'] * assets[symbol]['bid_price']:
                ## TODO: Sell Stop-Loss
                trading = True
                pass
            if assets[symbol]['ask_value'] <= tradeInfo[symbol]['minQty'] * assets[symbol]['ask_price']:
                # TODO: Buy Stop-Loss
                trading = True
                pass
            Sleep(1000)
            if not trading:
                Log('Stop-loss ended, if you need to rerun the strategy, lower the stop-loss parameter!')
                exit()
    else:  # No need for stop-loss
        return None

def Trade(symbol,direction,value):
    if int(time.time()) - assets['USDT']['update_time'] > 10 * 1000:
        Log('Account update is delayed and no transactions are performed.!!!')
    else:
        price = assets[symbol]['bid_price'] if direction =='SELL' else assets[symbol]['ask_price']
        amount = _N(min(IceValue,value) / price,tradeInfo[symbol]['amountSize'])
        if amount < tradeInfo[symbol]['minQty']:
            Log(symbol,'The contract value deviates or the iceberg order setting is too small, the minimum transaction amount cannot be reached, and the minimum required:', _N(tradeInfo[symbol]['minQty'] * price,4) + 1)
        else:
            # exchange.SetCurrency(symbol+'_USDT')
            # Log(direction)
            # exchange.SetDirection(direction)
            # f = 'Buy' if direction == 'Buy' else 'Sell'
            # Log(f)
            # place_order = getattr(exchange,direction) #Get trading object
            # id = place_order(price,amount,symbol)
            para = ''
            url = '/fapi/v1/order'
            para += 'symbol='+ symbol + 'USDT'
            para += '&side='+ direction
            para += '&type=LIMIT&timeInForce=IOC'
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

            TradingCounter('tradeVolume',amount * price)
            TradingCounter('tradeNumber',1)
            WinRateData[symbol]['tradeNumber'] += 1
            if direction == 'Buy':
                TradingCounter('buyNumber',1)
                WinRateData[symbol]['buyNumber'] += 1
            else:
                TradingCounter('sellNumber',1)
                WinRateData[symbol]['sellNumber'] += 1
            _G('WinRateData',WinRateData)
            return id

def FirstAccount():
    key = "initialAccount_" + exchange.GetLabel()
    initialAccount = _G(key)
    if initialAccount is None:
        initialAccount = exchange.GetAccount()
        _G(key, initialAccount)
    return initialAccount

def AppendedStatus():
    global TotalLong,TotalShort,RunTime,Funding,Account
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
    runday = runtimeData['dayDiff']
    if runday == 0:
        runday = 1
    if Funding == 0:
        Funding = float(FirstAccount()['Info']['totalWalletBalance'])
    profitColors = DangerColor
    totalProfit = assets['USDT']['total_balance'] - Funding
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
        str(_N(assets['USDT']['stop_balance'], 2)) + DangerColor,
        str(_N(totalProfit / Funding * 100, 2)) + "% = $" + str(_N(totalProfit, 2)) + (profitColors),
        str(_N(dayRate * 365, 2)) + "% = $" + str(_N(dayProfit * 365, 2)) + (profitColors),
        str(_N(dayRate * 30, 2)) + "% = $" + str(_N(dayProfit * 30, 2)) + (profitColors),
        str(_N(dayRate, 2)) + "% = $" + str(_N(dayProfit, 2)) + (profitColors)
    ])

    vloume = _G('tradeVolume') if _G('tradeVolume') is not None else 0

    feeTable['rows'].append([
        Index, #Index
        _G('tradeNumber') if _G('tradeNumber') is not None else 0, #Number of Trades
        _G('buyNumber') if _G('buyNumber') is not None else 0, #Number of long trades
        _G('sellNumber') if _G('sellNumber') is not None else 0, #Number of short trades
        str(_N(_G('profitNumber') / _G('totalProfit') * 100, 2) if _G('totalProfit') > 0 else 0) + '%', #Win rate
        '$' + str(_N(vloume, 2)) + ' ≈ ฿' + str(_N(vloume / ((assets['BTC']['bid_price'] + assets['BTC']['ask_price']) / 2), 6)), #Transaction amount
        '$' + str(_N(vloume * (SelfFee / 100), 4)), #trading fee
        '$' + str(_N(assets['USDT']['unrealised_profit'], 2)) + (SuccessColor if assets['USDT']['unrealised_profit'] >= 0 else DangerColor),
        '$' + str(_N(TotalLong + abs(TotalShort), 2)), #Total value of positions
        '$' + str(_N(TotalLong, 2)) + SuccessColor, #Total value of long trades
        '$' + str(_N(abs(TotalShort), 2)) + DangerColor, #Total value of short trades
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

    i = 0
    for symbol in tradeSymbols :
        price = _N((assets[symbol]['ask_price'] + assets[symbol]['bid_price']) / 2, tradeInfo[symbol]['priceSize'])
        if symbol not in tradeSymbols:
            indexTable['rows'].append([i + 1, symbol, price, assets[symbol]['btc_price'], _N((1 - assets[symbol]['btc_change']) * 100), assets[symbol]['btc_diff']], 0, 0, 0, '0%')
        else:
            i += 1
            WinRateData = _G("WinRateData")
            winRated = _N(WinRateData[symbol]['profitNumber'] / WinRateData[symbol]['totalProfit'] * 100, 2) if WinRateData[symbol]['totalProfit'] > 0 else 0
            indexTable['rows'].append([
                i,
                symbol + WrningColor,
                price,
                _N(assets[symbol]['btc_price'], 6),
                _N((1 - assets[symbol]['btc_change']) * 100),
                str(assets[symbol]['btc_diff']) + (SuccessColor if assets[symbol]['btc_diff'] >= 0 else DangerColor),
                WinRateData[symbol]['tradeNumber'],
                WinRateData[symbol]['sellNumber'],
                WinRateData[symbol]['buyNumber'],
                (str(winRated) if WinRateData[symbol]['profitNumber'] > 0 and WinRateData[symbol]['totalProfit'] > 0 else '0') + '%' + (SuccessColor if winRated >= 50 else DangerColor), #Win rate
            ])
    retData = {}
    #Log(runtimeData['str'])
    #retData['upTable'] = runtimeData['str'] + '\n' + "Last Update: " + _D() + '\n' + 'Version:' + Version + '\n' + '`' + json.dumps([accountTable, assetTable]) + '`\n' + '`' + json.dumps(feeTable) + '`\n'
    retData['upTable'] = runtimeData['str'] + '\n' + "Last Update: " + _D() + '\n' + 'Version:' + Version  + '\n' + '`' + json.dumps([accountTable, assetTable]) + '`\n' + '`' + json.dumps(feeTable) + '`\n'
    retData['indexTable'] = indexTable
    return retData



def UpdateStatus():
    global TotalLong,TotalShort,updateProfitTime,Funding,Profit
    TotalLong = 0
    TotalShort = 0
    table = {
        'type': 'table',
        'title': 'Trading pair information',
        'cols': ['Number', '[Mode][Multiple]', 'Currency Information', 'Opening Direction', 'Opening Quantity', 'Position Price', 'Current Price', 'Liquidation Price', 'Liquidation Difference', 'Position Value', 'Margin', 'Unrealized Profit and Loss', 'Surrender'],
        'rows': []
    }
    i = 0
    for symbol in tradeSymbols:
        i += 1
        direction = 'Short position'
        margin = direction
        if assets[symbol]['amount'] != 0:
            direction = 'go long' + SuccessColor if assets[symbol]['amount'] > 0 else 'go short' + DangerColor
            margin = 'Cross position' if assets[symbol]['marginType'] == 'cross' else 'Isolated position'
        price = _N((assets[symbol]['ask_price'] + assets[symbol]['bid_price']) / 2 ,tradeInfo[symbol]['priceSize'])
        value = _N((assets[symbol]['ask_value'] + assets[symbol]['bid_value'])/2 , 2)
        if value != 0:
            if value > 0:
                TotalLong += value
            else:
                TotalShort += value
        unrealised_profit_color = '#000000'
        if assets[symbol]['unrealised_profit'] > 0:
            unrealised_profit_color = SuccessColor
        if assets[symbol]['unrealised_profit'] < 0:
            unrealised_profit_color = DangerColor
        infoList = [
            i,
            '['+ margin +']' +'[' + str(assets[symbol]['leverage']) +'X]',
            symbol,
            direction,
            abs(assets[symbol]['amount']),
            assets[symbol]['hold_price'],
            price,
            assets[symbol]['liquidationPrice'],
            '0' if assets[symbol]['liquidationPrice'] == 0 else '$' + str(_N(assets[symbol]['liquidationPrice'] - price, 5)) + ' ≈ ' + str(_N(assets[symbol]['liquidationPrice'] / price * 100, 2)) + '%' + WrningColor, #Forced liquidation price
            abs(value),
            _N(assets[symbol]['positionInitialMargin'],2),
            str(_N(assets[symbol]['unrealised_profit'], 3)) + unrealised_profit_color,
            {
                'type': 'button',
                'cmd': 'There was supposed to be no retreat???:' + symbol + ':' + str(assets[symbol]['amount']) + ':',
                'name': symbol + ' Surrender'
            }

        ]
        table['rows'].append(infoList)
        logString = json.dumps(assets['USDT'])

        StatusData = AppendedStatus()
        LogStatus(StatusData['upTable'] + '`' + json.dumps([table, StatusData['indexTable']]) + '`\n' + logString)
        # LogStatus('`' + json.dumps([table, StatusData['indexTable']]) + '`\n' + logString)

        if int(time.time()*1000) - updateProfitTime > LogInterval * 1000:
            balance = assets['USDT']['total_balance']
            if Show:
                balance = assets['USDT']['total_balance'] - Funding
            LogProfit(_N(balance, 3), '&')
            updateProfitTime = int(time.time()*1000)
            if Profit != 0 and (_N(balance, 0) != Profit): #The first time will not be calculated, and the winning rate will not be calculated to the decimal point.
                TradingCounter("totalProfit", 1) #Count the number of prints, winning rate = number of profits/number of prints*100
                if _N(balance, 0) > Profit:
                    TradingCounter('profitNumber', 1) #Number of Wins
                WinRate()
            Profit = _N(balance,0)


# Main logic of strategy
def Process():
    # UpdateTick()
    for symbol in tradeSymbols:
        if assets[symbol]['ask_price'] == 0 : continue
        aim_value = -TradeValue * _N(assets[symbol]['btc_diff'] / 0.01 ,3)  #Calculate the positions that need to be added if the deviation is 1%
        #Offset Position - Held Position > Deviation add-position threshold and diff > Default minimum opening value and multi-position - Short position less than or equal to 1.1times the deviation, open a long position
        # if symbol == 'IOTA':
        #     Log(symbol,aim_value - assets[symbol]['ask_value'])
        if (aim_value - assets[symbol]['ask_value']) >= DeviateValue and assets[symbol]['btc_diff'] > MinDiff :
            Log('go long',symbol,'   aim_value:',aim_value,'   ask_value:',assets[symbol]['ask_value'],'amount:',(aim_value - assets[symbol]['ask_value']), '   Deviation from average:',assets[symbol]['btc_diff'])
            Trade(symbol,'BUY',aim_value - assets[symbol]['ask_value'])
        if (aim_value - assets[symbol]['bid_value']) <= -DeviateValue and assets[symbol]['btc_diff'] < MaxDiff:
            Log('go short',symbol,'   aim_value:',aim_value,'   ask_value:',assets[symbol]['ask_value'],'amount:',(aim_value - assets[symbol]['bid_value']),  '   Deviation from average:',assets[symbol]['btc_diff'])
            Trade(symbol,'SELL',-(aim_value - assets[symbol]['bid_value']) )


# Save transaction volume
def TradingCounter(key,newValue):
    value = _G(key)
    if value is None:
        _G(key,newValue)
    else:
        _G(key,value + newValue)


def WinRate():
    global WinRateData
    for symbol in tradeSymbols:
        unrealised = assets[symbol]['unrealised_profit']
        WinRateData[symbol]['totalProfit'] += 1
        if unrealised != 0:
            if unrealised > 0:
                WinRateData[symbol]['profitNumber'] += 1
    _G("WinRateData", WinRateData)

#Update win rate information
def InitRateData():
    global WinRateData
    if Reset:
        _G('WinRateData',None)
    if _G('WinRateData'):
        WinRateData = _G('WinRateData')
    for symbols in tradeSymbols:
        if symbols not in WinRateData:
                                 #Count of statistics        #Number of Wins          #Number of Trades       #Number of long trades        #Number of short trades
            WinRateData[symbols] = {'totalProfit': 0, 'profitNumber': 0,'tradeNumber': 0,'buyNumber': 0, 'sellNumber': 0}
    _G('WinRateData',WinRateData)
 #Get or create the strategy's first startup time
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
    exchange.SetContractType('swap')
    exchange.SetMarginLevel(20)
    SetErrorFilter("502:|503:|tcp|character|unexpected|network|timeout|WSARecv|Connect|GetAddr|no such|reset|http|received|EOF|reused|Unknown")
    global runtimeData
    while True:
        runtimeData = RunTime()
        #Update account and positions
        UpdateAccount()
        #Update Quotes
        UpdateTick()
        #Stop-Loss Module
        StopLoss()
        #Strategy Logic
        Process()
        #Output status bar information
        UpdateStatus()

        Sleep(Interval * 1000)

```

> Detail

https://www.fmz.com/strategy/322094

> Last Modified

2021-10-09 13:46:54
