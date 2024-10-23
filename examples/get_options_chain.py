import time
from prettytable import PrettyTable
from datetime import datetime
import json
import os
from dotenv import load_dotenv
# To use published library, uncomment line below:
# from py_schwab_wrapper.schwab_api import SchwabAPI
# For local development, uncomment code blow:
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from py_schwab_wrapper.schwab_api import SchwabAPI

from requests.exceptions import HTTPError

# Load environment variables from .env file
load_dotenv()
client_id = os.getenv('SCHWAB_CLIENT_ID')
client_secret = os.getenv('SCHWAB_CLIENT_SECRET')

# Initialize the API wrapper with your credentials
schwab_api = SchwabAPI(client_id=client_id, client_secret=client_secret)

symbol = "QQQ"
contract_type = "CALL"
strike_count = 10
include_underlying_quote = True
strategy = "SINGLE"
range_ = "OTM"
# Get today's date in the format YYYY-MM-DD
today = datetime.now().strftime("%Y-%m-%d")

try:
    options_chain = schwab_api.get_options_chain(
        symbol=symbol,
        contract_type=contract_type,
        strike_count=strike_count,
        include_underlying_quote=include_underlying_quote,
        strategy=strategy,
        range_=range_,
        from_date=today,
        to_date=today
    )


    # Extracting call option data from the response
    if 'callExpDateMap' in options_chain:
        print("Option Chain:")
        call_exp_map = options_chain['callExpDateMap']

        # Create a PrettyTable to display the option chain
        table = PrettyTable()
        table.field_names = ["Strike", "Bid", "Ask", "Last", "Volume", "Delta", "Gamma", "Theta", "Vega", "Rho", "Open Interest", "Option Name"]

        for exp_date, strikes in call_exp_map.items():
            for strike_price, options in strikes.items():
                for option in options:
                    strike = option['strikePrice']
                    bid = option.get('bid', 'N/A')
                    ask = option.get('ask', 'N/A')
                    last = option.get('last', 'N/A')
                    volume = option.get('totalVolume', 'N/A')
                    delta = option.get('delta', 'N/A')
                    gamma = option.get('gamma', 'N/A')
                    theta = option.get('theta', 'N/A')
                    vega = option.get('vega', 'N/A')
                    rho = option.get('rho', 'N/A')
                    open_interest = option.get('openInterest', 'N/A')
                    option_name = option.get('symbol','N/A')

                    # Add row to the table
                    table.add_row([strike, bid, ask, last, volume, delta, gamma, theta, vega, rho, open_interest, option_name])

        # Print the table
        print(table)
    else:
        print("No call options data available.")

except Exception as e:
    print(f"An error occurred: {e}")