
> Name

Share-Template-Reference-Error-Tracking

> Author

leviyuan

> Strategy Description

Usage method: First, reference this template class library
Add in each script file $.fileLineMark("main", 35)  First parameter: file name Second parameter: line number of this line of code in the file
And ensure that this line of code is executed before tracking errors
Finally add to strategy code  main = $.tryfunc(main)  To ensure that all calls passtry

When a policy error occurs, a red line will automatically indicate which file and which line it is in

Principle: The way to host js code is to merge all js codes, including class libraries, into one large file for loading; find out the position of each file in the large file, and when the error is finally reported, reverse the correspondence to know the specific line number of the error.

 ![IMG](https://www.fmz.com/upload/asset/443a3c3f50e09c3ca4be.png) 



> Source (javascript)

``` javascript
var fileStartLine = []
$.fileLineMark = function(file, line) {
    try{a=a+1}catch(ex){
        var markline = parseInt(ex.stack.split('\n')[3].split('(__FILE__:')[1].split(')')[0])
        fileStartLine.push([file, markline-line])
        fileStartLine.sort(function(a, b){
            return b[1] - a[1]
        })
    }
}

$.tryfunc = function(func) {
    return function(a,b,c,d,e,f,g,h,i,j,k,l,m,n) {
        try {
            return func(a,b,c,d,e,f,g,h,i,j,k,l,m,n)
        } catch(ex) {
            if (ex.message == "execution timeout") {
                Log("Ignore robot stop command")
                throw ex
                return
            }

            var line = parseInt(ex.stack.split('\n')[2].split('(__FILE__:')[1].split(')')[0])
            for (var ii = 0; ii < fileStartLine.length; ii++) {
                if (line > fileStartLine[ii][1]) {
                    Log("catch error at " + fileStartLine[ii][0] + ":" + (line-fileStartLine[ii][1])+"#ff0000")
                    break
                }
            }

            throw ex
        }
    }
}

function onTick() {

}

function main() {
    $.fileLineMark("main", 41)
    onTick = $.tryfunc(onTick)
    
    while(true){
        onTick()
        Sleep(1000)
    }
}

```

> Detail

https://www.fmz.com/strategy/182793

> Last Modified

2020-01-28 21:11:06
