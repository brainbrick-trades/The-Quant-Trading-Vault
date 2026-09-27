
> Name

Place-Orders-on-Time-and-Ready-Basis-Public

> Author

daniaoren

> Strategy Description

A plugin used for spot-futures paired trading, can be used in the trading terminal.

Self-use tool, the default support is Deribit's futures order opening. Just fill in the contract name and expected price difference in the contract according to the default value format.

If you want to support other exchanges, you may need to slightly modify it yourself.

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|ContractSwap|swap|Perpetual Contract|
|ContractFuture|quarter|Futures Contract|
|Amount|true|Order Quantity|
|DiffMin|6|Minimum orderable spread|
|RealTrade|false|Whether to place real orders|


> Source (python)

``` python
def main():
	exchange.SetContractType(ContractSwap)
	TickerSwap = exchange.GetTicker()
	TickerSwap['BuyAmount'] = TickerSwap['Info']['result']['best_bid_amount']
	TickerSwap['SellAmount'] = TickerSwap['Info']['result']['best_ask_amount']
	exchange.SetContractType(ContractFuture)
	TickerFuture = exchange.GetTicker()
	TickerFuture['BuyAmount'] = TickerFuture['Info']['result']['best_bid_amount']
	TickerFuture['SellAmount'] = TickerFuture['Info']['result']['best_ask_amount']

	Diff = _N(TickerFuture['Buy'] - TickerSwap['Sell'],2)

	Msg = ''
	Msg += str(ContractSwap) +' '+ str(TickerSwap['Sell']) +' '+ str(TickerSwap['SellAmount'])+ '\n'
	Msg += str(ContractFuture) +' '+ str(TickerFuture['Buy']) +' '+ str(TickerFuture['BuyAmount']) + '\n'
	Msg += 'Spread: ' + str(Diff) + '\n'

	if Diff <= DiffMin:
		return 'Price difference ' + str(_N(Diff,2)) + ' Less than the set price difference '+str(DiffMin)+',Do not place an order' + '\n\nAdditional information\n' +Msg

	if TickerFuture['BuyAmount'] < Amount or TickerFuture['SellAmount'] < Amount:
		return 'The order quantity in a certain direction is less than the set order quantity '+str(Amount)+',Do not place an order' + '\n\nAdditional information\n' +Msg

	if not RealTrade:
		return 'Non-real Trading' + '\n' + Msg

	exchange.SetContractType(ContractSwap)
	exchange.SetDirection("buy")
	BuyOrderId = exchange.Buy(TickerSwap['Sell'] + 0.2, Amount)

	exchange.SetContractType(ContractFuture)
	exchange.SetDirection("sell")
	SellOrderId = exchange.Sell(TickerFuture['Buy'] - 0.2, Amount)

	BuyOrder = exchange.GetOrder(BuyOrderId)
	SellOrder = exchange.GetOrder(SellOrderId)

	TradeMsg = 'Transaction completed\n'
	TradeMsg += 'Buy Order ' + str(BuyOrder['ContractType']) + ' ' + str(BuyOrder['Price']) + ' ' + str(BuyOrder['DealAmount']) + '/' + str(BuyOrder['Amount']) + '\n'
	TradeMsg += 'Sell Order ' + str(SellOrder['ContractType']) + ' ' + str(SellOrder['Price']) + ' ' + str(SellOrder['DealAmount']) + '/' + str(SellOrder['Amount']) + '\n'
	TradeMsg += '\n\nAdditional information\n' +Msg
	return TradeMsg
```

> Detail

https://www.fmz.com/strategy/232006

> Last Modified

2021-02-24 21:04:40
