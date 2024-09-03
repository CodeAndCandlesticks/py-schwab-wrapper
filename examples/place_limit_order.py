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
account_hash = os.getenv('ACCOUNT_HASH_4')

# Initialize the API wrapper with your credentials
schwab_api = SchwabAPI(client_id=client_id, client_secret=client_secret)

try:
    # Attempt to place a limit order to sell_short 1 unit of 'QQQ' at $470
    response = schwab_api.place_single_order(
        account_hash=account_hash,
        order_type='LIMIT',
        quantity=1,
        symbol='QQQ',
        price=470,
        duration='DAY', # OR GOOD_TILL_CANCEL
        session='NORMAL',
        instruction= 'SELL_SHORT' # OR BUY
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