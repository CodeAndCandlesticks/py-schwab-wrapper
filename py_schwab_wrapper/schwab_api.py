# py_schwab_wrapper/schwab_api.py

import time
import json
from requests.exceptions import RequestException
import base64
from datetime import datetime
import requests

class SchwabAPI:
    def __init__(self, client_id, client_secret, base_url='https://api.schwabapi.com', load_token_func=None, save_token_func=None):
        if not client_id or not client_secret:
            raise ValueError("client_id and client_secret are required for Schwab API access")

        self.client_id = client_id
        self.client_secret = client_secret
        self.base_url = base_url
        self.token_url = f"{self.base_url}/v1/oauth/token"
        
        # Use provided functions for loading and saving tokens, or default to file-based methods
        self.load_token_func = load_token_func or self.load_token
        self.save_token_func = save_token_func or self.save_token
        
        self.session = requests.Session()
        self.token = self.load_token_func()  # Call the provided or default method
        self.ensure_valid_token()

    # Default file-based load_token method
    def load_token(self):
        try:
            with open('token.json', 'r') as token_file:
                token = json.load(token_file)
            return token
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error loading token: {e}")
            return {'access_token': '', 'refresh_token': '', 'expires_at': 0}
        except Exception as e:  # Catch any other unexpected errors
            print(f"Unexpected error during token loading: {e}")
            return {'access_token': '', 'refresh_token': '', 'expires_at': 0}


    # Default file-based save_token method
    def save_token(self, token):
        self.token = token
        with open('token.json', 'w') as token_file:
            json.dump(token, token_file, indent=4)


    def ensure_valid_token(self):
        if 'expires_at' not in self.token or self.token['expires_at'] < time.time():
            self.refresh_token()
        # Add the access token to the session headers
        self.session.headers.update({'Authorization': f'Bearer {self.token["access_token"]}'})

    def refresh_token(self):
        token = self.load_token_func()  # Use load_token_func
        refresh_token = token.get('refresh_token')
        auth_str = f"{self.client_id}:{self.client_secret}"
        base64_auth_str = base64.b64encode(auth_str.encode('utf-8')).decode('utf-8')
        token_expiry = token.get('expires_at')

        if refresh_token:
            if token_expiry and float(token_expiry) > time.time():
                expiry_datetime = datetime.fromtimestamp(float(token_expiry)).strftime('%Y-%m-%d %H:%M:%S')
                print(f'Token is still valid, no need to refresh. Token expires at: {expiry_datetime}')
            else:   
                try:
                    print('Attempting to refresh the token...')

                    headers = {
                        'Authorization': f'Basic {base64_auth_str}',
                        'Content-Type': 'application/x-www-form-urlencoded'
                    }

                    payload = {
                        'grant_type': 'refresh_token',
                        'refresh_token': refresh_token
                    }

                    response = requests.post(self.token_url, headers=headers, data=payload)

                    if response.status_code == 200:
                        new_token = response.json()
                        if 'access_token' in new_token and 'expires_in' in new_token:
                            expires_in = new_token.get('expires_in')
                            if expires_in:
                                new_token['expires_at'] = time.time() + int(expires_in)
                            self.save_token_func(new_token)  # Use save_token_func
                            self.session = requests.Session()
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


    def get_account_info(self):
        url = f"{self.base_url}/accounts"
        try:
            self.ensure_valid_token()
            response = self.session.get(url)
            response.raise_for_status()
            return response.json()
        except requests.HTTPError as http_err:
            if response.status_code == 401:
                print("Unauthorized request. Please check credentials.")
            else:
                print(f"HTTP error occurred: {http_err}")
            raise  # Re-raise the error for upstream handling

    def get_with_retry(self, url, params=None, retries=3):
        for _ in range(retries):
            try:
                response = self.session.get(url, params=params)
                response.raise_for_status()  # Ensure we can raise exceptions for HTTP errors
                return response  # Return the full Response object, not the JSON
            except RequestException as e:
                print(f"Request failed: {e}. Retrying...")
                time.sleep(1)
        raise Exception("Failed after multiple retry attempts")

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

        response = self.get_with_retry(url, params=params)
        response.raise_for_status()
        return response.json()
