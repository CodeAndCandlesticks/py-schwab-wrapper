### Documentation: `get_options_chain` Method

---

### **Method Overview**

The `get_options_chain` method retrieves an options chain for a specified underlying symbol using Schwab's API. This method allows you to customize the options data returned by specifying various filters like contract type, expiration date, strike price, and options strategy.

---

### **Method Signature**

```python
def get_options_chain(
    symbol: str,
    contract_type: str = "ALL",
    strike_count: int = None,
    include_underlying_quote: bool = False,
    strategy: str = "SINGLE",
    interval: float = None,
    strike: float = None,
    range_: str = None,
    from_date: str = None,
    to_date: str = None,
    volatility: float = None,
    underlying_price: float = None,
    interest_rate: float = None,
    days_to_expiration: int = None,
    exp_month: str = "ALL",
    option_type: str = None,
    entitlement: str = None
) -> dict:
```

---

### **Available Parameters**

Each parameter controls a different aspect of the request to the Schwab API for fetching the option chain data. Below is a breakdown of each parameter and how it should be used.

#### **1. symbol (required)**

- **Type**: `str`
- **Description**: The underlying symbol for which you want to retrieve the options chain. For example, "AAPL" for Apple or "QQQ" for the Invesco QQQ Trust.
- **Example**: `"AAPL"`

#### **2. contract_type**

- **Type**: `str`
- **Default**: `"ALL"`
- **Description**: The type of option contracts to include in the chain.
  - `"CALL"`: Include only call options.
  - `"PUT"`: Include only put options.
  - `"ALL"`: Include both call and put options.
- **Example**: `"CALL"` or `"PUT"`

#### **3. strike_count**

- **Type**: `int`
- **Default**: `None`
- **Description**: The number of strike prices to return above or below the at-the-money strike price. For example, if you set `strike_count=5`, it will return 5 strikes above and 5 strikes below the at-the-money price.
- **Example**: `5`

#### **4. include_underlying_quote**

- **Type**: `bool`
- **Default**: `False`
- **Description**: Specifies whether to include the underlying stock's quote information in the response.
  - `True`: Include the underlying quote.
  - `False`: Exclude the underlying quote.
- **Example**: `True`

#### **5. strategy**

- **Type**: `str`
- **Default**: `"SINGLE"`
- **Description**: Specifies the options strategy to use. Determines how the options data is displayed and calculated.
  - `"SINGLE"`: Return individual options contracts.
  - `"ANALYTICAL"`: Allows theoretical values to be calculated based on the volatility, interest rate, and underlying price.
  - Other values: `"VERTICAL"`, `"CALENDAR"`, `"STRADDLE"`, etc.
- **Example**: `"SINGLE"`, `"VERTICAL"`, `"STRADDLE"`

#### **6. interval**

- **Type**: `float`
- **Default**: `None`
- **Description**: The strike interval for spread strategy chains (used with strategies like `VERTICAL` or `STRADDLE`).
- **Example**: `5.0`

#### **7. strike**

- **Type**: `float`
- **Default**: `None`
- **Description**: The specific strike price to filter by. If specified, only options with this strike price will be returned.
- **Example**: `150.0`

#### **8. range_**

- **Type**: `str`
- **Default**: `None`
- **Description**: Specifies the range of options to return based on their moneyness.
  - `"ITM"`: In-the-money options.
  - `"NTM"`: Near-the-money options.
  - `"OTM"`: Out-of-the-money options.
  - `"ALL"`: All options.
- **Example**: `"OTM"`, `"ITM"`

#### **9. from_date**

- **Type**: `str`
- **Default**: `None`
- **Description**: The starting expiration date of options to include in the chain. Must be in `YYYY-MM-DD` format.
- **Example**: `"2024-10-21"`

#### **10. to_date**

- **Type**: `str`
- **Default**: `None`
- **Description**: The ending expiration date of options to include in the chain. Must be in `YYYY-MM-DD` format.
- **Example**: `"2024-10-21"`

#### **11. volatility**

- **Type**: `float`
- **Default**: `None`
- **Description**: The volatility to use in theoretical calculations (used with the `"ANALYTICAL"` strategy).
- **Example**: `25.0`

#### **12. underlying_price**

- **Type**: `float`
- **Default**: `None`
- **Description**: The price of the underlying asset to use in theoretical calculations (used with the `"ANALYTICAL"` strategy).
- **Example**: `150.0`

#### **13. interest_rate**

