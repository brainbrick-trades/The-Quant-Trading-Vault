
> Name

Synthesize-Candlesticks-of-Any-Period-See-the-Very-Bottom-of-the-Source-Code-for-Usage

> Author

FawkesPan





> Source (python)

``` python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# encoding: utf-8
# 
# Candlestick merger.
#
# Copyright 2018 FawkesPan
# Contact : i@fawkex.me / Telegram@FawkesPan
#
# Do What the Fuck You Want To Public License
#

from math import *
from datetime import datetime

def timeFilter(records, since, to=1000000000000000):
    bars = []
    for i in records:
        if i['Time'] >= since and i['Time'] <= to:
            bars.append(i)

    return bars

def calcRecords(records, period=30, start=None):
    try:
        records[0]
    except IndexError:
        return []
    
    period_ms = period * 60000  # candlestick period in milliseconds
    end_in = records[len(records)-1]['Time']  # KEnd time of the line
    start_at = records[0]['Time']  # KStart time of the line
    
    # Obtain the starting time that can be used to calculate the target candlestick
    r_offest = start_at % period_ms
    start_at = start_at - r_offest + period_ms
    if start is not None:
        start_at = start
    
    target_count = ceil((end_in-start_at)/period_ms) # Number of target candlesticks
    
    n_records = []
    
    for i in range(0, target_count):
        bars = timeFilter(records, start_at+i*period_ms, start_at+(i+1)*period_ms-1000)
        try:
            bars[0]
        except IndexError:
            continue
        # Initialize newBar
        Time = bars[0]['Time']
        Open = bars[0]['Open']
        High = bars[0]['High']
        Low = bars[0]['Low']
        Close = bars[0]['Close']
        Volume = 0
        for item in bars:
            High = max(High, item['High'])
            Low = min(Low, item['Low'])
            Close = item['Close']
            Volume+=item['Volume']
            
        # Add Bar to the new candlestick
        n_records.append(dict({
            'Time' : Time,
            'Open' : Open,
            'High' : High,
            'Low' : Low,
            'Close' : Close,
            'Volume' : Volume
        }))
        
    return n_records

def getRecords(exchange, period=30):
    records = exchange.GetRecords(PERIOD_M1)
        
    return calcRecords(records, period)

def calcRecordsWithOldRecords(records, old_records, period=30):
    try:
        start = old_records[len(old_records)-1]['Time']
        del old_records[len(old_records)-1]
    except IndexError:
        old_records = []
        start = None
        
    return old_records + calcRecords(records=records, period=period, start=start)
        
ext.calcRecords = calcRecords
ext.getRecords = getRecords
ext.calcRecordsWithOldRecords = calcRecordsWithOldRecords

# Function Test
def main():
    LogReset()
    M1 = exchange.GetRecords(PERIOD_M1)
    M15 = exchange.GetRecords(PERIOD_M15)
    M15_GEN = ext.calcRecords(M1, 15) # Useext.calcRecordsFunction according to1MinuteKCalculate from line15MinuteKLine
    Log(M15[len(M15)-50:])
    Log(M15_GEN[len(M15_GEN)-50:])
```

> Detail

https://www.fmz.com/strategy/117473

> Last Modified

2018-09-21 13:24:55
