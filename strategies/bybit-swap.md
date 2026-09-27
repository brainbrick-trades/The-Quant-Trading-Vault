
> Name

bybit-swap

> Author

gulishiduan_高频排序

> Strategy Description

//Recently some friends reported smallbug,Go to the testnet first. Parameters can be adjusted freely as needed. The essence of strategy is to trackkThe deduction price for determining bulls or bears is simply by detecting signals in real time by detecting the moving average's inversion
//Register a new account, feel free to use my registration link:https://www.bytick.com/zh-CN/register/?affiliate_id=7586&language=en&group_id=0&group_type=2
//This link provides integration with many third-party strategies./
//Basic principle: ifkIf the line continues to rise, keep adding positions until the maximum position is reached./

//Iflong:Not suitable for bearish markets, but during a decline it won't continuously increase long positions./
//Ifshort:Not suitable for bullish markets, but will not keep adding positions during an uptrend.

//Note key points, long and short positions can also be opened together on two accounts.

//For other strategy purchases, please consult:weixin:ying5737
//Need to connect to the exchange yourself./Demo account for pre-test.Pay attention to risks


// Daily level, or weekly level, here we take the daily level as an example,
// Detectma5ma10,kLine closing price is atma5,ma10Above, andma5Uplink(Judged as yesterdaykLine closing price > counting forward the nth5RootkClosing price),Then place orders at market open daily or buy directly500u,Continuous upward, continuously add positions.
// Add positions: if two consecutive negative candlesticks appear during an uptrend, buy on the third day.500uAdd positions. Each two consecutive bearish orders are counted separately.

// sell,kThree consecutive gains, reduce positions1000u.(OrkFour consecutive gains, reduce positions2000u)
// Continuous Loop.
// Strategy Running,13Sky/Heaven(Or21Sky/Heaven),Automatically stop, close, or liquidate positions and orders.
// Maximum Position5000uIf the position is larger than this position, only reduce the position.

Upload Image:

https://wx1.sinaimg.cn/mw1024/c5775633ly1gbsjvtrgnhj20m80dmmxy.jpg
https://wx1.sinaimg.cn/mw1024/c5775633ly1gbsjvty48uj21hc0u077o.jpg
https://wx2.sinaimg.cn/mw1024/c5775633ly1gbsjvu4iipj20lr0h775f.jpg

