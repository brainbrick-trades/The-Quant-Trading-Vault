
> Name

Multi-Threaded-Batch-Tasks

> Author

一拳男孩

> Strategy Description

```
    var tasks = $.go([
        [exchange, 'GetDepth'],
        [exchange, 'GetTicker'],
    ])
    var retList = $.wait(tasks)
    Log(retList[0])
    Log(retList[1])
```

- **$.go()**
> Batch ExecutionGo
> Parameter Type Two-dimensional array
```
   [
        [exchange, 'GetDepth'],
        [exchange, 'GetTicker'],
    ]
```
> Return value cmdList array

- **$.wait(cmdList)**
> Get Results

- **$.gowait()**
> Execute Go and get the result

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|RETRY_INTERVAL|true|Retry interval (seconds)|


> Source (javascript)

``` javascript
$.go = function(tasks) {
    return _.map(tasks, function(args) {
        return {
            result: null,
            args: args,
            defer: args[0].Go.apply(args[0], args.slice(1))
        }
    })
}

$.gowait = function(tasks, maxConcurrent, retry) {
    return $.wait($.go(tasks), maxConcurrent, retry)
}

$.wait = function(cmdList, maxConcurrent, retry) {
    retry = retry || true
    maxConcurrent = Math.min(cmdList.length, maxConcurrent || 5)
    var total = Math.ceil(cmdList.length / maxConcurrent)
    return _.reduce(_.range(total), function(beforeResultList, currentPage) {
        var lastCmdList = cmdList.slice(currentPage * maxConcurrent, currentPage * maxConcurrent + maxConcurrent)
        while (1) {
            lastCmdList = _.map(lastCmdList, function(cmd) {
                var args = cmd.args
                if (cmd.result == null) {
                    var ret = cmd.defer.wait()
                    if (ret != null) {
                        return _.extend(cmd, {
                            result: ret
                        })
                    } else if (retry === true) {
                        return _.extend(cmd, {
                            defer: args[0].Go.apply(args[0], args.slice(1)),
                            result: null
                        })
                    }
                }
                return cmd
            })
            var isFinished = _.every(lastCmdList, function(cmd) {
                return cmd.result
            })
            if (isFinished) {
                break
            }
            Sleep(RETRY_INTERVAL * 1000)
        }
        var newResultList = lastCmdList.map(function(cmd) {
            return cmd.result
        })
        if (currentPage + 1 < total) {
            Sleep(1000)
        }
        return beforeResultList.concat(newResultList)
    }, [])
}
```

> Detail

https://www.fmz.com/strategy/159978

> Last Modified

2019-08-24 16:02:33
