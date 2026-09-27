
> Name

Fetch-All-Contract-Positions-on-Binance-At-Once-and-Format-Them-Into-an-Array-of-Inventor-Position-Structures

> Author

夏天不打你





> Source (javascript)

``` javascript
// Get the positions of a specific currency from the position list
function getPositionBySymbol(positions, symbol) {
    var index = -1;

    if (positions && positions.length > 0) {
        for (var i = 0; i < positions.length; i++) {
            if (positions[i][0].Symbol == symbol) {
                index = i;
                break;
            }
        }
    }

    return index == -1 ? null : positions[index];
}

// Get all position lists
function getAllPositionInBinance() {
    var ret = exchange.IO("api", "GET", "/fapi/v2/account");
    var positions = [];
    var i = 0;

    if (!ret || !ret.positions) {
        return null;
    }
    // Get all positions
    for (i = 0; i < ret.positions.length; i++) {
        if (ret.positions[i].positionAmt != 0 && ret.positions[i].symbol.endsWith("USDT")) {
            positions.push([{
                Symbol: ret.positions[i].symbol.substring(0, ret.positions[i].symbol.lastIndexOf("USDT")) + "_USDT",
                Amount: Number(Math.abs(ret.positions[i].positionAmt)),
                FrozenAmount: 0,
                Price: Number(ret.positions[i].entryPrice),
                Profit: Number(ret.positions[i].unrealizedProfit),
                Type: ret.positions[i].positionAmt < 0 ? PD_SHORT : PD_LONG,
                ContractType: "swap",
                Margin: Number(ret.positions[i].positionInitialMargin),
                LevelRate: Number(ret.positions[i].leverage)
            }]);
        }
    }
    // Merge positions of the same currency(Same currency, long and short two-way positions)
    if (positions.length >= 2) {
        for (i = 0; i < positions.length; i++) {
            for (var j = i + 1; j < positions.length; j++) {
                if (positions[i][0].Symbol == positions[j][0].Symbol) {
                    positions[i].push(JSON.parse(JSON.stringify(positions[j][0])));
                    positions.splice(j, 1);                     // Delete the same currency
                    break;
                }
            }
        }
    }

    return positions;
}
```

> Detail

https://www.fmz.com/strategy/315410

> Last Modified

2021-09-26 00:08:35
