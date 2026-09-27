
> Name

Websocket-Vs-Rest

> Author

momox

> Strategy Description

websocket Speed test of API and REST API, supports adding multiple exchanges for testing. Note that it will temporarily increase your API call frequency, please run it only if it does not affect the operation of other bots. If the error "Futures_OP 4: argument error" occurs, please update to the latest custodian program. 
Special reminder: You can only add exchanges that support the websocket interface (a bit nonsense, it does not support the websocket interface, how can you measure the speed), otherwise you will make mistakes. Currently, Huobi provides the websocket interface, but BTCC does not. For other information, please consult the relevant exchange API introduction or help



> Source (javascript)

``` javascript


var Interval=1000;

function _N(v, precision) {



    if (typeof (precision) != 'number') {



        precision = 4;



    }



    var d = parseFloat(v.toFixed(Math.max(10, precision + 5)));



    s = d.toString().split(".");



    if (s.length < 2 || s[1].length <= precision) {



        return	d;



    }


    var b = Math.pow(10, precision);



    return	Math.floor(d * b) / b;



}




function onexit() {
   
    Log("[[[System exit]]]");
} 


function main() {

   

	var start=Date.now();
   
    

 for (var i = 0; i < exchanges.length; i++) {


    var ecg=exchanges[i];
    //Log(ecg);
   
    ecg.IO("rest");//rest Mode
    var iii=0;
    var sum=0;
    while (iii<=10) {  //Continuous calls10Times, take the average
       
        var account = null;
        start=Date.now();       
        account = ecg.GetAccount();  //Test executionAPIfunction, can be modified as needed, such as GetTick
        iii=iii+1;
        if(account){
            var delay=(Date.now()-start);
            sum=sum+delay;            
             
        }




        Sleep(1000);
    
    }
     Log("Average milliseconds["+_N(sum/iii,2)+"]"+ecg.GetName()+" rest"); 
     
     ecg.IO("websocket"); //websocket Mode
    sum=0;
    iii=0;
    while (iii<=10) {  //Continuous calls10Times, take the average
       
        var account = null;
        start=Date.now();       
        account = ecg.GetAccount();  //Test executionAPIfunction, can be modified as needed, such as GetTick
        iii=iii+1;
        if(account){
            var delay=(Date.now()-start);
            sum=sum+delay;            
             
        }




        Sleep(1000); 
    
    }
     Log("Average milliseconds["+_N(sum/iii,2)+"]"+ecg.GetName()+" websocket"); 
 }
}





```

> Detail

https://www.fmz.com/strategy/7547

> Last Modified

2016-01-09 20:58:20
