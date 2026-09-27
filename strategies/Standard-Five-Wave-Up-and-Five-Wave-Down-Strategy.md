
> Name

Standard-Five-Wave-Up-and-Five-Wave-Down-Strategy

> Author

Zer3192





> Source (PineScript)

``` pinescript
//@version=4
// Standard five-wave up and five-wave down strategy
// Top1
s1 = lowest(low, 5)
// Bottom1
b1 = highest(high, 5)
// Top2
s2 = lowest(low[1], 5)
// Bottom2
b2 = highest(high[1], 5)
// Top3
s3 = lowest(low[2], 5)
// Bottom3
b3 = highest(high[2], 5)
// Top4
s4 = lowest(low[3], 5)
// Bottom4
b4 = highest(high[3], 5)
// Top5
s5 = lowest(low[4], 5)
// Bottom5
b5 = highest(high[4], 5)

// Rising five waves
up_waves = (b1 > b2) and (b2 > b3) and (b3 > b4) and (b4 > b5)
// Five waves down
down_waves = (s1 < s2) and (s2 < s3) and (s3 < s4) and (s4 < s5)

// Trading Conditions
if (up_waves)
    strategy.entry("long", strategy.long, 1, stop = low[4], comment = "long")

else if (down_waves)
    strategy.entry("short", strategy.short, 1, stop = high[4], comment = "short")

// Drawing
plotshape(up_waves, style = shape.triangleup, location = location.belowbar, color=green, title="Rising five waves")
plotshape(down_waves, style = shape.triangledown, location = location.abovebar, color=red, title="Five waves down")

```

> Detail

https://www.fmz.com/strategy/395584

> Last Modified

2023-01-03 21:31:11
