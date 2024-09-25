# py_schwab_wrapper/schwab_api.py

import time
import json
from requests.exceptions import RequestException, HTTPError, Timeout, ConnectionError
import base64
from datetime import datetime, timezone
import requests
import warnings
import pytz
from requests.exceptions import HTTPError
from .utils.parameter_utils import get_inverse_instruction

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
        last_exception = None
        for attempt in range(retries):
            try:
                response = self.session.get(url, params=params)
                response.raise_for_status()  # Raise HTTPError for bad responses (4xx, 5xx)
                return response  # Return the full Response object
            except HTTPError as e:
                if e.response.status_code == 401:  # Do not retry on 401 Unauthorized
                    print(f"Unauthorized (401) error: {e}. Not retrying.")
                    raise e
                last_exception = e
                print(f"Attempt {attempt + 1} failed with HTTP status {e.response.status_code}: {e}. Retrying...")
                time.sleep(1)  # Delay before retrying
            except (Timeout, ConnectionError) as e:
                last_exception = e
                print(f"Attempt {attempt + 1} failed: {e}. Retrying...")
                time.sleep(1)  # Delay before retrying
            except RequestException as e:
                # For other kinds of request exceptions, raise immediately without retrying
                print(f"RequestException encountered: {e}.")
                raise e  # Re-raise the exception immediately
        # If all retries are exhausted, raise the last encountered exception
        raise last_exception if last_exception else Exception("Failed after multiple retry attempts")

    def get_price_history(self, symbol, period_type=None, period=None, frequency_type=None, frequency=None, 
                        need_extended_hours_data=None, need_previous_close=None, start_date=None, end_date=None, 
                        periodType=None, frequencyType=None, needExtendedHoursData=None, needPreviousClose=None,
                        startDate = None, endDate = None):
        """
        Retrieve historical price data for a given symbol.

        This method fetches the price history for a specified symbol over a given time period and frequency. 
        It supports both the new snake_case and deprecated camelCase parameter names, issuing deprecation warnings 
        when the old parameters are used.

        :param symbol: The ticker symbol for which to retrieve price history (e.g., 'QQQ').
        :param period_type: The type of period to retrieve (e.g., 'day', 'month'). Default is None.
        :param period: The number of periods to retrieve (e.g., 1, 2). Default is None.
        :param frequency_type: The type of frequency with which to retrieve data (e.g., 'minute', 'daily'). Default is None.
        :param frequency: The frequency with which to retrieve data (e.g., 5 for every 5 minutes). Default is None.
        :param need_extended_hours_data: Whether to include extended hours data. Boolean. Default is None.
        :param need_previous_close: Whether to include the previous close price. Boolean. Default is None.
        :param start_date: The start date for the price history in milliseconds since the epoch. Default is None.
        :param end_date: The end date for the price history in milliseconds since the epoch. Default is None.
        :param periodType: (Deprecated) Use `period_type` instead.
        :param frequencyType: (Deprecated) Use `frequency_type` instead.
        :param needExtendedHoursData: (Deprecated) Use `need_extended_hours_data` instead.
        :param needPreviousClose: (Deprecated) Use `need_previous_close` instead.
        :param startDate: (Deprecated) Use `start_date` instead.
        :param endDate: (Deprecated) Use `end_date` instead.

        :return: A JSON response containing the price history data.
        :raises: HTTPError if the request fails or the response status is not 200.
        :raises: DeprecationWarning when deprecated parameters are used.
        """
        
        # Deprecation warnings for old parameters
        if periodType is not None:
            warnings.warn("The 'periodType' parameter is deprecated, use 'period_type' instead.", DeprecationWarning)
            period_type = periodType
        if frequencyType is not None:
            warnings.warn("The 'frequencyType' parameter is deprecated, use 'frequency_type' instead.", DeprecationWarning)
            frequency_type = frequencyType
        if needExtendedHoursData is not None:
            warnings.warn("The 'needExtendedHoursData' parameter is deprecated, use 'need_extended_hours_data' instead.", DeprecationWarning)
            need_extended_hours_data = needExtendedHoursData
        if needPreviousClose is not None:
            warnings.warn("The 'needPreviousClose' parameter is deprecated, use 'need_previous_close' instead.", DeprecationWarning)
            need_previous_close = needPreviousClose
        if startDate is not None:
            warnings.warn("The 'startDate' parameter is deprecated, use 'start_date' instead.", DeprecationWarning)
            start_date = startDate
        if endDate is not None:
            warnings.warn("The 'endDate' parameter is deprecated, use 'end_date' instead.", DeprecationWarning)
            end_date = endDate
        
        self.ensure_valid_token()
        url = f"{self.base_url}/marketdata/v1/pricehistory"
        params = {'symbol': symbol}
        
        if period_type is not None:
            params['periodType'] = period_type
        if period is not None:
            params['period'] = period
        if frequency_type is not None:
            params['frequencyType'] = frequency_type
        if frequency is not None:
            params['frequency'] = frequency
        if need_extended_hours_data is not None:
            params['needExtendedHoursData'] = str(need_extended_hours_data).lower()
        if need_previous_close is not None:
            params['needPreviousClose'] = str(need_previous_close).lower()
        if start_date is not None:
            params['startDate'] = start_date
        if end_date is not None:
            params['endDate'] = end_date

        response = self.get_with_retry(url, params=params)
        response.raise_for_status()
        return response.json()

    def get_account_numbers(self):
        """
        Get list of account numbers and their encrypted values.

        :return: JSON array containing a list of accountNumber and hashValue.
        """
        self.ensure_valid_token()
        url = f"{self.base_url}/trader/v1/accounts/accountNumbers"

        response = self.get_with_retry(url)
        response.raise_for_status()

        return response.json()
    
    def get_orders(self, account_hash, from_entered_time=None, to_entered_time=None, max_results=None, status=None):
        """
        Retrieve orders for a specific account within a given time range.

        :param account_hash: The hashed account identifier.
        :param from_entered_time: The starting time for the order search (ISO-8601 format). Default is today at 9:30 AM.
        :param to_entered_time: The ending time for the order search (ISO-8601 format). Default is today at 4:00 PM.
        :param max_results: The maximum number of orders to retrieve. Optional. Schwab's default is 3000
        :param status: Filter orders by status (e.g., 'FILLED', 'CANCELED', etc). Optional.
        :return: A JSON response containing the orders.
        :raises HTTPError: If mandatory parameters are missing or if the request fails.
        """

        self.ensure_valid_token()

        # Ensure mandatory parameters are provided
        if account_hash is None:
            raise HTTPError("400 Client Error: Mandatory parameter 'account_hash' is missing.")

        # Set default times if not provided
        eastern = pytz.timezone('America/New_York')
        now = datetime.now(eastern)

        if from_entered_time is None:
            from_entered_time = now.replace(hour=9, minute=30, second=0, microsecond=0).isoformat()
        if to_entered_time is None:
            to_entered_time = now.replace(hour=16, minute=0, second=0, microsecond=0).isoformat()

        # Build URL
        url = f"{self.base_url}/trader/v1/accounts/{account_hash}/orders"

        # Construct the params
        params = {
            'fromEnteredTime': from_entered_time,
            'toEnteredTime': to_entered_time
        }
        if max_results is not None:
            params['maxResults'] = max_results
        if status is not None:
            params['status'] = status

        response = self.get_with_retry(url, params=params)
        response.raise_for_status()
        return response.json()

    def post_order(self, account_hash, order_payload):
        """
        Post an order for a specified account using a fully constructed order payload.
        
        :param account_hash: The hashed account identifier.
        :param order_payload: A dictionary containing the entire order payload as required by the API.
        :return: The API response as a JSON object, or None if the response does not contain JSON.
        :raises HTTPError: If the request fails.
        """

        self.ensure_valid_token()

        # Build URL
        url = f"{self.base_url}/trader/v1/accounts/{account_hash}/orders"

        # Log the payload being sent
        print("POSTing order to URL:", url)
        print("Order payload being sent:", json.dumps(order_payload, indent=4))

        # Use the session's post method without retries
        response = self.session.post(url, json=order_payload)
        response.raise_for_status()

        # Attempt to parse JSON if the response is not empty
        if response.status_code == 201:
            return None  # Returning None because a 201 status typically has no content
        try:
            return response.json()
        except ValueError:
            # Response is not JSON, returning the raw response text
            print("Response did not contain JSON, returning raw text.")
            return response.text

    def place_single_order(self, account_hash, order_type, quantity, symbol, price=None, duration="DAY", session="NORMAL", instruction="BUY", **kwargs):
        """
        Place a single market or limit order without stop loss or profit target.
        
        :param account_hash: The hashed account identifier.
        :param order_type: The type of order (e.g., 'MARKET', 'LIMIT').
        :param quantity: The number of shares to buy/sell.
        :param symbol: The symbol of the security to trade.
        :param price: The price at which to execute the order (used for LIMIT orders).
        :param duration: The duration the order should remain active (default is 'DAY').
        :param session: The session in which the order should be placed (default is 'NORMAL').
        :param action: The action to take (e.g., 'BUY', 'SELL'). Default is 'BUY'.
        :return: The API response as a JSON object.
        """
        if order_type == "LIMIT" and price is None:
            raise ValueError("Price must be provided for LIMIT orders.")
        
        self.ensure_valid_token()

        # Construct the single order payload
        order_payload = {
            "session": session,
            "duration": duration,
            "orderType": order_type,
            "orderLegCollection": [
                {
                    "orderLegType": "EQUITY",
                    "instrument": {
                        "symbol": symbol,
                        "assetType": "EQUITY"
                    },
                    "instruction": instruction,  # Use the action parameter to determine 'BUY' or 'SELL'
                    "positionEffect": "AUTOMATIC",
                    "quantity": quantity
                }
            ],
            "orderStrategyType": "SINGLE"
        }

        # Add price if it's a limit order
        if order_type == "LIMIT" and price:
            order_payload["price"] = price

        # Add additional kwargs
        order_payload.update(kwargs)

        # Send the order
        return self.post_order(account_hash, order_payload)


    def place_first_triggers_oco_order(self, account_hash, order_type, quantity, symbol, instruction, price=None, 
                                    stop_loss=None, profit_target=None, duration="DAY", session="NORMAL", asset_type="EQUITY",
                                    **kwargs):
        """
        Place a First Triggers OCO (One-Cancels-the-Other) order with stop loss and profit target.

        :param account_hash: The hashed account identifier.
        :param order_type: The type of the initial order (e.g., 'MARKET', 'LIMIT').
        :param quantity: The number of shares to buy/sell.
        :param symbol: The symbol of the security to trade.
        :param instruction: The main instruction value (e.g., 'BUY', 'SELL_SHORT').
        :param price: The price at which to execute the primary order (used for LIMIT orders).
        :param stop_loss: The stop loss price.
        :param profit_target: The profit target price.
        :param duration: The duration the order should remain active (default is 'DAY').
        :param session: The session in which the order should be placed (default is 'NORMAL').
        :param asset_type: The type of asset to trade 'EQUITY' or 'OPTION' (default is 'EQUITY')
        :return: The API response as a JSON object.
        """
        self.ensure_valid_token()
        if stop_loss is None or profit_target is None:
            raise ValueError("Must provide both stop loss AND profit target for OCO")


        # Invert the instruction for stop loss and profit target
        inverse_instruction = get_inverse_instruction(instruction=instruction, asset_type=asset_type)

        # Construct the First Triggers OCO order payload
        order_payload = {
            "orderStrategyType": "TRIGGER",
            "session": session,
            "duration": duration,
            "orderType": order_type,
            "price": price if order_type == "LIMIT" else None,  # Only include price for LIMIT orders
            "orderLegCollection": [
                {
                    "instruction": instruction,
                    "quantity": quantity,
                    "instrument": {
                        "assetType": asset_type,
                        "symbol": symbol
                    }
                }
            ],
            "childOrderStrategies": [
                {
                    "orderStrategyType": "OCO",
                    "childOrderStrategies": [
                        {
                            "orderStrategyType": "SINGLE",
                            "session": session,
                            "duration": duration,
                            "orderType": "STOP",
                            "stopPrice": stop_loss,
                            "orderLegCollection": [
                                {
                                    "instruction": inverse_instruction,
                                    "quantity": quantity,
                                    "orderLegType": "EQUITY",
                                    "instrument": {
                                        "assetType": asset_type,
                                        "symbol": symbol
                                    }
                                }
                            ],
                        },
                        {
                            "orderStrategyType": "SINGLE",
                            "session": session,
                            "duration": duration,
                            "orderType": "LIMIT",
                            "price": profit_target,
                            "orderLegCollection": [
                                {
                                    "instruction": inverse_instruction,
                                    "quantity": quantity,
                                    "instrument": {
                                        "assetType": asset_type,
                                        "symbol": symbol
                                    }
                                }
                            ]
                        }
                    ]
                }
            ]
        }

        # Add additional kwargs (e.g., taxLotMethod)
        order_payload.update(kwargs)

        # Send the order
        return self.post_order(account_hash, order_payload)
