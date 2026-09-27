
> Name

Test-Strategy-Interface-Parameters

> Author

发明者量化-小小梦

> Strategy Description

This strategy is used to test the interface parameter functions in the Inventor Quantitative Trading Platform strategy design.

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|pNum1|Note for parameter pNum1 | (? numeric parameter) Description of parameter pNum1|
|pNum2|Remarks for parameter pNum2 | Description of parameter pNum2|
|pNum3|Remarks for parameter pNum3 | Description of parameter pNum3|
|pNum4|Remarks for parameter pNum4 | Description of parameter pNum4|
|pBool1|Note for parameter pBool1 | (? Boolean parameter) Description of parameter pBool1|
|pBool2|Note for parameter pBool2, used to control whether to display the description of pNum1|Parameter pBool2|
|pStr1|Note for parameter pStr1 | (? string parameter) Description of parameter pStr1|
|pStr2|Remarks for parameter pStr2 | Description of parameter pStr2|
|pStr3|Remarks for parameter pStr3 | Description of parameter pStr3|
|pStr4|Remarks for parameter pStr4 | Description of parameter pStr4|
|pCombox1|Remarks on parameter pCombox1 | (? Drop-down box type) Description of parameter pCombox1|
|pCombox2|Remark for parameter pCombox2 | Description for parameter pCombox2|
|pCombox3|Remark for parameter pCombox3 | Description for parameter pCombox3|
|pSecretStr1|Note for parameter pSecretStr1 | (?type of encryption string) description of parameter pSecretStr1|


> Source (javascript)

``` javascript
/*backtest
start: 2023-06-21 00:00:00
end: 2024-06-26 00:00:00
period: 1d
basePeriod: 1h
exchanges: [{"eid":"Futures_OKX","currency":"BTC_USD"}]
*/

function main() {
    Log("---------------------------Start testing numeric parameters---------------------------")
    Log("VariablespNum1:", pNum1, ", Variable value type:", typeof(pNum1))
    Log("VariablespNum2:", pNum2, ", Variable value type:", typeof(pNum2))
    Log("VariablespNum3:", pNum3, ", Variable value type:", typeof(pNum3))
    Log("VariablespNum4:", pNum4, ", Variable value type:", typeof(pNum4))
    
    Log("---------------------------Start testing boolean parameters---------------------------")
    Log("VariablespBool1:", pBool1, ", Variable value type:", typeof(pBool1))
    Log("VariablespBool2:", pBool2, ", Variable value type:", typeof(pBool2))

    Log("---------------------------Start testing string type parameters---------------------------")
    Log("VariablespStr1:", pStr1, ", Variable value type:", typeof(pStr1))
    Log("VariablespStr2:", pStr2, ", Variable value type:", typeof(pStr2))
    Log("VariablespStr3:", pStr3, ", Variable value type:", typeof(pStr3))
    Log("VariablespStr4:", pStr4, ", Variable value type:", typeof(pStr4))

    Log("---------------------------Start testing dropdown type parameters---------------------------")
    Log("VariablespCombox1:", pCombox1, ", Variable value type:", typeof(pCombox1))
    Log("VariablespCombox2:", pCombox2, ", Variable value type:", typeof(pCombox2))
    Log("VariablespCombox3:", pCombox3, ", Variable value type:", typeof(pCombox3))

    Log("---------------------------Start testing encrypted string type parameters---------------------------")
    Log("VariablespSecretStr1:", pSecretStr1, ", Variable value type:", typeof(pSecretStr1))
}
```

> Detail

https://www.fmz.com/strategy/455212

> Last Modified

2024-06-27 15:05:19
