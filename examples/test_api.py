# examples/test_api.py

import os
import sys
from datetime import datetime, timedelta
from dotenv import load_dotenv
# Add the project root to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from py_schwab_wrapper.schwab_api import SchwabAPI



# Load environment variables from .env file
load_dotenv()

def get_milliseconds_since_epoch(dt):
    return int(dt.timestamp() * 1000)

def main():
    client_id = os.getenv('SCHWAB_CLIENT_ID')
    client_secret = os.getenv('SCHWAB_CLIENT_SECRET')
    
    if not client_id or not client_secret:
        raise ValueError("Please set SCHWAB_CLIENT_ID and SCHWAB_CLIENT_SECRET environment variables")
    
    # Initialize SchwabAPI with the client credentials
    schwab_api = SchwabAPI(client_id, client_secret)
    
    try:
        # Calculate the start and end times for today's trading session
        now = datetime.now()
        start_of_day = now.replace(hour=9, minute=30, second=0, microsecond=0)
        end_of_day = now.replace(hour=16, minute=0, second=0, microsecond=0)
        
        if now < start_of_day:
            # If the current time is before the start of the trading day, use the previous trading day's times
            start_of_day = (start_of_day - timedelta(days=1)).replace(hour=9, minute=30, second=0, microsecond=0)
            end_of_day = (end_of_day - timedelta(days=1)).replace(hour=16, minute=0, second=0, microsecond=0)
        
        startDate = get_milliseconds_since_epoch(start_of_day)
        endDate = get_milliseconds_since_epoch(end_of_day)
        
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
        
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    main()
