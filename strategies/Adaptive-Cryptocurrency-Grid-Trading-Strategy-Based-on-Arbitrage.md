
> Name

Adaptive-Cryptocurrency-Grid-Trading-Strategy-Based-on-Arbitrage

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/ff773247df2a2ca360.png)
 
### Overview

This is an adaptive cryptocurrency grid trading strategy based on the grid trading methodology for arbitrage. It can automatically adjust the price range of grid trading based on market fluctuations and conduct efficient arbitrage trading within that price range.  

### Strategy Principle   

The core idea of this strategy is:  

1. Dynamically calculate a trading grid price range based on historical high and low prices.

2. Set N grid lines at equal intervals within this price range.  

3. When the price breaks through each grid line, open positions long or short with a fixed quantity.

4. Arbitrage between adjacent grid lines and close positions for profit.

5. When the price re-enters the grid range, continue to open positions at the marginal cost of the grid lines.  

6. Repeat this cycle for high-frequency arbitrage trading within the grid price range.   

Specifically, the strategy first calculates the upper and lower limits of the grid in real time according to the configured lookback window (i_boundLookback) and volatility range (i_boundDev) parameters.  

Then N grid lines (i_gridQty) are evenly divided between the upper and lower limits. The prices of these grid lines are stored in the gridLineArr array.  

When the price breaks through a grid line, a fixed quantity (strategy capital divided by number of grids) is used to open long or short positions. Order records are kept in the orderArr array.  

When the price breaks through the adjacent grid line again, it can be matched with previous orders for arbitrage and close positions for profit.  

Repeat this cycle for high-frequency arbitrage within the price fluctuation range.

### Advantage Analysis   

Compared with traditional grid strategies, the biggest advantage of this strategy is that the grid range is automatically adjusted to adapt to market fluctuations, with the following characteristics:  

1. Fully automated, no manual intervention required.

2. Able to capture price trends and trade in trend direction. 

3. Controllable risks, avoiding unilateral chasing risks.  

4. High trading frequency and profit margin.

5. Easy to understand, simple configuration. 

6. High capital utilization, not easily trapped.

7. Reflect market changes in real time, suitable for algorithmic trading.

### Risk Analysis

Although the strategy has many advantages, there are also some risks, mainly concentrated in:

1. Potential for greater losses in extreme price swings.  

2. Requires suitable holding period and trading pair to profit.

3. Capital scale needs to match volatility range.  

4. May require frequent monitoring and optimization of parameters.

Countermeasures include:  

1. Increase grid spacing to widen grid range.

2. Choose more stable trading pairs.  

3. Adjust capital scale for sufficient liquidity.

4. Establish automatic monitoring and alerting mechanisms.

### Optimization Directions   

The strategy can be optimized in the following aspects:

1. **Dynamic grid**: automatically adjust grid parameters based on volatility. 

2. **Stop loss mechanism**: set reasonable stop loss locations to limit extreme risks.

3. **Compound grid**: combine grids using different parameters for different periods to maximize usage of time.  

4. **Machine learning**: use neural networks to automatically optimize parameters instead of rules.

5. **Cross-market arbitrage**: arbitrage between exchanges or currency pairs.  

### Summary   

In summary, this is a very practical adaptive crypto grid trading strategy for arbitrage. Compared to traditional grid strategies, its biggest feature is the automatic adjustment of the grid range based on market changes, allowing traders to configure their own trading range. The strategy logic is clear and easy to understand and configure, suitable for individual investors with some foundation and also as a template for trading algorithms. With proper parameter tuning, very high capital utilization efficiency can be achieved.


> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_1|true|(?Grid Bounds)Use Auto Bounds?|
|v_input_2|0|(Auto) Bound Source: Hi & Low|Average|
|v_input_3|250|(Auto) Bound Lookback|
|v_input_4|0.1|(Auto) Bound Deviation|
|v_input_5|0.285|(Manual) Upper Boundry|
|v_input_6|0.225|(Manual) Lower Boundry|
|v_input_7|8|(?Grid Lines)Grid Line Quantity|


> Source (PineScript)

