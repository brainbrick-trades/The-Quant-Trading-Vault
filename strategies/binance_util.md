
> Name

binance_util

> Author

linsilence



> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|isDebug|false|Enable testing|


> Source (javascript)

``` javascript


const api_v1 = '/v1'
const api_v3 = '/v3'

const api_spot_host = 'https://api.binance.com'
const api_spot = '/api'
const api_margin_full = '/sapi'

const api_future_usdt = '/fapi'
const api_future_coin = '/dapi'

const api_transfer = api_v1 + '/asset/transfer'

const api_spot_exchange_info = api_v3 + '/exchangeInfo'
const api_margin_account = api_v1 + '/margin/account'

const api_future_exchange_info = api_v1 + '/exchangeInfo'
const api_funding_rate = api_v1 + '/premiumIndex'
const api_position_side = api_v1 + '/positionSide/dual'
const api_position_risk = api_v1 + '/positionRisk'

function adapt_currency(symbol_fmz) {
  // BTC_USDT -> BTCUSDT
  return symbol_fmz.replace('_', '')
}

function vers_adapt_currency(symbol_binance) {
  // BTCUSDT -> BTC_USDT
  return symbol_binance.replace(/^(.+)(USDT|USD)$/, '$1_$2')
}

function trim_currency(symbol_binance) {
  // BTCUSDT -> BTC
  return symbol_binance.replace(/^(.+)(USDT|USD)$/, '$1')
}

function api_future_base(is_coin_or_usdt) {
  return is_coin_or_usdt ? api_future_coin : api_future_usdt
}

function calculate_percision(num) {
  const p = String(parseFloat(num))
  if (p.includes('.')) {
    return p.split('.')[1].length
  } else {
    let pp = 0
    for (let i = p.length - 1; i >= 0; --i) {
      if (p.charAt(i) !== '0') {
        break
      }
      --pp
    }
    return pp
  }
}

/**
 *
 * @param {*} ex
 * @param {*} type
 *  MAIN_C2C Spot wallet transferred to C2C wallet
 *  MAIN_UMFUTURE Convert spot wallet to USDT-margined futures wallet
 *  MAIN_CMFUTURE Convert spot wallet to coin-margined futures wallet
 *  MAIN_MARGIN Transfer from spot wallet to leveraged cross wallet
 *  MAIN_MINING Spot wallet transferred to mining pool wallet
 *  C2C_MAIN C2CWallet switches to spot wallet
 *  C2C_UMFUTURE C2CWallet transferred to USDT-margined contract wallet
 *  C2C_MINING C2CWallet transferred to mining pool wallet
 *  UMFUTURE_MAIN UTransfer from fiat contract wallet to spot wallet
 *  UMFUTURE_C2C UStandard contract wallet to C2C wallet
 *  UMFUTURE_MARGIN UFrom standard contract wallet to leveraged full margin wallet
 *  CMFUTURE_MAIN Coin-margined contract wallet to spot wallet
 *  MARGIN_MAIN Transfer from leveraged cross wallet to spot wallet
 *  MARGIN_UMFUTURE Leveraged full-wallet switch to U-based contract wallet
 *  MINING_MAIN Mining pool wallet transferred to spot wallet
 *  MINING_UMFUTURE Mining pool wallet to USDT-margined contract wallet
 *  MINING_C2C Mining pool wallet transferred to C2C wallet
 *
 * @param {*} asset
 * @param {*} amount
 */
$.Binance_Api_Transfer = function (ex, type, asset, amount) {
  const ret = ex.IO(
    'api',
    'POST',
    api_margin_full + api_transfer,
    `type=${type}&asset=${asset}&amount=${amount}&timestamp=${_N(UnixNano() / 1000000, 0)}`,
  )
  if (isDebug) Log('Binance_Api_Transfer ret: ', ret)
  if (!ret) {
    return null
  }
  return ret.tranId
}

$.Binance_Api_Spot_ExchangeInfo = function (ex, symbolStr) {
  const query = symbolStr ? '?symbol=' + adapt_currency(symbolStr) : ''
  const url = api_spot_host + api_spot + api_spot_exchange_info + query
  // const ret = ex.IO('api', 'GET', api_spot + api_spot_exchange_info);
  const ret = JSON.parse(HttpQuery(url))
  if (isDebug) Log('Binance_Api_Spot_ExchangeInfo ret: ', ret)
  return ret
}

$.Binance_Api_Spot_ExchangeInfo_Symbol = function (ex, symbolStr) {
  const ret = $.Binance_Api_Spot_ExchangeInfo(ex, symbolStr)
  if (!ret) {
    return null
  }

  const symbols = ret.symbols
  if (!symbols || symbols.length === 0) {
    return null
  }

  let s = null
  for (const e of symbols) {
    if (e.symbol === adapt_currency(symbolStr)) {
      s = e
      break
    }
  }
  if (isDebug) Log('Binance_Api_Spot_ExchangeInfo_Symbol ret: ', s)
  return s
}

$.Binance_Api_Spot_ExchangeInfo_Symbol_filter = (ex, symbolStr) => {
  const ret = $.Binance_Api_Spot_ExchangeInfo_Symbol(ex, symbolStr)
  if (!ret) {
    return null
  }

  const f = {}
  ret.filters.forEach((e) => {
    if (e.filterType === 'PRICE_FILTER') {
      f.priceMin = e.minPrice
      f.priceMax = e.maxPrice
      f.pricePercision = calculate_percision(e.tickSize)
    }
    if (e.filterType === 'LOT_SIZE') {
      f.quantityPercision = calculate_percision(e.stepSize)
    }
    if (e.filterType === 'MIN_NOTIONAL') {
      f.amountMin = Number(e.minNotional)
    }
    if (e.filterType === 'MAX_NUM_ORDERS') {
      f.orderMax = Number(e.maxNumOrders)
    }
  })
  isDebug && Log('Binance_Api_Spot_ExchangeInfo_Symbol_filter:', f)

  // if (isNaN(f.pricePercision ?? NaN) || isNaN(f.quantityPercision ?? NaN) || isNaN(f.amountMin ?? NaN)) {
  //   return null
  // }
  return f
}

/**
 * Spot minimum transaction amount,price * quantity
 *
 * @param {*} ex
 * @param {*} symbolStr
 */
$.Binance_Api_Spot_ExchangeInfo_Symbol_MiniNotional = function (ex, symbolStr) {
  const ret = $.Binance_Api_Spot_ExchangeInfo_Symbol(ex, symbolStr)
  if (!ret) {
    return 0
  }

  const fs = ret.filters.filter((e) => e.filterType === 'MIN_NOTIONAL')
  if (!fs || fs.length !== 1) {
    return 0
  }

  return fs[0].minNotional
}

/**
 * Spot trading volume precision
 *
 * @param {*} ex
 * @param {*} symbolStr
 */
$.Binance_Api_Spot_ExchangeInfo_Symbol_Precision = function (ex, symbolStr) {
  const ret = $.Binance_Api_Spot_ExchangeInfo_Symbol(ex, symbolStr)
  if (!ret) {
    return 0
  }

  const fs = ret.filters.filter((e) => e.filterType === 'LOT_SIZE')
  if (!fs || fs.length !== 1) {
    return 0
  }

  const p = parseFloat(fs[0].stepSize)
  return String(p).includes('.') ? String(p).split('.')[1].length : 0
}

$.Binance_Api_Future_ExchangeInfo = function (ex) {
  const ret = ex.IO('api', 'GET', api_future_base(false) + api_future_exchange_info)
  if (isDebug) Log('Binance_Api_Future_ExchangeInfo ret: ', ret)
  return ret
}

$.Binance_Api_Future_ExchangeInfo_Symbol = function (ex, symbolStr) {
  const ret = $.Binance_Api_Future_ExchangeInfo(ex)
  if (!ret) {
    return null
  }

  const symbols = ret.symbols
  if (!symbols || symbols.length === 0) {
    return null
  }

  const ss = symbols.filter((e) => e.symbol === adapt_currency(symbolStr))
  if (!ss || ss.length !== 1) {
    return null
  }

  return ss[0]
}

$.Binance_Api_Future_ExchangeInfo_AllSymbol = function (ex) {
  const ret = $.Binance_Api_Future_ExchangeInfo(ex)
  if (!ret) {
    return null
  }

  const symbols = ret.symbols
  if (!symbols || symbols.length === 0) {
    return null
  }

  const ss = symbols.map((e) => trim_currency(e.symbol))
  if (isDebug) Log('Binance_Api_Future_ExchangeInfo_AllSymbol ret: ', ss)
  return ss
}

/**
 * Current funding rate
 *
 * @param {*} ex
 */
$.Binance_Api_FundingRate = function (ex) {
  const ret = ex.IO('api', 'GET', api_future_base(false) + api_funding_rate, 'symbol=' + adapt_currency(ex.GetCurrency()))
  if (isDebug) Log('Binance_Api_FundingRate ret: ', ret)
  if (!ret) {
    return 0
  }
  return ret.lastFundingRate
}

$.Binance_Api_FundingRate_All = function (ex) {
  const ret = ex.IO('api', 'GET', api_future_base(false) + api_funding_rate)
  if (isDebug) Log('Binance_Api_FundingRate_All ret: ', ret)
  if (!ret) {
    return 0
  }
  return ret
}

/**
 * Query position mode
 *
 * @param {*} ex
 *
 * @returns "true": Bidirectional hold mode; "false": One-way hold mode
 */
$.Binance_Api_PositionSide = function (ex) {
  const ret = ex.IO('api', 'GET', api_future_base(false) + api_position_side)
  if (isDebug) Log('Binance_Api_PositionSide ret: ', ret)
  return ret.dualSidePosition
}

/**
 * User position risk
 *
 * @param {*} ex
 * @param {*} positionType PD_LONG | PD_SHORT
 */
$.Binance_Api_PositionRisk = function (ex, positionType) {
  try {
    // [{
    //     "notional": "38.47520000",
    //     "unRealizedProfit": "0.52519000",
    //     "leverage": "10",
    //     "maxNotionalValue": "20000000",
    //     "isAutoAddMargin": "false",
    //     "liquidationPrice": "0",
    //     "marginType": "cross",
    //     "isolatedMargin": "0.00000000",
    //     "positionSide": "LONG",
    //     "symbol": "BTCUSDT",
    //     "positionAmt": "0.001",
    //     "entryPrice": "37950.01000",
    //     "markPrice": "38475.20000000"
    // }, {
    //     "leverage": "10",
    //     "marginType": "cross",
    //     "positionAmt": "0.000",
    //     "markPrice": "38475.20000000",
    //     "unRealizedProfit": "0.00000000",
    //     "maxNotionalValue": "20000000",
    //     "isolatedMargin": "0.00000000",
    //     "isAutoAddMargin": "false",
    //     "positionSide": "SHORT",
    //     "notional": "0",
    //     "symbol": "BTCUSDT",
    //     "entryPrice": "0.00000",
    //     "liquidationPrice": "0"
    // }]
    const symbol = adapt_currency(ex.GetCurrency())
    const ret = ex.IO('api', 'GET', api_future_base(false) + api_position_risk, 'symbol=' + symbol)
    if (isDebug) Log('Binance_Api_PositionRisk ret: ', ret)
    if (!ret || ret.length === 0) {
      return null
    }

    let side
    if ($.Binance_Api_PositionSide(ex)) {
      if (positionType === PD_LONG) {
        side = 'LONG'
      } else if (positionType === PD_SHORT) {
        side = 'SHORT'
      } else {
        Log('Binance_Api_PositionRisk positionType error - ', positionType)
        return null
      }
    } else {
      side = 'BOTH'
    }

    let r = null
    ret.forEach((e) => {
      if (e.symbol !== symbol) {
        return
      }
      if (e.positionSide === side) {
        r = e
        return
      }
    })

    return r
  } catch (e) {
    Log('Binance_Api_PositionRisk error: ', e, '#FF0000')
    return null
  }
}

/**
 * Get liquidation price of futures positions
 *
 * @param {*} ex
 * @param {*} positionType
 */
$.Binance_Api_PositionRisk_LiquidationPrice = function (ex, positionType) {
  const r = $.Binance_Api_PositionRisk(ex, positionType)
  if (!r) {
    return 0
  }
  return r.liquidationPrice
}

/**
 * Query full margin account details
 *
 * @param {*} ex
 */
$.Binance_Api_MarginAccount = function (ex) {
  const ret = ex.IO('api', 'GET', api_margin_full + api_margin_account)
  if (isDebug) Log('Binance_Api_MarginAccount ret: ', ret)
  return ret
}

/**
 * Query cross margin account details - risk rate
 *
 * @param {*} ex
 */
$.Binance_Api_MarginAccount_MarginLevel = function (ex) {
  const ret = this.Binance_Api_MarginAccount(ex)
  if (!ret) {
    return 0
  }
  return ret.marginLevel
}

function main() {
  Log($.Binance_Api_FundingRate(exchange))
  Log($.Binance_Api_PositionRisk(exchange))
}

```

> Detail

https://www.fmz.com/strategy/247137

> Last Modified

2023-07-18 20:14:08
