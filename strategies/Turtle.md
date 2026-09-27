
> Name

Turtle

> Author

aawww



> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|Donchian_open|20|Donchian_open|
|Donchian_stop|10|Donchian_stop|
|Atr|20|Atr|


> Source (python)

``` python
import json
import time

class Turtle:
    def __init__(self, account=None, donchian_channel_open_position=20, donchian_channel_stop_profit=10, atr_day_length=20, max_risk_ratio=0.5):
        self.donchian_channel_open_position = donchian_channel_open_position  # Donchian Channel period in days (opening))
        self.donchian_channel_stop_profit = donchian_channel_stop_profit  # Donchian Channel period in days (take profit))
        self.atr_day_length = atr_day_length  # ATRNumber of days used for calculation
        self.max_risk_ratio = max_risk_ratio  # Maximum risk level
        self.state = {
            "position": 0,  # Net position of this strategy (positive indicates long, negative indicates short, 0 indicates no position))
            "last_price": float("nan"),  # Last adjustment price
        }
        positions = _C(exchange.GetPosition)
        self.equity=0
        for position in positions:
            if position["Type"]==PD_LONG:
                self.state["position"]=position["Amount"]
                self.state["last_price"] = position["Price"]
                self.equity+=position["Margin"]
            elif position["Type"]==PD_SHORT:
                self.state["position"]=-position["Amount"]
                self.state["last_price"] = position["Price"]
                self.equity+=position["Margin"]
        self.account = _C(exchange.GetAccount)
        self.equity += self.account["Stocks"]+self.account["FrozenStocks"]
        #Log(self.equity)

        self.n = 0  # Average True Range (N value))
        self.unit = 0  # Trading Unit
        self.donchian_channel_high = 0  # Donchian Channel upper band
        self.donchian_channel_low = 0  # Donchian Channel lower band
        # Since ATR is a path-dependent function, longer data sequences are used for calculations to stabilize its value
        self.klines = exchange.GetRecords()

    def recalc_paramter(self):
        # Average True Range (N value))
        self.equity=0
        positions = _C(exchange.GetPosition)
        for position in positions:
            if position["Type"]==PD_LONG:
                self.equity+=position["Margin"]
            elif position["Type"]==PD_SHORT:
                self.equity+=position["Margin"]
        self.account = _C(exchange.GetAccount)
        self.equity += self.account["Stocks"]+self.account["FrozenStocks"]
        #Log(self.equity)
        records = _C(exchange.GetRecords)
        self.n =TA.ATR(records, self.atr_day_length)[-1]
        # Trading Unit
        self.current_price = records[-1]["Close"]
        self.unit = int((self.equity * 0.01*self.current_price*self.current_price) / (100 * self.n))
        # Donchian Channel upper band: highest price of the previous N trading days
        #Log(records)
        self.donchian_channel_high =TA.Highest(records, self.donchian_channel_open_position , 'High') #Donchian Channel upper band: highest price of the previous N trading days
        self.donchian_channel_high =TA.Highest(records, 55 , 'High')
        # Donchian Channel lower band: lowest price of the previous N trading days
        self.donchian_channel_low = TA.Lowest(records, self.donchian_channel_open_position , 'Low')
        self.donchian_channel_low = TA.Lowest(records, 55 , 'Low')
        #Log("Upper and lower bands of the Donchian channel: %f, %f" % (self.donchian_channel_high, self.donchian_channel_low))
        
        self.stop_high = TA.Highest(records, self.donchian_channel_stop_profit , 'High') 
        self.stop_high = TA.Highest(records, 20 , 'High') 
        self.stop_low = TA.Highest(records, self.donchian_channel_stop_profit , 'Low') 
        self.stop_low = TA.Highest(records, 20, 'Low') 

        
        boll = TA.BOLL(records, 50, 2)
        self.up_line = boll[0][-1]
        self.mid_line = boll[1][-1]
        self.down_line = boll[2][-1]
        close1 = records[-2]['Close']  # Latest closing price
        close30 = records[-30]['Close']  # Closing prices of the previous 30 candles
        hh30 = TA.Highest(records, 30, 'High')  # Recent30RootKHighest price of the line
        ll30 = TA.Lowest(records, 30, 'Low')  # Recent30RootKLowest price of the line
        self.cmi = abs((close1 - close30) / (hh30 - ll30)) * 100  # Calculate market volatility index

        return True
    def set_position(self, pos):
        self.state["position"] = pos
        self.state["last_price"] = self.current_price
        positions = _C(exchange.GetPosition)
        sell_amount =0
        long_amount = 0
        for position in positions:
            if position["Type"]==PD_LONG:
                long_amount=position["Amount"]
            elif position["Type"]==PD_SHORT:
                sell_amount=position["Amount"]

        if pos>0:
            if sell_amount>0:
                exchange.SetDirection("closesell")
                exchange.Buy(self.current_price*1.005,sell_amount)
            if pos>long_amount:
                exchange.SetDirection("buy")
                exchange.Buy(self.current_price*1.005,pos-long_amount)
            elif pos<long_amount:
                exchange.SetDirection("closebuy")
                exchange.Sell(self.current_price*0.995,long_amount-pos)
        elif pos<0:
            pos=-pos 
            if long_amount>0:
                exchange.SetDirection("closebuy")
                exchange.Sell(self.current_price*0.995,long_amount)
            if pos>sell_amount:
                exchange.SetDirection("sell")
                exchange.Sell(self.current_price*0.995,pos-sell_amount)
            elif pos<sell_amount:
                exchange.SetDirection("closesell")
                exchange.Buy(self.current_price*1.005,sell_amount-pos)
        else:
            if long_amount>0:
                exchange.SetDirection("closebuy")
                exchange.Sell(self.current_price*0.995,long_amount)      
            if sell_amount>0:
                exchange.SetDirection("closesell")
                exchange.Buy(self.current_price*1.005,sell_amount)                
        #self.target_pos.set_target_volume(self.state["position"])
    def try_open(self):
        """Opening Strategy"""
        while self.state["position"] == 0:
            self.recalc_paramter()
            #Log("Latest price: %f" % self.current_price)
            if self.current_price > self.donchian_channel_high:  # Current price > Donchian channel upper band, buy 1 unit; (holding long positions))
            #if self.cmi>20 and self.current_price>self.up_line:
                #Log("Current price>Donchian channel upper band, buy1Individual/UnitUnit(Hold long position): %d Hand" % self.unit)
                self.set_position(self.state["position"] + self.unit)
            elif self.current_price < self.donchian_channel_low:  # Current price < Tangqi An Channel lower rail, sell 1 unit; (holding a short position)
            #elif self.cmi>20 and self.current_price<self.down_line:
                #Log("Current price<Donchian channel lower band, sell1Individual/UnitUnit(Hold short position): %d Hand" % self.unit)
                self.set_position(self.state["position"] - self.unit)
    def try_close(self):
        """Trading strategy"""
        while self.state["position"] != 0:
            if True:
                self.recalc_paramter()
                Log("Latest price: ", self.current_price)
                #if self.cmi<20:
                #    self.set_position(0)
                if self.state["position"] > 0:  # Long positions
                    # Adding position strategy: If it is a long position and the latest market price has increased by 0.5N based on the last position opening (or adding position), add a unit long position, and the risk is within the set range (to prevent the position from being blown out))
                    if self.current_price >= self.state["last_price"] + 0.5 * self.n and self.state["position"] + self.unit<=4*self.unit:
                        Log("add to position:Add1Individual/UnitUnitLong position")
                        self.set_position(self.state["position"] + self.unit)
                    # Stop loss strategy: If it is a long position and the latest market price has dropped by 2N based on the last position opened (or added), sell the entire position to stop the loss.
                    elif self.current_price <= self.state["last_price"] - 2 * self.n:
                        Log("stop loss:Sell all positions")
                        self.set_position(0)
                    # Take-profit strategy: If the position is long and the latest market price falls below the lower track of the 10-day Tang Qian channel, then clear all positions to end the strategy and leave the market.
                    if self.current_price <= self.stop_low:
                    #if self.current_price<self.mid_line:
                        Log("take profit:Clear all positions to end the strategy,Leave")
                        self.set_position(0)
                elif self.state["position"] < 0:  # Short positions
                    # Adding position strategy: If it is a short position and the latest market price has dropped by 0.5N based on the last position opening (or adding position), add a short position of Unit, and the risk is within the set range (to prevent the position from being blown out))
                    if self.current_price <= self.state["last_price"] - 0.5 * self.n and (-self.state["position"]) + self.unit<=4*self.unit:
                        Log("add to position:Add1Individual/UnitUnitempty position")
                        self.set_position(self.state["position"] - self.unit)
                    # Stop loss strategy: If it is a short position and the latest market price has increased by 2N based on the last position opened (or added), close the position and stop the loss.
                    elif self.current_price >= self.state["last_price"] + 2 * self.n:
                        Log("stop loss:Sell all positions")
                        self.set_position(0)
                    # Take-profit strategy: If it is a short position and the latest market price rises above the upper track of the 10-day Tang Qian channel, then clear all positions to end the strategy and leave the market.
                    if self.current_price >= self.stop_high:
                    #if self.current_price>self.mid_line:
                        Log("take profit:Clear all positions to end the strategy,Leave")
                        self.set_position(0)
    def strategy(self):
        """Turtle Strategy"""
        Log("WaitKLines and account data...")
        while not self.recalc_paramter():
            raise Exception("Failed to retrieve data, please confirm the market connection is normal and the trading account is logged in")
        while True:
            self.try_open()
            self.try_close()


def main():
    exchange.SetContractType("quarter")
    turtle = Turtle(donchian_channel_open_position=Donchian_open,donchian_channel_stop_profit=Donchian_stop,atr_day_length=Atr)
    Log("Strategy starts running")

    Log("Current position size: %d, Last adjustment price: %f" % (turtle.state["position"], turtle.state["last_price"]))
    turtle.strategy()

```

> Detail

https://www.fmz.com/strategy/192353

> Last Modified

2020-03-23 14:44:24
