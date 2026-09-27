
> Name

Paul-The-Gambler-Lévy

> Author

FawkesPan

> Strategy Description

###### Futures Gambler Strategy
##### If the direction is wrong, automatically reverse and double the position
#### Live trading will lose all money!!!
### Live trading will lose all money!!!
## Live trading will lose all money!!!
# Live trading will lose all money!!!

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|STOP_LOSS|0.015|Stop loss distance|
|TAKE_PROFIT|0.03|Take Profit Distance|
|START_SIZE|true|Initial position|
|RISK_LIMIT|1025|Maximum position|
|LEVERAGE_RATE|20|Leverage Size|
|CONTRACT_TYPE|this_week|Contract Type|
|DELAY|30|Refresh interval|
|AMP|2|Reverse multiple|


> Source (python)

``` python


#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# encoding: utf-8
#
#  Paul "The Gambler" Lévy.
#
# Copyright 2018 FawkesPan
# Contact : i@fawkex.me / Telegram@FawkesPan
#
# Do What the Fuck You Want To Public License
#

import random
from math import *

Account = {}
Ticker = {}
LPosition = 0
SPosition = 0
Positions = {}
TotalLoss = 0
TotalWin = 0
FullLoss = 0
MaxPosition = 0
TotalLongs = 0
TotalShorts = 0

def cancelAllOrders():
    orders = exchange.GetOrders()
    for order in orders:
        exchange.CancelOrder(order['Id'], order)
    return True

def updateMarket():
    global Ticker

    Ticker = exchange.GetTicker()

    return True

def updateAccount():
    global Account
    global LPosition
    global SPosition
    global Positions
    global MaxPosition

    LPosition = 0
    SPosition = 0
    Positions = {}
    for item in exchange.GetPosition():
        if item['MarginLevel'] == LEVERAGE_RATE:
            if item['Type'] == 1:
                Positions['Short'] = item
                SPosition += item['Amount']
            else:
                Positions['Long'] = item
                LPosition += item['Amount']
        MaxPosition = max(MaxPosition, SPosition, LPosition)

    Account = exchange.GetAccount()

    return True

def updatePositions():
    global TotalWin
    global TotalLoss
    global FullLoss

    opened = False

    try:
        Long = Positions['Long']['Amount']
        LongEntry = Positions['Long']['Price']
        Current = Ticker['Sell']

        StopLoss = LongEntry * (1-STOP_LOSS)
        TakeProfit = LongEntry * (1+TAKE_PROFIT)

        if Current > TakeProfit:
            Risked = True
            Log('Long position reaches preset take-profit price. #0000FF')
            TotalWin+=1
            Log('Total number of times to take profit: ', TotalWin, ' Total number of stop losses: ', TotalLoss, ' Complete stop loss times: ', FullLoss, ' Maximum position held: ', MaxPosition, ' Total open long: ', TotalLongs, ' Total short opening: ', TotalShorts)
            coverLong(Long, True)
        if Current < StopLoss:
            Risked = True
            Log('Long position reaches preset stop-loss price. #FF0000')
            TotalLoss+=1
            Log('Total number of times to take profit: ', TotalWin, ' Total number of stop losses: ', TotalLoss, ' Complete stop loss times: ', FullLoss, ' Maximum position held: ', MaxPosition, ' Total open long: ', TotalLongs, ' Total short opening: ', TotalShorts)
            coverLong(Long, True)
            if Long*AMP < RISK_LIMIT:
                openShort(Long*AMP, True)
            else:
                FullLoss+=1
                Log('Exceeds the maximum allowed position and stops opening positions.. #FF0000')
                Log('Total number of times to take profit: ', TotalWin, ' Total number of stop losses: ', TotalLoss, ' Complete stop loss times: ', FullLoss, ' Maximum position held: ', MaxPosition, ' Total open long: ', TotalLongs, ' Total short opening: ', TotalShorts)

        opened = True
    except KeyError:
        pass

    try:
        Short = Positions['Short']['Amount']
        ShortEntry = Positions['Short']['Price']
        Current = Ticker['Buy']

        StopLoss = ShortEntry * (1+STOP_LOSS)
        TakeProfit = ShortEntry * (1-TAKE_PROFIT)

        if Current < TakeProfit:
            Risked = True
            Log('Short position reaches preset take-profit price. #0000FF')
            TotalWin+=1
            Log('Total number of times to take profit: ', TotalWin, ' Total number of stop losses: ', TotalLoss, ' Complete stop loss times: ', FullLoss, ' Maximum position held: ', MaxPosition, ' Total open long: ', TotalLongs, ' Total short opening: ', TotalShorts)
            coverShort(Short, True)
        if Current > StopLoss:
            Risked = True
            Log('Short position reaches preset stop-loss price. #FF0000')
            TotalLoss+=1
            Log('Total number of times to take profit: ', TotalWin, ' Total number of stop losses: ', TotalLoss, ' Complete stop loss times: ', FullLoss, ' Maximum position held: ', MaxPosition, ' Total open long: ', TotalLongs, ' Total short opening: ', TotalShorts)
            coverShort(Short, True)
            if Short*AMP < RISK_LIMIT:
                openLong(Short*AMP, True)
            else:
                FullLoss+=1
                Log('Exceeds the maximum allowed position and stops opening positions.. #FF0000')
                Log('Total number of times to take profit: ', TotalWin, ' Total number of stop losses: ', TotalLoss, ' Complete stop loss times: ', FullLoss, ' Maximum position held: ', MaxPosition, ' Total open long: ', TotalLongs, ' Total short opening: ', TotalShorts)

        opened = True
    except KeyError:
        pass

    if not opened:
        Log('Haven't opened a position yet, just open any position.')
        rand = random.choice([1,2,3,4,5,6])
        if rand in [1,3,5]:
            Log('The dice is thrown: ',rand,' Opening long position.')
            openLong(START_SIZE, True)
        else:
            Log('The dice is thrown: ',rand,' Opening short.')
            openShort(START_SIZE, True)

    return True

def openLong(Amount=0, marketPrice=False):
    global TotalLongs

    Amount = floor(Amount)

    TotalLongs+=Amount

    exchange.SetDirection('buy')

    if marketPrice:
        exchange.Buy(Ticker['Sell']*1.01, Amount)
    else:
        exchange.Buy(Ticker['Sell'], Amount)

    return True

def coverLong(Amount=0, marketPrice=False):
    exchange.SetDirection('closebuy')

    if marketPrice:
        exchange.Sell(Ticker['Buy']*0.99, Amount)
    else:
        exchange.Sell(Ticker['Buy'], Amount)

    return True

def openShort(Amount=0, marketPrice=False):
    global TotalShorts

    Amount = floor(Amount)

    TotalShorts+=Amount

    exchange.SetDirection('sell')

    if marketPrice:
        exchange.Sell(Ticker['Buy']*0.99, Amount)
    else:
        exchange.Sell(Ticker['Buy'], Amount)

    return True

def coverShort(Amount=0, marketPrice=False):
    exchange.SetDirection('closesell')

    if marketPrice:
        exchange.Buy(Ticker['Sell']*1.01, Amount)
    else:
        exchange.Buy(Ticker['Sell'], Amount)

    return True

def onTick():
    cancelAllOrders()
    updateMarket()
    updateAccount()
    updatePositions()

    return True

def main():
    exchange.SetContractType(CONTRACT_TYPE)
    exchange.SetMarginLevel(LEVERAGE_RATE)

    while True:
        onTick()
        Sleep(DELAY*1000)

```

> Detail

https://www.fmz.com/strategy/117768

> Last Modified

2018-09-21 01:34:13
