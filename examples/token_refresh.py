# examples/token_refresh.py

import os
import sys
import time
from datetime import datetime
from requests_oauthlib import OAuth2Session
from dotenv import load_dotenv
from py_schwab_wrapper.schwab_api import SchwabAPI

# Add the project root to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Load environment variables from .env file
load_dotenv()

# Configuration
client_id = os.getenv('SCHWAB_CLIENT_ID')
client_secret = os.getenv('SCHWAB_CLIENT_SECRET')
token_url = 'https://api.schwabapi.com/v1/oauth/token'

if not client_id or not client_secret:
    raise ValueError("Please set SCHWAB_CLIENT_ID and SCHWAB_CLIENT_SECRET environment variables")

def refresh_token():
    schwab_api = SchwabAPI(client_id=client_id, client_secret=client_secret)
    token = schwab_api.load_token()
    refresh_token = token.get('refresh_token')
    print(refresh_token)
    token_expiry = token.get('expires_at')

    if refresh_token and token_expiry:
        try:
            if float(token_expiry) > time.time():
                expiry_datetime = datetime.fromtimestamp(float(token_expiry)).strftime('%Y-%m-%d %H:%M:%S')
                print(f'Token is still valid! Token expires at: {expiry_datetime}')
                return
            else:
                print('Attempting to refresh the token...')
                oauth = OAuth2Session(client_id, token=token)
                new_token = oauth.refresh_token(
                    token_url,
                    refresh_token=refresh_token,
                    client_id=client_id,
                    client_secret=client_secret
                )
                schwab_api.save_token(new_token)
                print('Token refreshed successfully!')
                new_expiry_datetime = datetime.fromtimestamp(float(new_token['expires_at'])).strftime('%Y-%m-%d %H:%M:%S')
                print(f'New token expires at: {new_expiry_datetime}')
        except Exception as e:
            print(f'Error during token refresh: {e}')
    else:
        print('No refresh token available or token expiry not set.')

if __name__ == '__main__':
    refresh_token()
