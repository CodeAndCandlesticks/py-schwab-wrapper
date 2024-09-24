# OrderLeg Attributes Documentation

This section details the attributes that are part of an `OrderLeg` object, typically used in trading orders to represent individual legs of a multi-leg order.

## Attributes

- **askPrice** (`number`):  
  The current ask price of the asset.

- **bidPrice** (`number`):  
  The current bid price of the asset.

- **lastPrice** (`number`):  
  The last traded price of the asset.

- **markPrice** (`number`):  
  The mark price, which is often a midpoint between the bid and ask prices.

- **projectedCommission** (`number`):  
  The estimated commission for executing the order.

- **quantity** (`number`):  
  The quantity of the asset involved in the order.

- **finalSymbol** (`string`):  
  The final symbol representing the asset in the order.

- **legId** (`number`):  
  A unique identifier for this particular order leg.

- **assetType** (`string`):  
  The type of asset being traded.  
  **Enum Values**:
  - `EQUITY`
  - `MUTUAL_FUND`
  - `OPTION`
  - `FUTURE`
  - `FOREX`
  - `INDEX`
  - `CASH_EQUIVALENT`
  - `FIXED_INCOME`
  - `PRODUCT`
  - `CURRENCY`
  - `COLLECTIVE_INVESTMENT`

- **instruction** (`string`):  
  The action to take for this leg of the order.  
  **Enum Values**:
  - `BUY`
  - `SELL`
  - `BUY_TO_COVER`
  - `SELL_SHORT`
  - `BUY_TO_OPEN`
  - `BUY_TO_CLOSE`
  - `SELL_TO_OPEN`
  - `SELL_TO_CLOSE`
  - `EXCHANGE`
  - `SELL_SHORT_EXEMPT`

---

This documentation outlines the key fields in an `OrderLeg`, allowing you to understand the available properties for configuring trading orders.
