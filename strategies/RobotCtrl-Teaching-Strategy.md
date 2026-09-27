
> Name

RobotCtrl-Teaching-Strategy

> Author

发明者量化-小小梦

> Strategy Description

Related articles:https://www.fmz.com/digest-topic/5011

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|strRobotParams|["175708,14:55:33-15:10:33"]|Robot Timing Parameters|
|isPushMsg|false|Whether to Push to WeChat|
|accessKey|$$$__enc__$$$|FMZPlatform Extension APIACCESS KEY|
|secretKey|$$$__enc__$$$|FMZPlatform Extension APISECRET KEY|


> Source (python)

``` python
# -*- coding: utf-8 -*-
import time
import json

try:
    import md5
    import urllib2
    from urllib import urlencode
except:
    import hashlib as md5
    import urllib.request as urllib2
    from urllib.parse import urlencode

def api(method, *args):
    d = {
        'version': '1.0',
        'access_key': accessKey,
        'method': method,
        'args': json.dumps(list(args)),
        'nonce': int(time.time() * 1000),
        }

    d['sign'] = md5.md5(('%s|%s|%s|%d|%s' % (d['version'], d['method'], d['args'], d['nonce'], secretKey)).encode('utf-8')).hexdigest()
    return json.loads(urllib2.urlopen('https://www.fmz.com/api/v1', urlencode(d).encode('utf-8')).read().decode('utf-8'))

RobotParams = json.loads(strRobotParams)

def main():
    global RobotParams 
    arrParams = []
    nowDay = 0
    strPush = ""
    if isPushMsg:
        strPush = "@"

    for i in range(len(RobotParams)):
        param = {}
        arr = RobotParams[i].split(",")
        if len(arr) != 2:
            raise Exception("String configuration error: delimiter,")
        param["id"] = arr[0]
        param["isProcessOpenThisDay"] = False
        param["isProcessCloseThisDay"] = False

        arr = arr[1].split("-")
        if len(arr) != 2:
            raise Exception("String configuration error: delimiter-")

        begin = arr[0]
        arrBegin = begin.split(":")
        if len(arrBegin) != 3:
            raise Exception("String configuration error: start time delimiter:")
        
        param["begin"] = {}
        param["begin"]["hour"] = float(arrBegin[0])
        param["begin"]["min"] = float(arrBegin[1])
        param["begin"]["sec"] = float(arrBegin[2])

        end = arr[1]
        arrEnd = end.split(":")
        if len(arrEnd) != 3:
            raise Exception("String configuration error: end time delimiter:")            
        
        param["end"] = {}
        param["end"]["hour"] = float(arrEnd[0])
        param["end"]["min"] = float(arrEnd[1])
        param["end"]["sec"] = float(arrEnd[2])
        arrParams.append(param)

    # Test
    Log("Output Parameters", arrParams, "#FF0000")  

    while True:
        nowTime = time.localtime(time.time())
        nowHour = nowTime.tm_hour 
        nowMin = nowTime.tm_min
        nowSec = nowTime.tm_sec
        
        tbl = {
            "type" : "table", 
            "title" : "msg", 
            "cols" : ["id", "begin", "end", "Was a Start Executed Today, Was a Stop Executed Today"],
            "rows" : []
        }

        for i in range(len(arrParams)):
            tbl["rows"].append([arrParams[i]["id"], json.dumps(arrParams[i]["begin"]), json.dumps(arrParams[i]["end"]), arrParams[i]["isProcessOpenThisDay"], arrParams[i]["isProcessCloseThisDay"]])
            if nowDay != nowTime.tm_mday:
                arrParams[i]["isProcessOpenThisDay"] = False
                arrParams[i]["isProcessCloseThisDay"] = False

            if arrParams[i]["isProcessOpenThisDay"] == False:
                if nowTime.tm_hour == arrParams[i]["begin"]["hour"] and nowTime.tm_min >= arrParams[i]["begin"]["min"] and nowTime.tm_sec >= arrParams[i]["begin"]["sec"]:
                    ret = api('RestartRobot', int(arrParams[i]["id"]))                    
                    arrParams[i]["isProcessOpenThisDay"] = True
                    Log("robotID:", arrParams[i]["id"], "Execution started, please log in to the platform to check if it started successfully", "ExtendAPIReturn value:", ret, strPush)

            if arrParams[i]["isProcessCloseThisDay"] == False:
                if nowTime.tm_hour == arrParams[i]["end"]["hour"] and nowTime.tm_min >= arrParams[i]["end"]["min"] and nowTime.tm_sec >= arrParams[i]["end"]["sec"]:
                    ret = api('StopRobot', int(arrParams[i]["id"]))
                    arrParams[i]["isProcessCloseThisDay"] = True
                    Log("robotID:", arrParams[i]["id"], "Execution stopped, please log in to the platform to check if it stopped successfully", "ExtendAPIReturn value:", ret, strPush)
        
        if nowDay != nowTime.tm_mday:
            nowDay = nowTime.tm_mday

        LogStatus(_D(), nowTime, "\n`" + json.dumps(tbl) + "`")
        Sleep(500)

```

> Detail

https://www.fmz.com/strategy/184600

> Last Modified

2020-05-08 10:47:52
