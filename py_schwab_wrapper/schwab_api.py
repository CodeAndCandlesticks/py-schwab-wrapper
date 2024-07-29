# py_schwab_wrapper/schwab_api.py

import os
import time
from requests_oauthlib import OAuth2Session
from dotenv import load_dotenv
import requests

load_dotenv()

class SchwabAPI:
    def __init__(self, client_id, client_secret, base_url='https://api.schwabapi.com'):
        self.client_id = client_id
        self.client_secret = client_secret
        self.base_url = base_url
        self.token_url = f"{base_url}/v1/oauth/token"
        self.token = self.load_token()
        self.session = self.authenticate()

    def load_token(self):
        token = {
            'access_token': os.getenv('SCHWAB_ACCESS_TOKEN'),
            'refresh_token': os.getenv('SCHWAB_REFRESH_TOKEN'),
            'expires_at': float(os.getenv('SCHWAB_TOKEN_EXPIRY', 0))
        }
        return token

    def save_token(self, token):
        self.token = token
        os.environ['SCHWAB_ACCESS_TOKEN'] = token['access_token']
        os.environ['SCHWAB_REFRESH_TOKEN'] = token.get('refresh_token', '')
        os.environ['SCHWAB_TOKEN_EXPIRY'] = str(token['expires_at'])
        with open('.env', 'w') as f:
            f.write(f'SCHWAB_ACCESS_TOKEN={token["access_token"]}\n')
            if 'refresh_token' in token:
                f.write(f'SCHWAB_REFRESH_TOKEN={token["refresh_token"]}\n')
            f.write(f'SCHWAB_TOKEN_EXPIRY={token["expires_at"]}\n')

    def refresh_token(self):
        extra = {
            'client_id': self.client_id,
            'client_secret': self.client_secret
        }
        oauth = OAuth2Session(self.client_id, token=self.token)
        new_token = oauth.refresh_token(self.token_url, **extra)
        self.save_token(new_token)

    def authenticate(self):
        # Refresh the token if it is expired
        if self.token['expires_at'] < time.time():
            self.refresh_token()
        schwab = OAuth2Session(client_id=self.client_id, token=self.token)
        return schwab

    def get_account_info(self):
        url = f"{self.base_url}/accounts"
        response = self.session.get(url)
        response.raise_for_status()  # Raise an error for bad responses
        return response.json()

    def place_order(self, account_id, order_data):
        url = f"{self.base_url}/accounts/{account_id}/orders"
        response = self.session.post(url, json=order_data)
        response.raise_for_status()  # Raise an error for bad responses
        return response.json()

    def get_market_data(self, symbol):
        url = f"{self.base_url}/marketdata/{symbol}/quotes"
        response = self.session.get(url)
        response.raise_for_status()  # Raise an error for bad responses
        return response.json()

    def get_price_history(self, symbol, periodType='day', period=1, frequencyType='minute', frequency=5, needExtendedHoursData=False, needPreviousClose=True, startDate=None, endDate=None):
        url = f"{self.base_url}/marketdata/v1/pricehistory"
        params = {
            'symbol': symbol,
            'periodType': periodType,
            'period': period,
            'frequencyType': frequencyType,
            'frequency': frequency,
            'needExtendedHoursData': str(needExtendedHoursData).lower(),
            'needPreviousClose': str(needPreviousClose).lower()
        }
        if startDate:
            params['startDate'] = startDate
        if endDate:
            params['endDate'] = endDate

        headers = {
            'accept': 'application/json',
            'Authorization': f'Bearer {self.token["access_token"]}'
        }
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()  # Raise an error for bad responses
        return response.json()
