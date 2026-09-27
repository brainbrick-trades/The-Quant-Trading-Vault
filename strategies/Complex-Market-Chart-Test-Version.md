
> Name

Complex-Market-Chart-Test-Version

> Author

qq89520



> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|slowEMA|26|2|
|fastEMA|12|1|
|signalEMA|9|3|
|rsi_period|9|9|


> Source (python)

``` python

'''backtest
start: 2020-03-11 00:00:00
end: 2020-04-09 23:59:00
period: 1d
exchanges: [{"eid":"Bitfinex","currency":"BTC_USD"}]
'''
import pandas as pd
import numpy as np
import re
preBarTime_1=0
'''
shortChart = {
    "__isStock" : True,
    "extension" : {
        "layout" : "group",  #singleDo not participate in grouping; display separately, default is grouped 'group'
        "height" : 300, 
    },
    "title" : {"text": 'rb888' + '__15MTrading signal chart'},
    "xAxis" : {"type" : "datetime"}, # Time series axis
    "yAxis" : [{"labels": {
        "align": 'right',
        "x": -3
    },
                "title": {
                    "text": 'Market Depth'
                },
                "height": "45%",  # Relative width size
                "resize": {
                    "enabled": True  # Whether to enable reset width  
                },
                "opposite": True,  # Whether to display the axis on the opposite side, default is left
                "offset": 0,  # Coordinate axis offset: positive right, negative left
                "lineWidth": 2  # Line width
               }, {"labels": {
        "align": 'right',
        "x": -3
    },
                   "title": {
                       "text": 'RSI'
                   },
                   "top": '45%',
                   "height": '25%',
                   "opposite": True,
                   "offset": 0,
                   "lineWidth": 2
                  }, {"labels": {
        "align": 'right',
        "x": -3
    },
                      "title": {
                          "text": 'MACD_5'
                      },
                      "top": '70%',
                      "height": '30%',
                      "opposite": True,
                      "offset": 0,
                      "lineWidth": 2
                     }    
              ],
    "tooltip":{
        "split": False,  # Nativejs??
        "xDateFormat" : "%Y-%m-%d %H:%M:%S, %A"
    },
    "series" : [{'type': 'candlestick',
                 'name': 'kLine',
                 #'color': 'green',
                 #'lineColor': 'green',  # Default display color settings; if not null, it is displayed according to this setting.
                 #'upColor': 'red',
                 #'upLineColor': 'red',
                 "data" : [],
                }, {
            "type" : "line",
            "name" : "rsi",
            "data" : [],
            "yAxis": 1  # Relative position
        }
        , {
            "type" : "line",
            "name" : "diff",
            "data" : [],
            "yAxis": 2  # Relative position
        }, {
            "type" : "line",
            "name" : "dea",
            "data" : [],
            "yAxis": 2  # Relative position
        }, {
            "type" : "column",
            "name" : "macd",
            "data" : [],
            "yAxis": 2  # Relative position
        }
    ]
}
'''
"""
shortChart = {
    "__isStock" : True,
    "extension" : {
        "layout" : "single",  #singleDo not participate in grouping; display separately, default is grouped 'group'
        "height" : 300, 
    },
    "title" : {"text": 'rb888' + '__15MTrading signal chart'},
    "xAxis" : {"type" : "datetime"}, # Time series axis
    "yAxis" : {"labels": {
                    "align": 'right',
                    "x": -3
                },
                "title": {
                    "text": 'Market Depth'
                },
                #"height": "45%",  # Relative width size
                #"resize": {
                #    "enabled": True  # Whether to enable reset width  
                "opposite": True,  # Whether to display the axis on the opposite side, default is left
                "offset": 0,  # Coordinate axis offset: positive right, negative left
                "lineWidth": 2  # Line width
    },
    "tooltip" : {
        "split": false,  # Nativejs??
        "xDateFormat" : "%Y-%m-%d %H:%M:%S, %A"
    },
    "series" : {'type': 'candlestick',
                'name': 'kLine',
                #'color': 'green',
                #'lineColor': 'green',  # Default display color settings; if not null, it is displayed according to this setting.
                #'upColor': 'red',
                #'upLineColor': 'red',
                "data" : [],
            }
}
"""
shortChart = {
    "__isStock" : True,
    "extension" : {
    "layout" : "single",  #singleDo not participate in grouping; display separately, default is grouped 'group'
    #"height" : 500, 
    },
    'legend': {
        'enabled': true  # Legend true enabled
    },
    'title' : {
        'text' : 'Column candlestick'
    },
    "xAxis" : {
        "type" : "datetime",
        #'dashStyle': 'dash'  # Center line style dashed line
    }, # Time series axis
    'yAxis' : [{
        'labels':{
            'align':'right',
            'x':-3
        },
        'height':"40%",
        'lineWidth':2,
        #'crosshair': true,  # Crosshair Line
        'resize':{
            'enabled':true
        }
    },{
        'labels':{
            'align':'right',
            'x':-3
        },
        'title':{
            'text' : 'Volume'
        },
        'top':'40%',
        'height':'15%',
        'offset':0,
        #'crosshair': true,
        'lineWidth':2
    },{"labels": {
            "align": 'right',
            "x":-3
        },
        "title": {
            "text": 'RSI'
        },
        "top": '55%',
        "height": '20%',
        "opposite": True,
        "offset": 0,
        #'crosshair': true,
        "lineWidth": 2,
        'plotLines': [{
                'value': 75,  # Value Size
                'color': 'green',  # Color
                'dashStyle': 'shortdash', # Line style
                'width': 0.5,
                #'label': {
                #    'text': 'Long position take-profit line'
                #}
        },{
                'value': 25,
                'color': 'red',
                'dashStyle': 'shortdash',
                'width': 0.5,
                #'label': {
                #    'text': 'Short position take-profit line'
                #}
        }
        ]
    }, {"labels": {
            "align": 'right',
            "x":-3
    },
        "title": {
            "text": 'MACD'
        },
        "top": '75%',
        "height": '25%',
        "opposite": True,
        "offset": 0,
        "lineWidth": 2
    }
    ],
    'tooltip':{
        #'shared': true,  # Whether to enable sharing of prompt tags, the effect is basically the same under multiple images.split
        "xDateFormat" : "%Y-%m-%d %H:%M:%S, %A",
        'shared': true,
		'crosshairs': true,
        'valueDecimals':2, # Keep decimals
        #'split':true, # Separate tooltip
        #'distance': 30,
		#'padding': 5
        #'positioner': {
        #    'x':150,
        #    'y':150
        #},
        #'shadow': false,
        #'borderWidth': 0,
        #'backgroundColor': 'rgba(255,255,255,0.8)'
    },
    'series':[{
        'type':'candlestick',
        'animationLimit':'Infinity',
        'color': 'green',
        'lineColor': 'green',  # Default display color settings; if not null, it is displayed according to this setting.
        'upColor': 'red',
        'upLineColor': 'red',
        'name':'appl',
        'data':[]
    },{
        'type':'column',
        'name':'Volume',
        'data':[],
        'yAxis':1
    },{
        "type" : "line",
        "name" : "rsi",
        "data" : [],
        "yAxis": 2  # Relative position
    },{
        "type" : "line",
        "name" : "diff",
        "data" : [],
        "yAxis": 3  # Relative position
    },{
        "type" : "line",
        "name" : "dea",
        "data" : [],
        "yAxis": 3  # Relative position
    },{
        "type" : "column",
        "name" : "macd",
        "data" : [],
        'maxPointWidth':2,  # Maximum width of volume bar
        "yAxis": 3  # Relative position
    }

    ]
}
    

longChart = {
    "__isStock" : True,
    "extension" : {
        "layout" : "group", 
        #"height" : 300, 
    },
    'rangeSelector':{
        'selected' : 0 
    },
    'chart': {  # Main configuration items
        #'height': 630,  # Height, the platform does not support configuration
        'type': 'line',
        'zoomType': 'x',  # Zoom
        #'selectionMarkerFill':'rgba(51,92,223,0.25)',  # Background color of the zoom box
        #'panning': true,  # Turn on panning
        #'panKey': 'shift'  # Pan
        'borderColor': '#EBBA95', # Frame configuration items
        'borderWidth': 2,  ##
        'borderRadius': 10, ##
    },
    "rangeSelector" : {
        "buttons" : [{
            "type" : "hour",
            "count" : 1,
            "text" : "1h",
        }, {
            "type" : 'hour',
            "count" : 3,
            "text" : "3h"
        }, {
            "type" : "day",
            "count" : 1,
            "text" : "1d"
        }, {
            "type" : "week",
            "count" : 1,
            "text" : "1w"
        }, {
            "type" : "year",
            "count" : 1,
            "text" : "1Y"
        }, {
            "type" : "all",
            "text" : "All"
        }],
        "selected" : 1,
        "inputEnabled" : True
    },
    'legend': {
        'enabled': true  # Legend true enabled
    },
    'title' : {
        'text' : '15'
    },
    'subtitle': {
        'text': 'Xiangshui Kanpan Chart', #'Current price:'+str(records_5[-1]['Close'] if records_5[-1]['Close'] is not None else **)+' || '+'Current time:'+str(Time_5 if Time_5 is not None else **)
    },
    "xAxis" : {
        "type" : "datetime",
        #'dashStyle': 'dash'  # Center line style dashed line
    }, # Time series axis
    "xAxis" : {"type" : "datetime"},
    "yAxis" : [{
            "title": {
                "text": 'Kline'
            },
            "height": "60%",  # Relative width size
            "offset": 0,  # Coordinate axis offset: positive right, negative left
            "lineWidth": 2  # Line width
        },{
            "title": {
                "text": 'MACD'
            },
            "top": '62%',
            "height": '38%',
            "offset": 0,
            "lineWidth": 2
        }    
    ],
    "series" : [
        {
            "type" : "candlestick", 
            "name" : "k_15",
            "id" : "k",
            "data" : [],
            "yAxis": 0  # Relative position
        },{
            "type" : "column",
            "name" : "macd_15",
            "data" : [],  
            "yAxis": 1  # Relative position
        }
    ]
}

chart0 = {                                        
    "__isStock" : True,
    "extension" : {
        "layout" : "group", 
        #"height" : 300, 
    },

    'title' : { 'text' : 'Daily candlestick chart'},                       
    'xAxis': { 'type': 'datetime'},            
    'series' : [                                          
        {                                      
            'type': 'candlestick',                         
            'name': 'r',   
            'id': 'r',                                     
            'data': []                                           
        }, {                                      
            'type': 'column',           
            'name': 'vol',          
            'data': [],               
        }
    ]
}

chart1 = {  
    "__isStock" : True,
    "extension" : {
        "layout" : "group", 
        #"height" : 300, 
    },
                                      
    'title' : { 'text' : 'ris'},                       
    'xAxis': { 'type': 'datetime'},                       
    'yAxis' : {                                           
            'title': {'text': 'rsi'},                           
            'opposite': false                                 
    },
    'series' :                                      
        { 
            'type': 'line',
            #'yAxis': 1, 
            'name': 'rsi',
            'data': []
    },
}


chart2 = {  
    "__isStock" : True,
    "extension" : {
        "layout" : "group", 
        #"height" : 300, 
    },
                                      
    'title' : { 'text' : 'macd'},                       
    'xAxis': { 'type': 'datetime'},                       
    'yAxis' : {                                           
            'title': {'text': 'macd'},                           
            'opposite': false                                 
    },
    'series' :  [           
        { 
            'type': 'line',
            #'yAxis': 1, 
            'name': 'dif',
            'data': []
    },{ 
            'type': 'line',
            #'yAxis': 1, 
            'name': 'eda',
            'data': []
    },{ 
            'type': 'line',
            #'yAxis': 1, 
            'name': 'macd',
            'data': []
    },
    ]
}


hart1 = {                                        
    "__isStock" : True,
    "extension" : {
        "layout" : "group", 
        #"height" : 300, 
    },

    'title' : { 'text' : 'MACD_5'},                       
    'xAxis': { 'type': 'datetime'},             
    'series' : [                                          
        {                                      
            'type': 'candlestick',                             
            'name': 'k',   
            'id': 'r1',                                     
            'data': []                                           
        }, {                                      
            'type': 'column',           
            'name': 'macd_15',          
            'data': [],               
        }
    ]
}




macd_15 = []
runTime = {}
runTime['preBarTime_1'] = [0,0]
runTime['arrKIndex'] = []
_5_lengh = 50
_15_lengh = 50
def ticks_(records, k):
    if len(records) == 0:
        return []
    if isinstance(records[0], int) or isinstance(records[0], float):
        return records

    ticks = [None] * len(records)
    for i in range(len(records)):
        ticks[i] = records[i][k]
        return ticks


def plot(arr,_5_lengh,_15_lengh,index_2,runTime,chart):
    for x,symbol in enumerate(arr):
        #Log(symbol,_D(),)
        runTime['arrKIndex'] = [index_2[x],index_2[x]+7]   # [0,7] [8,15]
        #Log(symbol)
        exchange.SetContractType(symbol)
        #Log(symbol,_D())
        records_5 = _C(exchange.GetRecords,PERIOD_M5)  # Return as list-type dictionary
        records_15 = _C(exchange.GetRecords,PERIOD_M15)
        r = records_5
        m = records_15
        Time_5 = records_5[-1]['Time']
        Time_5_list = pd.Series(ticks_(records_5,'Time'))  # Small cycle opening time array
        #Open_5 = records_5['Open']
        #High_5 = records_5['High']
        #Low_5 = records_5['Low']
        Close_5 = pd.Series(ticks_(records_5,'Close'))  # Small period closing price array

        Time_15 = records_15[-1]['Time']
        Time_15_list = pd.Series(ticks_(records_15,'Time'))  # Small cycle opening time array
        #Open_5 = records_5['Open']
        #High_5 = records_5['High']
        #Low_5 = records_5['Low']
        Close_15 = pd.Series(ticks_(records_15,'Close'))  # Small period closing price array

        #Log(2)
        '''
        nowdea_15 = dea_15[-1]
        nowdiff_15 = diff_15[-1]
        nowmacd_15 = macd_15[-1]
        '''

        '''
        predea_15 = dea_15[-2]
        prediff_15 = diff_15[-2]
        premacd_15 = macd_15[-2]
        '''
        #index_1 += 5
        if not r or not m:
            return
        #Log(3,len(r))

        if len(r) < _5_lengh:  # Filter out situations where the candlestick is too short
            return

        #Log(4)
        Macd_5 = TA.MACD(r, fastEMA = fastEMA, slowEMA=slowEMA, signalEMA=signalEMA)
        diff_5 = Macd_5[0]
        dea_5 = Macd_5[1]
        macd_5 = pd.Series(Macd_5[2]).fillna(0)
        macd_5 = macd_5.values*2  # TAThe MACD algorithm of has not been multiplied2

        Macd_15 = TA.MACD(r, fastEMA = fastEMA, slowEMA=slowEMA, signalEMA=signalEMA)
        diff_15 = Macd_15[0]
        dea_15 = Macd_15[1]
        macd_15 = pd.Series(Macd_15[2]).fillna(0)
        macd_15 = macd_15.values*2  # TAThe MACD algorithm of has not been multiplied2

        RSI = TA.RSI(records_5, period = rsi_period)
        nowdea_5 = dea_5[-1]
        nowdiff_5 = diff_5[-1]
        nowmacd_5 = macd_5[-1]
        if len(macd_15) > 2:
            nowmacd_15 = macd_15[-1]
        nowrsi = RSI[-1]
        
        predea_5 = dea_5[-2]
        prediff_5 = diff_5[-2]
        premacd_5 = macd_5[-2]
        if len(macd_15) > 2:
            premacd_15 = macd_15[-2]
        prersi = RSI[-2]
        #Log('KLine length',len(r),'dea_5',len(dea_5),'rsi',len(RSI),preBarTime_1)
            
            

        if len(macd_15)>0:        
            #Log(time.strftime("%Y-%m-%d %H:%M:%S",  time.localtime(int(records_5[-1]['Time'])/1000)),_D(),macd_15[-1])
            pass
        
        #r = records_5
        #m = records_15
        arr_ = [r,m]        

        #Log(index_2)
        index_2 = index_2.copy()
        #index_2 = index_2.tolist()
        for i in range(len(arr_)):  # i Is candlestick period loop

            #Log(runTime['arrKIndex'])
            for j in range(len(arr_[i])):  # Time period cycle
                #Log(arr_[i][j]["Time"],runTime['preBarTime_1'][i])
                if arr_[i][j]["Time"] == runTime['preBarTime_1'][i]:  # preBarTimeInitially0
                    if i == 0:  #5Minute #index_2 0 8
                        chart.add(int(index_2[x]), [arr_[i][j]["Time"], arr_[i][j]["Open"], arr_[i][j]["High"], arr_[i][j]["Low"], arr_[i][j]["Close"]], -1)  # Select different periodsKLine'sindex
                        #Log(1,int(index_2[i]))
                    if i == 0 and len(arr_[i]) > _5_lengh:
                        #Log(2)
                        if j == len(arr_[i]) - 2:
                            #Log(3)
                            chart.add(int(index_2[x]) + 1, [arr_[i][j]["Time"], arr_[i][j]["Volume"]],-1)  
                            chart.add(int(index_2[x]) + 2, [arr_[i][j]["Time"], prersi], -1)    # Fast line
                            chart.add(int(index_2[x]) + 3, [arr_[i][j]["Time"], prediff_5], -1)    # Slow line
                            chart.add(int(index_2[x]) + 4, [arr_[i][j]["Time"], predea_5], -1)
                            chart.add(int(index_2[x]) + 5, [arr_[i][j]["Time"], premacd_5], -1)
                        elif j == len(arr_[i]) - 1:
                            #Log(4,int(index_2[i]))
                            chart.add(int(index_2[x]) + 1, [arr_[i][j]["Time"], arr_[i][j]["Volume"]],-1)  
                            #Log(4.1)
                            chart.add(int(index_2[x]) + 2, [arr_[i][j]["Time"], nowrsi], -1)    # Fast line
                            #Log(4.2)
                            chart.add(int(index_2[x]) + 3, [arr_[i][j]["Time"], nowdiff_5], -1)    # Slow line
                            #Log(4.3)
                            chart.add(int(index_2[x]) + 4, [arr_[i][j]["Time"], nowdea_5], -1)
                            #Log(4.4)
                            chart.add(int(index_2[x]) + 5, [arr_[i][j]["Time"], nowmacd_5], -1)
                            #Log(4.5)
                    '''
                    if i == 1 and len(arr_[i]) > _15_lengh:
                        if j == len(arr_[i]) - 2:
                            chart.add(index_2 + 8, [arr_[i][j]["Time"], premacd_15], -1)    # Fast line
                        elif j == len(arr_[i]) - 2:
                            chart.add(index_2 + 8, [arr_[i][j]["Time"], nowmacd_15], -1)    # Fast line
                    '''
                elif arr_[i][j]["Time"] > runTime['preBarTime_1'][i]:  # Initial run here every 5, run twice every 15 minutes
                    
                    if i ==1:
                        pass
                        
                        #Log(time.strftime("%Y-%m-%d %H:%M:%S",  time.localtime(int(arr_[i][j]["Time"])/1000)),time.strftime("%Y-%m-%d %H:%M:%S",  time.localtime(int(runTime['preBarTime_1'][i])/1000)),'//',i)
                    runTime['preBarTime_1'][i] = arr_[i][j]["Time"]  # KAssign line time topreBarTime
                    Log(runTime['preBarTime_1'][0],runTime['preBarTime_1'][1])
                    # 0 7 8 15
                    chart.add(int(runTime['arrKIndex'][x]), [arr_[i][j]["Time"], arr_[i][j]["Open"], arr_[i][j]["High"], arr_[i][j]["Low"], arr_[i][j]["Close"]])
                    if i ==0 and len(arr_[i]) > _5_lengh:
                        #Log('i=0',int(runTime['arrKIndex'][x]))
                        if j == len(arr_[i]) - 1:
                            chart.add(int(index_2[x]) + 1, [arr_[i][j]["Time"], arr_[i][j]["Volume"]])
                            chart.add(int(index_2[x]) + 2, [arr_[i][j]["Time"], nowrsi])
                            chart.add(int(index_2[x]) + 3, [arr_[i][j]["Time"], nowdiff_5])
                            chart.add(int(index_2[x]) + 4, [arr_[i][j]["Time"], nowdea_5])
                            chart.add(int(index_2[x]) + 5, [arr_[i][j]["Time"], nowmacd_5])
                    
                    if i == 1 and len(arr_[i]) > _15_lengh:
                        Log('i=1',int(index_2[x]) + 7)
                        if j == len(arr_[i]) - 1:
                            chart.add(int(index_2[x]) + 7, [arr_[i][j]["Time"], nowmacd_5])

def main():
    """
    """
    global preBarTime_1,macd_15,runTime,_5_lengh,_15_lengh,shortChart,longChart,chart0,chart1,chart2,hart1
    if exchange.GetName().find("CTP") == -1:
        raise Exception("Only supports commodity futuresCTP")
    SetErrorFilter("login|ready|Flow control | Connection failed | Initial|Timeout")
    mode = exchange.IO("mode", 0)
    if mode is None:
        raise Exception("Mode switch failed, please update to the latest host!")
    while not exchange.IO("status"):
        Sleep(3000)
        LogStatus("Waiting to connect to the trading server," + _D())
    positions = _C(exchange.GetPosition)  # Get the current position information dictionary
    if len(positions) > 0:
        Log("If the current position is detected, the system will start to try to restore the progress....")
        Log("Position information:", positions)


    tts = []  # 
    arrChart_1 = []  # Chart array
    arrChart_2 = []
    index_ = 0  # 
    index_2 = []
    arrKIndex = []
    a = []
    b = []
    c = []
    d = []

    #while True:
    #Log(1)
    symbolFilter = {}  # Array for filtering
    arr = Instruments.split(",")  # Contract list
    for i in range(len(arr)):  # Iterate through contract list
        symbol = re.sub(r'/\s+$/g', "", re.sub(r'/^\s+/g', "", arr[i]))  # Standardize contract string
        if symbol in symbolFilter.keys():  # If there is a branch named in the filter array symbolProperty, then display the information and skip.
            raise Exception(symbol + "already exists, please check the parameters!")
        symbolFilter[symbol] = True  # Add keys named symbol to the filter array. The same contract code will be filtered next time. Ensure that each contract only passes parameters once to the Manager class method.
        hasPosition = False  # Initialize `hasPosition` variable as false, representing no current positions. 
        for j in range(len(positions)):  # Iterate through the obtained position information
            if positions[j]["ContractType"] == symbol:  # If there is a contract name equal to in the positionssymbol
                Log('cc')
                hasPosition = True  # mark True for position
                break  # Jump out
        #fastPeriod = int(arrFastPeriod[i])  # Normalize to numeric type
        #slowPeriod = int(arrSlowPeriod[i])
        Log(123)
        obj_1 = shortChart #  Instantiate the Manager class
        obj_2 = longChart
        index_2.append(index_)  # 0 8
        index_ += 8 # Long-period chartindex
        
        #tts.append(obj)  # ttsThe list is passed in. Finally, according to the contract list, several varieties of control objects are generated and stored inttsArray 
        #Log(obj)
        arrChart_1.append(obj_1)   # At/InforIn a loop, sequentially pass the chart information dictionary into the chart array.
        #arrChart_2.append(obj_2)
        a.append(chart0)
        b.append(chart1)
        c.append(chart2)
        d.append(hart1)
        Log(len(arrChart_1))
        Log(111 if arrChart_1[0]==shortChart else 000)
        #arrChart_2.append(obj.longChart)
    # Create chart object
    #chart = Chart([arrChart_1, arrChart_2])  # __isStock" : Truemeans it is a highstock chart, False means it is a highcharts chart. Use multiple chart objects and convert it to a two-dimensional array.
    #chart = Chart([arrChart_1,arrChart_2])
    chart = Chart([a,b,c,d])
    #Log(len(arrChart_1),len(arrChart_2))
    index_2 = np.array(index_2)
    chart.reset()  # Clear chart data from the last polling

    while True:
        #c = Chart(shortChart)
        preTicker = None
        #while True:
        #Log(1)
        if exchange.IO('status'):
            LogStatus(_D(),'Already connected')
            #t = exchange.GetTicker()
            plot(arr,_5_lengh,_15_lengh,index_2,runTime,chart)
        Sleep(1000)                      
        ''' 
        if i ==0:
            if signals['buy_sell_sig'+str(trueSymbol)] ==1:
                Log(1)
                #ext.PlotFlag(r[-2]['Time'],'open long','L','circlepin','K')
                chart.add(index_2 + 6, [arr_[i][j]["Time"], {'X':arr_[i][j]["Time"],'title':'L','text':'open long'}])
                signals['buy_sell_sig'+str(trueSymbol)] =0
            if signals['buy_sell_sig'+str(trueSymbol)] ==2:
                Log(2)
                #ext.PlotFlag(r[-2]['Time'],'open short','S','circlepin','K')
                chart.add(index_2 + 6, [arr_[i][j]["Time"], {'X':arr_[i][j]["Time"],'title':'S','text':'open short'}])
                signals['buy_sell_sig'+str(trueSymbol)] =0
            if signals['buy_sell_sig'+str(trueSymbol)] ==3:
                Log(3)
                #ext.PlotFlag(r[-2]['Time'],'close long','UL','circlepin','K')
                chart.add(index_2 + 6, [arr_[i][j]["Time"], {'X':arr_[i][j]["Time"],'title':'UL','text':'close long'}])
                signals['buy_sell_sig'+str(trueSymbol)] =0
            if signals['buy_sell_sig'+str(trueSymbol)] ==4:
                Log(4)
                #ext.PlotFlag(r[-2]['Time'],'close short','US','circlepin','K')
                chart.add(index_2 + 6, [arr_[i][j]["Time"], {'X':arr_[i][j]["Time"],'title':'US','text':'close short'}])
                signals['buy_sell_sig'+str(trueSymbol)] =0

        '''

                    #index_1 += 9  # Short-period chartindex

        
```

> Detail

https://www.fmz.com/strategy/216948

> Last Modified

2020-07-07 13:53:18
