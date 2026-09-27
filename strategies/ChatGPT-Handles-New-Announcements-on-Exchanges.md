
> Name

ChatGPT-Handles-New-Announcements-on-Exchanges

> Author

ChaoZhang

> Strategy Description

An effective way to solve the problem of inconsistent listing time on exchanges is to use ChatGPT for processing and avoid using regular expressions for cumbersome matching. Handing announcements directly to ChatGPT allows it to identify and process the time formats of various exchanges, making it a convenient and efficient application scenario.

By passing the announcement text to the openaiCompletions function, you can leverage the power of ChatGPT to extract key information from listing announcements on various exchanges. This approach not only improves processing efficiency, but also enhances compatibility with different time formats.

Before using this function, you need to set the policy parameter OPENAI_API_KEY, which provides your OpenAI API key. You can use your own key to access gpt-3.5-turbo API.

Function Name:openaiCompletions

Function Overview: This function uses OpenAI's gpt-3.5-turbo model to determine whether the input announcement content is an announcement of a new spot trading pair on an exchange. If the announcement meets the conditions, the function will return a JSON object containing a success indicator, the trading pair, and Beijing time; if the announcement does not meet the conditions, it will only return a failure indicator.

Input Parameters:
content:Announcement content that needs to be judged.

Output Results:
JSON Object, containing the following key-value pairs:

success:Boolean value, indicating whether the judgment result is successful or not.
pair:(Only exists when success is true) String array representing the trading pair.
time:(The string exists only when success is true, indicating the announcement release time, converted to Beijing time.(UTC+8).
Function execution process:

Define the URL, request headers, and request data for the gpt-3.5-turbo API.
Call the HttpQuery method to send the request data to gpt-3.5-turbo API.
Parse the JSON data returned by the gpt-3.5-turbo API and extract the required information.
Returns the processed JSON object.

Usage Example:

```
var content = "An exchange announced, it will be2023Year3Moon22day12:00(UTC+8)is onlineID/USDTtrading pair.";
var result = openaiCompletions(content);
Log(result);
```

Output Results:

```
{
  "success": true,
  "pair": ["ID_USDT"],
  "time": "2023-03-22 12:00:00"
}

```

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|OPENAI_API_KEY|xxxx|API KEY|


> Source (javascript)

``` javascript

// Encapsulated function
function openaiCompletions(content) {
    var url = 'https://api.openai.com/v1/chat/completions';
    var headers = 'Content-Type: application/json\nAuthorization: Bearer ' + OPENAI_API_KEY;
    var data = {
        model: 'gpt-4',//If the API does not have GPT-4 access, it can be modified heregpt-3.5-turbo
        messages: [
          {role: "system", "content": 'Determine the content of the announcement. Is it an announcement about a new trading pair listing on the exchange spot market? If it is, you only need to return it in the JSON format {"success":true,"pair":["ID_USDT"],"time":"2023-03-22 12:00:00"}, with the time converted to Beijing time (UTC+8). If not, return{"success":false}'},
          {role: 'user', content: content}
          ]
    };

    var response = HttpQuery(url, JSON.stringify(data),null,headers,false);
    response = JSON.parse(response)
    return JSON.parse(response.choices[0].message.content);
}

// Usage Example
function main() {
    let announcement = `Fellow Binancians,
Binance will list Radiant Capital (RDNT) in the Innovation Zone and will open trading for these spot trading pairs at 2023-03-30 07:30 (UTC):
New Spot Trading Pairs: RDNT/BTC, RDNT/USDT, RDNT/TUSD
Users can now start depositing RDNT in preparation for trading
Withdrawals for RDNT will open at 2023-03-31 07:30 (UTC)
RDNT Listing Fee: 0 BNB
Users will enjoy zero maker fees on the RDNT/TUSD trading pairs until further notice
Note: The withdrawal open time is an estimated time for users' reference. Users can view the actual status of withdrawals on the withdrawal page.
In addition, Binance will add RDNT as a new borrowable asset with these new margin pairs on Isolated Margin, within 48 hours from 2023-03-30 07:30 (UTC):
New Isolated Margin Pairs: RDNT/USDT
Please refer to Margin Data for a list of the most updated marginable assets and further information on specific limits and rates.
What is Radiant Capital (RDNT)?
Radiant Capital is a decentralized omnichain money market protocol. Users can stake their collateral on one of the major chains and borrow from another chain. RDNT is the utility token for liquidity mining and governance.
Reminder:
The Innovation Zone is a dedicated trading zone where users are able to trade new, innovative tokens that are likely to have higher volatility and pose a higher risk than other tokens.
Before being able to trade in the Innovation Zone, all users are required to visit the web version of the Innovation Zone trading page to carefully read the Binance Terms of Use and complete a questionnaire as part of the Initial Disclaimer. Please note that there will not be any trading restrictions on trading pairs in the Innovation Zone.
RDNT is a relatively new token that poses a higher than normal risk, and as such will likely be subject to high price volatility. Please ensure that you exercise sufficient risk management, have done your own research in regards to RDNT's fundamentals, and fully understand the project before opting to trade the token.
Details:
Radiant Capital Website
RDNT Token Contract Addresses - Arbitrum, BNB Chain
Fees
Rules
Thanks for your support!
Binance Team
2023-03-30`
Log(openaiCompletions(announcement))

}

```

> Detail

https://www.fmz.com/strategy/407636

> Last Modified

2023-04-03 14:03:09
