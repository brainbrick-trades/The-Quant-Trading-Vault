
> Name

TBD-Python2-3

> Author

FawkesPan

> Strategy Description

# OkEX Advanced API functions (FMZ.com)

### Initialize
This library integrates some OkEX advanced API functions and needs to be initialized before use.
#### OkEXfutures
```
# OkEX futures
# future Optional parameter this_week next_week quarter, default if not filled in this_week
OkEXFuture = ext.OkEXFuturePlus(exchange, future=string)    # Create a new interface object 
# Multiple exchanges
OkEXFuture = ext.OkEXFuturePlus(exchanges[0], future=string)    # exchanges[This depends on which number your exchange is added at]
```
#### OkEXspot
#Still writing

### Order operation - futures
#### Bulk order
##### BulkAdd() Add new order to the local order list
```
side price amount is a required parameter
symbol future If not filled, the default trading pair settings will be used
matchPrice Default is False, set to True to use counterparty price trading
OkEXFuture.BulkAdd(side=string, price=float, amount=integer, matchPrice=False, symbol=string, future=string) 
```
##### BulkClear() Clear local unsubmitted orders
```
symbol After specifying, you can clear orders of the specified trading pair; if not specified, all orders will be cleared
notify Whether to display logs, default is display
OkEXFuture.BulkClear(symbol=string, notify=True)
```
##### BulkPost() Submit local unsubmitted orders
```
symbol If specified, only submit orders for the specified trading pair; if not specified, submit all orders
future Must specify symbol simultaneously to use; after specifying, only submit orders for the specific contract of the specific trading pair
OkEXFuture.BulkPost(symbol=string, future=string)
```
##### BulkOrders() View local unsubmitted orders
```
symbol After specifying, only the specified trading pair orders are viewed; if not specified, all orders are viewed
future Must specify symbol simultaneously to use; after specifying, only view orders for the specific contract of the specific trading pair
OkEXFuture.BulkOrders(symbol=string, future=string)
```

