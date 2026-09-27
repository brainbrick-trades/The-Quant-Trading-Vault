
> Name

WR-Breakthrough-Martin

> Author

老虎量化



> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|period|15|KLine period|
|marginLevel|20|Leverage multiple|
|baseAmount|10|Initial Position OpenedU|
|WRperiod|14|WRtimeframe|
|zhiy|100|take profit%|
|zhis|100|stop loss%|
|autoMoveStocks|false|Automatically remove when available assets exceed *U100U|
|maxBuc|10|Maximum multiplication times|




|Button|Default|Description|
|----|----|----|
|Liquidation shutdown|__button__|Liquidation shutdown|


> Source (python)

``` python
'''backtest
start: 2021-03-19 05:00:00
end: 2021-03-21 00:00:00
period: 15m
basePeriod: 15m
exchanges: [{"eid":"Futures_HuobiDM","currency":"BTC_USD"},{"eid":"Futures_HuobiDM","currency":"ETH_USD","stocks":300},{"eid":"Futures_HuobiDM","currency":"EOS_USD","stocks":5000}]
args: [["openConMode",null]]
'''

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import time
import talib
import math
import urllib.request

ChartCfg = {
    '__isStock': True,
    'title': {
        'text': 'WR'
    },
    'yAxis': [{
        'title': {'text': 'WR'},
        'style': {'color': '#4572A7'},
        'opposite': False #Right axis
    }],
    'series': [{
        'type': 'line',
        'id': 'wr',
        'name': 'wr',
        'data': []
    }]
}

def MyLog(str1,ktime,price=''):
    if (_G('str')!=str1 or _G('ktime')!=ktime) and  not (_G('str2')==str1 and ktime==_G('ktime2')) :
        _G('str2',_G('str'))
        _G('ktime2',_G('ktime'))

        _G('str',str1)
        _G('ktime',ktime)
        Log(str1+str(price)) 


def moveStocks(_moveStocks):
    global todayProfit
    if exchanges[0].GetName().find('Binance')>=0:#Futures_Binance  Only the currency standard has delivery and shares funds 2-U standard to spot 4-Coin standard to spot ReturntranId
        if exchanges[0].GetCurrency().find('USDT')>=0:
            movecurrency = 'USDT'
            mtype = 2
        else:#Coin-based
            movecurrency = 'BTC'
            mtype = 4
        timestamp = Unix()*1000       
        params = "type="+str(mtype)+"&asset="+movecurrency+"&amount="+str(_moveStocks)+"&timestamp="+str(timestamp)
        exchanges[0].SetBase('https://api.binance.com')
        moveid = exchange.IO("api", "POST", "/sapi/v1/futures/transfer", params)   
        exchanges[0].SetBase('https://fapi.binance.com')
        if moveid is not None:
            Log('Fund withdrawal successful',moveid)
            _G('moveStocks',_G('moveStocks')+_moveStocks)
            todayProfit["initStocks"] = todayProfit["initStocks"] - _moveStocks
            _G('todayProfit',todayProfit)
            
        else:
            Log('Fund withdrawal failed')
    else:
        Log('Transfer from this exchange is not supported yet')
    
def cancelOD(i):
    orders = _C(exchanges[i].GetOrders)
    for order in orders:
        exchanges[i].CancelOrder(order.Id)
        Sleep(100)

def coverAll(i):
    position = _C(exchanges[i].GetPosition)
    cancelOD(i)
    Sleep(200)
    for j in range(len(position)):
        pamount = position[j]["Amount"] #-position[0]["FrozenAmount"]
        if position[j]["Type"]==0:     #Long positions
            Deal(-1 , pamount, "closebuy", exchanges[i].GetCurrency()+'Manual market closing',i)
        elif position[j]["Type"]==1:     #Short positions
            Deal(-1 , pamount, "closesell", exchanges[i].GetCurrency()+'Manual market closing',i)
        
def  getOpenPrice(position):
    if hasattr(position[0],'Info') and hasattr(position[0].Info,'cost_open'):#huobi
        return position[0].Info.cost_open
    elif hasattr(position[0],'Info') and hasattr(position[0].Info,'avg_cost'):#ok
        return position[0].Info.avg_cost
    elif hasattr(position[0],'Info') and hasattr(position[0].Info,'entryPrice'):#binance
        return position[0].Info.entryPrice
    else:
        return position[0]["Price"] 

    
def UpdateAccout():
    accout = _C(exchanges[0].GetAccount)
    acc1 = accout.FrozenBalance    #Frozen balance of other coins – whether to share?
    acc2 = accout.Balance
    
    _G("ableAccount", acc2)#Current AvailableU
    _G("allAccount",acc1+acc2+GetMargin()) #Unrealized profit not calculated
    if acc2<1:
        Log("Insufficient account margin balance")
        Sleep(8000)

def GetMargin():
    allMargin = 0
    for i in range(len(exchanges)):
        allMargin += _G("margin")[i]
    return _N(allMargin,2)


def GetHighest(records,i,period):
    high = 0
    for i in range(i-period+1,i+1):
        if records[i].High > high:
            high = records[i].High
    return high

def GetLowest(records,i,period):
    low = 1000000
    for i in range(i-period+1,i+1):
        if records[i].Low < low:
            low = records[i].Low
    return low
    
        
def SetType(type):
    if type==0:
        _G("contractType","swap")
    elif type==1:
        _G("contractType","this_week")
    elif type==2:
        _G("contractType","next_week")
    elif type==3:
        _G("contractType","quarter")
    elif type==4:
        _G("contractType","next_quarter")
        
def Deal(price, num, btype, beizhu='',i=0 ):
    Sleep(50)
    #if beizhu!='':
    #    Log(beizhu)
    exchanges[i].SetDirection(btype)
    if btype=="closebuy" or btype=="sell" :
        exchanges[i].Sell(price , num, beizhu)
        #Log('open short',price)
    else:
        exchanges[i].Buy(price , num, beizhu)
        #Log('open long',price)


def myProfit():
    LogProfit( _G("allAccount")-_G("initStocks") )


def initData():
    SetErrorFilter("502:|503:|tcp|character|unexpected|network|timeout|WSARecv|Connect|GetAddr|no such|reset|http|received|EOF|No need to change|reused")
    global allCoinData
    Log("Initializing...")

    if exchanges[0].GetName().find('Binance')>=0:#Futures_Binance
        getBinanceAllCoinData()
        Sleep(3000)
        Log("Finished obtaining exchange information")
    else:
        Log('This exchange is not supported yet')
        return
    
    if _G("moveStocks") is None:
        _G("moveStocks",0)
    if _G("moveInStocks") is None:
        _G("moveInStocks",0)
        
    for i in range(len(exchanges)):#Initialize exchange
        symbol = exchanges[i].GetCurrency().split('_')[0]
        exchanges[i].SetContractType("swap")
        exchanges[i].SetPrecision(allCoinData[symbol]['tick_size'], allCoinData[symbol]['size_increment'])
        exchanges[i].SetMarginLevel(marginLevel)
        timestamp = Unix()*1000      
        exchanges[i].IO("api", "POST", "/fapi/v1/positionSide/dual", "dualSidePosition=true&timestamp="+str(timestamp))
        
    
        
def main():
    global allCoinData, orderID
    if _G("contractType") is None:
        _G("contractType","swap")
    global ChartCfg
    preTime = 0
    chart = Chart(ChartCfg)
    chart.reset()
    
    margin = [0 for i in range(len(exchanges)) ] 
    _G("margin",margin)
    preTime = 0
    bucTimes = [0 for i in range(len(exchanges)) ] 
    initData()
    #LogProfitReset(1)
    #Position insufficiency not yet considered
    while(true):
        #Log('Test Loop')
        cmd = GetCommand()
        if cmd:
            if cmd == "Stop Clearing Positions":
                for i in range(len(exchanges)):
                    Sleep(100)
                    coverAll(i)
                Sleep(1000)
                return
            if cmd.find('cover-')>=0:
                arr = cmd.split("-")
                coverAll(int(arr[1]))
                Sleep(2000)
            elif cmd == 'cancelOD':
                cancelOD()
                Sleep(1000)
        
        tab1 = {
            "type": "table", 
            "title": "Account Information", 
            "cols": ["Initial funds", "Current funds", "Available funds", "Withdrawn funds", "Total profit rate"], 
            "rows": []
        }
        tab2 = {
            "type": "table", 
            "title": "Position Status", 
            "cols": ["Currency", "Latest Price", "Number of Positions", "Average Position Price", "Floating P&L", "Operation"], 
            "rows": []
        }
        
        
        UpdateAccout() 
        if _G("initStocks") is None or _G("initStocks")<10 :
            _G("initStocks", _G("allAccount"))
        if autoMoveStocks>100 and _G('ableAccount')>autoMoveStocks :
                Log('Automatic fund removal:100U#32CD32')
                moveStocks(100)
                continue

        for i in range(len(exchanges)):
            Sleep(100)
            records = _C(exchanges[i].GetRecords,60 * period)
            #wr_high = TA.Highest(records, WRperiod, 'High')
            #wr_low = TA.Lowest(records, WRperiod, 'Low')
            #wr = (records[-1].Close-wr_high)/(wr_high-wr_low)*100
            position = _C(exchanges[i].GetPosition)
            margin = _G("margin")
            if len(position)>0:
                oprice = float(getOpenPrice(position))
                margin[i] = position[0]["Margin"]
                floatProfit =  float(position[0]["Profit"])
                pamount = float(position[0]['Amount'])
                #stop loss
                if -1*floatProfit > oprice*pamount/marginLevel*zhis/100:
                    if position[0]['Type']==0:
                        Deal(-1, pamount, 'closebuy',exchanges[i].GetCurrency()+' Long Position Stop Loss'+format(records[-1].Close,'.4f'),i)
                    else:
                        Deal(-1, pamount, 'closesell',exchanges[i].GetCurrency()+' Short Position Stop Loss'+format(records[-1].Close,'.4f'),i)
                    Sleep(500)
                    myProfit()
                    bucTimes[i] += 1
                    if bucTimes[i]>maxBuc:
                        bucTimes[i] = maxBuc
                #take profit
                if floatProfit > oprice*pamount/marginLevel*zhiy/100:
                    if position[0]['Type']==0:
                        Deal(-1, pamount, 'closebuy',exchanges[i].GetCurrency()+' Long Position Take Profit'+format(records[-1].Close,'.4f'),i)
                    else:
                        Deal(-1, pamount, 'closesell',exchanges[i].GetCurrency()+' Short Position Take Profit'+format(records[-1].Close,'.4f'),i)
                    Sleep(500)
                    myProfit()
                    bucTimes[i] = 0
            else:
                oprice = 0
                margin[i] = 0
                floatProfit = ''

            _G("margin", margin)
            
            
            for k in range(50, len(records)):

                wr_high1 = GetHighest(records,k, WRperiod)
                wr_low1 = GetLowest(records,k, WRperiod)
                wr1 = (records[k].Close-wr_high1)/(wr_high1-wr_low1)*100
                if k==len(records)-1:
                    if wr1>-5:#open short
                        if len(position)==0 or (len(position)>0 and position[0]['Type']==0):#close long
                            if len(position)>0:
                                Deal(-1, pamount, 'closebuy',exchanges[i].GetCurrency()+' Close Long Position'+format(records[-1].Close,'.4f'),i)
                                Sleep(500)
                                myProfit()
                                if floatProfit<0:
                                    bucTimes[i] += 1
                                    if bucTimes[i]>maxBuc:
                                        bucTimes[i] = maxBuc
                                else:
                                    bucTimes[i] = 0
                            symbol = exchanges[i].GetCurrency().split('_')[0]
                            famount = _N( baseAmount/records[-1].Close, allCoinData[symbol]['size_increment'] )
                            if famount==0:
                                Log(exchanges[i].GetCurrency(),'Current Open PositionUInsufficient to buy, please change currency or increase opening positionU')
                                continue
                            pamount = (baseAmount*(2**bucTimes[i]))/records[-1].Close
                            Log(exchanges[i].GetCurrency(),baseAmount,bucTimes[i],records[-1].Close)
                            Deal(-1, pamount, 'sell',exchanges[i].GetCurrency()+' Open Short Position'+format(records[-1].Close,'.4f')+' WR:'+str(wr1),i)
                    elif wr1<-95:#open long
                        if len(position)==0 or (len(position)>0 and position[0]['Type']==1):#close short
                            if len(position)>0:
                                Deal(-1, pamount, 'closesell',exchanges[i].GetCurrency()+' Close Short Position'+format(records[-1].Close,'.4f'),i)
                                Sleep(500)
                                myProfit()
                                if floatProfit<0:
                                    bucTimes[i] += 1
                                    if bucTimes[i]>maxBuc:
                                        bucTimes[i] = maxBuc
                                else:
                                    bucTimes[i] = 0
                            symbol = exchanges[i].GetCurrency().split('_')[0]
                            famount = _N( baseAmount/records[-1].Close, allCoinData[symbol]['size_increment'] )
                            if famount==0:
                                Log(exchanges[i].GetCurrency(),'Current Open PositionUInsufficient to buy, please change currency or increase opening positionU')
                                continue
                            pamount = (baseAmount*(2**bucTimes[i]))/records[-1].Close
                            Log(exchanges[i].GetCurrency(),baseAmount,bucTimes[i],records[-1].Close)
                            Deal(-1, pamount, 'buy',exchanges[i].GetCurrency()+' Open Long Position'+format(records[-1].Close,'.4f')+' WR:'+str(wr1),i)        
                    #Log(wr1)
                
                #Drawing
                if i==0 and records[k]['Time'] == preTime:
                    chart.add(0, [records[k]['Time'], wr1], -1)
                elif i==0 and records[k]['Time'] > preTime:
                    #Log('insert',records[k]['Time'],wr_high1,wr_low1,records[k].Close,wr1)
                    chart.add(0, [records[k]['Time'], wr1])
                    preTime = records[k]['Time']
            

            #myProfit()

            if len(position)>0 and position[0]['Type']==0:
                pamount = 'Many:'+str(position[0]['Amount'])+str('#32CD32')
            elif len(position)>0 and position[0]['Type']==1:
                pamount = 'Empty:'+str(position[0]['Amount'])+str('#BC1717')
            else:
                pamount = ''
            if len(position)>0:
                floatProfit = format( position[0]["Profit"],'.2f')
            symbol = exchanges[i].GetCurrency().split('_')[0]
            tab2["rows"].append([ exchanges[i].GetCurrency() , records[-1].Close \
                             , pamount, format(oprice,'.'+str(allCoinData[symbol]['tick_size'])+'f'), floatProfit \
                             , { "type": "button",  "cmd": 'cover-'+str(i), "name": "close all positions" } ])

        #Total profit
        allzhiy = float(_G('allAccount'))-float(_G('moveInStocks'))+float(_G('moveStocks'))-float(_G('initStocks'))
        if _G('initStocks')==0:
            allzhiyl=0
        else:
            allzhiyl = (float(_G('moveStocks'))+float(_G('allAccount'))-float(_G('moveInStocks'))-float(_G('initStocks')))/float(_G('initStocks'))*100
         
        tab1["rows"].append([format(_G('initStocks'),'.1f')+'U', format(_G('allAccount'),'.1f')+'U', format(_G('ableAccount'),'.1f')+'U', format(_G('moveStocks'),'.1f')+'U' \
                             , format(allzhiyl,'.1f')+'%('+format(allzhiy,'.1f')+'U)'])    
        LogStatus(  '`' +json.dumps(tab1) + "`\n" +"`" + json.dumps(tab2) + "`\n"  )
           
        Sleep(1000)
           
                

