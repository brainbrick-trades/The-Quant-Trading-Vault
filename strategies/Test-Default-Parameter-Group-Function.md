
> Name

Test-Default-Parameter-Group-Function

> Author

发明者量化-小小梦

> Strategy Description

### How to use code to precisely adjust the 'backtesting system default settings'"

> In the parameter testing of strategies, backtesting in different time periods, backtesting on multiple underlying objects, etc., the parameters need to be adjusted repeatedly when backtesting the strategy, and cannot be recorded, so they need to be reset the next time backtesting. In order to facilitate parameter adjustment, the platform has added a new function - precise adjustment of "backtest system default settings using code"".

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|number|9999|Numeric type|
|bool|true|Boolean Type|
|string|Hello World!|String type|
|comboBox|0|Dropdown menu: combo1|combo2|combo3|


> Source (javascript)

``` javascript
/*backtest
start: 2017-03-01        
end: 2017-03-02           
period: 15              
mode: 1                 
*/

/*defaults
number : 0
bool: false
string: Hello BotVS!
comboBox : 2
*/

function main(){
    while(true){
        LogStatus("Test default parameters!");
        Sleep(1000);
    }
}
```

> Detail

https://www.fmz.com/strategy/40155

> Last Modified

2021-07-02 16:33:15