# Medium frequency unilateral trend strategy
## Monitoring Variables
1. FastMA
2. SlowMA
3. Closing price
## Configuration Parameters
1. Single order quantityAmount
2. Single position reduction amountCloseAmount
3. Maximum positionMaxPosition
## go long
### Necessary Conditions
1. kLine closing price is greater than fast MA and slow MAMA
2. and the MA is about to rise (judge as yesterday's candlestick closing price higher than the previous 5th candlestick closing price).)
### Place Order
1. Three consecutive bullish candles, reduce positionsCloseAmount
2. Two consecutive bearish candlesticks, increase position Amount. That is, an order will be placed when two consecutive bearish candlesticks appear.2*Amount
3. Normal situation, open an orderAmount
### Limit
1. No orders will be opened if the maximum open interest exceeds MaxPosition
### Exit
1. Exit after running N candlesticks

## go short
### Necessary Conditions
1. kThe closing price of the line is less than the fast MA and slow MAMA
2. And the fast MA is rising (determined by yesterday's candlestick closing price being lower than the closing price of the Nth candlestick before, based on the fast MA period))
### Place Order
1. Three consecutive bearish candles, reduce positionsCloseAmount
2. Two consecutive bullish candlesticks, increase position Amount. That is, an order will be placed when two consecutive bearish candlesticks appear.2*Amount
3. Normal situation, open an orderAmount
### Limit
1. No orders will be opened if the maximum open interest exceeds MaxPosition
### Exit
1. Exit after running N candlesticks
## Notes
1. the program will obtain account position information each time as the strategy's position volume
2. Please bind FMZ WeChat, the program will push important notifications to WeChat
3. 
## Parameters
1. Fast MA Period
2. Slow MA Period	
3. Polling Interval(ms)	
4. Long/Short Selection
5. Leverage size: 0 means cross margin mode
6. Contract type: Currently fmex only supports swap, and only swap can be filled in. OKEx backtesting can be used during backtesting, which can be set to this_week, this_month, etc.
7. Single position reduction amount. When the conditions for reducing positions are met, the amount of one-time reduction
8. Maximum Position(u)
9. APIBase address. Can be set to https://api.fmex.com,Orhttps://api.testnet.fmex.com
10. Exit the Strategy K-Count. After running a certain number of candlesticks, the strategy exits normally
11. Whether to clear positions when the strategy actively exits.
12. Whether interaction is required. The strategy exits normally after meeting the exit conditions. If interaction is required, commands such as manual intervention will be awaited. If it is not needed, the program exits directly.
13. Whether to take the order. If checked, the order is a market order; if not checked, it is a pending order. The buy order is placed at Buy 1, and the sell order is placed at Sell 1
14. Number of consecutive bullish (bearish) candlesticks (when going long, consecutive bullish candles). Position reduction signals, such as consecutive bullish candles when going long, reduce positions
15. Number of consecutive bearish (bullish) candlesticks (for bullish positions, continuous bearish candles). Number of consecutive bearish (bullish) candlesticks (for bullish positions, continuous bearish candles).)	
16. Whether it is a ranging market. Check if it is a ranging market
## Interaction
**Interaction Only When`Interaction required?`Effective at**
**Interaction occurs when the strategy exits normally**
1. Continue. Continue means resetting the strategy and running the same parameters again.
2. Stop. Strategy stops and exits
3. Continue after switching the strategy market. Switch the market to shock or trend and continue running. It is an extension of interaction 1 'Continue'

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|fastMaPeriod|5|Fast MA Period|
|slowMaPeriod|10|Slow MA Period|
|interval|1000|Polling Interval(ms)|
|direction|0|Long and short options: long|short|
|marginLevel|false|Leverage Size|
|contractType|swap|Contract Type (default perpetual)|
|amount|500|Single order/position volume(u)|
|closeAmount|1000|Single position reduction amount(u)|
|maxHoldAmount|5000|Maximum Position(u)|
|baseUrl|https://api.bybit.com|APIBase address|
|runNBars|13|Exit when strategy K counts reached|
|isCleanPosition|true|Whether to clear positions when the strategy actively exits|
|enableCommand|true|Interaction required?|
|isTaker|true|Whether to Take Orders|
|maxSameDirKNum|3|Number of consecutive bullish (bearish) candlesticks (when going long, reduce positions after consecutive bullish lines))|
|maxOppositeDirKNum|2|Number of consecutive bearish (bullish) candlesticks (when going long, add positions on consecutive bearish lines)|
|isShock|false|Is it a volatile market?|




|Button|Default|Description|
|----|----|----|
|Continue |__button__| Whether to continue|
|Stop |__button__| Whether to stop|
|Switch strategy market |0| Continue after switching strategy market: Range | Trend|


> Source (javascript)

