
> Name

Switch-OKEx-V5-Simulated-Trading-Terminal-Plugin

> Author

发明者量化-小小梦

> Strategy Description

## Trading terminal OKEX_V5 simulation disk switching plug-in

When the OKEX V5 exchange object is configured (using OKEX V5's simulated disk API KEY configuration), since the simulated disk environment is not switched, the following error will be reported:

```
{"msg":"Broker id of APIKey does not match current environment.","code":"50101"}
```

Can use this plugin to switch, as shown in the figure:

- #### Click the add button:

  ![IMG](https://www.fmz.com/upload/asset/1789d89b0004425112f5.png) 

- #### Select plugin:

  ![IMG](https://www.fmz.com/upload/asset/1714b6edacde6828eba2.png) 

- #### Execute plugin

  ![IMG](https://www.fmz.com/upload/asset/169ace291c5d0da6e210.png) 

- #### Execute immediately

  ![IMG](https://www.fmz.com/upload/asset/170bac2eacc494c2eba3.png)  

- #### The simulated account assets are then read out

  ![IMG](https://www.fmz.com/upload/asset/168a45cf491f249d7189.png) 

If you want to switch back to the real disk environment, just uncheck the option and execute it again.



> Source (javascript)

``` javascript
function main() {    
    exchange.IO("simulate", true)
    return "Switched toOKEX V5Simulation Account"
}
```

> Detail

https://www.fmz.com/strategy/288769

> Last Modified

2021-06-08 15:08:47
