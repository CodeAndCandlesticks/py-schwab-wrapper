import os
import sys
import time
from datetime import datetime
from requests_oauthlib import OAuth2Session
import requests
import base64
from dotenv import load_dotenv
from requests.exceptions import RequestException
import logging
import http.client as http_client

# Add the project root to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from py_schwab_wrapper.schwab_api import SchwabAPI

# Load environment variables from .env file
load_dotenv()

# Configuration
client_id = os.getenv('SCHWAB_CLIENT_ID')
client_secret = os.getenv('SCHWAB_CLIENT_SECRET')
token_url = 'https://api.schwabapi.com/v1/oauth/token'


if os.getenv('DEBUG') == '1':
    import logging
    import http.client as http_client
    http_client.HTTPConnection.debuglevel = 1
    logging.basicConfig(level=logging.DEBUG)
    logging.getLogger().setLevel(logging.DEBUG)


if not client_id or not client_secret:
    raise ValueError("Please set SCHWAB_CLIENT_ID and SCHWAB_CLIENT_SECRET environment variables")

def refresh_token():
    schwab_api = SchwabAPI(client_id=client_id, client_secret=client_secret)
    token = schwab_api.load_token()
    refresh_token = token.get('refresh_token')
    # Encode client_id:client_secret in Base64
    auth_str = f"{client_id}:{client_secret}"
    base64_auth_str = base64.b64encode(auth_str.encode('utf-8')).decode('utf-8')
    token_expiry = token.get('expires_at')

    if refresh_token:
        if token_expiry and float(token_expiry) > time.time():
            expiry_datetime = datetime.fromtimestamp(float(token_expiry)).strftime('%Y-%m-%d %H:%M:%S')
            print(f'Token is still valid, no need to refresh. Token expires at: {expiry_datetime}')
        else:   
            try:
                print('Attempting to refresh the token...')

                # Create the headers for the request
                headers = {
                    'Authorization': f'Basic {base64_auth_str}',
                    'Content-Type': 'application/x-www-form-urlencoded'
                }

                # Prepare the payload
                payload = {
                    'grant_type': 'refresh_token',
                    'refresh_token': refresh_token
                }

                # Make the POST request to refresh the token
                response = requests.post(token_url, headers=headers, data=payload)

                # Handle the response
                if response.status_code == 200:
                    new_token = response.json()
                    if 'access_token' in new_token and 'expires_in' in new_token:
                        expires_in = new_token.get('expires_in')
                        if expires_in:
                            new_token['expires_at'] = time.time() + int(expires_in)
                        schwab_api.save_token(new_token)
                        print('Token refreshed and saved successfully!')
                    else:
                        print(f'Unexpected token response: {new_token}')
                elif response.status_code == 401:
                    print('Unauthorized. Check your client_id and client_secret.')
                elif response.status_code == 400:
                    print('Bad request. Check the refresh token or payload.')
                else:
                    print(f'Unexpected error: {response.status_code}')
                        
            except RequestException as e:
                print(f'Network error: {e}')
            except ValueError as e:
                print(f'Error parsing token response: {e}')
    else:
        print('No refresh token available.')

if __name__ == '__main__':
    refresh_token()
