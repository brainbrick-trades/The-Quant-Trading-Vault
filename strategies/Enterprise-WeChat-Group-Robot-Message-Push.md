
> Name

Enterprise-WeChat-Group-Robot-Message-Push

> Author

BTC[策略代写]团队



> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|webhook|https://...|webhook|


> Source (python)

``` python
#!Python3

"""
"Strategy writing » and (this program helps), write toQQ:35787501

Enterprise WeChat message push, used for group custom bots
Similarly: modify the data, and you can also access other software webhook
"""

import requests


def send(text):
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "msgtype": "text",
        "text": {
            "content": text,
        }
    }
    response = requests.post(webhook, headers=headers, json=data)
    records = response.json()
    return records


def LogQYWX(*args):
    text = " ".join(args)
    Log(text, send(text))


ext.LogQYWX = LogQYWX

```

> Detail

https://www.fmz.com/strategy/430810

> Last Modified

2023-11-02 10:14:01
