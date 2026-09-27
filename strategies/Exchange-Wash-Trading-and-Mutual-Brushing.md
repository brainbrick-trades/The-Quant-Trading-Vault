
> Name

Exchange-Wash-Trading-and-Mutual-Brushing

> Author

apple7474



> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|nnum|5|Quantity|
|pprice|3|Price|
|trade_num|5|Number of Trades|




|Button|Default|Description|
|----|----|----|
|Start|__button__|Start volume brushing|


> Source (python)

``` python
def main():
    # Set exchange address
    exchanges[0].SetBase("")
    exchanges[1].SetBase("")
    Log("Waiting for instructions")
    while True:
        LogStatus(_D())
        cmd = GetCommand()
        if cmd:
            arr = cmd.split(":")
            # Number of Trades
            for i in range(trade_num):
                Account0 = exchanges[0].GetAccount()
                Account1 = exchanges[1].GetAccount()
                # Log("Account0-usdt", Account0["Balance"], "Account0-DEC", Account0["Stocks"])
                # Log("Account 1-usdt", Account1["Balance"], "Account1-DEC", Account1["Stocks"])
                # Get the coins of A0 and A1
                A0_stocks = Account0["Stocks"]
                A1_stocks = Account1["Stocks"]
                error = 0
                if A0_stocks > A1_stocks:
                    Log("Account0There are coins")
                    # Reset index
                    ex_chang = [exchanges[0], exchanges[1]]
                    if abstest(A0_stocks, A1_stocks) == 1:
                        break
                    else:
                        # Log("Can continue trading")
                        pass
                else:
                    Log("Account1Yesdec")
                    # Reset index
                    ex_chang = [exchanges[1], exchanges[0]]
                    if abstest(A0_stocks, A1_stocks) == 1:
                        break
                    else:
                        # Log("Can continue trading")
                        pass
                # 0Index always sells    
                ex_chang[0].Sell(pprice, nnum)
                # 1Index always sells  
                ex_chang[1].Buy(pprice, nnum)
                Log("Transaction completed",i)
                Sleep(5)
            if abstest(A0_stocks, A1_stocks) == 1:
                break
            else:
                # Log("Can continue trading")
                pass
    Log("Run finished")

def abstest(a, b):
    # Simple judgment
    abs_value = abs(a - b)
    # Log("Currency difference:" + str(abs_value))
    if abs_value == 0:
        Log("Insufficient coins, please check")
        error = 1
    else:
        # Log("Can continue trading")
        error = 0
    return error


```

> Detail

https://www.fmz.com/strategy/226845

> Last Modified

2021-07-14 15:44:40
