
> Name

Arbitrage-Order

> Author

ChaoZhang



> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|SYMBOL1|Go long on top|Trading pair1|
|SYMBOL2|Go long on the downside | Trading pair2|
|VALUE|Cannot be less than the minimum opening value, which is the opening value per single currency | opening value.|
|DIRECTION|Go long when it crosses the first contract, go long when it crosses the second contract | Direction|


> Source (javascript)

``` javascript
function main() {
    exchange.SetContractType("swap");
    Log(SYMBOL1,SYMBOL2)
    // exchange.IO("cross", true);
    exchange.SetMarginLevel(10);
    const markets = exchange.GetMarkets();
    const ticker1 = exchange.GetTicker(SYMBOL1);
    const ticker2 = exchange.GetTicker(SYMBOL2);
    const market1 = markets[SYMBOL1 ];
    const market2 = markets[SYMBOL2];
    // Log(market1)
    if (DIRECTION === 0 || DIRECTION === 1) {
        return openPositions(ticker1, ticker2, market1, market2);
    } else if (DIRECTION === 2) {
        return closePositions(ticker1, ticker2);
    } else if (DIRECTION === 3) {
        return reversePositions(ticker1, ticker2, market1, market2);
    }
}

function openPositions(ticker1, ticker2, market1, market2) {
    // Log(exchange.GetName(), VALUE, ticker1.Last, market1.AmountPrecision)
    let amount1 = _N(VALUE / ticker1.Last, market1.AmountPrecision);
    let amount2 = _N(VALUE / ticker2.Last, market2.AmountPrecision);
    if (exchange.GetName() === "Futures_OKCoin") {
        amount1 = _N(VALUE / ticker1.Last / market1.CtVal, market1.AmountPrecision);
        amount2 = _N(VALUE / ticker2.Last / market2.CtVal, market2.AmountPrecision);
    }

    const isBuy = DIRECTION === 0;

    const order1 = createOrder(SYMBOL1, isBuy, amount1);
    const order2 = createOrder(SYMBOL2, !isBuy, amount2);

    return {
        symbol1: createOrderInfo(order1, ticker1.Last, market1, isBuy ? "Open long position : Open short position", amount1),
        symbol2: createOrderInfo(order2, ticker2.Last, market2, isBuy ? "Open short position : Open long position", amount2)
    };
}

function closePositions(ticker1, ticker2) {
    const positions = exchange.GetPositions("");
    const position1 = positions.find(pos => pos.Symbol === SYMBOL1 );
    const position2 = positions.find(pos => pos.Symbol === SYMBOL2 );

    let result = {};

    if (position1) {
        const order1 = closePosition(position1);
        result.symbol1 = createOrderInfo(order1, ticker1.Last, null, position1.Type === PD_LONG ? "Close long position" : "Close short position", position1.Amount);
    } else {
        result.symbol1 = { message: "No Position to Close" };
    }

    if (position2) {
        const order2 = closePosition(position2);
        result.symbol2 = createOrderInfo(order2, ticker2.Last, null, position2.Type === PD_LONG ? "Close long position" : "Close short position", position2.Amount);
    } else {
        result.symbol2 = { message: "No Position to Close" };
    }

    return result;
}

function reversePositions(ticker1, ticker2, market1, market2) {
    const positions = exchange.GetPositions("");
    const position1 = positions.find(pos => pos.Symbol === SYMBOL1 );
    const position2 = positions.find(pos => pos.Symbol === SYMBOL2 );

    let result = {};

    if (position1) {
        const closeOrder1 = closePosition(position1);
        const openOrder1 = createOrder(SYMBOL1, position1.Type === PD_LONG ? false : true, position1.Amount);
        result.symbol1 = {
            close: createOrderInfo(closeOrder1, ticker1.Last, null, position1.Type === PD_LONG ? "Close long position" : "Close short position", position1.Amount),
            open: createOrderInfo(openOrder1, ticker1.Last, market1, position1.Type === PD_LONG ? "Open short position : Open long position", position1.Amount)
        };
    } else {
        result.symbol1 = { message: "Can reverse without position" };
    }

    if (position2) {
        const closeOrder2 = closePosition(position2);
        const openOrder2 = createOrder(SYMBOL2, position2.Type === PD_LONG ? false : true, position2.Amount);
        result.symbol2 = {
            close: createOrderInfo(closeOrder2, ticker2.Last, null, position2.Type === PD_LONG ? "Close long position" : "Close short position", position2.Amount),
            open: createOrderInfo(openOrder2, ticker2.Last, market2, position2.Type === PD_LONG ? "Open short position : Open long position", position2.Amount)
        };
    } else {
        result.symbol2 = { message: "Can reverse without position" };
    }

    return result;
}

function createOrder(symbol, isBuy, amount) {
    const orderType = isBuy ? "buy" : "sell";
    return exchange.CreateOrder(symbol, orderType, -1, amount);
}

function closePosition(position) {
    const closeType = position.Type === PD_LONG ? "closebuy" : "closesell";
    return exchange.CreateOrder(position.Symbol, closeType, -1, position.Amount);
}

function createOrderInfo(orderId, price, market, direction, amount) {
    return {
        id: orderId,
        price: price,
        market: market,
        direction: direction,
        amount: amount
    };
}

```

> Detail

https://www.fmz.com/strategy/455638

> Last Modified

2024-07-11 18:34:51
