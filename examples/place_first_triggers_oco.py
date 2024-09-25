import time
from datetime import datetime
import json
import os
from dotenv import load_dotenv
from requests.exceptions import HTTPError
# from py_schwab_wrapper.schwab_api import SchwabAPI  # Uncomment for published library

import sys # Uncomment for local development
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) # Uncomment for local development
from py_schwab_wrapper.schwab_api import SchwabAPI # Uncomment for local development

# Load environment variables from .env file
load_dotenv()
client_id = os.getenv('SCHWAB_CLIENT_ID')
client_secret = os.getenv('SCHWAB_CLIENT_SECRET')
account_hash = os.getenv('ACCOUNT_HASH_4')

# Check for missing environment variables
if not client_id or not client_secret or not account_hash:
    raise ValueError("Missing necessary environment variables for Schwab API authentication")

# Initialize the API wrapper with your credentials
schwab_api = SchwabAPI(client_id=client_id, client_secret=client_secret)

try:
    # Attempt to place a Market order to buy 1 QQQ and trigger an OCO
    response = schwab_api.place_first_triggers_oco_order(
        account_hash=account_hash,
        order_type='LIMIT',
        price=480,  
        quantity=1,
        symbol='QQQ', # OPTION "SPXW  240925P05720000" or "QQQ   240925P00487000"
        duration='DAY',  # Can also be 'GOOD_TILL_CANCEL'
        instruction='BUY',  
        asset_type='EQUITY',
        stop_loss=479,
        profit_target=490
    )

    # Handle the response
    if response is None:
        print("Order placed successfully with status 201.")
    else:
        print("Order response:", json.dumps(response, indent=4))

except HTTPError as http_err:
    print(f"HTTP error occurred: {http_err}")
    if http_err.response is not None:
        try:
            # Attempt to parse the error response as JSON
            error_details = http_err.response.json()
            print (error_details)
            # Check for both "message" and "errors"
            message = error_details.get('message', 'No message provided')
            errors = error_details.get('errors', [])

            # Print the error message and errors array
            print(f"Error message: {message}")
            if errors:
                print("Errors:")
                for err in errors:
                    print(f"  - {err}")
            else:
                print("No additional errors provided.")

        except ValueError:
            # If the response isn't JSON, print the raw response text
            print("Non-JSON response content:", http_err.response.text)

except Exception as e:
    print(f"An unexpected error occurred: {e}")
