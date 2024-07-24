import requests
from requests_oauthlib import OAuth2Session
from oauthlib.oauth2 import BackendApplicationClient

class SchwabAPI:
    def __init__(self, client_id, client_secret, base_url):
        self.client_id = client_id
        self.client_secret = client_secret
        self.base_url = base_url
        self.token_url = f"{base_url}/oauth2/token"
        self.session = self.authenticate()

    def authenticate(self):
        client = BackendApplicationClient(client_id=self.client_id)
        oauth = OAuth2Session(client=client)
        token = oauth.fetch_token(token_url=self.token_url,
                                  client_id=self.client_id,
                                  client_secret=self.client_secret)
        return oauth

    def get_account_info(self):
        url = f"{self.base_url}/accounts"
        response = self.session.get(url)
        return response.json()

    def place_order(self, account_id, order_data):
        url = f"{self.base_url}/accounts/{account_id}/orders"
        response = self.session.post(url, json=order_data)
        return response.json()

    def get_market_data(self, symbol):
        url = f"{self.base_url}/marketdata/{symbol}/quotes"
        response = self.session.get(url)
        return response.json()

# Example usage:
if __name__ == "__main__":
    client_id = 'your_client_id'
    client_secret = 'your_client_secret'
    base_url = 'https://api.schwab.com'

    schwab_api = SchwabAPI(client_id, client_secret, base_url)

    # Get account information
    account_info = schwab_api.get_account_info()
    print(account_info)

    # Place an order
    order_data = {
        "symbol": "AAPL",
        "qty": 10,
        "side": "buy",
        "type": "market",
        "time_in_force": "gtc"
    }
    account_id = 'your_account_id'
    order_response = schwab_api.place_order(account_id, order_data)
    print(order_response)

    # Get market data
    market_data = schwab_api.get_market_data("AAPL")
    print(market_data)