### Contact me
Email i@fawkex.me
Telegram [FawkesPan](https://telegram.me/FawkesPan)

Accept policy customization

### About this library
[OkEX APIDocumentation](https://github.com/okcoin-okex/API-docs-OKEx.com/)

[Use GNU General Public License v3](https://www.gnu.org/licenses/gpl-3.0.en.html)

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|LANG|ZH|Language / Language|


> Source (python)

``` python

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# encoding: utf-8
#
# OkEX Advanced API Interface for FMZ.com.
#
# Copyright 2018 FawkesPan
# Contact : i@fawkex.me / Telegram@FawkesPan
#
# GNU General Public License v3.0
#

import json
import time

QUOTES = {}
QUOTES['ZH'] = {
    'GREET' : '[OkEX Interface initialized] Currency: %s Contract: %s. %s',
    'INITF' : 'The exchange being used is incorrect, current exchange: %s',
    'PARAMERR' : '***Incorrect parameter passed, check your code*** %s',
    'NEWORDER' : '[Add order] Currency: %s Contract: %s Direction: %s Price: %.4f Quantity: %d pieces. %s',
    'ORDCOUNT' : '[This batch of orders sent] Total: %d items. %s',
    'THISBATCH' : '[Information] Processing Currency: %s Contract: %s Number of items: %d. %s',
    'ORDSENT' : '[Sent Orders] Currency: %s Contract: %s Number of Orders: %d. %s',
    'NEEDSPLIT' : '[Information] Since the single contract volume is greater than 5, sharding processing is required. %s',
    'CLEARALL' : '[INFO] All local orders cleared. %s',
    'CLEARS' : '[[Info] All %s local orders have been cleared. %s',
    'CLEAR' : '[[Info] Cleared all %s %s local orders. %s'
}

COLORS = {
    'DEEPBLUE' : '#1F618D',
    'BLUE' : '#0000FF',
    'LIGHTBLUE' : '#5DADE2',
    'DEEPGREEN' : '#27AE60',
    'GREEN' : '#00FF00',
    'LIGHTGREEN' : '#58D68D',
    'LAPIS' : '#26619C',
    'DEEPRED' : '#CB4335',
    'RED' : '#FF0000',
    'LIGHTRED' : '#EC7063'
}


class OkEXFuture:

    def __init__(self, exchange, future='this_week'):
        self.QUOTES = {}
        exchange.GetCurrency()
        if isinstance(exchange.GetCurrency(), bytes):
            self.symbol = str(exchange.GetCurrency(), "utf-8").lower()
            name = str(exchange.GetName(), "utf-8")
        else:
            self.symbol = exchange.GetCurrency()
            name = exchange.GetName()
        self.IO = exchange.IO
        self.future = future
        self.bulks = {}
        self.bulks[self.symbol] = {}
        self.bulks[self.symbol][self.future] = []
        if 'OKCoin' in str(name):
            Log(QUOTES[LANG]['GREET'] % (self.symbol.upper(),self.future.upper(),COLORS['LAPIS']))
        else:
            Log(QUOTES[LANG]['INITF'] % (name))

    def BulkAdd(self, side=None, price=None, amount=None, matchPrice=False, symbol=None, future=None):
        if type is None or price is None or amount is None:
            Log(QUOTES[LANG]['PARAMERR'] % (COLORS['RED']))
            return False
        side = side.lower()
        if side == 'buy':
            tp = 1
            cl = COLORS['DEEPGREEN']
        if side == 'sell':
            tp = 2
            cl = COLORS['DEEPRED']
        if side == 'closebuy':
            tp = 3
            cl = COLORS['LIGHTRED']
        if side == 'closesell':
            tp = 4
            cl = COLORS['LIGHTGREEN']
        if symbol is None:
            symbol = self.symbol
        if future is None:
            future = self.future

        order = {}
        order['price'] = price
        order['amount'] = amount
        order['type'] = tp

        if matchPrice:
            order['matchPrice'] = 1

        try:
            self.bulks[symbol]
        except KeyError:
            self.bulks[symbol] = {}
        try:
            self.bulks[symbol][future]
        except KeyError:
            self.bulks[symbol][future] = []

        self.bulks[symbol][future].append(order)

        Log(QUOTES[LANG]['NEWORDER'] % (symbol.upper(),future.upper(),side.upper(),price,amount,cl))

        return True

    def BulkOrders(self, symbol=None, future=None):
        if symbol is None:
            return self.bulks
        else:
            if future is None:
                return self.bulks[symbol]
            else:
                return self.bulks[symbol][future]

    def BulkClear(self, symbol=None, future=None, notify=True):
        if symbol is None:
            self.bulks = {}
            if notify:
                Log(QUOTES[LANG]['CLEARALL'] % (COLORS['RED']))
        else:
            if future is None:
                self.bulks[symbol] = {}
                if notify:
                     Log(QUOTES[LANG]['CLEARS'] % (symbol.encode().upper(), COLORS['RED']))
            else:
                self.bulks[symbol][future] = []
                if notify:
                    Log(QUOTES[LANG]['CLEAR'] % (symbol.encode().upper(), future.encode().upper(), COLORS['RED']))
                    #Log(QUOTES[LANG]['CLEAR'] % (symbol.upper(), future.upper(), COLORS['RED']))

        return True

    #exchange.IO("api", "POST", "/api/v1/future_batch_trade.do", "symbol=etc_usd&contract_type=this_week&orders_data="+json.dumps(orders))
    def __post(self, symbol='', future=''):
        count = len(self.bulks[symbol][future])
        orders = self.bulks[symbol][future]
        ret = []
        if count == 0:
            return
        Log(QUOTES[LANG]['THISBATCH'] % (symbol.upper(),future.upper(),count,COLORS['LAPIS']))
        if count <= 5:
            params = 'symbol=%s&contract_type=%s&orders_data=%s' % (symbol, future, json.dumps(orders))
            res = self.IO("api", "POST", "/api/v1/future_batch_trade.do", params)
            ret+=res['order_info']
            Log(QUOTES[LANG]['ORDSENT'] % (symbol.upper(),future.upper(),len(orders),COLORS['LAPIS']))
        if count > 5:
            Log(QUOTES[LANG]['NEEDSPLIT'] % (COLORS['LAPIS']))
            batch = []
            for item in orders:
                batch.append(item)
                if len(batch) == 5:
                    params = 'symbol=%s&contract_type=%s&orders_data=%s' % (symbol, future, json.dumps(batch))
                    res = self.IO("api", "POST", "/api/v1/future_batch_trade.do", params)
                    try:
                        ret+=res['order_info']
                    except:
                        pass
                    Log(QUOTES[LANG]['ORDSENT'] % (symbol.upper(),future.upper(),len(batch),COLORS['LAPIS']))
                    batch = []
                    time.sleep(0.3)               # OkEXLimit to three requests per second

            params = 'symbol=%s&contract_type=%s&orders_data=%s' % (symbol, future, json.dumps(batch))
            res = self.IO("api", "POST", "/api/v1/future_batch_trade.do", params)
            try:
                ret+=res['order_info']
            except:
                pass
            Log(QUOTES[LANG]['ORDSENT'] % (symbol.upper(),future.upper(),len(batch),COLORS['LAPIS']))

        return ret

    def BulkPost(self, symbol=None, future=None):
        ret = []
        count = 0
        if symbol is None:
            symbols = self.bulks.keys()
            for s in symbols:
                futures = self.bulks[s].keys()
                for f in futures:
                    count+=len(self.bulks[s][f])
                    ret+=self.__post(s, f)
                    time.sleep(0.3)               # OkEXLimit to three requests per second

            self.BulkClear(notify=False)
        else:
            if future is None:
                futures = self.bulks[symbol].keys()
                for f in futures:
                    count+=len(self.bulks[symbol][f])
                    ret+=self.__post(symbol, f)
                    time.sleep(0.3)               # OkEXLimit to three requests per second

                self.BulkClear(symbol=symbol, notify=False)
            else:
                count+=len(self.bulks[symbol][future])
                ret+=self.__post(symbol, future)

                self.BulkClear(symbol=symbol, future=future, notify=False)

        Log(QUOTES[LANG]['ORDCOUNT'] % (count,COLORS['LAPIS']))
        return ret

class OkEXSpot:

    def __init__(self, exchange):
        self.IO = exchange.IO

    #TBD

ext.OkEXFuturePlus = OkEXFuture # ExportOkEXFuture Class, The main strategy can passFuturePlus = ext.OkEXFuturePlus(exchange, future)Call
ext.OkEXSpotPlus = OkEXSpot # ExportOkEXSpot Class, The main strategy can passSpotPlus = ext.OkEXSpotPlus(exchange)Call

# Module Function Test
def main():
    LogReset()
    Log(exchange.GetAccount())
    OKEXPlus = ext.OkEXFuturePlus(exchange)
    # 4 Buy 2 Sell 1 next_week
    base_price = exchange.GetTicker()['Last']
    OKEXPlus.BulkAdd("sell", base_price*1.2, 1)
    OKEXPlus.BulkAdd("closebuy", base_price*1.2, 1)
    OKEXPlus.BulkAdd("sell", base_price*1.3, 1)
    OKEXPlus.BulkAdd("buy", base_price*0.7, 1, future='next_week')

    OKEXPlus.BulkClear()

    OKEXPlus.BulkAdd("buy", base_price*0.8, 1)
    OKEXPlus.BulkAdd("closebuy", base_price*1.2, 1)
    OKEXPlus.BulkAdd("sell", base_price*1.3, 1)
    OKEXPlus.BulkAdd("buy", base_price*0.7, 1, future='next_week')

    OKEXPlus.BulkClear(symbol=(exchange.GetCurrency()).lower(),future='this_week')
    OKEXPlus.BulkClear(symbol=(exchange.GetCurrency()).lower(),future='next_week')

    OKEXPlus.BulkAdd("buy", base_price*0.8, 1)
    OKEXPlus.BulkAdd("buy", base_price*0.7, 1, future='next_week')
    OKEXPlus.BulkClear(symbol=(exchange.GetCurrency()).lower())

    OKEXPlus.BulkAdd("buy", base_price*0.8, 1)
    OKEXPlus.BulkAdd("buy", base_price*0.81, 1)
    OKEXPlus.BulkAdd("buy", base_price*0.82, 1)
    OKEXPlus.BulkAdd("closesell", base_price*0.8, 1)
    OKEXPlus.BulkAdd("sell", base_price*1.2, 1)
    OKEXPlus.BulkAdd("closebuy", base_price*1.2, 1)
    OKEXPlus.BulkAdd("sell", base_price*1.3, 1)
    OKEXPlus.BulkAdd("buy", base_price*0.7, 1, future='next_week')

    Log(OKEXPlus.BulkOrders())
    for item in OKEXPlus.BulkPost():
        Log(str(item))
    Log(OKEXPlus.BulkOrders())

```

> Detail

https://www.fmz.com/strategy/113979

> Last Modified

2018-11-12 20:55:49
