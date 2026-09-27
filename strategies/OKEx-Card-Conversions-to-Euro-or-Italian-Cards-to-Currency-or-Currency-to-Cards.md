
> Name

OKEx-Card-Conversions-to-Euro-or-Italian-Cards-to-Currency-or-Currency-to-Cards

> Author

Exodus[策略代写]

> Strategy Description

As the title:
![IMG](https://www.fmz.com/upload/asset/1f4d7d7de4354276de970.png)  
![IMG](https://www.fmz.com/upload/asset/1f448a3f706ccc2712c15.png) 
![IMG](https://www.fmz.com/upload/asset/1f43c354a217fb6575477.png) 
![IMG](https://www.fmz.com/upload/asset/1f4073ba260e47fcc5a3c.png) 


By the way, I will undertake the ghostwriting of strategies.



> Source (javascript)

``` javascript
//Test Module
//The link can be initiated by any exchange, and you can enter the corresponding pair name, price, quantity, etc
function main() {
    
    let currency=_C(exchange.GetCurrency);//Currency Pair Name
    
    let curPrice=_C(exchange.GetTicker).Last;//Current Price
    
    let atz=AmountToZhang(currency,curPrice,1);//How many contracts one coin equals?
    
    let zta=ZhangToAmount(currency,curPrice,1);//How many coins equal one lot?
    
    
    Log(currency+"1One Coin Equals"+atz+"Zhang,","1sheets equal to"+zta+"Currency");
    
}

//currency to sheets
//currencyrepresents the currency pair name,pxPrice indicated during conversion,szRepresents the quantity of coins, calculate the number of contracts based on coin quantity(Leverage not calculated)
function AmountToZhang(currency,px,sz){
    
    //okThe trading pair format when requested by the exchange isETH-USDT-SWAP,instead ofETH_USDT,So be carefulinstIdThe underscore must be converted to-,That is, the minus sign
    let instId=currency.replace("_","-")+"-SWAP";
    
    
    let str="https://www.okx.com/api/v5/public/convert-contract-coin?"+"instId="+instId+"&px="+px+"&sz="+sz;
    let ret=JSON.parse(HttpQuery(str));
    
    Log("currency to sheetsHttpLink"+str,"Return Result:"+JSON.stringify(ret));
    
    
    return ret.data[0].sz;//Return how many contracts correspond to one coin
    
}

//Contracts to coins ratio, indicating how many coins one contract corresponds to
//currencyrepresents the currency pair name ,pxPrice indicated during conversion,szRepresents Number of Sheets,Pass in the number of sheets and obtain the corresponding number of coins (leverage is not calculated)
function ZhangToAmount(currency,px,sz){
    //okThe trading pair format when requested by the exchange isETH-USDT-SWAP,instead ofETH_USDT,So be carefulinstIdThe underscore must be converted to-,That is, the minus sign
    let instId=currency.replace("_","-")+"-SWAP";
    
    let str="https://www.okx.com/api/v5/public/convert-contract-coin?"+"type=2&instId="+instId+"&px="+px+"&sz="+sz;
    let ret=JSON.parse(HttpQuery(str));
    
    Log("sheets to currencyHttpLink"+str,"Return Result:"+JSON.stringify(ret));
    
    
    return ret.data[0].sz;//Note that the results do not calculate leverage, such asokA sheetBCH,Corresponding number of coins is10,If you want to place an order for a coin with the same amount of margin on other exchanges, you must calculate the leverage, that is, place an order10/20(leverage),0.5Currency.
    
}
```

> Detail

https://www.fmz.com/strategy/387901

> Last Modified

2022-10-29 18:47:50
