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

def save_to_json(api_response, filename):
    """
    Save the API response to a JSON file with indent=4.
    
    :param api_response: The response object from the API call.
    :param filename: The name of the file to save the JSON data to.
    """
    with open(filename, "w") as f:
        json.dump(api_response, f, indent=4)
    print(f"Response saved to {filename}")

# Load environment variables from .env file
load_dotenv()
client_id = os.getenv('SCHWAB_CLIENT_ID')
client_secret = os.getenv('SCHWAB_CLIENT_SECRET')
account_hash = os.getenv('ACCOUNT_HASH_4') # Update according to your implementation

# Check if environment variables are loaded correctly
if not client_id or not client_secret or not account_hash:
    raise ValueError("Missing environment variables: Make sure SCHWAB_CLIENT_ID, SCHWAB_CLIENT_SECRET, and ACCOUNT_HASH_4 are set.")

# Trim account_hash to last 4 characters for display and file naming
account_hash_short = account_hash[-4:]

# Initialize the API wrapper with your credentials
schwab_api = SchwabAPI(client_id=client_id, client_secret=client_secret)

try:
    # Fetch orders for the given account
    orders = schwab_api.get_orders(account_hash=account_hash)
    
    # Generate a filename with a timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"orders_for_{account_hash_short}_{timestamp}.json"
    
    # Save the response to a JSON file
    save_to_json(orders, filename=filename)

except Exception as e:
    print(f"An error occurred while fetching orders: {e}")