# Get all currency pair news of Binance perpetual contract
def getBinanceAllCoinData():
    global allCoinData
    tmp = dict()
    data = getUrlData("http://fapi.binance.com/fapi/v1/exchangeInfo")
    for item in data['symbols']:
        # USDT is required as the measuring currency pair
        if "USDT" in item["symbol"]:
            size = item['filters'][1]['stepSize']    # DOGE 1.00000000   BTC 0.00000100
            if float(size) == 1:
                sizein = 0
            elif len(size.split("."))>1:
                sizein = str(size).split(".")[1].find('1')+1
            else:
                sizein = 0
            tmp[item["baseAsset"]] = {
                'tick_size': int(item['pricePrecision']),  # Price Precision
                'old_increment': item['filters'][1]['stepSize'],#Minimum purchase value
                'size_increment': sizein # Converted Quantity
            }
    allCoinData = tmp
    
    
# Get data via URL
def getUrlData(url):
    response = urllib.request.urlopen(url)
    html = response.read().decode('utf-8')#decode('utf-8') Solve:the JSON object must be str, not 'bytes'
    try:
        tmp = json.loads(html)
        return json.loads(html)
    except Exception as e:
        Log('e:',e)      

        
# Perform take-profit and stop-loss on the contract cangType=0, the default is isolated position =1 full position
def zhiyingzhisun(i, amount, directionStr, positionSide, zhiying, zhisun, cangType = 0):
    return bianSwap(i, amount, directionStr, positionSide, zhiying, zhisun)
 
