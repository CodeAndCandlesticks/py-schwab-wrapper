# OrderStrategy Attributes Documentation

This section details the attributes that are part of an `OrderStrategy` object, typically used in trading orders to represent strategies like OCO (One-Cancels-the-Other) or OTO (One-Triggers-the-Other).

## Attributes

- **accountNumber** (`string`):  
  The account number associated with the order.

- **advancedOrderType** (`string`):  
  The type of advanced order strategy being used.  
  **Enum Values**:
  - `NONE`
  - `OTO`
  - `OCO`
  - `OTOCO`
  - `OT2OCO`
  - `OT3OCO`
  - `BLAST_ALL`
  - `OTA`
  - `PAIR`

- **closeTime** (`string`):  
  The time when the order was closed, in ISO-8601 date-time format.

- **enteredTime** (`string`):  
  The time when the order was entered, in ISO-8601 date-time format.

- **orderBalance** (`OrderBalance`):  
  Contains balance details for the order.  
  - **orderValue** (`number`): The total value of the order.
  - **projectedAvailableFund** (`number`): The projected available funds after the order.
  - **projectedBuyingPower** (`number`): The projected buying power after the order.
  - **projectedCommission** (`number`): The projected commission for the order.

- **orderStrategyType** (`string`):  
  The type of strategy being used for the order.  
  **Enum Values**:
  - `SINGLE`
  - `CANCEL`
  - `RECALL`
  - `PAIR`
  - `FLATTEN`
  - `TWO_DAY_SWAP`
  - `BLAST_ALL`
  - `OCO`
  - `TRIGGER`

- **orderVersion** (`number`):  
  The version number of the order.

- **session** (`string`):  
  The trading session during which the order is executed.  
  **Enum Values**:
  - `NORMAL`
  - `AM`
  - `PM`
  - `SEAMLESS`

- **status** (`string`):  
  The current status of the order.  
  **Enum Values**:
  - `AWAITING_PARENT_ORDER`
  - `AWAITING_CONDITION`
  - `AWAITING_STOP_CONDITION`
  - `AWAITING_MANUAL_REVIEW`
  - `ACCEPTED`
  - `AWAITING_UR_OUT`
  - `PENDING_ACTIVATION`
  - `QUEUED`
  - `WORKING`
  - `REJECTED`
  - `PENDING_CANCEL`
  - `CANCELED`
  - `PENDING_REPLACE`
  - `REPLACED`
  - `FILLED`
  - `EXPIRED`
  - `NEW`
  - `AWAITING_RELEASE_TIME`
  - `PENDING_ACKNOWLEDGEMENT`
  - `PENDING_RECALL`
  - `UNKNOWN`

- **allOrNone** (`boolean`):  
  Whether the order must be fully filled or not at all.

- **discretionary** (`boolean`):  
  Whether the order is discretionary.

- **duration** (`string`):  
  The duration for which the order is valid.  
  **Enum Values**:
  - `DAY`
  - `GOOD_TILL_CANCEL`
  - `FILL_OR_KILL`
  - `IMMEDIATE_OR_CANCEL`
  - `END_OF_WEEK`
  - `END_OF_MONTH`
  - `NEXT_END_OF_MONTH`
  - `UNKNOWN`

- **filledQuantity** (`number`):  
  The number of units filled for this order.

- **orderType** (`string`):  
  The type of order being placed.  
  **Enum Values**:
  - `MARKET`
  - `LIMIT`
  - `STOP`
  - `STOP_LIMIT`
  - `TRAILING_STOP`
  - `CABINET`
  - `NON_MARKETABLE`
  - `MARKET_ON_CLOSE`
  - `EXERCISE`
  - `TRAILING_STOP_LIMIT`
  - `NET_DEBIT`
  - `NET_CREDIT`
  - `NET_ZERO`
  - `LIMIT_ON_CLOSE`
  - `UNKNOWN`

- **orderValue** (`number`):  
  The total value of the order.

- **price** (`number`):  
  The price at which the order is placed.

- **quantity** (`number`):  
  The quantity of assets involved in the order.

- **remainingQuantity** (`number`):  
  The quantity of the order that has not yet been filled.

- **sellNonMarginableFirst** (`boolean`):  
  Whether to sell non-marginable assets first.

- **settlementInstruction** (`string`):  
  The settlement instruction for the order.  
  **Enum Values**:
  - `REGULAR`
  - `CASH`
  - `NEXT_DAY`
  - `UNKNOWN`

- **strategy** (`string`):  
  The complex order strategy type.  
  **Enum Values**:
  - `NONE`
  - `COVERED`
  - `VERTICAL`
  - `BACK_RATIO`
  - `CALENDAR`
  - `DIAGONAL`
  - `STRADDLE`
  - `STRANGLE`
  - `COLLAR_SYNTHETIC`
  - `BUTTERFLY`
  - `CONDOR`
  - `IRON_CONDOR`
  - `VERTICAL_ROLL`
  - `COLLAR_WITH_STOCK`
  - `DOUBLE_DIAGONAL`
  - `UNBALANCED_BUTTERFLY`
  - `UNBALANCED_CONDOR`
  - `UNBALANCED_IRON_CONDOR`
  - `UNBALANCED_VERTICAL_ROLL`
  - `MUTUAL_FUND_SWAP`
  - `CUSTOM`

- **amountIndicator** (`string`):  
  The unit of measurement for the order amount.  
  **Enum Values**:
  - `DOLLARS`
  - `SHARES`
  - `ALL_SHARES`
  - `PERCENTAGE`
  - `UNKNOWN`

### Order Legs

- **orderLegs** (`OrderLeg[]`):  
  A list of legs associated with the order. Each leg contains the following attributes:
  - **askPrice** (`number`): The ask price for the leg.
  - **bidPrice** (`number`): The bid price for the leg.
  - **lastPrice** (`number`): The last traded price for the leg.
  - **markPrice** (`number`): The mark price for the leg.
  - **projectedCommission** (`number`): The projected commission for the leg.
  - **quantity** (`number`): The quantity involved in the leg.
  - **finalSymbol** (`string`): The final symbol for the leg.
  - **legId** (`number`): The unique ID for the leg.
  - **assetType** (`string`): The asset type for the leg.  
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
  - **instruction** (`string`): The action for the leg.  
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

This documentation outlines the key fields and enums for configuring and managing complex order strategies with multiple legs in a trading system.
