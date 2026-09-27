
> Name

Financing-and-Currency-Statistics

> Author

数·狂

> Strategy Description

Use the exchange api function to display the current financing situation of the exchange (the unpaid portion, including handling fees). Currently only OKCoin and Huobi are supported, welcome to continue to improve.
Latest version of the custodian required.



> Source (javascript)

``` javascript
function getLoanInfo(exchange, type) {
    var loanInfo;
    var dueAmount;
    if (exchange.GetName() == "OKCoin") { 
        loanInfo = exchange.IO("api", "borrows_info", "symbol=cny");
        if (type == "btc") {
            dueAmount = loanInfo.borrow_btc + loanInfo.interest_btc;
        }
        else if (type == "ltc") {
            dueAmount = loanInfo.borrow_ltc + loanInfo.interest_ltc;
        }   
        else if (type == "cny") {
            dueAmount = loanInfo.borrow_cny + loanInfo.interest_cny;
        }
    }
    else if (exchange.GetName() == "Huobi") {
        loanInfo = exchange.IO("api", "get_loans", "market=cny");
        dueAmount = 0;
            for (var i = 0; i < loanInfo.length; i++) {
                if (type == "cny" && loanInfo[i].type == 1 || type == "btc" && loanInfo[i].type == 2 || type == "ltc" && loanInfo[i].type == 3) {
                    dueAmount += (Number(loanInfo[i].loan_amount) - Number(loanInfo[i].repayment_amount) + Number(loanInfo[i].interest_nopay) + Number(loanInfo[i].interest_payed));
                }
            }
    }
    else 
        throw "Exchange not supported yet: " + exchange.GetName();
    return dueAmount;
}

function main() {
    for (var i = 0; i < exchanges.length; i++)
        Log(exchanges[i].GetName(),
            "Not returnedCNY:", getLoanInfo(exchanges[i], "cny"),
            "Not returnedBTC:", getLoanInfo(exchanges[i], "btc"),
            "Not returnedLTC:", getLoanInfo(exchanges[i], "ltc")
           );
}
```

> Detail

https://www.fmz.com/strategy/8954

> Last Modified

2016-01-13 19:03:22
