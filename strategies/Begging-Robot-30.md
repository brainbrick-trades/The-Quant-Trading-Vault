
> Name

Begging-Robot-30

> Author

量化多杰

> Strategy Description

Thought Process:
1. Normal grid.
2. Close position to hedge against decline.
3. During hedging, simulate a trade; exit the real trade only after the profit is sufficient.

(This idea was backtested **can't avoid major disaster**, so it's open-sourced for everyone to mock and laugh at.)
What if you tweak it and can make money.

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|UI_AttackRatio|true|Proportion of amount used|
|UI_NodeCount|20|Number of grids|
|UI_AttackThreshold|50|Attack Threshold|
|UI_DefenceThreshold|3|Defense Threshold|


> Source (python)

``` python

#!,encrypt
'''backtest
start: 2022-01-01 00:00:00
end: 2022-01-31 23:59:00
period: 1m
basePeriod: 1m
exchanges: [{"eid":"OKX","currency":"ETH_USDT","balance":1000,"stocks":0,"fee":[0.08,0.1]}]
'''

from datetime import datetime, timedelta, timezone
import json

Is_Debug = False
manager = None
debug = None
log = None

def main():
    Log('Started begging')
    EnableLog(Is_Debug)
    OnInit()
    while True:
        Sleep(1000)
        manager.LoadData()
        OnCommand()
        manager.OnTick()
        manager.SaveData()
    Log('Finished begging')

#If there was no data, initialize all data.
def OnInit():
    #Set retry time interval
    _CDelay(600000)
    #Filter network error logs
    global Is_Debug
    if Is_Debug == False:
        SetErrorFilter("400:|503:|429:|504:")
    
    global manager
    manager = Manager()

    return

#Handle FromUIInteraction response
def OnCommand():
    pass


class Manager:
    Account = None
    Tick = None
    State = ""
    Node_List = []

    BuyPrice = 0
    SellPrice = 0
    Balance = 0
    Stocks = 0
    TickTime = 0
    FrozenBalance = 0
    FrozenStocks = 0

    #Number of profitable trades in defense mode
    DefenceProfitCount = 0

    ClearOrder = 0

    def Ins():
        global manager
        if manager == None:
            manager = Manager()
        return manager

    def GetInfo(self):
        self.Tick = _C(exchange.GetTicker)
        if self.Tick == None:
            return False
        
        self.Account = _C(exchange.GetAccount)
        if self.Account == None:
            return False
        
        self.SellPrice = self.Tick["Sell"]
        self.BuyPrice = self.Tick["Buy"]
        self.Balance = self.Account["Balance"]
        self.Stocks = self.Account['Stocks']
        self.TickTime = self.Tick['Time']
        self.FrozenBalance = self.Account['FrozenBalance']
        self.FrozenStocks = self.Account['FrozenStocks']
        return True

    def OnTick(self):
        if self.GetInfo() == False:
            return

        if self.State == "":
            #First run
            MyLog.Ins().StartTime = self.TickTime
            MyLog.Ins().StartMoney = self.TotalMoney()
            self.ToAttack()
        else:
            MyLog.Ins().PrintLog()

        if self.State == "Close Position":
            self.ClearTick()
            return

        if self.State == 'Defense':
            if self.DefenceProfitCount >= UI_AttackThreshold:
                MyLog.Write("Defensive scoring is sufficient, enter offensive mode.")
                self.ToAttack()
                return

        if len(self.Node_List) == 0:
            #Position empty, buy on the spot
            node = Node.Buy(self.SellPrice, self.GetBuyNumber())
            if node != None:
                self.Node_List.append(node)
                last_node = Node.Buy(Node.MinLeftPrice(), self.GetBuyNumber())
                if last_node != None:
                    self.Node_List.insert(0, last_node)
            return

        if Node.CenterNode() != None:
            #I am in the middle of the node
            if self.NodeCheck(Node.CenterNode()):
                #Check Self
                return
            
            index = Manager.Ins().Node_List.index(Node.CenterNode())
            if index > 0:
                #Indicates there is a node on the left
                left = self.Node_List[index-1]
                #Ask Node
                if self.NodeCheck(left):
                    return
                #Ask Buy Order
                if Node.CenterNode()['buy_order'] == 0:
                    self.NodeBuy(Node.CenterNode())
                    MyLog.AddBuyBuyTimes()
                    return
            else:
                #Indicates no node on the left
                if len(self.Node_List) < UI_NodeCount:
                    #Then create a node
                    left_node = Node.Buy(Node.CenterNode()['buy_price'] * 0.995, self.GetBuyNumber())
                    if left_node != None:
                        self.Node_List.insert(0, left_node)
                    MyLog.AddBuyBuyTimes()
                    return

            #Check the right side again
            if index < len(self.Node_List) - 1:
                right = self.Node_List[index + 1]
                if self.NodeCheck(right):
                    return
                #The one on the right, do not place a buy order, otherwise it will lose

        if self.SellPrice < Node.MinPrice():
            #Recheck whether you are on the left side of all nodes
            if len(self.Node_List) >= UI_NodeCount:
                #Check if there are junk positions at high levels
                if Node.HasSell(Node.MaxNode()) == False:
                    #Check again if the buy order was successful, just in case
                    if Node.CheckBuy(Node.MaxNode()) == False:
                        #This is a junk order, can be deleted
                        Node.NodeClear(Node.MaxNode())
                        self.Node_List.remove(Node.MaxSellPrice)
                        return
                #Close Position
                MyLog.Write("Node is at the far left, and position is full, close the position" + "Current Price:" + str(self.SellPrice))
                self.ToClear()
                return
            else:
                #Buy one at the edge
                MyLog.Write("Node on the far left, position not good, buy one order" + "Current Price:" + str(self.SellPrice))
                new_node = Node.Buy(Node.MinLeftPrice(),self.GetBuyNumber())
                if new_node != None:
                    self.Node_List.insert(0,new_node)
                MyLog.AddBuyBuyTimes()
                return

        if self.SellPrice > Node.MaxSellPrice():
            #I am to the right of all nodes
            #Check to see if it is full, place an order if it is not full, and reduce your position if it is full.
            if len(self.Node_List) >= UI_NodeCount:
                #Full, reduce position
                if Node.HasSell(Node.MinNode()) == False:
                    if Node.HasBuy(Node.MinNode()) == False or Node.CheckBuy(Node.MinNode()) == False:
                        MyLog.Write("Sudden surge, order is full, reduce a position" + ".Current Price:" + str(self.SellPrice))
                        Node.NodeClear(Node.MinNode())
                        self.Node_List.remove(Node.MinNode())
                        return
                self.NodeCheck(Node.MinNode())
            else:
                #Place Order, Post
                MyLog.Write("Sudden surge, order not full, add position from bottom to top" + "Current Price:" + str(self.SellPrice))
                new_node = Node.Buy(Node.MaxSellPrice(), self.GetBuyNumber())
                if new_node != None:
                    self.Node_List.append(new_node)


    def NodeBuy(self,_node):
        node = Node.Buy(_node['buy_price'], self.GetBuyNumber())
        if node == None:
            return None
        _node['buy_order'] = node['buy_order']
        _node['state'] = node['state']
        _node['number'] = 0
        
        return _node

    def NodeCheck(self,_node):
        if Node.HasSell(_node):
            #I Have Sell Order,Check sell order
            if Node.CheckSell(_node):
                MyLog.Write("The node I am at has sold." + "Current Price:" + str(self.SellPrice))
                MyLog.Ins().WriteProfit(Node.GetProfit(_node))
                Node.Reset_Node(_node)
                MyLog.Ins().BuyBuy_Count = 0#Recount
                return True
        else:
            if Node.HasBuy(_node):
                if Node.CheckBuy(_node):
                    Node.Sell(_node)
                    return True
        return False

    def DelEmptyNode(self,_node):
        self.Node_List.remove(_node)
        Node.NodeClear(_node)
        return

    #Process sold nodes.
    def DelSellNode(self,_node):
        self.Node_List.remove(_node)
        MyLog.Ins().WriteProfit(Node.GetProfit(_node))
        return


    #Close Position
    def ClearTick(self):
        #Collect the list and cancel one by one
        MyLog.Write("Closing position in progress")
        orders = exchange.GetOrders()
        if len(orders) > 0:
            MyLog.Write("Unprocessed orders greater than0,Cancel order")
            for _o in orders:
                Node.CancelOrder(_o['Id'])
            return
        self.Node_List.clear()
        #Count positions and sell uniformly
        if self.Stocks + self.FrozenStocks > 50 / self.BuyPrice:
            MyLog.Write("Have position, sell")
            if self.ClearOrder == 0:
                #For sale
                MyLog.Write("Have position, quantity:" + str(_N(self.Stocks,4)) + ". Sell Price:" + str(_N(self.BuyPrice * 0.999,4)))
                order_id = exchange.Sell(self.BuyPrice * 0.999, self.Stocks)
                if order_id == None:
                    MyLog.Write("A strange error occurred,160Row left and right.")
                    return
                self.ClearOrder = order_id
                Sleep(100000)
                return
            else:
                order = _C(exchange.GetOrder,self.ClearOrder)
                if order['Status'] != 1:
                    MyLog.Write("The order was not sold, change the price again")
                    Node.CancelOrder(self.ClearOrder)
                    self.ClearOrder = 0
                    return
                elif order['Status'] == 1:
                    MyLog.Write("The order was sold, exit the closing mode")
                    self.ClearOrder = 0

                #Infinite loop until all coins are sold
        
        #When Inventory Is0,Position is0,Then enter defense mode.
        self.ToDefence()

    #Transfer to defense stage
    def ToDefence(self):
        MyLog.Write('Enter Defense')
        if self.State == "Close Position":
            MyLog.Ins().Defence_Count += 1
        MyLog.Ins().StateWrite("Defense",self.State)
        self.State = "Defense"
        self.DefenceProfitCount = 0
    
    #Transfer to offense stage
    def ToAttack(self):
        MyLog.Write('Enter offensive mode')
        MyLog.Ins().StateWrite("Attack",self.State)
        MyLog.Ins().Attack_Count += 1
        self.State = "Attack"
        self.Node_List.clear()

    #Move to the closing phase
    def ToClear(self):
        MyLog.Write('Start Closing Position')
        if self.State == "Defense":#If it comes from the defensive mode, there is no need to close the position and directly re-enter the defensive mode.
            self.Node_List.clear()
            self.ToDefence()
            return
        MyLog.Ins().StateWrite("Close Position",self.State)
        self.State = "Close Position"
        self.ClearOrder = 0

    def LoadData(self):
        MyLog.Ins().LoadData()
        if MyLog.Ins().StartTime == None:
            #First run, do not load subsequent data
            return
        self.Node_List = json.loads(_G('Node_List'))
        self.State = _G("State")
        self.DefenceProfitCount = _G('DefenceProfitCount')
        self.ClearOrder = _G('ClearOrder')

    def SaveData(self):
        MyLog.Ins().SaveData()
        _G("Node_List",json.dumps(self.Node_List))
        _G("State",self.State)
        _G("DefenceProfitCount",self.DefenceProfitCount)
        _G("ClearOrder",self.ClearOrder)
    
    def TotalMoney(self):
        return self.Balance + self.FrozenBalance + (self.Stocks + self.FrozenStocks) * self.BuyPrice

    def GetBuyNumber(self):
        number = self.TotalMoney() * UI_AttackRatio / UI_NodeCount / self.SellPrice
        #Remove too much precision
        return _N(number,4)

class Node:

    #Create a data and return
    def CreateNodeData(_state):
        data = {}
        data['state'] = _state
        data['buy_price'] = 0
        data['sell_price'] = 0
        data['buy_order'] = 0
        data['sell_order']=0
        data['number'] = 0
        return data

    #NodeStill need, reset it
    def Reset_Node(_node):
        _node['number'] = 0
        _node['buy_order'] = 0
        _node['sell_order'] = 0


    def Buy(_price,_number):
        MyLog.Write('Buy order, price:' + str(_price) + '. Quantity:' + str(_number) + ". Value:" + str(_N(_number * _price,2)))
        if Manager.Ins().State == "Attack":
            buy_id = exchange.Buy(_price, _number)
            if buy_id == None:
                return None
        else:
            buy_id = 1
        node = Node.CreateNodeData(Manager.Ins().State)
        node['state'] = Manager.Ins().State
        node['buy_price'] = _price
        node['sell_price'] = _price * 1.005
        node['buy_order'] = buy_id
        node['number'] = 0

        return node

    def HasBuy(_node):
        return _node['buy_order'] != 0

    def HasSell(_node):
        return _node['sell_order'] != 0
    
    #Check if this node is the right-side node
    def IsRight(_node):
        right_price = Manager.Ins().SellPrice * 1.005
        if right_price > _node['buy_price'] and right_price < _node['sell_price']:
            return True
        return False

    def IsLeft(_node):
        right_price = Manager.Ins().SellPrice * 0.995
        if right_price > _node['buy_price'] and right_price < _node['sell_price']:
            return True
        return False

    def CenterNode():
        for node in Manager.Ins().Node_List:
            if Manager.Ins().SellPrice > node['buy_price'] and Manager.Ins().SellPrice < node['sell_price']:
                return node
        return None

    def MaxNode():
        return Manager.Ins().Node_List[-1]

    def MaxBuyPrice():
        return Node.MaxNode()['buy_price']

    def MaxSellPrice():
        return Node.MaxNode()['sell_price']

    def MaxHasSell():
        return Node.MaxNode()['sell_order'] != 0

    def MinNode():
        return Manager.Ins().Node_List[0]

    def MinPrice():
        return Manager.Ins().Node_List[0]['buy_price']

    def MinLeftPrice():
        return _N(Node.MinPrice() * 0.995,4)

    #Check if buy orderOK
    def CheckBuy(_node):
        if _node['state'] == "Defense":
            _node['number'] = 1
            return True
        order = _C(exchange.GetOrder,_node['buy_order'])
        if order['Status'] == 1:
            _node['number'] = order['DealAmount']
            return True
        return  False

    def MinSellPrice():
        return Manager.Ins().Node_List[0]['sell_price']

    def MinHasSell():
        return Manager.Ins().Node_List[0]['sell_order'] != 0
    
    def Sell(_node):
        MyLog.Write('Sell order, price:' + str(_node['sell_price']))
        if _node['state'] == "Defense":
            _node['sell_order'] = 1
            return True
        # Position judgment, tolerance
        # if Manager.Ins().Stocks < _node['number']:
        #     _node['number'] = Manager.Ins().Stocks
        
        order_id = exchange.Sell(_node['sell_price'], _node['number'])
        if order_id == None:
            return False
        _node['sell_order'] = order_id
        return True

    def CheckSell(_node):
        if _node['state'] == "Defense":
            if Manager.Ins().BuyPrice > _node['sell_price']:
                return True
            return False
        
        order = _C(exchange.GetOrder,_node['sell_order'])
        #Precise position again
        if order['Status'] == 1:
            return True
        return False

    def GetProfit(_node):
        value = (_node['sell_price'] - _node['buy_price']) * _node['number']
        return _N(value,2)
    
    def NodeClear(_node):
        if _node['state'] == "Defense":
            return

        if _node['sell_order'] != 0:
            Node.CancelOrder(_node['sell_order'])
        if _node['buy_order'] != 0:
            Node.CancelOrder(_node['buy_order'])

    #Ensure the order is successfully canceled
    def CancelOrder(_id):
        MyLog.Write('Cancel order:' + str(_id))
        while True:
            order = _C(exchange.GetOrder,_id)
            if order['Status'] == 1:
                return True
            if order['Status'] != 2:
                result = exchange.CancelOrder(_id)
                if result == True:
                    return True
                Sleep(1000)
            elif order['Status'] == 2:
                return True


class MyLog:
    #First run time
    StartTime = 0
    StartMoney = 0
    Profit_List = []
    State_List = []
    Log_Tables = []

    Attack_Count = 0
    Defence_Count = 0
    Exchange_Count = 0

    #Current grid profit
    StateProfit = 0

    #Consecutive purchase count
    BuyBuy_Count = 0
    BuyBuyClear_Count = 0

    def Ins():
        global log
        if log == None:
            log = MyLog()
        
        return log
    
    def LoadData(self):
        self.Log_Tables = []
        self.StartTime = _G("StartTime")
        if self.StartTime == None:
            return
        
        self.StartMoney = _G("StartMoney")
        self.Profit_List = json.loads(_G("Profit_List"))
        self.State_List = json.loads(_G("State_List"))
        self.Attack_Count = _G("Attack_Count")
        self.Defence_Count = _G("Defence_Count")
        self.Exchange_Count = _G("Exchange_Count")
        self.StateProfit = _G("StateProfit")
        self.BuyBuy_Count = _G("BuyBuy_Count")
        self.BuyBuyClear_Count = _G("BuyBuyClear_Count")

    def SaveData(self):
        _G("StartTime",self.StartTime)
        _G("StartMoney",self.StartMoney)
        _G("Profit_List",json.dumps(self.Profit_List))
        _G("State_List",json.dumps(self.State_List))
        _G("Attack_Count",self.Attack_Count)
        _G("Defence_Count",self.Defence_Count)
        _G("Exchange_Count",self.Exchange_Count)
        _G("StateProfit",self.StateProfit)
        _G("BuyBuy_Count", self.BuyBuy_Count)
        _G("BuyBuyClear_Count", self.BuyBuyClear_Count)

    def WriteProfit(self,_value):
        if Manager.Ins().State == "Defense":
            #Log("Defensive scoring once")
            Manager.Ins().DefenceProfitCount += 1
            return

        #Log("Thanks to the kind person, gave me" + str(_value) + "USDT.")
        self.StateProfit += _value
        self.Exchange_Count += 1
        data = []
        #Date, profit, current floating loss,Current Coin Price
        data.append(self.GetTimeStr(Manager.Ins().TickTime))
        data.append(_value)
        data.append(_N(Manager.Ins().TotalMoney() - self.StartMoney,2))
        data.append(_N(Manager.Ins().BuyPrice,2))
        if len(self.Profit_List) > 10:
            self.Profit_List.pop()
        self.Profit_List.insert(0,data)
        #Profit Log
        LogProfit(_N(Manager.Ins().TotalMoney() - self.StartMoney,2))

    def AddBuyBuyTimes():
        MyLog.Ins().BuyBuy_Count += 1
        if MyLog.Ins().BuyBuy_Count >= UI_DefenceThreshold and Manager.Ins().State == "Attack":
            MyLog.Write("Reached the continuous purchase threshold, enter defense mode")
            if Manager.Ins().State == "Attack":
                MyLog.Ins().BuyBuyClear_Count += 1
            Manager.Ins().ToClear()


    def GetTimeStr(self,_time):
        utc_dt = datetime.utcfromtimestamp(_time/1000)
        cn_dt = utc_dt.astimezone(timezone(timedelta(hours=8)))
        d = cn_dt.strftime('%Y-%m-%d %H:%M:%S')
        return d
    
    def GetRunDays(self):
        now_date = datetime.utcfromtimestamp(Manager.Ins().TickTime/1000)
        start_date = datetime.utcfromtimestamp(self.StartTime/1000)
        span = now_date - start_date
        run_time = span.days
        if run_time < 1:
            run_time = 1
        return run_time

    def GetToTalProfit(self):
        return Manager.Ins().TotalMoney() - self.StartMoney

    def GetAnnualized(self):
        a = self.GetToTalProfit() / self.GetRunDays() * 365 / self.StartMoney * 100
        return _N(a,2)

    def PrintLog(self):
        #Basic information table
        rows = []
        rows.append(["Current start time:",self.GetTimeStr(self.StartTime)])
        rows.append(["Current initial funds:", self.StartMoney])
        rows.append(["Current Total Position:", _N(Manager.Ins().TotalMoney(),4)])
        rows.append(["Current Profit:",_N(self.GetToTalProfit(),4)])
        rows.append(["Current Annualized:",str(self.GetAnnualized()) + "%"])
        rows.append(["Current Held Coins:",_N(Manager.Ins().Stocks,4)])
        rows.append(["Current Locked Coins:", _N(Manager.Ins().FrozenStocks,4)])
        rows.append(["Wallet Balance:", _N(Manager.Ins().Balance,4)])
        rows.append(["Wallet Frozen:", _N(Manager.Ins().FrozenBalance,4)])
        rows.append(['Current Status:',Manager.Ins().State])
        rows.append(["Defense Count:", self.Defence_Count])
        rows.append(["Forced Liquidation Count:", self.BuyBuyClear_Count])
        self.Add_Log_Table("Basic Information",["Project","Content"], rows)
        #Log(json.dumps(rows))
        #Build and add position table
        n_list = []
        for _node in Manager.Ins().Node_List:
            n = []
            n.append(_node['buy_price'])
            n.append(_node['buy_order'])
            n.append(_node['sell_price'])
            n.append(_node['sell_order'])
            n.append(_node['number'])
            n_list.append(n)
        global Is_Debug
        if Is_Debug:
            self.Add_Log_Table("Position Information",['Buy Price','Buy Order',"Sell Price","Sell Order","Number of Positions"],n_list)
        #Add profit table
        self.Add_Log_Table("Earnings Record",["Time","profit","Current Floating Loss","Current Coin Price"], self.Profit_List)
        #Add status table
        self.Add_Log_Table("Status table",["Time","Enter Status","Previous Status","Current Coin Price","Current Profit","Last grid profit","Last Period Transaction Volume"],self.State_List)
        #Parameter Adjustment Log
        
        LogStatus('`' + json.dumps(self.Log_Tables) + '`')
    
    def StateWrite(self,_name,_lastname):
        #Time, status, previous status, current market price, current profit
        data = [self.GetTimeStr(Manager.Ins().TickTime), _name, _lastname, _N(Manager.Ins().SellPrice,2), _N(self.GetToTalProfit(),2),_N(self.StateProfit,2),self.Exchange_Count]
        self.State_List.insert(0, data)

        if len(self.State_List) >= 100:
            self.State_List.pop()
        
        self.StateProfit = 0
        self.Exchange_Count = 0
        self.BuyBuy_Count = 0

    def Add_Log_Table(self, _title, _cols, _rows):
        table = {
            "type" : "table", 
            "title" : _title, 
            "cols" : _cols, 
            "rows" : _rows
        }
        self.Log_Tables.append(table)

    def Write(_str):
        global Is_Debug
        if Is_Debug:
            Log(str(_str))
```

> Detail

https://www.fmz.com/strategy/377408

> Last Modified

2022-10-06 14:58:03