# Send Request
def AsynIo(i, paramList):
        if (len(paramList) == 3):
            arrRoutine = exchanges[i].Go("IO", paramList[0], paramList[1], paramList[2])
        elif (len(paramList) == 4):
            arrRoutine = exchanges[i].Go("IO", paramList[0], paramList[1], paramList[2], paramList[3])
        elif (len(paramList) == 5):
            arrRoutine = exchanges[i].Go("IO", paramList[0], paramList[1], paramList[2], paramList[3], paramList[4])
        data, ok = arrRoutine.wait()
        Log(data)
        return data

# Binance contract
def bianSwap(i, amount, directionStr, positionSide, zhiying, zhisun):
    global orderID
    instrument_id = exchanges[i].GetCurrency().replace('_',"")
    # UStandard or currency standard, set requesturl
    if instrument_id.find('USDT') >= 0 :
        url = "/fapi/v1/order"
    elif instrument_id.find('USD') >= 0 :
        url = '/dapi/v1/order'
    else:
        return False
    # stop loss  side = SELL  BUY
    '''
    timestamp = Unix()*1000      
    params = "symbol="+instrument_id+"&side="+str(directionStr)+"&positionSide="+positionSide+"&type=STOP_MARKET&stopPrice="+str(zhisun)+"&closePosition=true&timestamp="+str(timestamp)
    Log(params)
    zhisunData = exchanges[i].IO("api", "POST", "/fapi/v1/order", params)
    Log(zhisunData)
    '''
    zhisunData = AsynIo(i, ['api', 'POST', url , '', json.dumps({
        "symbol": instrument_id,
        "side": directionStr,
        "positionSide":positionSide,
        "type": "STOP_MARKET",
        #"quantity": amount,
        "closePosition":"true",
        #"price": zhisun,
        "stopPrice": zhisun,
        "timestamp": str(int(round(time.time() * 1000)))
    })])

    if int(float(zhisunData['stopPrice'])) != int(float(zhisun)):
        Log('Stop loss prices are different',float(zhisunData['stopPrice']),int(float(zhisunData['stopPrice'])), float(zhisun), int(float(zhisun)) )
        return False
    orderID[i][0] = zhisunData['orderId']
    Log('Settings'+exchanges[i].GetCurrency()+'Stop loss, order number:'+str(orderID[i][0]))
    # take profit
    zhiyingData = AsynIo(i, ['api', 'POST', url , '', json.dumps({
        "symbol": instrument_id,
        "side": directionStr,
        "positionSide":positionSide,
        "type": "TAKE_PROFIT_MARKET",
        #"quantity": amount,
        "closePosition":"true",
        #"price": zhiying,
        "stopPrice": zhiying,
        "timestamp": str(int(round(time.time() * 1000)))
    })])
    if int(float(zhiyingData['stopPrice'])) != int(zhiying):
        Log('The take-profit prices are different',float(zhiyingData['stopPrice']),int(float(zhiyingData['stopPrice'])), float(zhiying), int(float(zhiying)) )
        return False
    orderID[i][1] = zhiyingData['orderId']
    Log('Settings'+exchanges[i].GetCurrency()+'Take profit, order number:'+str(orderID[i][1]))
    _G("orderID",orderID)
    return True
   
    

    
```

> Detail

https://www.fmz.com/strategy/301145

> Last Modified

2021-09-02 13:06:24
