import time
from datetime import datetime, timedelta
import json
import os
from dotenv import load_dotenv

# To use published library, uncomment line below:
# from py_schwab_wrapper.schwab_api import SchwabAPI
# For local development, uncomment code blow:
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from py_schwab_wrapper.schwab_api import SchwabAPI


def save_price_history_to_json(api_response, filename):
    """
    Save the price history API response to a JSON file with indent=4.
    
    :param api_response: The response object from the API call.
    :param filename: The name of the file to save the JSON data to.
    """
    with open(filename, "w") as f:
        json.dump(api_response, f, indent=4)
    print(f"Price history response saved to {filename}")

def fetch_and_save_price_history(schwab_api, symbol, start_date, end_date):
    """
    Fetch price history data and save it to a JSON file.
    
    :param schwab_api: An instance of SchwabAPI.
    :param symbol: The stock symbol to fetch price history for.
    :param start_date: The start date in milliseconds since epoch.
    :param end_date: The end date in milliseconds since epoch.
    """
    # Fetch price history
    price_history = schwab_api.get_price_history(
        symbol='QQQ', 
        period_type='day', 
        period=1, 
        frequency_type='minute', 
        frequency=5, 
        need_extended_hours_data=False, 
        need_previous_close=True, 
        start_date=start_date, 
        end_date=end_date
    )

    # Save to JSON with a filename based on the current timestamp
    now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    save_price_history_to_json(price_history, filename=f"price_history_{symbol}_{now}.json")


# Load environment variables from .env file
load_dotenv()
client_id = os.getenv('SCHWAB_CLIENT_ID')
client_secret = os.getenv('SCHWAB_CLIENT_SECRET')
# Initialize the API wrapper with your credentials
schwab_api = SchwabAPI(client_id=client_id, client_secret=client_secret)

# Define the time range
while True:
    now = datetime.now()
    start_of_day = now.replace(hour=9, minute=30, second=0, microsecond=0)
    end_of_day = now.replace(hour=16, minute=0, second=0, microsecond=0)
    start_date = int(start_of_day.timestamp() * 1000)
    end_date = int(end_of_day.timestamp() * 1000)

    # Fetch and save price history
    fetch_and_save_price_history(schwab_api, symbol='QQQ', start_date=start_date, end_date=end_date)

    # Wait for 5 minutes (300 seconds)
    time.sleep(300)