``` javascript

/*Contact WeChat:ying5737(Strategy discussion, support paid writing)
# Medium frequency unilateral trend strategy
## Monitoring Variables
1. FastMA
2. SlowMA
3. Closing price
## Configuration Parameters
1. Single order quantityAmount
2. Single position reduction amountCloseAmount
3. Maximum positionMaxPosition
## go long
### Necessary Conditions
1. kLine closing price is greater than fast MA and slow MAMA
2. and the MA is about to rise (judge as yesterday's candlestick closing price higher than the previous 5th candlestick closing price).)
### Place Order
1. Three consecutive bullish candles, reduce positionsCloseAmount
2. Two consecutive bearish candlesticks, increase position Amount. That is, an order will be placed when two consecutive bearish candlesticks appear.2*Amount
3. Normal situation, open an orderAmount
### Limit
1. No orders will be opened if the maximum open interest exceeds MaxPosition
### Exit
1. Exit after running N candlesticks

## go short
### Necessary Conditions
1. kThe closing price of the line is less than the fast MA and slow MAMA
2. and the fast MA is falling (judged as yesterday's candlestick closing price is lower than the previous Nth (fast MA5 cycle) K-closing price).)
### Place Order
1. Three consecutive bearish candles, reduce positionsCloseAmount
2. Two consecutive bullish candlesticks, increase position Amount. That is, an order will be placed when two consecutive bearish candlesticks appear.2*Amount
3. Normal situation, open an orderAmount
### Limit
1. No orders will be opened if the maximum open interest exceeds MaxPosition
### Exit
1. Exit after running N candlesticks
## Notes
1. the program will obtain account position information each time as the strategy's position volume
2. Please bind FMZ WeChat, the program will push important notifications to WeChat
## Parameters
1. Fast MA Period
2. Slow MA Period	
3. Polling Interval(ms)	
4. Long/Short Selection
5. Leverage size: 0 means cross margin mode
6. Contract type: Currently fmex only supports swap, and only swap can be filled in. OKEx backtesting can be used during backtesting, which can be set to this_week, this_month, etc.
7. Single position reduction amount. When the conditions for reducing positions are met, the amount of one-time reduction
8. Maximum Position(u)
9. APIBase address. Can be set to https://api.fmex.com,OrTestnethttps://api.testnet.fmex.com
10. Exit the Strategy K-Count. After running a certain number of candlesticks, the strategy exits normally
11. Whether to clear positions when the strategy actively exits.
12. Whether interaction is required. The strategy exits normally after meeting the exit conditions. If interaction is required, commands such as manual intervention will be awaited. If it is not needed, the program exits directly.
13. Whether to take the order. If checked, the order is a market order; if not checked, it is a pending order. The buy order is placed at Buy 1, and the sell order is placed at Sell 1
14. Number of consecutive bullish (bearish) candlesticks (when going long, consecutive bullish candles). Position reduction signals, such as consecutive bullish candles when going long, reduce positions
15. Number of consecutive bearish (bullish) candlesticks (for bullish positions, continuous bearish candles). Number of consecutive bearish (bullish) candlesticks (for bullish positions, continuous bearish candles).)	
16. Whether it is a ranging market. Check if it is a ranging market
## Interaction
**Interaction Only When`Interaction required?`Effective at**
**Interaction occurs when the strategy exits normally**
1. Continue. Continue means resetting the strategy and running the same parameters again.
2. Stop. Strategy stops and exits
3. Continue after switching the strategy market. Switch the market to shock or trend and continue running. It is an extension of interaction 1 'Continue'
*/
////////////////// params ////////////////////////
//var fastMaPeriod = 5
//var slowMaPeriod = 10
//var direction = go long|go short
//var interval = 1000
//var amount = 500
//var maxHoldAmount = 5000
//var closeAmount = 1000
//var runNBars = 13
//var marginLevel = 0
//var contractType = 'swap'
//var enableCommand = false
//var isTaker = true
//var maxOppositeDirKNum = 2
//var maxSameDirKNum = 3
//var isShock = false
////////////////// variable ////////////////////////

var makeLong = direction == 0 ? true:false
var startTime = null
var holdAmount = 0
var lastBar = null
var yinxianCnt = 0
var yangxianCnt = 0
var lastClose = 0
var last5thClose = 0
var fastMa = []
var slowMa = []
var barCnt = 0
var localIsShock = false
////////////////////////////////////////////////
var PreBarTime = 0
var isFirst = true

function PlotMA_Kline(records){
    $.PlotRecords(records, 'K')
    if(fastMa.length == 0) {
        fastMa = TA.MA(records, fastMaPeriod)
    }
    if(slowMa.length == 0) {
        slowMa = TA.MA(records, slowMaPeriod)
    }
    if(isFirst){
        $.PlotFlag(records[records.length - 1].Time, 'Start', 'STR')
        for(var i = records.length - 1; i >= 0; i--){
            if(fastMa[i] !== null){
                $.PlotLine('ma'+fastMaPeriod, fastMa[i], records[i].Time)
            }
            if(slowMa[i] !== null){
                $.PlotLine('ma'+slowMaPeriod, slowMa[i], records[i].Time)
            }
        }
        PreBarTime = records[records.length - 1].Time
        isFirst = false
    } else {
        if(PreBarTime !== records[records.length - 1].Time){
            $.PlotLine('ma'+fastMaPeriod, fastMa[fastMa.length - 2], records[fastMa.length - 2].Time)
            $.PlotLine('ma'+slowMaPeriod, slowMa[slowMa.length - 2], records[slowMa.length - 2].Time)
            PreBarTime = records[records.length - 1].Time
        }
        $.PlotLine('ma'+fastMaPeriod, fastMa[fastMa.length - 1], records[fastMa.length - 1].Time)
        $.PlotLine('ma'+slowMaPeriod, slowMa[slowMa.length - 1], records[slowMa.length - 1].Time)
}
}

function init () {
    if (fastMaPeriod > slowMaPeriod) {
        throw 'Fast MA period > Slow MA period, please check settings'
    }
    Log('Fast MA Period	    :'  + fastMaPeriod)
    Log('Slow MA Period	    :' + slowMaPeriod)
    Log('Polling Interval(ms)   :' + interval)
    Log('Is it a shock strategy?  :' + (isShock?'Yes/Is':'No/Not'))
    Log('Long/Short Selection	    :' + (direction == 0 ? 'Many':'Empty'))
    Log('Leverage Size	    :' + (marginLevel == 0 ? 'Full Position':marginLevel))
    Log('Consecutive bullish(Cloudy/Gloomy)KNumber of Lines(When going long, continuous positive lines)Number   :' + maxSameDirKNum)
    Log('Consecutive bearish(Sun/Positive)KNumber of Lines(When going long, continuous negative lines)   :' + maxOppositeDirKNum)
    Log('Run How Many BarsKExit later   :' + runNBars)
    startTime = new Date()
    localIsShock = isShock
}

function onexit() {
    Log('Exit')
}

function onerror() {
    Log('Exit on Error')
}

function openLong(ex, openAmount) {
    if (holdAmount + openAmount <= maxHoldAmount) {
        Log('Already holding position: ' + holdAmount + ', add to position:' + openAmount)
        ex.SetDirection('buy')
        if(isTaker) {
            ex.Buy(-1, openAmount, 'take liquidity')
            holdAmount += openAmount
        } else {
            var ticker = _C(ex.GetTicker)
            if(ticker == null) {
                return false
            }
            ex.Buy(ticker.Buy, openAmount, 'pending order')
        }
        return true
    } else {
        Log('Open Position('+holdAmount+') Too many, do not increase positions')
        return false
    }
}

function closeLong(ex, closeAmount) {
    if (holdAmount >= closeAmount) {
        Log('Already holding position: ' + holdAmount + ', reduce position:' + closeAmount)
        ex.SetDirection('closebuy')
        ex.Sell(-1, closeAmount)
        holdAmount -= closeAmount
        return true
    } else {
        Log('Open Position('+holdAmount+') Too few, do not decrease positions')
        return false
    }
}

function openShort(ex, openAmount) {
    if (holdAmount + openAmount <= maxHoldAmount) {
        Log('Already holding position: ' + holdAmount + ', add to position:' + openAmount)
        ex.SetDirection('sell')
        if(isTaker) {
            ex.Sell(-1, openAmount, 'take liquidity')
            holdAmount += openAmount
        } else {
            var ticker = _C(ex.GetTicker)
            if(ticker == null) {
                return false
            }
            ex.Sell(ticker.Sell, openAmount, 'pending order')
        }
        return true
    } else {
        Log('Open Position('+holdAmount+') Too many, do not increase positions')
        return false
    }
}

function closeShort(ex, closeAmount) {
    if (holdAmount >= closeAmount) {
        Log('Already holding position: ' + holdAmount + ', reduce position:' + closeAmount)
        ex.SetDirection('closesell')
        ex.Buy(-1, closeAmount)
        holdAmount -= closeAmount
        return true
    } else {
        Log('Open Position('+holdAmount+') Too few, do not decrease positions')
        return false
    }
}

function cancelOrders(ex) {
    Log('Cancel all pending orders')
    while(true) {
        var orders = _C(ex.GetOrders)
        if (orders.length == 0) {
            break
        }
        for(var i = 0; i < orders.length;i++) {
            ex.CancelOrder(orders[i].Id)
        }
    }
}

function updatePosition(ex) {
    var pos = ex.GetPosition()
    if(typeof(pos) === 'undefined' || pos === null || 
        pos.length == 0 || typeof(pos[0].Type) == 'undefined'  || typeof(pos[0].Amount) == 'undefined' ) {
        return
    }
    Log('Position Information:' + (pos[0].Type == 0?'Long position,   ':'Short position,  ') + JSON.stringify(pos))
    if(pos.length>0){
        holdAmount = pos[0].Amount
        // if(pos[0].Type == 0){ //Long position
        //     ordersInfo.pos = pos[0].Amount
        // }else{
        //     ordersInfo.pos = -pos[0].Amount
        // }
    }
}

function longStrategy(ex, records) {
    var lastSecondBar = records[records.length-2]

    if ((   lastSecondBar.Close > fastMa[fastMa.length - 2] && 
            lastSecondBar.Close > slowMa[slowMa.length - 2] && 
            lastSecondBar.Close > records[records.length - 2 - fastMaPeriod].Close
        ) || localIsShock){
            var openAmount = amount
            if (lastSecondBar.Close < lastSecondBar.Open) {
                yinxianCnt += 1
                yangxianCnt = 0
            } else if (lastSecondBar.Close > lastSecondBar.Open){
                yinxianCnt = 0
                yangxianCnt += 1
            } else {
                yangxianCnt = 0
                yinxianCnt = 0
            }

            if (yinxianCnt >= maxOppositeDirKNum) {
                Log('Two Lianyin')
                openAmount += amount
                yinxianCnt = 0
            }

            if (yangxianCnt >= maxSameDirKNum) {
                Log('Sanlianyang')
                yangxianCnt = 0
                Log('Preparing to Reduce Position')
                if(closeLong(ex, closeAmount)){
                    $.PlotFlag(records[records.length - 1].Time, 'closeLong', 'CL')
                }
            } else {
                Log('Preparing to Open Position')
                if(localIsShock) {
                    openAmount -= amount
                }
                if(openLong(ex, openAmount)){
                    $.PlotFlag(records[records.length - 1].Time, 'openLong', 'OL')
                }
            }
    }
}

function shortStrategy(ex, records) {
    var lastSecondBar = records[records.length-2]

    if ((   lastSecondBar.Close < fastMa[fastMa.length - 2] && 
            lastSecondBar.Close < slowMa[slowMa.length - 2] && 
            lastSecondBar.Close < records[records.length - 2 - fastMaPeriod].Close
        ) || localIsShock){
            var openAmount = amount
            if (lastSecondBar.Close < lastSecondBar.Open) {
                yinxianCnt += 1
                yangxianCnt = 0
            } else if (lastSecondBar.Close > lastSecondBar.Open){
                yinxianCnt = 0
                yangxianCnt += 1
            } else {
                yangxianCnt = 0
                yinxianCnt = 0
            }

            if (yangxianCnt >= maxOppositeDirKNum) {
                Log('Lianyang')
                yangxianCnt = 0
                openAmount += amount
            } 

            if (yinxianCnt >= maxSameDirKNum) {
                Log('Sanlianyin')
                yinxianCnt = 0
                Log('Preparing to Reduce Position')
                if(closeShort(ex, closeAmount)){
                    $.PlotFlag(records[records.length - 1].Time, 'closeShort', 'CS')
                }
            } else {
                Log('Preparing to Open Position')
                if(localIsShock) {
                    openAmount -= amount
                }
                if(openShort(ex, openAmount)){
                    $.PlotFlag(records[records.length - 1].Time, 'openShort', 'OS')
                }
            }
    }
}

function onBar (ex) {
    var records = _C(ex.GetRecords)
    if (records === null || records.length < slowMaPeriod) {
        return 
    }
    if (lastBar == null) {
        lastBar = records[records.length-1]
    }
    
    if (lastBar.Time == records[records.length-1].Time) {
        return
    }
    lastBar = records[records.length-1]
    updatePosition(ex)
    PlotMA_Kline(records)
    barCnt += 1

    var lastSecondBar = records[records.length-2]
    fastMa = TA.MA(records, fastMaPeriod)
    slowMa = TA.MA(records, slowMaPeriod)
    lastClose = lastSecondBar.Close
    last5thClose = records[records.length - 2 - 5].Close

    Log('Closing price:' +lastSecondBar.Close + 
    ', Previous 5 closing prices:' +records[records.length - 2 - 5].Close + 
    ', FastMA:' + _N(fastMa[fastMa.length - 2]) +
    ', SlowMA:' + _N(slowMa[slowMa.length - 2]))
    if (makeLong) {
        longStrategy(ex, records)
    } else {
        shortStrategy(ex, records)
    }
}

function runLife(ex) {
    // var pass = new Date() - startTime
    if (barCnt >= runNBars) {
        if(isCleanPosition) {
            Log('Run'+barCnt+'Ktimeframe,End, cancel orders, clear positions#ff0000@')
            cancelOrders(ex)
            updatePosition(ex)
            $.PlotFlag(lastBar.Time, 'Exit', 'EXT')
            
            if (makeLong) {
                closeLong(ex, holdAmount)
            } else {
                closeShort(ex, holdAmount)
            }    
        } else {
            Log('Run'+barCnt+'Ktimeframe,End, do not cancel orders, do not clear positions#ff0000@')
            updatePosition(ex)
            $.PlotFlag(lastBar.Time, 'Exit', 'EXT')
        }
        return true
    } else {
        return false
    }
}

function status() {
    var table = {
        type: 'table',
        title: 'Information',
        cols: [
            'Running K Count',
            'Position',
            'Yang line',
            'Yinxian',
            'Closing price',
            'Previous 5 closing prices',
            'MA'+fastMaPeriod,
            'MA'+slowMaPeriod,
        ],
        rows: []
      }
      table.rows.push([
            barCnt,
            holdAmount,
            yangxianCnt,
            yinxianCnt,
            lastClose,
            last5thClose,
            fastMa.length == 0 ? 0 : _N(fastMa[fastMa.length - 2]),
            slowMa.length == 0 ? 0 : _N(slowMa[slowMa.length - 2])
      ])
    LogStatus(
        'Current Time:' +_D() +
        '\nStart Time:' +startTime +
        '\n`' +
        JSON.stringify(table)+
        '`\n' +
        '\nCustodian Version:' +Version() +
        '\nContactWechat:ying5737#00ff00' +
        '\nWechat: ying5737info#ff000f'
      )

}

