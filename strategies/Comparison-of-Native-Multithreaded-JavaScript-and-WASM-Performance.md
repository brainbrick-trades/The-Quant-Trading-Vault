
> Name

Comparison-of-Native-Multithreaded-JavaScript-and-WASM-Performance

> Author

发明者量化

> Strategy Description


The inventor quantitatively tried to make Javascript support real multi-threading from the native low-level, and added the WASM function. Below is a DEMO. Download the latest host to have an early experience.
This function is not a Worker function of Javascript. It can be used to communicate with each other within multiple threads or with the main thread.

CLanguage to wasm can generate tests from this website: https://wasdk.github.io/WasmFiddle/


The C language code compiled to wasm is as follows

```
int fib(int f) {
  if (f < 2) return f;
  return fib(f - 1) + fib(f - 2);
}
```

After compilation, download the wasm file and convert it into a hex string using python
```
python -c "print('data:hex,'+bytes.hex(open('program.wasm','rb').read()))"
```

Just replace the content after the variables in the code

> __Thread(function, arguments...)

Create a thread and return the thread tid. The function of the accepted thread body function must complete all function codes within the thread function. References to other closure functions are not supported. All APIs of the platform can be called within the thread, but other user-defined functions cannot be called.

Simple Example:
```
let tid = __Thread(function(x, y) {
    return x + y
}, 1, 2)
Log(__threadJoin(tid))
```

Example of multithreaded requests:
```
function main() {
    let threads = [
        "https://www.baidu.com",
        "https://www.163.com"
    ].map(function(url) {
        return __Thread(function(url) {
            Log("GET", url)
            return HttpQuery(url)
        }, url)
    })
    threads.forEach(function(tid) {
        Log(__threadJoin(tid))
    })
}
```

> Thread-local storage

Supports thread local storage variables. To facilitate data sharing, the data is valid when the thread is not terminated by `__threadJoin` waiting for exit success or `__threadTerminate`

```
__threadGetData(tid, key)
__threadSetData(tid, key, value)
```

tid0 indicates the current thread. If the value is not specified, it indicates deletion of the key. It supports mutual access of shared variables between threads. The value must be a serializable variable.

> Thread communication

```
__threadPostMessage(tid, msg) // Send a message to the specified thread. When tid is 0, it is sent to the main thread, that is, the current main function. The call within the thread points to the main thread to reply the message. The message can be captured by EventLoop.
__threadPeekMessage(tid, timeout) // Receive messages from the specified thread. If timeout (milliseconds) is not specified, it will wait forever. A tid of 0 means waiting for messages from the main thread.
```

> __threadJoin(tid, timeout)

Waiting for the thread to end, specify timeout (milliseconds) to specify the waiting timeout, you can not specify it, just wait until the thread ends, successfully return a structure containing the function return value and recycle resources, the structure is as follows
```
{
    id: tid, // Threadid
    elapsed: 1111, // Thread runtime (nanoseconds))
    terminated: false, // Whether the thread is forced to end 
    ret: 123, // Return value of thread function
}
```
Return if timeoutundefined
    
    
> __threadTerminate(tid)

Force end the thread and reclaim resources (cannot use __threadJoin to wait for completion anymore).)
    
> NOTE

__ThreadThe function does not support referencing variables outside the function (runs in an isolated environment). Referencing external variables will cause compilation to fail






> Source (javascript)

``` javascript
function main() {
    let cycle = 100
    let input = 30
    let threads = [
        __Thread(function(cycle, input) {
            function fib(f) {
                if (f < 2) return f
                return fib(f - 1) + fib(f - 2)
            }
            let ret = 0
            for (let i = 0; i < cycle; i++) {
                ret = fib(input);
                Log("javascript progress: ", i)
            }
            return 'javascript fib: ' + ret
        }, cycle, input),
        
        __Thread(function(cycle, input) {
            let data = 'data:hex,0061736d010000000186808080000160017f017f0382808080000100048480808000017000000583808080000100010681808080000007908080800002066d656d6f727902000366696200000aa480808000019e80808000000240200041024e0d0020000f0b2000417f6a10002000417e6a10006a0b'
            let m = wasm.parseModule(data)

            let instance = wasm.buildInstance(m, {
                stack_size: 65 * 1024 * 1024,
            })

            let ret = 0
            for (let i = 0; i < cycle; i++) {
                ret = instance.callFunction('fib', input)
                Log("wasm progress: ", i)
            }

            return 'wasm fib: ' + ret
        }, cycle, input)
    ]

    threads.forEach(function(tid) {
        let info = __threadJoin(tid)
        Log('#'+tid, info.ret, 'elapsed:', info.elapsed / 1e6, "#ff0000")
    })
}
```

> Detail

https://www.fmz.com/strategy/401463

> Last Modified

2023-03-03 03:42:24
