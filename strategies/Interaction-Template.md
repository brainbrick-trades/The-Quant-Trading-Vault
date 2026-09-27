
> Name

Interaction-Template

> Author

发明者量化-小小梦

> Strategy Description

- Test Code

  ```
  // Test Code
  function main() {
      $.BindingFunc("test1", function(cmd, param){                     // Bind control name to test1 button,function(cmd, param){...} For the response function of this button, the first parameter of the response function is the name of the control that triggers the response function.:test1
          var ticker = exchange.GetTicker()                            // The second param Parameters are parameters that are attached when the control is clicked (numeric types, string types, Boolean types, and drop-down boxes all have attached parameters, but button types do not have attached parameters.)
          Log("Control:", cmd, "ticker:", ticker, " Parameters:", param)
      })
      $.BindingFunc("test3", function(cmd, param){                     // Binding test3 ...
          var account = exchange.GetAccount()
          Log("account:", account, "cmd:", cmd, "param:", param)
      })
      $.BindingFunc("test5", function(){                               // Binding test5 ... 
          Log(exchange.GetName())
      })
      while(1){
          $.GetCommand()                                               // Detect interactive commands in the main loop.
          Sleep(2000)
      }
  }
  ```

- Interface function

  - Bind control response function
    $.BindingFunc(cmdControlName, function(cmd, param){...})

  - Interaction detection function
    Replaces the platform API GetCommand() function
    $.GetCommand()                                        
    
- Test code configured control screenshot
  ![IMG](https://www.fmz.com/upload/asset/166da027c40813fe1311.png)

- If you have any questions, feel free to ask or leave a comment.



> Source (javascript)

``` javascript
var _CmdMap = {}

$.BindingFunc = function(cmdName, cmdFunc) {
    _CmdMap[cmdName] = cmdFunc
}

$.GetCommand = function() {
    var cmd = GetCommand()
    if(cmd) {
        strArr = cmd.split(":")
        func = _CmdMap[strArr[0]]
        if(strArr.length == 1) {
            // Call the corresponding command response function
            if(func) {
                func(strArr[0])
            }
        } else if(strArr.length == 2) {
            // Call the corresponding command response function
            if(func) {
                func(strArr[0], strArr[1])
            }
        } else {
            var param = strArr[1]
            for(var i = 2; i < strArr.length; i++) {
                param += (":" + strArr[i])
            }
            
            // Call the corresponding command response function
            if(func) {
                func(strArr[0], param)
            }
        }
        if(!func) {
            Log(strArr[0], "This command has no registered response function.", "#FF0000")
        }
    }
}

// Test Code
function main() {
    $.BindingFunc("test1", function(cmd, param){                     // Bind control name to test1 button,function(cmd, param){...} For the response function of this button, the first parameter of the response function is the name of the control that triggers the response function.:test1
        var ticker = exchange.GetTicker()                            // The second param Parameters are parameters that are attached when the control is clicked (numeric types, string types, Boolean types, and drop-down boxes all have attached parameters, but button types do not have attached parameters.)
        Log("Control:", cmd, "ticker:", ticker, " Parameters:", param)
    })
    $.BindingFunc("test3", function(cmd, param){                     // Binding test3 ...
        var account = exchange.GetAccount()
        Log("account:", account, "cmd:", cmd, "param:", param)
    })
    $.BindingFunc("test5", function(){                               // Binding test5 ... 
        Log(exchange.GetName())
    })
    while(1){
        $.GetCommand()                                               // Detect interactive commands in the main loop.
        Sleep(2000)
    }
}
```

> Detail

https://www.fmz.com/strategy/137403

> Last Modified

2019-02-15 11:49:52