- **Type**: `float`
- **Default**: `None`
- **Description**: The interest rate to use in theoretical calculations (used with the `"ANALYTICAL"` strategy).
- **Example**: `1.5`

#### **14. days_to_expiration**

- **Type**: `int`
- **Default**: `None`
- **Description**: The number of days to expiration to use in theoretical calculations (used with the `"ANALYTICAL"` strategy).
- **Example**: `30`

#### **15. exp_month**

- **Type**: `str`
- **Default**: `"ALL"`
- **Description**: Specifies the expiration month of the options to include.
  - `"JAN"`, `"FEB"`, `"MAR"`, etc., to filter by a specific month.
  - `"ALL"`: Include options for all expiration months.
- **Example**: `"OCT"`

#### **16. option_type**

- **Type**: `str`
- **Default**: `None`
- **Description**: Specifies the option type to include.
  - `"S"`: Standard options.
  - `"NS"`: Non-standard options.
  - If not specified, all option types are returned.
- **Example**: `"S"`

#### **17. entitlement**

- **Type**: `str`
- **Default**: `None`
- **Description**: Specifies the entitlement for clients (used with retail tokens).
  - `"PP"`: Paying Pro.
  - `"PN"`: Non-Paying Pro.
  - `"NP"`: Non-Pro.
- **Example**: `"PP"`, `"NP"`

---

### **Response Example**

The method returns a dictionary containing the options chain data, including information about each option contract, Greeks, prices, volume, and more.

Example response:

