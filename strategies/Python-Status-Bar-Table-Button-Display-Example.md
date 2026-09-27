
> Name

Python-Status-Bar-Table-Button-Display-Example

> Author

发明者量化-小小梦





> Source (python)

``` python
import json

def main():
    tab = {
        "type" : "table", 
        "title" : "demo", 
        "cols" : ["a", "b", "c"], 
        "rows" : [["1", "2", {"type" : "button", "cmd" : "coverAll", "name" : "Close position"}]] # Configure a button on the first row and third column of the status bar table. The name is Close position
    }
    
    LogStatus("`" + json.dumps(tab) + "`")

```

> Detail

https://www.fmz.com/strategy/147155

> Last Modified

2019-05-10 11:35:13
