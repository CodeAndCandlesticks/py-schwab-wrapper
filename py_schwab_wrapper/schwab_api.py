# py_schwab_wrapper/schwab_api.py

import os
import time
import logging
import json
from requests_oauthlib import OAuth2Session
from dotenv import load_dotenv, set_key, find_dotenv

class SchwabAPI:
    def __init__(self, client_id=None, client_secret=None, base_url='https://api.schwabapi.com'):
        load_dotenv()
        self.client_id = client_id or os.getenv('SCHWAB_CLIENT_ID')
        self.client_secret = client_secret or os.getenv('SCHWAB_CLIENT_SECRET')
        self.base_url = base_url
        self.token_url = f"{base_url}/v1/oauth/token"
        self.token = self.load_token()
        #self.session = self.authenticate()

    def load_token(self):
        try:
            with open('token.json', 'r') as token_file:
                token = json.load(token_file)
            return token
        except FileNotFoundError:
            return {
                'access_token': '',
                'refresh_token': '',
                'expires_at': 0
            }

    def save_token(self, token):
        self.token = token
        with open('token.json', 'w') as token_file:
            json.dump(token, token_file, indent=4)

    def refresh_token(self):
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

    def authenticate(self):
        if self.token['expires_at'] < time.time():
            self.refresh_token()
        return OAuth2Session(client_id=self.client_id, token=self.token)

    def get_account_info(self):
        url = f"{self.base_url}/accounts"
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()

    def place_order(self, account_id, order_data):
        url = f"{self.base_url}/accounts/{account_id}/orders"
        response = self.session.post(url, json=order_data)
        response.raise_for_status()
        return response.json()

    def get_market_data(self, symbol):
        url = f"{self.base_url}/marketdata/{symbol}/quotes"
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()

    def get_price_history(self, symbol, periodType=None, period=None, frequencyType=None, frequency=None, needExtendedHoursData=None, needPreviousClose=None, startDate=None, endDate=None):
        url = f"{self.base_url}/marketdata/v1/pricehistory"
        params = {'symbol': symbol}
        
        if periodType is not None:
            params['periodType'] = periodType
        if period is not None:
            params['period'] = period
        if frequencyType is not None:
            params['frequencyType'] = frequencyType
        if frequency is not None:
            params['frequency'] = frequency
        if needExtendedHoursData is not None:
            params['needExtendedHoursData'] = str(needExtendedHoursData).lower()
        if needPreviousClose is not None:
            params['needPreviousClose'] = str(needPreviousClose).lower()
        if startDate is not None:
            params['startDate'] = startDate
        if endDate is not None:
            params['endDate'] = endDate

        headers = {
            'accept': 'application/json',
            'Authorization': f'Bearer {self.token["access_token"]}'
        }
        response = self.session.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()
