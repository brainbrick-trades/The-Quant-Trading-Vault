
> Name

Fee-Summary

> Author

yulong

> Strategy Description

Select any exchange and start.



> Source (javascript)

``` javascript


function main() {
    const binanceFundingRate = {
        type: 'table',
        title: 'Binance Fees',
        cols: ['Trading pair', 'Index price', 'Mark price', 'Basis', 'Funding rate', 'Rate time''],
        rows: []
    };

    const gateFundingRate = {
        type: 'table',
        title: 'GateIORate',
        cols: ['Trading pair', 'Index price', 'Mark price', 'Basis', 'Funding rate', 'Rate time''],
        rows: []
    };

    const okexFundingRate = {
        type: 'table',
        title: 'OKEXRate',
        cols: ['Trading pair', 'Index price', 'Mark price', 'Basis', 'Funding rate', 'Rate time''],
        rows: []
    };

    while (true) {
        const data = JSON.parse(HttpQuery('https://fapi.binance.com/fapi/v1/premiumIndex'));
        binanceFundingRate.rows = data.map(({ symbol, lastFundingRate, markPrice, indexPrice, nextFundingTime }) => [
            symbol,
            indexPrice,
            markPrice,
            _N((+markPrice - indexPrice) / +indexPrice * 100, 4) + '%',
            _N(lastFundingRate * 100, 4) + '%',
            _D(nextFundingTime)]);

        const dataGate = JSON.parse(HttpQuery('https://api.gateio.ws/api/v4/futures/usdt/contracts'));
        gateFundingRate.rows = dataGate.map(({ name, funding_rate, mark_price, index_price, funding_next_apply }) => [
            name,
            index_price,
            mark_price,
            _N((+mark_price - index_price) / +index_price * 100, 4) + '%',
            _N(funding_rate * 100, 4) + '%',
            _D(funding_next_apply * 1000)]);

        const instruments = JSON.parse(HttpQuery('https://www.okex.com/api/swap/v3/instruments'));
        okexFundingRate.rows = [];
        instruments.map(a => a.instrument_id).forEach(instrument_id => {
            const item = JSON.parse(HttpQuery(`https://www.okex.com/api/swap/v3/instruments/${instrument_id}/funding_time`))
            okexFundingRate.rows.push([instrument_id, '-', '-', '-', _N(item.funding_rate * 100, 4) + '%', _D(new Date(item.funding_time))]);
        });

        LogStatus('\n`' + JSON.stringify([binanceFundingRate, gateFundingRate, okexFundingRate]) + '`\n');
        Sleep(60000);
    }
}
```

> Detail

https://www.fmz.com/strategy/229619

> Last Modified

2021-02-06 07:54:07