```json
{
  "symbol": "QQQ",
  "status": "SUCCESS",
  "underlying": {
    "symbol": "QQQ",
    "description": "INVSC QQQ TRUST SRS 1 ETF",
    "change": -0.23,
    "percentChange": -0.05,
    "close": 494.47,
    "quoteTime": 1729535882040,
    "tradeTime": 1729535881008,
    "bid": 494.24,
    "ask": 494.26,
    "last": 494.24,
    "mark": 494.24,
    "markChange": -0.23,
    "markPercentChange": -0.05,
    "bidSize": 11,
    "askSize": 1,
    "highPrice": 496.23,
    "lowPrice": 491.31,
    "openPrice": 493.25,
    "totalVolume": 20265914,
    "exchangeName": "NASDAQ",
    "fiftyTwoWeekHigh": 503.52,
    "fiftyTwoWeekLow": 342.35,
    "delayed": false
  },
  "strategy": "SINGLE",
  "interval": 0.0,
  "isDelayed": false,
  "isIndex": false,
  "interestRate": 4.738,
  "underlyingPrice": 494.25,
  "volatility": 29.0,
  "daysToExpiration": 0.0,
  "numberOfContracts": 5,
  "assetMainType": "EQUITY",
  "assetSubType": "ETF",
  "isChainTruncated": false,
  "callExpDateMap": {
    "2024-10-21:0": {
      "493.0": [
        {
          "putCall": "CALL",
          "symbol": "QQQ 241021C00493000",
          "description": "QQQ 10/21/2024 493.00 C",
          "exchangeName": "OPR",
          "bid": 1.35,
          "ask": 1.39,
          "last": 1.33,
          "mark": 1.37,
          "bidSize": 150,
          "askSize": 1,
          "bidAskSize": "150X1",
          "lastSize": 0,
          "highPrice": 3.5,
          "lowPrice": 0.38,
          "openPrice": 0.0,
          "closePrice": 2.53,
          "totalVolume": 143833,
          "tradeTimeInLong": 1729535877617,
          "quoteTimeInLong": 1729535882310,
          "netChange": -1.2,
          "volatility": 13.804,
          "delta": 0.82,
          "gamma": 0.187,
          "theta": -0.132,
          "vega": 0.026,
          "rho": 0.001,
          "openInterest": 2993,
          "timeValue": 0.09,
          "theoreticalOptionValue": 1.402,
          "theoreticalVolatility": 29.0,
          "strikePrice": 493.0,
          "expirationDate": "2024-10-21T20:00:00.000+00:00",
          "daysToExpiration": 0,
          "expirationType": "W",
          "lastTradingDay": 1729555200000,
          "multiplier": 100.0,
          "settlementType": "P",
          "deliverableNote": "100 QQQ",
          "percentChange": -47.5,
          "markChange": -1.16,
          "markPercentChange": -45.77,
          "intrinsicValue": 1.24,
          "extrinsicValue": 0.09,
          "optionRoot": "QQQ",
          "exerciseType": "A",
          "high52Week": 8.12,
          "low52Week": 0.38,
          "nonStandard": false,
          "pennyPilot": true,
          "inTheMoney": true,
          "mini": false
        }
      ],
      "494.0": [
        {
          "putCall": "CALL",
          "symbol": "QQQ 241021C00494000",
          "description": "QQQ 10/21/2024 494.00 C",
          "exchangeName": "OPR",
          "bid": 0.59,
          "ask": 0.61,
          "last": 0.57,
          "mark": 0.6,
          "bidSize": 82,
          "askSize": 63,
          "bidAskSize": "82X63",
          "lastSize": 0,
          "highPrice": 2.66,
          "lowPrice": 0.18,
          "openPrice": 0.0,
          "closePrice": 1.87,
          "totalVolume": 208836,
          "tradeTimeInLong": 1729535877569,
          "quoteTimeInLong": 1729535882430,
          "netChange": -1.3,
          "volatility": 11.906,
          "delta": 0.589,
          "gamma": 0.325,
          "theta": -0.352,
          "vega": 0.039,
          "rho": 0.001,
          "openInterest": 8456,
          "timeValue": 0.33,
          "theoreticalOptionValue": 0.622,
          "theoreticalVolatility": 29.0,
          "strikePrice": 494.0,
          "expirationDate": "2024-10-21T20:00:00.000+00:00",
          "daysToExpiration": 0,
          "expirationType": "W",
          "lastTradingDay": 1729555200000,
          "multiplier": 100.0,
          "settlementType": "P",
          "deliverableNote": "100 QQQ",
          "percentChange": -69.51,
          "markChange": -1.27,
          "markPercentChange": -67.92,
          "intrinsicValue": 0.24,
          "extrinsicValue": 0.33,
          "optionRoot": "QQQ",
          "exerciseType": "A",
          "high52Week": 7.07,
          "low52Week": 0.18,
          "nonStandard": false,
          "pennyPilot": true,
          "inTheMoney": true,
          "mini": false
        }
      ],
      "495.0": [
        {
          "putCall": "CALL",
          "symbol": "QQQ 241021C00495000",
          "description": "QQQ 10/21/2024 495.00 C",
          "exchangeName": "OPR",
          "bid": 0.15,
          "ask": 0.16,
          "last": 0.16,
          "mark": 0.16,
          "bidSize": 292,
          "askSize": 178,
          "bidAskSize": "292X178",
          "lastSize": 0,
          "highPrice": 1.89,
          "lowPrice": 0.09,
          "openPrice": 0.0,
          "closePrice": 1.29,
          "totalVolume": 211344,
          "tradeTimeInLong": 1729535870819,
          "quoteTimeInLong": 1729535882433,
          "netChange": -1.13,
          "volatility": 10.593,
          "delta": 0.246,
          "gamma": 0.296,
          "theta": -0.155,
          "vega": 0.032,
          "rho": 0.0,
          "openInterest": 7160,
          "timeValue": 0.16,
          "theoreticalOptionValue": 0.155,
          "theoreticalVolatility": 29.0,
          "strikePrice": 495.0,
          "expirationDate": "2024-10-21T20:00:00.000+00:00",
          "daysToExpiration": 0,
          "expirationType": "W",
          "lastTradingDay": 1729555200000,
          "multiplier": 100.0,
          "settlementType": "P",
          "deliverableNote": "100 QQQ",
          "percentChange": -87.6,
          "markChange": -1.13,
          "markPercentChange": -87.98,
          "intrinsicValue": -0.76,
          "extrinsicValue": 0.92,
          "optionRoot": "QQQ",
          "exerciseType": "A",
          "high52Week": 6.78,
          "low52Week": 0.09,
          "nonStandard": false,
          "pennyPilot": true,
          "inTheMoney": false,
          "mini": false
        }
      ],
      ...
    }
  }
}
```

---

### **Example Usage**

Here is an example of calling the `get_options_chain` method to retrieve a filtered option chain for QQQ:

```python
schwab = SchwabAPI(api_key="your_api_key_here")

# Get options chain for QQQ, for today’s expiration, out-of-the-money call options
option_chain = schwab.get_options_chain(
    symbol="QQQ",
    contract_type="CALL",
    strike_count=5,
    include_underlying_quote=True,
    strategy="SINGLE",
    range_="OTM",
    from_date="2024-10-21",
    to_date="2024-10-21"
)

# Process the response
for exp_date, strikes in option_chain['callExpDateMap'].items():
    for strike_price, options in strikes.items():
        for option in options:
            print(f"Strike: {option['strikePrice']}, Bid: {option['bid']}, Ask: {option['ask']}")
```
