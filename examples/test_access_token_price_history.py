# examples/test_api.py

import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def main():
    access_token = os.getenv('SCHWAB_ACCESS_TOKEN')
    if not access_token:
        raise ValueError("Please set SCHWAB_ACCESS_TOKEN in the environment variables")

    # API endpoint and headers
    url = 'https://api.schwabapi.com/marketdata/v1/pricehistory?symbol=AAPL'
    headers = {
        'accept': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }

    # Make the API request
    response = requests.get(url, headers=headers)
    
    # Check for HTTP errors
    response.raise_for_status()

    # Print the response
    data = response.json()
    print("Price History Data for AAPL:", data)

if __name__ == "__main__":
    main()
