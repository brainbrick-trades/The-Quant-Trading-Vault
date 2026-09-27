
> Name

Trading-Pair-Accuracy-Calibration

> Author

斯巴达玩量化





> Source (javascript)

``` javascript
/*
-- After the strategy references this template, use it directly $.Test() Call this method
-- main The function will not be triggered in the strategy, only serves as an entry point for template debugging

-- GetExPrecision The function's precision calibration only supports units place, and does not currently support trading pair precision of tens/hundreds/thousands...
-- [Warning] If the market depth is too low to accurately represent true accuracy, the function may lose its accuracy
*/

let gCache = {};

let scientificToNumber = function(num) {
    if (/\d+\.?\d*e[\+\-]*\d+/i.test(num)) { //Regular expression to match numbers in scientific notation
        var zero = '0', //
            parts = String(num).toLowerCase().split('e'), //Split into coefficient and exponent
            e = parts.pop(), //Store exponent
            l = Math.abs(e), //Take absolute value,l-1That's it0Number of
            sign = e / l, //Determine positive or negative
            coeff_array = parts[0].split('.'); //Split the coefficient by decimal point
        if (sign === -1) { //If it is a decimal
            num = zero + '.' + new Array(l).join(zero) + coeff_array.join(''); //Concatenate strings, if it's a decimal, concatenate0Sum decimal point
        } else {
            var dec = coeff_array[1];
            if (dec) l = l - dec.length; //If it is an integer, count the non-zero digits of the integer except the first digit into the number of digits, and reduce it accordingly.0Number of
            num = coeff_array.join('') + new Array(l + 1).join(zero); //Concatenate strings; if it's an integer, no need to concatenate the decimal point
        }
    }
    return num;
}

$.GetPrecision = function(depth) {
    let maxLenAmt = 0;
    let maxLenPrice = 0;
    depth.Asks.forEach(function(ask) {
        let price = scientificToNumber(ask["Price"]).toString();
        if (price.indexOf('.') > -1) {
            let priceP = price.split(".")[1].length;
            if (priceP > maxLenPrice) {
                maxLenPrice = priceP;
            }
        }
        let amt = scientificToNumber(ask["Amount"]).toString();
        if (amt.indexOf('.') > -1) {
            let amtP = amt.split(".")[1].length;
            if (amtP > maxLenAmt) {
                maxLenAmt = amtP;
            }
        }
    })
    return [maxLenPrice, maxLenAmt];
}

// Return array [Price precision, Precision of quantity]
$.GetExPrecision = function(ex, force) {
    if (IsVirtual()) {
        return null;
    }
    let key = ex.GetName() + '_ex_precision_' + ex.GetCurrency();
    let cache = gCache[key];
    if (!force && cache) {
        return cache;
    }
    let r = $.GetPrecision(_C(ex.GetDepth));
    gCache[key] = r;
    Log("Cache precision information locally", key, r);
    return r;
}

function main() {
    $.GetExPrecision(exchange, false);
}
```

> Detail

https://www.fmz.com/strategy/372101

> Last Modified

2022-09-23 16:16:20
