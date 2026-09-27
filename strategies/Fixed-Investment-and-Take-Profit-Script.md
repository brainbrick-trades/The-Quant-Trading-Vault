
> Name

Fixed-Investment-and-Take-Profit-Script

> Author

Zer3192



> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_1|5|Maximum loss percentage|
|v_input_2|3|Take profit value|


> Source (PineScript)

``` pinescript
//@version=4

strategy("Regular Investment Profit Taking", overlay=true)

//Define the maximum loss percentage
maxLossPercent = input(title="Maximum loss percentage", type=float,defval=5)

//Define take-profit number
stopProfitVal = input(title="Take profit value", type=float, defval=3) 

//The main contract holds a long position
longCondition = crossover(open, close) //The main contract goes long by breaking through the closing price horizontally at the opening price

if (longCondition)
    strategy.entry("Long", strategy.long, comment="Open Long") 

//Stop-loss condition
//if (strategy.position_size > 0)  
    //strategy.exit("Exit long", stop=strategy.position_avg_price * (1 - maxLossPercent/100)) 

//Profit Taking Conditions
profitExit = strategy.position_avg_price + stopProfitVal
if (strategy.position_size > 0)
     strategy.exit("Exit long", limit = profitExit)

```

> Detail

https://www.fmz.com/strategy/396182

> Last Modified

2023-01-29 09:49:34
