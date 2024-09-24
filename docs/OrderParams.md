# OrderRequest Attributes Documentation

## Order-Level Attributes

- **session**:  
  Enum: [ NORMAL, AM, PM, SEAMLESS ]

- **duration**:  
  Enum: [ DAY, GOOD_TILL_CANCEL, FILL_OR_KILL, IMMEDIATE_OR_CANCEL, END_OF_WEEK, END_OF_MONTH, NEXT_END_OF_MONTH, UNKNOWN ]

- **orderType (Request)**:  
  Enum: [ MARKET, LIMIT, STOP, STOP_LIMIT, TRAILING_STOP, CABINET, NON_MARKETABLE, MARKET_ON_CLOSE, EXERCISE, TRAILING_STOP_LIMIT, NET_DEBIT, NET_CREDIT, NET_ZERO, LIMIT_ON_CLOSE ]

- **cancelTime**:  
  Type: string (ISO-8601 date-time)

- **complexOrderStrategyType**:  
  Enum: [ NONE, COVERED, VERTICAL, BACK_RATIO, CALENDAR, DIAGONAL, STRADDLE, STRANGLE, COLLAR_SYNTHETIC, BUTTERFLY, CONDOR, IRON_CONDOR, VERTICAL_ROLL, COLLAR_WITH_STOCK, DOUBLE_DIAGONAL, UNBALANCED_BUTTERFLY, UNBALANCED_CONDOR, UNBALANCED_IRON_CONDOR, UNBALANCED_VERTICAL_ROLL, MUTUAL_FUND_SWAP, CUSTOM ]

- **quantity**:  
  Type: number (double)

- **filledQuantity**:  
  Type: number (double)

- **remainingQuantity**:  
  Type: number (double)

- **destinationLinkName**:  
  Type: string

- **releaseTime**:  
  Type: string (ISO-8601 date-time)

- **stopPrice**:  
  Type: number (double)

- **stopPriceLinkBasis**:  
  Enum: [ MANUAL, BASE, TRIGGER, LAST, BID, ASK, ASK_BID, MARK, AVERAGE ]

- **stopPriceLinkType**:  
  Enum: [ VALUE, PERCENT, TICK ]

- **stopPriceOffset**:  
  Type: number (double)

- **stopType**:  
  Enum: [ STANDARD, BID, ASK, LAST, MARK ]

- **priceLinkBasis**:  
  Enum: [ MANUAL, BASE, TRIGGER, LAST, BID, ASK, ASK_BID, MARK, AVERAGE ]

- **priceLinkType**:  
  Enum: [ VALUE, PERCENT, TICK ]

- **price**:  
  Type: number (double)

- **taxLotMethod**:  
  Enum: [ FIFO, LIFO, HIGH_COST, LOW_COST, AVERAGE_COST, SPECIFIC_LOT, LOSS_HARVESTER ]

## OrderLegCollection Attributes

- **orderLegType**:  
  Enum: [ EQUITY, OPTION, INDEX, MUTUAL_FUND, CASH_EQUIVALENT, FIXED_INCOME, CURRENCY, COLLECTIVE_INVESTMENT ]

- **legId**:  
  Type: integer (int64)

### Instrument Attributes (AccountsInstrument)

- **assetType**:  
  Enum: [ EQUITY, OPTION, INDEX, MUTUAL_FUND, CASH_EQUIVALENT, FIXED_INCOME, CURRENCY, COLLECTIVE_INVESTMENT ]

- **cusip**:  
  Type: string

- **symbol**:  
  Type: string

- **description**:  
  Type: string

- **instrumentId**:  
  Type: integer (int64)

- **netChange**:  
  Type: number (double)

### Instruction, Position, and Quantity

- **instruction**:  
  Enum: [ BUY, SELL, BUY_TO_COVER, SELL_SHORT, BUY_TO_OPEN, BUY_TO_CLOSE, SELL_TO_OPEN, SELL_TO_CLOSE, EXCHANGE, SELL_SHORT_EXEMPT ]

- **positionEffect**:  
  Enum: [ OPENING, CLOSING, AUTOMATIC ]

- **quantity**:  
  Type: number (double)

- **quantityType**:  
  Enum: [ ALL_SHARES, DOLLARS, SHARES ]

- **divCapGains**:  
  Enum: [ REINVEST, PAYOUT ]

- **toSymbol**:  
  Type: string

## Additional Order Attributes

- **activationPrice**:  
  Type: number (double)

- **specialInstruction**:  
  Enum: [ ALL_OR_NONE, DO_NOT_REDUCE, ALL_OR_NONE_DO_NOT_REDUCE ]

- **orderStrategyType**:  
  Enum: [ SINGLE, CANCEL, RECALL, PAIR, FLATTEN, TWO_DAY_SWAP, BLAST_ALL, OCO, TRIGGER ]

- **orderId**:  
  Type: integer (int64)

- **cancelable**:  
  Type: boolean (default: false)

- **editable**:  
  Type: boolean (default: false)

- **status**:  
  Enum: [ AWAITING_PARENT_ORDER, AWAITING_CONDITION, AWAITING_STOP_CONDITION, AWAITING_MANUAL_REVIEW, ACCEPTED, AWAITING_UR_OUT, PENDING_ACTIVATION, QUEUED, WORKING, REJECTED, PENDING_CANCEL, CANCELED, PENDING_REPLACE, REPLACED, FILLED, EXPIRED, NEW, AWAITING_RELEASE_TIME, PENDING_ACKNOWLEDGEMENT, PENDING_RECALL, UNKNOWN ]

- **enteredTime**:  
  Type: string (ISO-8601 date-time)

- **closeTime**:  
  Type: string (ISO-8601 date-time)

- **accountNumber**:  
  Type: integer (int64)

## Order Activity Collection

### Order Activity Attributes

- **activityType**:  
  Enum: [ EXECUTION, ORDER_ACTION ]

- **executionType**:  
  Enum: [ FILL ]

- **quantity**:  
  Type: number (double)

- **orderRemainingQuantity**:  
  Type: number (double)

### ExecutionLegs Attributes

- **legId**:  
  Type: integer (int64)

- **price**:  
  Type: number (double)

- **quantity**:  
  Type: number (double)

- **mismarkedQuantity**:  
  Type: number (double)

- **instrumentId**:  
  Type: integer (int64)

- **time**:  
  Type: string (ISO-8601 date-time)

## ChildOrderStrategies and Other Collections

- **replacingOrderCollection**:  
  List of strings or other types

- **childOrderStrategies**:  
  List of strings or other types

- **statusDescription**:  
  Type: string
