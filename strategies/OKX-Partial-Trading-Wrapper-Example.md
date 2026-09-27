
> Name

OKX-Partial-Trading-Wrapper-Example

> Author

作手君TradeMan





> Source (python)

``` python
#!/usr/bin/python
# coding=UTF-8

import hmac
import base64
import urllib
from hashlib import sha256
import datetime
import json
import requests
from logger import logger


class Okex(object):

    def __init__(self, api_key, secret_key, passphrase):
        self.api_key = api_key
        self.secret_key = secret_key
        self.passphrase = passphrase
        self.host = 'https://www.okex.com'
        self.timestamp = ''
        self.method = ''
        self.request_path = ''

    # Place Order
    def trade_order(self, symbol, pos_side, trade_side, sz, client_id, ord_type="market", px=None):
        self.request_path = '/api/v5/trade/order'
        self.method = 'POST'
        inst_id = symbol.upper() + '-USDT-SWAP'
        post_data = {
            'instId': inst_id,
            'tdMode': 'cross',
            'side': trade_side,
            'ordType': ord_type,
            'posSide': pos_side,
            'sz': str(sz),
            'tag': 'BrokerCode',
            'clOrdId': '4dc650bdb59cBCDE' + str(client_id)
        }
        if ord_type == 'limit':
            post_data['px'] = str(px)
        try:
            # 0 Success: 1 Pause for a few seconds, 2 Ignore this trade, 3 User stops the strategy
            order = self.send(post_data)
            # print(order)
            if len(order['data']) == 0:
                return {"code": 2, "msg": 'OKEXError in order interface return data', "data": {}}
            order_info = order['data'][0]
            if order['code'] == '0' and order_info['sCode'] == '0':
                return {"code": 0, "msg": 'success', "data": order_info}

            if order_info['sCode'] == '50004' or order_info['sCode'] == '51029' or order_info['sCode'] == '51030':
                #  failed, you can try again later
                return {"code": 1, "msg": order_info['sMsg'], "data": {}}
            if order_info['sCode'] == '51008':
                # Failed, pause buying
                return {"code": 3, "msg": order_info['sMsg'], "data": {}}
        except Exception as e:
            return {"code": 2, "msg": str(e), "data": {}}
        # Failed, pause operation
        return {"code": 2, "msg": order_info['sMsg'], "data": {}}

    # Cancel order
    def cancel_order(self, data):
        self.request_path = '/api/v5/trade/cancel-batch-orders'
        self.method = 'POST'
        try:
            order = self.send(data)
            if len(order['data']) == 0:
                return {"code": 3, "msg": 'OKEXError in cancel order interface return data', "data": {}}
            if order['code'] == '0':
                return {"code": 0, "msg": 'success', "data": order}

        except Exception as e:
            # logger.error(e)
            return {"code": 3, "msg": str(e), "data": {}}
        # Failed, pause operation
        return {"code": 3, "msg": order['msg'], "data": {}}

    # Get the list of pending orders
    def get_open_order(self):
        self.request_path = '/api/v5/trade/orders-pending'
        self.method = 'GET'
        post_data = {
            'instType': 'SWAP',
        }
        order = self.send(post_data)
        if order['code'] != '0':
            raise ValueError(order['msg'])
        return order['data']

    # Get the position list
    def get_positions(self, symbol=None):
        self.request_path = '/api/v5/account/positions'
        self.method = 'GET'
        post_data = {
            'instType': 'SWAP',
        }
        if symbol:
            post_data['instId'] = symbol.upper() + '-USDT-SWAP'

        order = self.send(post_data)
        if order['code'] != '0':
            raise ValueError(order['msg'])
        return order['data']

    # Get candlestick
    def get_kline(self, symbol, limit, interval, after=None):
        self.request_path = '/api/v5/market/history-candles'
        self.method = 'GET'

        post_data = {
            'instId': symbol.upper() + '-USDT-SWAP',
            'bar': interval,
            'limit': limit,
        }
        if after:
            post_data['after'] = after
        order = self.send(post_data)
        if order['code'] != '0':
            raise ValueError(order['msg'])
        return order['data']

    # Signature
    def generate_sign(self, data):
        if self.method == 'GET':
            self.request_path = self.request_path + '?' + urllib.parse.urlencode(data)
        req_str = self.timestamp + self.method + self.request_path

        if self.method == 'POST':
            req_str = (req_str + json.dumps(data))

        req_strs = req_str.encode('utf-8')
        signature = base64.b64encode(hmac.new(self.secret_key.encode('utf-8'), req_strs, digestmod=sha256).digest())
        return signature

    # timestamp
    def set_timestamp(self):
        utc_t = datetime.datetime.utcnow().isoformat()
        self.timestamp = utc_t[:-3] + 'Z'

    # Request
    def send(self, data):
        self.set_timestamp()
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'OK-ACCESS-KEY': self.api_key,
            'OK-ACCESS-SIGN': self.generate_sign(data),
            'OK-ACCESS-TIMESTAMP': self.timestamp,
            'OK-ACCESS-PASSPHRASE': self.passphrase,
        }
        if self.method == 'GET':
            response = requests.get(self.host + self.request_path, headers=headers, timeout=30)
        else:
            post_data = json.dumps(data)
            response = requests.post(self.host + self.request_path, headers=headers, data=post_data, timeout=30)
        # logger.info('okexRequest information')
        # logger.info(data)
        # logger.info(response.text)
        return json.loads(response.text)
```

> Detail

https://www.fmz.com/strategy/417576

> Last Modified

2023-06-14 17:57:16
