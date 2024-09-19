import time
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
account_hash = os.getenv('ACCOUNT_HASH_1')

# Initialize the API wrapper with your credentials
schwab_api = SchwabAPI(client_id=client_id, client_secret=client_secret)

try:
    # Attempt to place a Market order to buy 1 AAPL and trigger an OCO
    response = schwab_api.place_first_triggers_oco_order(
        account_hash=account_hash,
        order_type="MARKET",
        quantity=1,
        symbol="AAPL",
        duration='DAY', # OR GOOD_TILL_CANCEL
        instruction='BUY', # or SELL_SHORT
        stop_loss=140.00,
        profit_target=160.00
    )

    # Handle the response
    if response is None:
        print("Order placed successfully with status 201.")
    else:
        print("Order response:", response)

except HTTPError as http_err:
    print(f"HTTP error occurred: {http_err}")
    if http_err.response is not None:
        try:
            # Attempt to parse the error response as JSON
            error_details = http_err.response.json()
            print("Error details:", error_details)
        except ValueError:
            # If the response isn't JSON, print the raw response text
            print("Non-JSON response content:", http_err.response.text)
except Exception as e:
    print(f"An unexpected error occurred: {e}")