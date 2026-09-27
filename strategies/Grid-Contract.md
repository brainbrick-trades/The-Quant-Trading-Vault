
> Name

Grid-Contract

> Author

Zer3192



> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|contract_type|swap|Contract Type|
|margin_level|10|Leverage multiple|
|net_type|0|Grid type: long|short|long and short|
|net_interval|0.01|Grid Spacing|
|net_amount|true|grid opening count|
|net_limit|100|Grid number limit|
|stop_profit|15|Take-profit point|
|stop_loss|15|Stop-loss point|


> Source (python)

``` python
'''backtest
start: 2020-02-27 00:00:00
end: 2020-02-27 00:00:00
period: 1d
exchanges: [{"eid":"Futures_OKCoin","currency":"ETH_USD","stocks":1.6}]
'''
#Regular upper and lower grids
import json
global_param={
              'sell_id':0,
              'buy_id':0,
              'buy_amount':0,#Current long position quantity
              'sell_amount':0,#Current short position quantity
              'buy_profit':0,#Long Position Profit
              'sell_profit':0#Short Position Profit
             }

def open_order(price):
    net_buy_count = global_param['buy_amount'] / net_amount
    net_sell_count = global_param['sell_amount'] / net_amount
    if(net_buy_count>= net_limit or net_sell_count>=net_limit):
        Log("Exceeds the grid quantity limit, do not open a position!")
        return
    if(net_type == 1 or net_type == 2):#If set to open short or both long and short
        exchange.SetDirection("sell")#Set order type to short
        order_id = exchange.Sell(_N(price*(1+net_interval),2),net_amount)#Open a short at the current price upper limit, contract quantity is10Place order
        global_param['sell_id'] = order_id
    if(net_type == 0 or net_type == 2):#If set to open long or both long and short
        exchange.SetDirection("buy")#Set order type to long
        order_id = exchange.Buy(_N(price*(1-net_interval),2),net_amount)#Open a long at the current price lower limit, contract quantity is10Place order                        
        global_param['buy_id'] = order_id
        
def cancel_order():
    for order in _C(exchange.GetOrders):
        _C(exchange.CancelOrder,int(order['Id']))
    global_param['sell_id']=0
    global_param['buy_id']=0
        
def judge_order_finish():
    if(global_param['buy_id']!=0):
        order = exchange.GetOrder(global_param['buy_id'])
        if(order["Status"]==ORDER_STATE_CLOSED):
            return True
        else:
            return False
    if(global_param['sell_id']!=0):
        order = exchange.GetOrder(global_param['sell_id'])
        if(order["Status"]==ORDER_STATE_CLOSED):
            return True  
        else:
            return False
    return True
        
def get_position():
    global_param['sell_amount'] = 0
    global_param['sell_profit'] = 0
    global_param['buy_amount'] = 0
    global_param['buy_profit'] = 0
    positions= exchange.GetPosition()
    for position in positions:
        if(position['Type']==PD_SHORT): #Short position      
            global_param['sell_amount'] = position['Amount']#Get short positions
            global_param['sell_profit'] = position['Profit']#Get short profit
        elif(position['Type']==PD_LONG):
            global_param['buy_amount'] = position['Amount']#Get long positions
            global_param['buy_profit'] = position['Profit']#Get long profit

    
def check_stop(price):#Take-profit and stop-loss judgment
    total_profit = global_param['sell_profit'] + global_param['buy_profit']
    if( total_profit>= stop_profit or total_profit<=-stop_loss):#Close position if profit reaches take-profit value or loss reaches stop-loss value
        Log("Take profit and stop loss closing, current total profit of the position",total_profit)
        if(global_param['sell_amount']>0):  
            Log("sell_amount",global_param['sell_amount'])
            exchange.SetDirection("closesell");#Set order type to close short
            exchange.Buy(_N(price*1.005,2),global_param['sell_amount'])
        if(global_param['buy_amount']>0):
            Log("buy_amount",global_param['buy_amount'])
            exchange.SetDirection("closebuy");#Set order type to close long
            exchange.Sell(_N(price*0.995,2),global_param['buy_amount'])
                
def main():
    exchange.SetContractType(contract_type)#Set Contract
    exchange.SetMarginLevel(margin_level)#Leverage Ratio
    while True:
        ticker = exchange.GetTicker()
        price = ticker['Last']
        get_position()
        check_stop(price)
        if(judge_order_finish()):
            Log("current price is:",price)
            cancel_order()#Cancel order
            open_order(price)#Place Order
        Sleep(1000)
            

            
        
        

```

> Detail

https://www.fmz.com/strategy/227783

> Last Modified

2021-09-04 13:40:25
