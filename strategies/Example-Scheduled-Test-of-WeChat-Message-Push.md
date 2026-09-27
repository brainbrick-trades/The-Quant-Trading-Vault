
> Name

Example-Scheduled-Test-of-WeChat-Message-Push

> Author

发明者量化-小小梦

> Strategy Description

Regular test of WeChat message push example ~ To provide reference for users to learn from.



> Source (javascript)

``` javascript
function main(){
    var initTime = (new Date()).getTime() ;
    Log("Program Start Time:",$.getTimeByNormal(initTime) );
    var preDif = 0;
    var str = "";
    while(true){
        var nowTime = (new Date()).getTime();
        if(  Math.floor((nowTime - initTime) / (1000*60*10) ) !== preDif ){
            str = $.getTimeByNormal(nowTime);
            Log("Time elapsed since the program started executing10Minutes! Reminder."+"--Current Time:"+str+"Push WeChat@" );
            preDif = Math.floor((nowTime - initTime) / (1000*60*10) ) ;
        }
        Sleep(2000); 
    }
}
```

> Detail

https://www.fmz.com/strategy/15098

> Last Modified

2017-01-04 12:00:55
