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
        self.session = self.authenticate()

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
            json.dump(token, token_file)

    def refresh_token(self):
        logging.basicConfig(level=logging.DEBUG)
        oauth = OAuth2Session(self.client_id, token=self.token)

        # Prepare the request details
        refresh_token_url = self.token_url
        refresh_token = self.token['refresh_token']
        client_id = self.client_id
        client_secret = self.client_secret

        # Print the request details for debugging
        logging.debug(f"Refresh Token URL: {refresh_token_url}")
        logging.debug(f"Refresh Token: {refresh_token}")
        logging.debug(f"Client ID: {client_id}")
        logging.debug(f"Client Secret: {client_secret}")

        try:
            new_token = oauth.refresh_token(
                refresh_token_url,
                refresh_token=refresh_token,
                client_id=client_id,
                client_secret=client_secret
            )
            self.save_token(new_token)
            logging.debug(f"New Token: {json.dumps(new_token, indent=2)}")
        except Exception as e:
            logging.error(f"Error during token refresh: {e}")
            raise e

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
