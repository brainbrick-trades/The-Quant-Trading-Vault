
> Name

Local-Storage

> Author

FawkesPan

> Strategy Description

# What?

FMZLocal storage calls simplified tool
For local storage, please visit [FMZ API Documentation]](https://www.fmz.com/api)


# What's the use?

Simplified the way FMZ local storage is called, more elegant, no need to call `_G()` anymore.

# How to use
### Import template
First copy this template to your strategy library, then check this template in the strategy where you want to use this tool.
### In Strategy Code
Create an object with the following code at the beginning of the strategy
```
PS = ext.PersistentStorage()
```
Done
This object `PS` can be used as an ordinary Python dictionary, but it can only store content that can be JSON serialized.**

# About this library
[Use WTFPL – Do What the Fuck You Want to Public License](http://www.wtfpl.net/)




> Source (python)

``` python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# encoding: utf-8
#
#  Persistent Storage for FMZ
#
# Copyright 2020 FawkesPan
# Contact : i@fawkex.me / Telegram@FawkesPan
#
#            DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE 
#                    Version 2, December 2004 
#
# Copyright (C) 2004 Sam Hocevar <sam@hocevar.net> 
#
# Everyone is permitted to copy and distribute verbatim or modified 
# copies of this license document, and changing it is allowed as long 
# as the name is changed. 
#
#            DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE 
#   TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION 
#
#  0. You just DO WHAT THE FUCK YOU WANT TO.
#

class PersistentStorage:
    
    def __init__(self):
        keys = _G('__keys__')
        if isinstance(keys, list):
            self.__keys__ = keys
        else:
            self.__keys__ = []
            self.__setitem__('__keys__', self.__keys__)
        return
    
    def _add_key(self, key):
        if key == '__keys__':
            return
        self.__keys__.append(key)
        self.__setitem__('__keys__', self.__keys__)
        return
        
    def _del_key(self, key):
        if key == '__keys__':
            return
        if key in self.__keys__:
            del self.__keys__[self.__keys__.index(key)]
        self.__setitem__('__keys__', self.__keys__)
        return
    
    def __setitem__(self, key, value):
        _G(key, value)
        self._add_key(key)
        return
    
    def __delitem__(self, key):
        _G(key, None)
        self._del_key(key)
        return
    
    def __getitem__(self, key):
        return _G(key)

    def keys(self):
        return self.__keys__
        

ext.PersistentStorage = PersistentStorage
```

> Detail

https://www.fmz.com/strategy/201253

> Last Modified

2020-04-22 19:11:31
