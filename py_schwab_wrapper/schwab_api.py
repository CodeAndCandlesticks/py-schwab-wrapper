# py_schwab_wrapper/schwab_api.py

import json
from requests_oauthlib import OAuth2Session

class SchwabAPI:
    def __init__(self, client_id, client_secret, base_url='https://api.schwabapi.com'):
        self.client_id = client_id
        self.client_secret = client_secret
        self.base_url = base_url
        self.token_url = f"{base_url}/v1/oauth/token"
        self.token = self.load_token()
        self.session = self.authenticate()

    def load_token(self):
        try:
            with open('token.json', 'r') as token_file:
                return json.load(token_file)
        except FileNotFoundError:
            raise FileNotFoundError("Token file not found. Please authenticate first.")

    def authenticate(self):
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
