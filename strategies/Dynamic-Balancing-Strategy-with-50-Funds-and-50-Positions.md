
> Name

Dynamic-Balancing-Strategy-with-50-Funds-and-50-Positions

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/198847a3568ae2ba0ec.png)

### Strategy Overview

This strategy dynamically balances between 50% funds and 50% positions to control risk. By continuously adjusting the ratio between funds and positions, it manages risk for investors who cannot monitor the market in real-time.  

### Strategy Logic

1. Initialize capital at 1 million, divided equally into 50% funds and 50% positions.

2. During the trading period, if remaining funds exceed unrealized profit/loss by 1.05 times at each open, use 2.5% of remaining funds to add positions.  

3. If unrealized profit/loss exceeds remaining funds by 1.05 times, sell partial positions to restore balance.

4. Close all positions at end of trading period.

### Advantages 

1. Effective risk control by dynamically balancing funds and positions, avoiding huge losses in extreme market conditions.

2. Simple to operate for busy investors, only need to adjust fund/position ratios.

3. Customizable parameters to meet varying risk appetites.

### Risks

1. Unable to capitalize on short-term fluctuations, profit potential limited.  

2. Long one-sided run may result in insufficient position size. 

3. Improper parameter tuning leads to excess position flipping or low capital utilization.

### Enhancement Opportunities 

1. Introduce more parameters for finer fund/position control.  

2. Incorporate stop loss/profit taking for larger positions.

3. Test different trading period parameters to improve adaptability.

### Conclusion
This strategy achieves risk control by dynamically balancing between funds and positions. Simple to implement compared to other strategies. Can be further improved by introducing more adjustable parameters and combining with other strategy concepts.




> Source (PineScript)

``` pinescript
/*backtest
start: 2023-12-17 00:00:00
end: 2023-12-18 19:00:00
period: 1m
basePeriod: 1m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=4
strategy("00631L Trading Simulation", shorttitle="Sim", overlay=true, initial_capital = 1000000)

// Set principal
capital = 1000000

// Set purchase and sale date range
start_date = timestamp(2020, 11, 4)
next_date = timestamp(2020, 11, 5)
sell_date = timestamp(2023, 10, 24)
end_date = timestamp(2023, 10, 25)  // End date changed to October 25, 2023

// Determine if it is during trading hours
in_trade_period = true
// Realized profit and loss
realized_profit_loss = strategy.netprofit
plot(realized_profit_loss, title="realized_profit_loss", color=color.blue)
// Unrealized profit and loss
open_profit_loss = strategy.position_size * open
plot(open_profit_loss, title="open_profit_loss", color=color.red)
// Remaining funds
remaining_funds = capital  + realized_profit_loss - (strategy.position_size * strategy.position_avg_price)
plot(remaining_funds, title="remaining_funds", color=color.yellow)
// Total equity
total_price = remaining_funds + open_profit_loss
plot(total_price, title="remaining_funds", color=color.white)
// Buying logic: buy on each trading day during the trading period daily_investment Amount of products
first_buy = time >= start_date and time <= next_date
buy_condition = in_trade_period and dayofmonth != dayofmonth[1]
// Selling logic : Sell all commodities on the expiration date during the trading period.
sell_all = time >= sell_date

// Buy on the first day of the trading period50%Principal
if first_buy
    strategy.order("First", strategy.long, qty = capital/2/open)
// in eachKBuy at the opening of the line

// Adding logic : Remaining funds > Unrealized profit and loss * 1.05
add_logic = remaining_funds > open_profit_loss * 1.05
if buy_condition
    strategy.order("Buy", strategy.long, when = add_logic, qty = remaining_funds * 0.025 / open)
//

// Subtraction logic : Remaining funds > Unrealized profit and loss * 1.05
sub_logic = open_profit_loss > remaining_funds * 1.05
if buy_condition
    strategy.order("Sell", strategy.short, when = sub_logic, qty = open_profit_loss * 0.025/open)
//

strategy.order("Sell_all",  strategy.short, when = sell_all, qty = strategy.position_size)

// Draw a rectangular area during the trading period
bgcolor(in_trade_period ? color.green : na, transp=90)


```

> Detail

https://www.fmz.com/strategy/436515

> Last Modified

2023-12-25 14:12:30
