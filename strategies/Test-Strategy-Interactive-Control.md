
> Name

Test-Strategy-Interactive-Control

> Author

发明者量化-小小梦

> Strategy Description

This strategy is used to test the interactive control functions in the Inventor Quantitative Trading Platform strategy design.

> Strategy Arguments





|Button|Default|Description|
|----|----|----|
|cmdNum1|Note of interactive control cmdNum1|(?Numeric Type) Description of interactive control cmdNum1|
|cmdNum2|Notes for interactive control cmdNum2 | Description for interactive control cmdNum2|
|cmdNum3|Notes for interactive control cmdNum3 | Description for interactive control cmdNum3|
|cmdBool1|Notes on the interaction control cmdBool1 | (? Boolean type) Description of the interactive control cmdBool1|
|cmdStr1|Notes on the cmdStr1 interaction control| (?string type) Description of the cmdStr1 interaction control|
|cmdStr2|Note for interactive control cmdStr2 | Description of interactive control cmdStr2|
|cmdStr3|Note for interactive control cmdStr3 | Description of interactive control cmdStr3|
|cmdStr4|Note for interactive control cmdStr4 | Description of interactive control cmdStr4|
|cmdCombox1|Note of interactive control cmdCombox1 | (? dropdown type) description of interactive control cmdCombox1.|
|cmdCombox2|Remarks on interactive control cmdCombox2|Description of interactive control cmdCombox2|
|cmdCombox3|Remarks on interactive control cmdCombox3|Description of interactive control cmdCombox3|
|cmdBtn|Notes on the cmdBtn interaction control | (? Button type) Description of the cmdBtn interactive control|


> Source (javascript)

``` javascript
function main() {
    var lastCmd = ""
    while (true) {
        var cmd = GetCommand()
        if (cmd) {
            Log(cmd)
            lastCmd = cmd
        }
        LogStatus(_D(), lastCmd)
        Sleep(500)
    }
}
```

> Detail

https://www.fmz.com/strategy/455231

> Last Modified

2024-06-27 15:06:27