``` pinescript
/*backtest
start: 2024-01-11 00:00:00
end: 2024-01-18 00:00:00
period: 1m
basePeriod: 1m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=4
strategy("(IK) Grid Script", overlay=true, pyramiding=14, close_entries_rule="ANY", default_qty_type=strategy.cash, initial_capital=100.0, currency="USD", commission_type=strategy.commission.percent, commission_value=0.1)
i_autoBounds    = input(group="Grid Bounds", title="Use Auto Bounds?", defval=true, type=input.bool)                             // calculate upper and lower bound of the grid automatically? This will theorhetically be less profitable, but will certainly require less attention
i_boundSrc      = input(group="Grid Bounds", title="(Auto) Bound Source", defval="Hi & Low", options=["Hi & Low", "Average"])     // should bounds of the auto grid be calculated from recent High & Low, or from a Simple Moving Average
i_boundLookback = input(group="Grid Bounds", title="(Auto) Bound Lookback", defval=250, type=input.integer, maxval=500, minval=0) // when calculating auto grid bounds, how far back should we look for a High & Low, or what should the length be of our sma
i_boundDev      = input(group="Grid Bounds", title="(Auto) Bound Deviation", defval=0.10, type=input.float, maxval=1, minval=-1)  // if sourcing auto bounds from High & Low, this percentage will (positive) widen or (negative) narrow the bound limits. If sourcing from Average, this is the deviation (up and down) from the sma, and CANNOT be negative.
i_upperBound    = input(group="Grid Bounds", title="(Manual) Upper Boundry", defval=0.285, type=input.float)                      // for manual grid bounds only. The upperbound price of your grid
i_lowerBound    = input(group="Grid Bounds", title="(Manual) Lower Boundry", defval=0.225, type=input.float)                      // for manual grid bounds only. The lowerbound price of your grid.
i_gridQty       = input(group="Grid Lines",  title="Grid Line Quantity", defval=8, maxval=15, minval=3, type=input.integer)       // how many grid lines are in your grid

f_getGridBounds(_bs, _bl, _bd, _up) =>
    if _bs == "Hi & Low"
        _up ? highest(close, _bl) * (1 + _bd) : lowest(close, _bl)  * (1 - _bd)
    else
        avg = sma(close, _bl)
        _up ? avg * (1 + _bd) : avg * (1 - _bd)

f_buildGrid(_lb, _gw, _gq) =>
    gridArr = array.new_float(0)
    for i=0 to _gq-1
        array.push(gridArr, _lb+(_gw*i))
    gridArr

f_getNearGridLines(_gridArr, _price) =>
    arr = array.new_int(3)
    for i = 0 to array.size(_gridArr)-1
        if array.get(_gridArr, i) > _price
            array.set(arr, 0, i == array.size(_gridArr)-1 ? i : i+1)
            array.set(arr, 1, i == 0 ? i : i-1)
            break
    arr

var upperBound      = i_autoBounds ? f_getGridBounds(i_boundSrc, i_boundLookback, i_boundDev, true) : i_upperBound  // upperbound of our grid
var lowerBound      = i_autoBounds ? f_getGridBounds(i_boundSrc, i_boundLookback, i_boundDev, false) : i_lowerBound // lowerbound of our grid
var gridWidth       = (upperBound - lowerBound)/(i_gridQty-1)                                                       // space between lines in our grid
var gridLineArr     = f_buildGrid(lowerBound, gridWidth, i_gridQty)                                                 // an array of prices that correspond to our grid lines
var orderArr        = array.new_bool(i_gridQty, false)                                                              // a boolean array that indicates if there is an open order corresponding to each grid line

var closeLineArr    = f_getNearGridLines(gridLineArr, close)                                                        // for plotting purposes - an array of 2 indices that correspond to grid lines near price
var nearTopGridLine = array.get(closeLineArr, 0)                                                                    // for plotting purposes - the index (in our grid line array) of the closest grid line above current price
var nearBotGridLine = array.get(closeLineArr, 1)                                                                    // for plotting purposes - the index (in our grid line array) of the closest grid line below current price
strategy.initial_capital = 50000
for i = 0 to (array.size(gridLineArr) - 1)
    if close < array.get(gridLineArr, i) and not array.get(orderArr, i) and i < (array.size(gridLineArr) - 1)
        buyId = i
        array.set(orderArr, buyId, true)
        strategy.entry(id=tostring(buyId), long=true, qty=(strategy.initial_capital/(i_gridQty-1))/close, comment="#"+tostring(buyId))
    if close > array.get(gridLineArr, i) and i != 0
        if array.get(orderArr, i-1)
            sellId = i-1
            array.set(orderArr, sellId, false)
            strategy.close(id=tostring(sellId), comment="#"+tostring(sellId))

if i_autoBounds
    upperBound  := f_getGridBounds(i_boundSrc, i_boundLookback, i_boundDev, true)
    lowerBound  := f_getGridBounds(i_boundSrc, i_boundLookback, i_boundDev, false)
    gridWidth   := (upperBound - lowerBound)/(i_gridQty-1)
    gridLineArr := f_buildGrid(lowerBound, gridWidth, i_gridQty)

closeLineArr    := f_getNearGridLines(gridLineArr, close)
nearTopGridLine := array.get(closeLineArr, 0)
nearBotGridLine := array.get(closeLineArr, 1)




```

> Detail

https://www.fmz.com/strategy/439343

> Last Modified

2024-01-19 14:17:50
