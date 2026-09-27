
> Name

FMZ-Real-Offer-Robot-Automatically-Detects-and-Restarts-Program-WeChat-Push

> Author

eason04

> Strategy Description

**FMZLive trading robot automatically detects and restarts the program (WeChat push notifications))**
 ![IMG](https://www.fmz.com/upload/asset/27d06163dac4df7fe8520.png) 
 Fill in the API and application you applied for on the FMZ platform hereAPIkey
 ![IMG](https://www.fmz.com/upload/asset/27cef09a09fbccac93116.png) 
 Variable tokens are used to send WeChat push notifications. Here is how to apply
 Open the website: https://www.pushplus.plus/ Log in with your own WeChat and follow the official account (not advertising)
 ![IMG](https://www.fmz.com/upload/asset/27d5d579fa87c8f486136.png) 
 Click one-on-one message
 ![IMG](https://www.fmz.com/upload/asset/27d526d1a1f71b1e4fc15.png) 
 Copy the token and fill it into the token variable
 ![IMG](https://www.fmz.com/upload/asset/27dd43d36cf1e78165bc7.png) 
 robotIdFill in the variable with the number of the real trading robot you want to monitor (in list form))
 ![IMG](https://www.fmz.com/upload/asset/27e6ff0ca668d74343caf.png) 
 The real offer robot number can be obtained from the website by opening the real offer in the FMZ web version.
 
**The code can be run directly locally,
However, you need to keep the computer on all the time,
can also be run on your own server,
Running on the server requires installing third-party libraries in advance**




> Source (python)

``` python
'''
The code can be run directly locally,
However, the computer needs to be kept on continuously, or it can be run on your own server
'''

import time
import json
import ssl
import requests
ssl._create_default_https_context = ssl._create_unverified_context

try:
    import md5
    import urllib2
    from urllib import urlencode
except:
    import hashlib as md5
    import urllib.request as urllib2
    from urllib.parse import urlencode

accessKey = '48xxxxxxxxxxxxxxxxxxxxxxxxxxxxde'
secretKey = '91xxxxxxxxxxxxxxxxxxxxxxxxxxxx84'

def api(method, *args):
    d = {
        'version': '1.0',
        'access_key': accessKey,
        'method': method,
        'args': json.dumps(list(args)),
        'nonce': int(time.time() * 1000),
        }

    d['sign'] = md5.md5(('%s|%s|%s|%d|%s' % (d['version'], d['method'], d['args'], d['nonce'], secretKey)).encode('utf-8')).hexdigest()
    # Note: urllib2.urlopen function, timeout problem, you can set the timeout, urllib2.urlopen('https://www.fmz.com/api/v1', urlencode(d).encode('utf-8'), timeout=10) sets the timeout to 10 seconds
    return json.loads(urllib2.urlopen('https://www.fmz.com/api/v1', urlencode(d).encode('utf-8')).read().decode('utf-8'))

def send_wechat(msg):
    token = '93xxxxxxxxxxxxxxxxxxxxxxxxxxxx57'  # Copied to the previous onetoken
    title = '[Waring] Strategy Information'
    content = msg
    template = 'html'
    url = f"https://www.pushplus.plus/send?token={token}&title={title}&content={content}&template={template}"
    #print(url)
    r = requests.get(url=url)
    print(json.loads(r.text)['msg'])

robotId = [xxx,xxx,xxx]    #The robot code that needs to be monitored


while True:
    for j in range(len(robotId)):
        detail = api('GetRobotDetail', robotId[j])
        if detail['data']['result']['robot']['status'] == 1 and detail['data']['result']['robot']['wd'] == 1:
            print(f"The status of real disk {robotId[j]} is normal status = {detail['data']['result']['robot']['status']}, real disk monitoring has been turned on wd = {detail['data']['result']['robot']['wd']}")
            pass
        elif detail['data']['result']['robot']['status'] == 1 :
            print(f"The real disk {robotId[j]} status is normal status = {detail['data']['result']['robot']['status']}, the real disk monitoring is not turned on wd = {detail['data']['result']['robot']['wd']}")
            pass
        else:
            print(f"Live trading {robotId[j]} status abnormal status = {detail['data']['result']['robot']['status']}")
            #Attempt to restart the live account Number of attempts = 4    Every5s Try Once
            status = False
            for i in range(4):
                api('RestartRobot', robotId[j])
                robotDetail = api('GetRobotDetail', robotId[j])
                print(f"Try restarting the live {robotId[j]} for {i+1} time")
                if robotDetail['data']['result']['robot']['status'] == 1 :
                    mess = api('GetRobotLogs',robotId[j],0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
                    print(f"Live trading {robotId[j]} restart completed status = {api('GetRobotDetail', robotId[j])['data']['result']['robot']['status']}\n"
                          f"Return error message1:{mess['data']['result']['logs'][0]['Arr'][0][6]}\n"
                          f"Return error message2:{mess['data']['result']['logs'][0]['Arr'][1][6]}\n")
                    send_wechat(f"Live trading {robotId[j]} restart completed status = {api('GetRobotDetail', robotId[j])['data']['result']['robot']['status']}\n"
                                f"Return error message1:{mess['data']['result']['logs'][0]['Arr'][0][6]}\n"
                                f"Return error message2:{mess['data']['result']['logs'][0]['Arr'][1][6]}\n")
                    status = True
                    break
                else:
                    print(f"{i+1}th restart failed!!")
                time.sleep(5)
            if status == False :
                print(f"Four attempts to restart the live disk {robotId[j]} failed, sending a warning message!!")
                send_wechat(f"Attempts to restart the real disk {robotId[j]} 4 times failed, please check in time! ! \nAttempts to restart the real disk {robotId[j]} 4 times failed, please check in time! ! \nAttempts to restart the real disk {robotId[j]} 4 times failed, please check in time!!\n")
    time.sleep(60*10)

```

> Detail

https://www.fmz.com/strategy/383695

> Last Modified

2022-09-22 18:27:23
