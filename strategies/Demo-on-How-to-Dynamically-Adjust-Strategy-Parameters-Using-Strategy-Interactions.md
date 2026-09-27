
> Name

Demo-on-How-to-Dynamically-Adjust-Strategy-Parameters-Using-Strategy-Interactions

> Author

momox

> Strategy Description

The strategy requires constant testing and adjustment, and the parameters are often changed. Stopping and restarting every time is laborious and laborious, and the original profit progress will be lost (although it can also be restored through global parameters). In fact, botvs has provided a way to dynamically adjust parameters-"Strategy Interaction""

> Strategy Arguments





|Button|Default|Description|
|----|----|----|
|A3|999|AAAParameters of|
|B3|Botvs|BBBParameters of|


> Source (javascript)

``` javascript
var Interval=2000;

//AAA,BBBParameters in the strategy that are intended to be dynamically adjusted
var AAA=0;
var BBB="hello world";

function main() {
    while(true){
        onTick();
        Sleep(Interval);
    }
}

function onTick(){
    set_command();
    Log("AAA="+AAA,"       BBB="+BBB);
}

//Obtain dynamic parameters (strategy interaction content))
 function set_command() {

     var get_command = GetCommand();//  GetCommandThe method is to get parameters, the obtained parameters are in string format, format is "Parameter Name:Parameter Value" SeeBotVS APIDocumentation
     if (get_command != null) {
         if (get_command.indexOf("A3:") == 0) {  //If the incoming parameter is namedA3(with"A3:"Leading, indicatingA3Parameters)

             AAA = (get_command.replace("A3:", "")); //Assign to the value in the strategyAAA(Replace the leading string with empty, and the remaining is our parameter value)

             Log("AAABecome:" + AAA);
         }
         
          if (get_command.indexOf("B3:") == 0) {  //If the incoming parameter is namedB3(with"B3:"Leading, indicatingB3Parameters)

             BBB = (get_command.replace("B3:", "")); //Assign to the value in the strategyBBB(Replace the leading string with empty, and the remaining is our parameter value)

             Log("BBBBecome:" + BBB);
         }

     }
 }
```

> Detail

https://www.fmz.com/strategy/8379

> Last Modified

2016-01-09 21:18:07
