
> Name

Test-Real-Network-Latency-Between-Hosts-and-Exchange-Servers-Supports-Testing-Multiple-Exchanges-Simultaneously

> Author

Xueqiu Bot

> Strategy Description

Contact : ck@xueqiubot.com / WeChat@stay37
This strategy is to test the real network delay between the host and the server. The test method is: compare the time of sending the request and the time of receiving the result, and take the average multiple times. 
Supports simultaneous testing of multiple exchanges. Just add different trading platforms, but the numpy module needs to be installed.



> Source (python)

``` python
# Contact : ck@xueqiubot.com / WeChat@stay37

import time
import numpy as np


def test():
    #Delayed data receiver
    delay_list = []
    for i in range(len(exchanges)):
        delay_list.append([])
    while True:
        #Delayed data acquisition
        for i in range(len(exchanges)):
            send_t = time.time()
            ticker = exchanges[i].GetTicker()
            delay_list[i].append(round((time.time() - send_t) * 1000 , 2))
        #Data Output 
        delay_table = {"type":'table',"title":'Latency Data',"cols": ['Account Serial Number','Latest Delay','Average Latency','Number of Tests Completed.''],"rows":[]}
        for i in range(len(delay_list)):
            delay_table['rows'].append([i + 1, str(delay_list[i][-1])+' ms', str(round(np.mean(delay_list[i]) , 2)) + ' ms', len(delay_list[i])])
        LogStatus("Output delay is: send onceget_tickerThe real time from request to data retrieval" + "\n" + "`" + json.dumps(delay_table) + "`")
        time.sleep(0.05)

                
def main():
    for i in range(len(exchanges)):
        exchanges[i].SetContractType('swap')
    test()
                

```

> Detail

https://www.fmz.com/strategy/236426

> Last Modified

2021-01-10 19:22:52