function reset() {
    holdAmount = 0
    lastBar = null
    yinxianCnt = 0
    yangxianCnt = 0
    lastClose = 0
    last5thClose = 0
    fastMa = []
    slowMa = []
    barCnt = 0
}

function main () {
    var ex = exchanges[0]

    Log('Start construction   '+ex.GetName())
 //   if(ex.GetName() != 'Futures_FMex' && !IsVirtual()) {
  //      throw 'Only SupportsFMex'
  //  }
    Log('Base address  ' + baseUrl)
    if(!IsVirtual()){
        ex.IO('base', baseUrl) //Switch the base address to facilitate switching between live and demo accounts, live account address:https://api.fmex.com
    }
    ex.SetTimeout(1000);
    _CDelay(500)
    ex.SetContractType(contractType)
    ex.SetMarginLevel(marginLevel)
    updatePosition(ex)
    while (true) {
        try {
            if(!IsVirtual() && runLife(ex)) {
                if((typeof(GetCommand) == 'function') && enableCommand){
                    Log('Waiting for instructions, Continue | Stop #ff0000@')
                    while (true) {
                        var cmd = GetCommand()
                        if (cmd) {
                            Log('Instruction received: '+cmd)
                            switch(cmd) {
                                case 'Stop':
                                    Log('Stop, Exit!#ff0000@')
                                    return
                                case 'Continue':
                                    reset()
                                    Log('Continue, Reset, Start Work!#ff0000@')
                                    break
                                case 'Switch strategy market:0':
                                    reset()
                                    localIsShock = true
                                    Log('Switch strategy continues when market is ranging, Reset, Start Work!#ff0000@')
                                    break
                                case 'Switch strategy market:1':
                                    reset()
                                    localIsShock = false
                                    Log('Switch strategy continues when market is trending, Reset, Start Work!#ff0000@')
                                    break
                            }
                            if (cmd == 'Stop'){
                                Log('Stop, Exit!#ff0000@')
                                return
                            } else if (cmd == 'Continue') {
                                reset()
                                Log('Continue, Reset, Start Work!#ff0000@')
                                break
                            }
                        }
                        updatePosition(ex)
                        status()
                        Sleep(1000)
                    }
                } else {
                    Log('Stop, Exit!#ff0000@')
                    return
                }
            }
            onBar(ex)
            status()
        } catch(e) {
            Log('Something went wrong:'+e+', Please Handle in Time#ff0000@')
        }
        Sleep(interval)
    }
}

```

> Detail

https://www.fmz.com/strategy/205469

> Last Modified

2021-01-08 19:20:42
