
> Name

Momentum-and-Volume-Trading-Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/1aa8761b36c2162ddfb.png)
 
## Overview

This strategy makes buy and sell decisions based on the momentum indicator and trading volume indicator of stocks. It buys when the upward momentum of stock prices accelerates and trading volume surges, and sells when the downward momentum accelerates and trading volume surges. The strategy captures short-term price momentum brought by market herd behavior.   

## Strategy Principle

The strength and duration of stock price change trends determine momentum. This strategy calculates the change from the previous day's close to judge price momentum. Momentum is positive when prices rise consecutively and negative when prices fall consecutively. The strategy also combines the trading volume indicator. Buy and sell signals are only triggered when trading volume is significantly higher than the 20-day moving average (above threshold).

Specifically, the buy condition is a crossover of the momentum indicator above 0 with trading volume more than 2 times the 20-day average. The sell condition is the opposite. After buying, the profit target is set at 0.8 times the entry price, and the stop loss is 0.5 times. The profit target and stop loss after selling are reversed accordingly.  

## Advantages

The biggest advantage is capturing short-term market trends and herd behavior. When stock prices show sustained rises or falls, lots of retail and institutional investors will follow the stronger price momentum to trade. This creates a self-reinforcing short-term price trend. The strategy generates excess returns by leveraging such market psychology. Compared with passive index tracking strategies, the expected excess return of this strategy is higher.  

## Risks  

Firstly, short-term price fluctuations are unpredictable. There are risks of sharp reversals due to sudden events, which cannot be fully avoided despite stop losses. Secondly, the data quality of trading volumes varies. The possibility of manipulation cannot be fully ruled out, which distorts trade signals. Thirdly, simple price and volume analysis cannot precisely control short-term trends. Major structural market shifts can affect strategy performance.

## Enhancement 

More data sources could be incorporated to improve strategy efficacy. For example, the volume of related stock discussions on social media platforms can indicate future price movements. This data could provide supplementary entry and exit signals. Fundamental indicators like P/E ratio and P/B ratio could also help verify price change sustainability and reduce erroneous trades.  

## Conclusion  

By capturing integrated changes in price momentum and trading volume, this strategy judges short-term trends and herd behavior. Such big data and behavioral finance-based quantitative strategies can yield higher expected returns than traditional strategies. But risks need acknowledgment and prevention. Input parameters require constant optimization to keep improving trading outcomes.


> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_1|0.8|Profit Target (%)|
|v_input_2|0.5|Stop Loss (%)|
|v_input_3|2|Volume Threshold|


> Source (PineScript)

``` pinescript
/*backtest
start: 2022-12-12 00:00:00
end: 2023-12-18 00:00:00
period: 1d
basePeriod: 1h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=5
strategy('Momentum and Volume Bot', overlay=true)

// Define strategy parameters
profit_target_percent = input(0.8, title='Profit Target (%)')
stop_loss_percent = input(0.5, title='Stop Loss (%)')
volume_threshold = input(2, title='Volume Threshold')

// Calculate momentum
momentum = close - close[1]

// Calculate average volume
avg_volume = ta.sma(volume, 20)

// Buy condition
buy_condition = ta.crossover(momentum, 0) and volume > avg_volume * volume_threshold

// Sell condition
sell_condition = ta.crossunder(momentum, 0) and volume > avg_volume * volume_threshold

// Strategy logic
strategy.entry('Buy', strategy.long, when=buy_condition)
strategy.entry('Sell', strategy.short, when=sell_condition)

// Set profit target and stop loss
strategy.exit('Take Profit/Stop Loss', from_entry='Buy', profit=close * profit_target_percent / 100, loss=close * stop_loss_percent / 100)
strategy.exit('Take Profit/Stop Loss', from_entry='Sell', profit=close * profit_target_percent / 100, loss=close * stop_loss_percent / 100)

// Plotting
plotshape(series=buy_condition, title='Buy Signal', color=color.new(color.green, 0), style=shape.triangleup, size=size.small)
plotshape(series=sell_condition, title='Sell Signal', color=color.new(color.red, 0), style=shape.triangledown, size=size.small)


```

> Detail

https://www.fmz.com/strategy/435894

> Last Modified

2023-12-19 15:37:16
