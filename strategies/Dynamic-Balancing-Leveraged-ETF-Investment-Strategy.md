
> Name

Dynamic-Balancing-Leveraged-ETF-Investment-Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/e20a71f1a3e9eea3b0.png)

### Overview

This strategy takes Hong Kong Hang Seng Index ETF (00631L) as the investment target and dynamically adjusts the cash position and position ratio to balance the return and risk of the investment portfolio in real time. The strategy is simple and easy to implement without the need to judge market trends and is suitable for investors who cannot frequently check the market.

### Principles  

1. Initially invest 50% of the total funds to purchase 00631L;

2. Monitor the ratio between unrealized profit and remaining cash; 
   
   Sell 5% of position when unrealized profit exceeds remaining cash by 10%;

   Add 5% to position when remaining cash exceeds unrealized profit by 10%;  

3. Dynamically adjust position and cash ratio to control portfolio return and risk.

### Advantage Analysis  

1. Simple and easy to operate without the need to judge market conditions;

2. Dynamically adjusting positions effectively manages investment risk;  

3. Two-way tracking to timely stop loss or take profit;

4. Suitable for investors who cannot frequently check the market.

### Risks and Mitigations

1. Leveraged ETFs have higher volatility;

   Adopt gradual position building and spaced investments.  

2. Unable to timely stop loss;

   Set stop loss line to control maximum loss.

3. Higher trading costs; 

   Relax balancing range to reduce position adjustments.

### Optimization Ideas

1. Optimize position and cash ratio;

2. Test return effectiveness across different ETF products;  

3. Incorporate trend indicators to improve capital utilization efficiency.


### Conclusion  

By constructing a dynamic balancing portfolio, this strategy controls investment risks without the need to judge market trends. Simple to operate, it is a highly practical quantitative investment strategy suitable for investors who cannot frequently check the market.




> Source (PineScript)

``` pinescript
/*backtest
start: 2024-01-01 00:00:00
end: 2024-01-24 23:59:59
period: 1h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=4
strategy("00631L Trading Simulation", shorttitle="Sim", overlay=true, initial_capital = 1000000)

// Set principal
capital = 1000000

// Set purchase and sale date range
start_date = timestamp(2022, 10, 6) 
next_date = timestamp(2022, 10, 7)  // Better start date
//start_date = timestamp(2022, 3, 8) 
//next_date = timestamp(2022, 3, 9)  // Inferior start date 
sell_date = timestamp(2024, 1, 19) 
end_date = timestamp(2024, 1, 21)  // End date is January 21, 2024

// Determine if it is during trading hours
in_trade_period = time >= start_date and time <= end_date
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

https://www.fmz.com/strategy/442087

> Last Modified

2024-02-19 11:09:29
