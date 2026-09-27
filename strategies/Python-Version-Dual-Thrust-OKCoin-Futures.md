
> Name

Python-Version-Dual-Thrust-OKCoin-Futures

> Author

发明者量化-小小梦

> Strategy Description

Dual Thrust The strategy includes complete chart display, dynamic chart updates, template references, and other functions, which can be used as learning templates.

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|ContractTypeIdx|0|contract types: this week | next week | quarter|
|MarginLevelIdx|0|Leverage Size: 10|20|
|NPeriod|4|Calculation cycle|
|Ks|0.5|Upper rail coefficient|
|Kx|0.5|Lower rail coefficient|
|AmountOP|true|Open contract quantity|
|Interval|2000|Retry interval (milliseconds))|
|LoopInterval|3|Polling interval (seconds)|
|PeriodShow|500|Maximum number of candlestick bars displayed on chart|


> Source (python)

``` python
import time
class Error_noSupport(BaseException):
    def __init__(self):
        Log("only supportsOKCoinfutures!#FF0000")

class Error_AtBeginHasPosition(BaseException):
    def __init__(self):
        Log("Futures positions at startup! #FF0000")

ChartCfg = {
    '__isStock': True,
    'title': {
        'text': 'Dual Thrust Upper and lower track diagram'
    },
    'yAxis': {
        'plotLines': [{
            'value': 0,
            'color': 'red',
            'width': 2,
            'label': {
                'text': 'Upper rail',
                'align': 'center'
            },
        }, {
            'value': 0,
            'color': 'green',
            'width': 2,
            'label': {
                'text': 'Lower Band',
                'align': 'center'
            },
        }]
    },
    'series': [{
        'type': 'candlestick',
        'name': 'Current cycle',
        'id': 'primary',
        'data': []
    }, {
        'type': 'flags',
        'onSeries': 'primary',
        'data': []
    }]
}

STATE_IDLE = 0
STATE_LONG = 1
STATE_SHORT = 2
State = STATE_IDLE

LastBarTime = 0
UpTrack = 0
BottomTrack = 0
chart = None
InitAccount = None
LastAccount = None
Counter = {
    'w': 0,
    'l': 0
}

def GetPosition(posType):  # if the positions has no this posType ,will return [] ,Another case is return a dict of object
    positions = exchange.GetPosition()
    return [{'Price': position['Price'], 'Amount': position['Amount']} for position in positions if position['Type'] == posType]

def CancelPendingOrders():
    while True:
        orders = exchange.GetOrders()
        [exchange.CancelOrder(order['Id']) for order in orders if not Sleep(500)]
        if len(orders) == 0:
            break 

def Trade(currentState,nextState):
    global InitAccount,LastAccount,OpenPrice,ClosePrice
    ticker = _C(exchange.GetTicker)
    slidePrice = 1
    pfn = exchange.Buy if nextState == STATE_LONG else exchange.Sell 
    if currentState != STATE_IDLE:
        Log(_C(exchange.GetPosition)) # ceshi 
        exchange.SetDirection("closebuy" if currentState == STATE_LONG else "closesell")
        while True:
            ID = pfn( (ticker['Last'] - slidePrice) if currentState == STATE_LONG else (ticker['Last'] + slidePrice), AmountOP) # xiugai Limit order
            # ID = pfn(-1, AmountOP) # xiugai  market order
            # ID = pfn(AmountOP) # xiugai  market order
            Sleep(Interval)
            Log(exchange.GetOrder(ID)) # xiugai
            ClosePrice = (exchange.GetOrder(ID))['AvgPrice'] # 
            CancelPendingOrders()
            if len(GetPosition(PD_LONG if currentState == STATE_LONG else PD_SHORT)) == 0:
                break 
        account = exchange.GetAccount()
        if account['Stocks'] > LastAccount['Stocks']:
            Counter['w'] += 1
        else:
            Counter['l'] += 1
        # Log("ceshi account:",account,InitAccount) #ceshi
        Log(account) # xiugai
        LogProfit((account['Stocks'] - InitAccount['Stocks']),"Yield:", ((account['Stocks'] - InitAccount['Stocks']) * 100 / InitAccount['Stocks']),'%')
        Cal(OpenPrice,ClosePrice)
        LsatAccount = account 
    
    exchange.SetDirection("buy" if nextState == STATE_LONG else "sell") 
    Log(_C(exchange.GetAccount))
    while True:
        ID = pfn( (ticker['Last'] + slidePrice) if nextState == STATE_LONG else (ticker['Last'] - slidePrice), AmountOP) # Limit order
        # ID = pfn(-1, AmountOP) # market order
        # ID = pfn(AmountOP) # market order
        Sleep(Interval)
        Log(exchange.GetOrder(ID)) # xiugai
        CancelPendingOrders()
        pos = GetPosition(PD_LONG if nextState == STATE_LONG else PD_SHORT)
        if len(pos) != 0:
            Log("Average position price",pos[0]['Price'],"Quantity:",pos[0]['Amount'])
            OpenPrice = (exchange.GetOrder(ID))['AvgPrice'] # pos[0]['Price']
            Log("now account:",exchange.GetAccount())
            break 

def onTick(exchange):
    global LastBarTime,chart,State,UpTrack,DownTrack,LastAccount
    records = exchange.GetRecords()
    if not records or len(records) <= NPeriod:
        return 
    Bar = records[-1]
    if LastBarTime != Bar['Time']:
        HH = TA.Highest(records, NPeriod, 'High')
        HC = TA.Highest(records, NPeriod, 'Close')
        LL = TA.Lowest(records, NPeriod, 'Low')
        LC = TA.Lowest(records, NPeriod, 'Close')
        
        Range = max(HH - LC, HC - LL)
        UpTrack = _N(Bar['Open'] + (Ks * Range))
        DownTrack = _N(Bar['Open'] - (Kx * Range))
        if LastBarTime > 0:
            PreBar = records[-2]
            chart.add(0, [PreBar['Time'], PreBar['Open'], PreBar['High'], PreBar['Low'], PreBar['Close']], -1)
        else:
            for i in range(len(records) - min(len(records), NPeriod * 3), len(records)):
                b = records[i]
                chart.add(0,[b['Time'], b['Open'], b['High'], b['Low'], b['Close']])
                
        chart.add(0,[Bar['Time'], Bar['Open'], Bar['High'], Bar['Low'], Bar['Close']])
        ChartCfg['yAxis']['plotLines'][0]['value'] = UpTrack 
        ChartCfg['yAxis']['plotLines'][1]['value'] = DownTrack 
        ChartCfg['subtitle'] = {
            'text': 'Upper rail' + str(UpTrack) + 'Lower Band' + str(DownTrack)
        }
        chart.update(ChartCfg)
        chart.reset(PeriodShow)
        
        LastBarTime = Bar['Time']
    else:
        chart.add(0,[Bar['Time'], Bar['Open'], Bar['High'], Bar['Low'], Bar['Close']], -1)
        
    LogStatus("Price:", Bar["Close"], "up:", UpTrack, "down:", DownTrack, "wins:", Counter['w'], "losses:", Counter['l'], "Date:", time.time())
    msg = ""
    if State == STATE_IDLE or State == STATE_SHORT:
        if Bar['Close'] >= UpTrack:
            msg = "Go long, trigger price:" + str(Bar['Close']) + "Upper rail" + str(UpTrack)
            Log(msg)
            Trade(State, STATE_LONG)
            State = STATE_LONG 
            chart.add(1,{'x': Bar['Time'], 'color': 'red', 'shape': 'flag', 'title': 'Many', 'text': msg})
    
    if State == STATE_IDLE or State == STATE_LONG:
        if Bar['Close'] <= DownTrack:
            msg = "Short selling, trigger price:" + str(Bar['Close']) + "Lower Band" + str(DownTrack)
            Log(msg)
            Trade(State, STATE_SHORT)
            State = STATE_SHORT
            chart.add(1,{'x': Bar['Time'], 'color': 'green', 'shape': 'circlepin', 'title': 'Empty', 'text': msg})

OpenPrice = 0
ClosePrice = 0
def Cal(OpenPrice, ClosePrice):
    global AmountOP,State
    if State == STATE_SHORT:
        Log(AmountOP,OpenPrice,ClosePrice,"Strategic Profit and Loss:", (AmountOP * 100) / ClosePrice - (AmountOP * 100) / OpenPrice, "Coins, transaction fee:", - (100 * AmountOP * 0.0003), "US Dollar,Equivalent:", _N( - 100 * AmountOP * 0.0003/OpenPrice,8), "Currency")
        Log(((AmountOP * 100) / ClosePrice - (AmountOP * 100) / OpenPrice) + (- 100 * AmountOP * 0.0003/OpenPrice))
    if State == STATE_LONG:
        Log(AmountOP,OpenPrice,ClosePrice,"Strategic Profit and Loss:", (AmountOP * 100) / OpenPrice - (AmountOP * 100) / ClosePrice, "Coins, transaction fee:", - (100 * AmountOP * 0.0003), "US Dollar,Equivalent:", _N( - 100 * AmountOP * 0.0003/OpenPrice,8), "Currency")
        Log(((AmountOP * 100) / OpenPrice - (AmountOP * 100) / ClosePrice) + (- 100 * AmountOP * 0.0003/OpenPrice))

def main():
    global LoopInterval,chart,LastAccount,InitAccount
    if exchange.GetName() != 'Futures_OKCoin':
        raise Error_noSupport
    exchange.SetRate(1)
    exchange.SetContractType(["this_week","next_week","quarter"][ContractTypeIdx]) 
    exchange.SetMarginLevel([10,20][MarginLevelIdx])
    
    # Log("Fee:",exchange.GetFee())
    if len(exchange.GetPosition()) > 0:
        raise Error_AtBeginHasPosition
    CancelPendingOrders()
    InitAccount = LastAccount = exchange.GetAccount()
    LoopInterval = min(1,LoopInterval)
    Log("Trading platform:",exchange.GetName(), InitAccount)
    LogStatus("Ready...")
    
    LogProfitReset()
    chart = Chart(ChartCfg)
    chart.reset()
    
    LoopInterval = max(LoopInterval, 1)
    while True:
        onTick(exchange)
        Sleep(LoopInterval * 1000)
    
    


```

> Detail

https://www.fmz.com/strategy/21856

> Last Modified

2018-03-23 16:53:49
