
> Name

BTCUSDT-Quantitative-Trading-Executor

> Author

zomo

> Strategy Description

```
https://github.com/Find-Dream/BTCUSDT
```

> Currently only supports Ouyi API interface and BTCUSDT perpetual contract trading. Quantitative trading pursues stable income, so please do not set high leverage. It is recommended that the leverage multiple be 5 times or less.

- WindowsThe version is the interface version. After downloading, first configure the exchange API through set_api, and then run the btcusdt program to start automatic trading.;
- PythonThe source code interface version can run on any desktop operating system. Just install and configure the Python environment. It is recommended to use Python3.7.7 version. You need to install the requests library. The usage method is similar to the Windows version for the interface version.;
- PythonThe source code command line version can run on any operating system. Just install and configure the Python environment. It is recommended to use Python3.7.7 version. You need to install the requests library and configure the exchange API by manually modifying the `okex_api.json` file. Under CentOS, the executable can be automatically executed in the background through the following command:
```
nohup python3 start.py &
```
Terminate the process and stop trading using the following command:
```
ps -aux | grep start.py
kill -9 Obtained process number
```


### APINotes:

- If you are not running on a fixed IP cloud server, please do not set a bound IP, otherwise it will not work;
- When applying for API for the security of your account, please check the read-only and transaction permissions, and do not check the withdrawal permissions.;
- `okex_api.json`The flag in it is the trading account option, 0 for live account, 1 for simulated account;

### Frequently Asked Questions
##### Stuck after starting trading

- APIThe settings are incorrect. Please check whether the API is configured correctly. The APIs of real disks and simulated disks are different and need to be set separately.;
- Domestic networks cannot access exchanges. Please use an overseas cloud host to run the execution body, Hong Kong cloud host recommended;
- Please do not use circumvention software to open the executable body in China. Due to compatibility issues, there is a high probability that the circumvention software will not be able to run.;





> Source (python)

