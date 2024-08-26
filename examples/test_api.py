# examples/test_api.py

import os
import sys
from datetime import datetime, timedelta
from dotenv import load_dotenv
import pytz
from requests.exceptions import RequestException
import logging

# Add the project root to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from py_schwab_wrapper.schwab_api import SchwabAPI

# Load environment variables from .env file
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)

def get_milliseconds_since_epoch(dt):
    return int(dt.timestamp() * 1000)

def main():
    client_id = os.getenv('SCHWAB_CLIENT_ID')
    client_secret = os.getenv('SCHWAB_CLIENT_SECRET')

    # Enhanced environment variable check
    if not client_id or not client_secret:
        raise ValueError("SCHWAB_CLIENT_ID and SCHWAB_CLIENT_SECRET must be set as environment variables")
    
    # Initialize SchwabAPI with the client credentials
    schwab_api = SchwabAPI(client_id, client_secret)

    try:
        # Set timezone to Eastern (for NYSE trading hours)
        eastern = pytz.timezone('America/New_York')
        now = datetime.now(eastern)
        start_of_day = now.replace(hour=9, minute=30, second=0, microsecond=0)
        end_of_day = now.replace(hour=16, minute=0, second=0, microsecond=0)

        # If the current time is before the start of the trading day, use the previous trading day's times
        if now < start_of_day:
            start_of_day = (start_of_day - timedelta(days=1)).replace(hour=9, minute=30, second=0, microsecond=0)
            end_of_day = (end_of_day - timedelta(days=1)).replace(hour=16, minute=0, second=0, microsecond=0)

        # Convert start and end times to milliseconds since epoch
        startDate = get_milliseconds_since_epoch(start_of_day)
        endDate = get_milliseconds_since_epoch(end_of_day)

        # Log the time range for fetching data
        logging.info(f"Fetching data for symbol QQQ from {start_of_day} to {end_of_day}")

        # Fetch and print price history data for a symbol
        symbol = 'QQQ'
        price_history = schwab_api.get_price_history(
            symbol, 
            periodType='day', 
            period=1, 
            frequencyType='minute', 
            frequency=5, 
            needExtendedHoursData=False, 
            needPreviousClose=True, 
            startDate=startDate, 
            endDate=endDate
        )
        print(f"Price History Data for {symbol}:", price_history)

    except ValueError as ve:
        print("ValueError:", ve)
    except RequestException as re:
        print("Network error:", re)
    except Exception as e:
        print("Unexpected error:", e)

if __name__ == "__main__":
    main()
