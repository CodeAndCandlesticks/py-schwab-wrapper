
### Documentation: Customizing Option Chain Display

---

### **Overview**

This guide explains how to customize the display of an option chain response from the Schwab API using Python. The goal is to modify the output based on parameters from the API response, allowing you to dynamically select and display relevant fields, including option Greeks, pricing, and volume.

---

### **Functionality Overview**

You will use the Schwab API's `/chains` endpoint to retrieve an option chain for a given symbol and configure which fields to display in a `PrettyTable` format. By modifying the `field_names` and the extraction logic, you can customize which parameters (like bid, ask, delta, etc.) are shown in the output.

---

### **Key Parameters Available from API Response**

Based on the sample response you shared, here are the key fields you can customize:

1. **Option Pricing:**
   - `bid`: The current bid price.
   - `ask`: The current ask price.
   - `last`: The last traded price.

2. **Option Volume & Open Interest:**
   - `totalVolume`: The total volume of contracts traded.
   - `openInterest`: The number of open contracts.

3. **Option Greeks:**
   - `delta`: The sensitivity of the option's price to changes in the price of the underlying asset.
   - `gamma`: The rate of change of delta.
   - `theta`: The time decay of the option's price.
   - `vega`: The sensitivity to changes in volatility.
   - `rho`: The sensitivity to interest rate changes.

4. **Expiration Information:**
   - `expirationDate`: The expiration date of the option.
   - `daysToExpiration`: Days remaining until expiration.
   
5. **Miscellaneous:**
   - `strikePrice`: The strike price of the option.
   - `intrinsicValue`: The portion of the option price that is "in-the-money."
   - `extrinsicValue`: The portion of the option price that is based on time and volatility.

---

### **Customizing the Display**

#### **1. Modify `field_names` in `PrettyTable`:**
   
The `field_names` in `PrettyTable` define the columns shown in the output. You can modify this list based on the parameters you want to include.

For example, to display bid, ask, volume, delta, and expiration date, you would modify the `field_names` like this:

```python
table.field_names = ["Strike", "Bid", "Ask", "Volume", "Delta", "Expiration Date"]
```

#### **2. Dynamically Include Data Fields:**

In the loop that processes the response, you can selectively include or exclude data fields. For example, if you only want to show `delta` and `theta` for an options strategy that relies heavily on these Greeks, modify the loop to extract only those values:

```python
for exp_date, strikes in call_exp_map.items():
    for strike_price, options in strikes.items():
        for option in options:
            strike = option['strikePrice']
            bid = option.get('bid', 'N/A')
            ask = option.get('ask', 'N/A')
            volume = option.get('totalVolume', 'N/A')
            delta = option.get('delta', 'N/A')
            expiration_date = option['expirationDate']

            # Add selected data to the table
            table.add_row([strike, bid, ask, volume, delta, expiration_date])
```

#### **3. Add New Fields as Required:**

If you decide to display additional fields, such as `intrinsicValue` or `extrinsicValue`, simply add them to both the `field_names` and the data extraction logic:

```python
# Add intrinsic and extrinsic value fields
table.field_names = ["Strike", "Bid", "Ask", "Intrinsic Value", "Extrinsic Value", "Volume", "Expiration Date"]

for exp_date, strikes in call_exp_map.items():
    for strike_price, options in strikes.items():
        for option in options:
            strike = option['strikePrice']
            bid = option.get('bid', 'N/A')
            ask = option.get('ask', 'N/A')
            intrinsic_value = option.get('intrinsicValue', 'N/A')
            extrinsic_value = option.get('extrinsicValue', 'N/A')
            volume = option.get('totalVolume', 'N/A')
            expiration_date = option['expirationDate']

            # Add new fields to the table
            table.add_row([strike, bid, ask, intrinsic_value, extrinsic_value, volume, expiration_date])
```

#### **4. Handle Missing Data Gracefully:**

Some fields may not be available in the API response. Use the `get()` method with a default value (`'N/A'`) to handle these cases gracefully. For example:

```python
bid = option.get('bid', 'N/A')
ask = option.get('ask', 'N/A')
delta = option.get('delta', 'N/A')
```

This ensures that if a particular field is missing, your program will continue running, and the missing data will simply be displayed as `'N/A'` in the table.

---

### **Final Example Implementation**

Below is an example showing how you can create a flexible table that displays dynamically based on your chosen parameters:

```python
from schwab_api import SchwabAPI
from datetime import datetime
from prettytable import PrettyTable

def main():
    # Initialize the SchwabAPI with your API key
    api_key = "your_api_key_here"
    schwab = SchwabAPI(api_key)

    # Define parameters for the option chain
    symbol = "QQQ"
    contract_type = "CALL"
    strike_count = 5
    include_underlying_quote = True
    strategy = "SINGLE"
    range_ = "OTM"
    today = datetime.now().strftime("%Y-%m-%d")

    try:
        option_chain = schwab.get_option_chain(
            symbol=symbol,
            contract_type=contract_type,
            strike_count=strike_count,
            include_underlying_quote=include_underlying_quote,
            strategy=strategy,
            range_=range_,
            from_date=today,
            to_date=today
        )

        # Extracting call option data
        if 'callExpDateMap' in option_chain:
            call_exp_map = option_chain['callExpDateMap']

            # Customize the fields you want to display
            table = PrettyTable()
            table.field_names = ["Strike", "Bid", "Ask", "Delta", "Theta", "Volume", "Expiration Date"]

            # Populate the table with selected fields
            for exp_date, strikes in call_exp_map.items():
                for strike_price, options in strikes.items():
                    for option in options:
                        strike = option['strikePrice']
                        bid = option.get('bid', 'N/A')
                        ask = option.get('ask', 'N/A')
                        delta = option.get('delta', 'N/A')
                        theta = option.get('theta', 'N/A')
                        volume = option.get('totalVolume', 'N/A')
                        expiration_date = option['expirationDate']

                        # Add selected data to the table
                        table.add_row([strike, bid, ask, delta, theta, volume, expiration_date])

            # Print the customized table
            print(table)

        else:
            print("No call options data available.")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
```

---

### **Customizing Further**

You can easily modify this code to display any fields from the API response. The flexibility of `PrettyTable` allows you to include or exclude fields dynamically based on your needs. Just adjust the `field_names` and the loop that populates the table to match the data you need.

### **Example Use Cases:**
- **Greeks-Focused Display**: Display only fields related to Delta, Gamma, Theta, Vega, and Rho for analyzing option sensitivity.
- **Price-Focused Display**: Show only Bid, Ask, Last, and Volume for quick trading decisions.
- **Expiration-Focused Display**: Add fields like `daysToExpiration` and `expirationDate` for expiration-specific strategies.

