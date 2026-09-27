
> Name

Telegram-Mail-Interface-V200-Python

> Author

FawkesPan

> Strategy Description

# Telegram APIInterface (FMZ.com)

##### This Library Can Only Send Messages via Telegram for Now, More Features Will Be Added Later.

### Initialize
```
# key is Bot key
## To obtain Bot key, please refer to https://www.ccino.org/create-a-telegram-bot.html
# chat_id For receiving usersTelegram ID
## Telegram ID It can be obtained through the @dwx_aibot robot. After connecting to this robot, send /getid to obtain it. ChatID
Telegram = ext.Telegram(key=string, chat_id=integer)    # Create a new interface object
```
### Send mail
```
# chat_id Optional, by default will use the settings at initializationChatID
# message Is the information content
Telegram.Send(message=string, chat_id=integer)
```
### Notes
Before you can send messages to yourself, you need to send a /start message to your robot in Telegram, otherwise the robot will not be able to send you messages.
### Contact me
Email i@fawkex.me
Telegram [FawkesPan](https://telegram.me/FawkesPan)

Accept policy customization

### About this library
[Telegram APIDocumentation](https://core.telegram.org/bots/api)

[Use WTFPL – Do What the Fuck You Want to Public License](http://www.wtfpl.net/)

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|DEBUG|0|DEBUGMode: 0|1|
|KEY||Telegram robot Key|
|CHATID|false|Telegram session ID|


> Source (python)

``` python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# encoding: utf-8
# 
# Telegram Interface for FMZ.com
#
# Copyright 2018 FawkesPan
# Contact : i@fawkex.me / Telegram@FawkesPan
#
# Do What the Fuck You Want To Public License
#

try:
    import requests
except:
    print('Requests not installed. Try: pip install requests')
    Log('Requests not installed. Try: pip install requests')
    
    raise Exception('Requests not installed. Try: pip install requests')

class Telegram:
    def __init__(self):
        self.key = KEY
        self.chat_id = CHATID
        self.url = 'https://api.telegram.org/bot%s' % self.key
        
    def Send(self, message='', chat_id=None):
        if chat_id is None:
            chat_id = self.chat_id
        PARAM = {}
        PARAM['chat_id'] = chat_id
        PARAM['text'] = message
        PARAM['parse_mode'] = 'markdown'
        URL = self.url + '/sendMessage'
        try:
            res = requests.post(URL, data = PARAM)
            return True
        except IOError as e:
            print(e)
            return False
        

ext.Telegram = Telegram

# Module Function Test
def main():
    if DEBUG == 1:
        msger = ext.Telegram(KEY, CHATID)
        msger.Send("Hello World!")
    
    return True
```

> Detail

https://www.fmz.com/strategy/116201

> Last Modified

2019-05-16 20:06:03
