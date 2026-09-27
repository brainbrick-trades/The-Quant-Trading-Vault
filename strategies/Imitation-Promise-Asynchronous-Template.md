
> Name

Imitation-Promise-Asynchronous-Template

> Author

nogo

> Strategy Description

Imitation Promise asynchronous template

Not much to say, usage is similar to Promise.



> Source (javascript)

``` javascript

class Task {
    static PENDING = 'pending'
    static FULFILLED = 'fulFilled'
    static REJECTED = 'rejected'
    static WaitResults = []

    constructor(executor) {
        this.status = Task.PENDING
        this.value = undefined
        this.reason = undefined
        this.onResolvedCallbacks = []
        this.onRejectedCallbacks = []

        // Success
        let _resolve = (value) => {
            // If it is the result of an asynchronous request, thenwaitAt/InTask.waitHandled uniformly in the middle
            if (this.status == Task.PENDING) {
                if (value && value.wait instanceof Function) {
                    Task.WaitResults.push({
                        handle: value.wait,
                        resolve: _resolve,
                        reject: _reject
                    })
                } else {
                    this.status = Task.FULFILLED
                    this.value = value
                    let handler;
                    while (handler = this.onResolvedCallbacks.shift()) {
                        handler(this.reason)
                    }
                }
            }
        }

        //Failed
        let _reject = (reason) => {
            if (this.status == Task.PENDING) {
                this.status = Task.REJECTED
                this.reason = reason
                let handler;
                while (handler = this.onRejectedCallbacks.shift()) {
                    handler(this.value)
                }
            }
        }

        executor(_resolve, _reject)
    }

    then(onFulfilled, onRejected) {
        let promise = this
        return new Task((resolve, reject) => {
            function handler(value) {
                var ret = typeof onFulfilled === 'function' && onFulfilled(value);
                if (ret instanceof Task) {
                    ret.then(resolve, reject)
                } else {
                    resolve(ret);
                }
            }

            function errback(reason) {
                let ret = typeof onRejected === 'function' && onRejected(reason) || reason;
                if (ret instanceof Task) {
                    ret.then(resolve, reject)
                } else {
                    reject(ret);
                }
            }

            if (promise.status === Task.PENDING) {
                //Log("PENDING")
                promise.onResolvedCallbacks.push(handler);
                promise.onRejectedCallbacks.push(errback);
            } else if (promise.status === Task.FULFILLED) {
                //Log("FULFILLED")
                handler(promise.value);
            } else if (promise.status === Task.REJECTED) {
                //Log("REJECTED")
                errback(promise.reason);
            }
        })
    }

    catch(onReJected) {
        return this.then(undefined, onReJected)
    }

    //Synchronize multiple asynchronous operations
    static all = (list) => {
        return new Task((resolve, reject) => {
            var resArray = []
            let index = 0
            function processData(i, data) {
                resArray[i] = data
                index += 1
                if (index == list.length) {
                    resolve(resArray)
                }
            }
            for (let i = 0; i < list.length; i++) {
                let item = list[i]
                if (item instanceof Task) {
                    item.then(data => {
                        processData(i, data);
                    }, err => {
                        reject(err)
                        return;
                    })
                } else {
                    processData(i, item);
                }
            }
        })
    }

    //Get asynchronous results
    static wait = function () {
        let obj;
        while (obj = Task.WaitResults.shift()) {
            if (!obj) break;
            let { handle, resolve, reject } = obj;
            let data = handle(6000)
            if (data !== undefined) {
                resolve(data)
            } else {
                 // Return if asynchronous times outwaitobject, you can try again later, or query the request results directly.
                reject(handle)
            }
        }
    }
}

function main() {
    exchange.SetContractType("swap")

    new Task(function (resolve, reject) {
        resolve(exchange.Go("GetDepth"))
    }).then(data => {
        Log(data)
        return data
    }).then((data) => {
        //Chain execution
        Log(data)
    })

    new Task(function (resolve, reject) {
        reject("Error testing")
    }).then(data => {
        Log(data)
    }, error => {
        Log(error)
        return "Pass it after error handling tocatchMethod"
    }).catch(error => {
        Log(error)
    })

    Task.all([
        new Task(function (resolve, reject) {
            resolve(exchange.Go("GetDepth"))
        }),
        new Task(function (resolve, reject) {
            resolve(exchange.Go("GetTicker"))
        }),
        new Task(function (resolve, reject) {
            resolve(100)
        }),
        { a: 1 },
        { b: 2 }
    ]).then(data => {
        Log(data[0])
        Log(data[1])
        Log(data[2])
        Log(data[3])
        Log(data[4])
    })

    //Exceptions occur when multiple requests are synchronized; need to handle the results of asynchronous query requests
    Task.all([
        new Task((resolve, reject) => {
            resolve(1)
        }),
        new Task((resolve, reject) => {
            resolve(2)
        }),
        new Task((resolve, reject) => {
            //Error
            reject(3)
        }),
        new Task((resolve, reject) => {
            resolve(4)
        }),

    ]).then((data) => {
        console.log(data)
    }, error => {
        console.log("error", error)
        return 5
    }).catch(error => {
        console.log("catch", error)
    })

    //Must execute, all asynchronous calls will be made herewaitMethod, get result.
    Task.wait()
}

```

> Detail

https://www.fmz.com/strategy/386497

> Last Modified

2022-10-16 13:24:40