``` python
from okex.trade import trade,pos_info,acc_info,select_last
import okex.api as api
import okex.Trade_api as Trade
import time
import json
from okex.log import log

# Strategy source code full version download address https://github.com/Find-Dream/BTCUSDT

def main():
    nowtime = time.time()
    st = time.localtime(nowtime)
    update = time.strftime('%Y-%m-%d',st)
    filenamedate = time.strftime('%Y%m%d',st)
    logfilename = 'mark_'+ str(filenamedate)

    log(logfilename,'========================[Start by getting basic information]========================')

    btcusdt_api_data = api.btcusdt_api()

    log(logfilename,'btcusdt_api_data:'+str(btcusdt_api_data))

    btcusdt_api = btcusdt_api_data['rule']
    log(logfilename,'btcusdt_api'+str(btcusdt_api))

    pos_api = btcusdt_api_data['pos']
    log(logfilename,'pos_api'+str(pos_api))

    pos_okex = {}
    acc_okex = {}
    try:
        acc_api = api.select_acc()
        log(logfilename,'Read locally saved account information'+str(acc_api))
    except:
        acc_okex['lever'] = 1


    acc_info_data = acc_info()[0]['details']


    for i in acc_info_data:
        if i['ccy'] == 'USDT':
            acc_okex['ccy'] = i['cashBal']
            log(logfilename,'Read interface account balance'+str(i['cashBal']))

    for i in pos_info():
        if i['mgnMode'] == 'cross' and i['posSide'] == 'long':
            pos_okex['long'] = i['pos']
            if i['pos'] != '0':
                acc_okex['lever'] = i['lever']
                log(logfilename,'Read interface long account leverage multiple:'+str(i['lever']))
            else:
                acc_okex['lever'] = acc_api['lever']
                log(logfilename,'Read the local long account leverage multiple:'+str(acc_api['lever']))
        elif i['mgnMode'] == 'cross' and i['posSide'] == 'short':
            pos_okex['short'] = i['pos']
            if i['pos'] != '0':
                acc_okex['lever'] = i['lever']
                log(logfilename,'Read the leverage of the short account via API:'+str(i['lever']))
            

    api.set_acc(json.dumps(acc_okex))
    log(logfilename,'Write local account information:'+str(acc_okex))
    last = float(select_last())
    log(logfilename,'Reading current price:'+str(last))

    max_sz = int(float(acc_okex['ccy']) * float(acc_okex['lever']) / last * 100)
    log(logfilename,'Maximum transaction volume:'+str(max_sz))

    sz_r = max_sz / 20
    log(logfilename,'Trading volume coefficient:'+str(sz_r))

    pos_api_id = int(btcusdt_api['id'])
    pos_api_posSide = btcusdt_api['posside']
    pos_api_side = btcusdt_api['side']
    pos_api_sz = int(int(btcusdt_api['sz']) * sz_r)
    pos_api_uptime = int(btcusdt_api['uptime'])
    pos_api_long = int(int(pos_api['long']) * sz_r)
    pos_api_short = int(int(pos_api['short']) * sz_r)

    log(logfilename,'pos_api_long:'+str(pos_api_long)+',pos_api_short:'+str(pos_api_short)+',pos_api_sz:'+str(pos_api_sz))
    log(logfilename,'Local position informationpos_okex:'+str(pos_okex))


    try:
        pos_log_done = int(api.pos_log_done())
    except:
        pos_log_done = api.pos_log_done()
    
    log(logfilename,'pos_log_done:'+str(pos_log_done))

    log(logfilename,'========================[End of obtaining basic information]========================')
    log(logfilename,'========================[markTask Start]========================')
    log(logfilename,'Check whether pos_log_done_id is of type int:'+str(type(pos_log_done)))
    if isinstance(pos_log_done,int):
        log(logfilename,'pos_log_done_idIs of type int, check pos_log_done_id andpos_log_id,pos_api_id:'+str(pos_api_id)+',pos_log_done:'+str(pos_log_done))
        if pos_api_id > pos_log_done:
            log(logfilename,'APIIf the pos_log_id is greater than pos_log_done_id, determine whether the API update time is within 10 seconds.,nowtime:'+str(nowtime)+',pos_api_uptime:'+str(pos_api_uptime))
            if nowtime < (pos_api_uptime + 13):
                log(logfilename,'apiUpdate time within 10 seconds, determine the API trading direction,pos_api_posSide'+str(pos_api_posSide)+',pos_api_side:'+str(pos_api_side))
                if pos_api_posSide == 'long' and pos_api_side == 'buy':
                    log(logfilename,'apiTrade direction: long-buy, determine whether the current position information is consistent with the API')
                    if int(pos_okex['long']) + int(pos_api_sz) == int(pos_api_long):
                        log(logfilename,'The current position information is consistent with the API, execute the transaction, current position: '+str(pos_okex['long'])+', API position: '+str(pos_api_long)+', API transaction number:'+str(pos_api_sz))
                        trade_ok = trade(pos_api_side,pos_api_posSide,pos_api_sz,pos_api_id)
                        log(logfilename,'Execution Result:'+str(trade_ok))
                    elif int(pos_okex['long']) + int(pos_api_sz) < int(pos_api_long):
                        log(logfilename,'The current position information is consistent with the API, execute the transaction, current position: '+str(pos_okex['long'])+', API position: '+str(pos_api_long)+', API transaction number:'+str(pos_api_sz))
                        trade_ok = trade(pos_api_side,pos_api_posSide,pos_api_sz,pos_api_id)
                        log(logfilename,'Execution Result:'+str(trade_ok))
                    else:
                        log(logfilename,'longThe position information is inconsistent. Please close the long position manually before performing automatic trading. Current position: '+str(pos_okex['long'])+', API position: '+str(pos_api_long)+', API transaction quantity:'+str(pos_api_sz))

                elif pos_api_posSide == 'long' and pos_api_side == 'sell':
                    log(logfilename,'apiTrading direction: long-sell, check if it meets the closing conditions')
                    if int(pos_okex['long']) > 0:
                        log(logfilename,'Meets the closing conditions, current position: '+str(pos_okex['long'])+', API position: '+str(pos_api_short)+', API transaction quantity:'+str(pos_api_sz))
                        trade_ok = trade(pos_api_side,pos_api_posSide,int(pos_okex['long']),pos_api_id)
                        log(logfilename,'Execution Result:'+str(trade_ok))
                    else:
                        log(logfilename,'longThe position information is inconsistent. Please close the long position manually before performing automatic trading. Current position: '+str(pos_okex['long'])+', API position: '+str(pos_api_short)+', API transaction quantity:'+str(pos_api_sz))

                elif pos_api_posSide == 'short' and pos_api_side == 'sell':
                    log(logfilename,'apiTransaction direction: short-sell, determine whether the current position information is consistent with the API')
                    if int(pos_okex['short']) + int(pos_api_sz) == int(pos_api_short):
                        log(logfilename,'Meet the conditions for opening a position, execute the transaction, current position: '+str(pos_okex['short'])+', API position: '+str(pos_api_short)+', number of API transactions:'+str(pos_api_sz))
                        trade_ok = trade(pos_api_side,pos_api_posSide,pos_api_sz,pos_api_id)
                        log(logfilename,'Execution Result:'+str(trade_ok))
                    elif int(pos_okex['short']) + int(pos_api_sz) < int(pos_api_short):
                        log(logfilename,'Meet the conditions for opening a position, execute the transaction, current position: '+str(pos_okex['short'])+', API position: '+str(pos_api_short)+', number of API transactions:'+str(pos_api_sz))
                        trade_ok = trade(pos_api_side,pos_api_posSide,pos_api_sz,pos_api_id)
                        log(logfilename,'Execution Result:'+str(trade_ok))
                    else:
                        log(logfilename,'shortThe position information is inconsistent. Please close the short position manually before performing automatic trading. Current position: '+str(pos_okex['short'])+', API position: '+str(pos_api_short)+', API transaction quantity:'+str(pos_api_sz))

                elif pos_api_posSide == 'short' and pos_api_side == 'buy':
                    log(logfilename,'apiTrading direction: short-buy, check if it meets the closing conditions')
                    if int(pos_okex['short']) > 0:
                        log(logfilename,'Meets the closing conditions, current position: '+str(pos_okex['short'])+', API position: '+str(pos_api_short)+', API transaction quantity:'+str(pos_api_sz))
                        trade_ok = trade(pos_api_side,pos_api_posSide,pos_okex['short'],pos_api_id)
                        log(logfilename,'Execution Result:'+str(trade_ok))
                    else:
                        log(logfilename,'shortThe position information is inconsistent. Please close the short position manually before performing automatic trading. Current position: '+str(pos_okex['short'])+', API position: '+str(pos_api_short)+', API transaction quantity:'+str(pos_api_sz))
            else:
                log(logfilename,'apiIf the update time exceeds 10 seconds, the best trading time has been missed.,nowtime:'+str(nowtime)+',pos_api_uptime:'+str(pos_api_uptime))
        else:
            log(logfilename,'APIThe pos_log_id is not greater than pos_log_done_id, there is no new data in the API, and monitoring continues.,pos_api_id:'+str(pos_api_id)+',pos_log_done:'+str(pos_log_done))
    else:
        log(logfilename,'pos_log_done_idNot of int type')
        api.set_pos_log_done(pos_api_id)
    log(logfilename,'========================[markTask End]========================')

```

> Detail

https://www.fmz.com/strategy/321120

> Last Modified

2021-10-03 09:32:41
