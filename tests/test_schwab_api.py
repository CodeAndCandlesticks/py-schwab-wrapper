import json
import pytest
import requests_mock
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from py_schwab_wrapper.schwab_api import SchwabAPI
from requests.exceptions import HTTPError
from datetime import datetime
import pytz

@pytest.fixture
def schwab_api(monkeypatch, requests_mock):
    # Mock the token refresh POST request
    requests_mock.post(
        "https://api.schwabapi.com/v1/oauth/token",
        json={
            "expires_in": 1800,
            "token_type": "Bearer",
            "scope": "api",
            "refresh_token": "mock_refresh_token",
            "access_token": "mock_access_token",
            "id_token": "mock_id_token",
            "expires_at": 1726754346.9192016
        }
    )
    
    # Mock the load_token function to return a test token
    def mock_load_token(self):
        return {
            "expires_in": 1800,
            "token_type": "Bearer",
            "scope": "api",
            "refresh_token": "mock_refresh_token",
            "access_token": "mock_access_token",
            "id_token": "mock_id_token",
            "expires_at": 1726754346.9192016
        }
    
    # Mock the save_token function to do nothing (prevent writing to file)
    def mock_save_token(self, token_data):
        pass  # Do nothing

    def mock_ensure_valid_token(self):
        pass

    def mock_refresh_token(self):
        pass
    
    # Correct paths for both load_token and save_token
    monkeypatch.setattr('py_schwab_wrapper.schwab_api.SchwabAPI.load_token', mock_load_token)
    monkeypatch.setattr('py_schwab_wrapper.schwab_api.SchwabAPI.save_token', mock_save_token)
    monkeypatch.setattr('py_schwab_wrapper.schwab_api.SchwabAPI.ensure_valid_token', mock_ensure_valid_token)
    monkeypatch.setattr('py_schwab_wrapper.schwab_api.SchwabAPI.refresh_token', mock_refresh_token)
    
    api = SchwabAPI(client_id="test_client_id", client_secret="test_client_secret")

    return api

# Helper functions
def load_test_data(filename):
    with open(f"tests/test_data/{filename}", "r") as f:
        return json.load(f)

def assert_valid_candles(candles):
    for candle in candles:
        assert "open" in candle
        assert "close" in candle
        assert "high" in candle
        assert "low" in candle
        assert "volume" in candle
        assert "datetime" in candle

# Tests Start

def test_get_price_history_camel_case_compatibility(schwab_api, recwarn, requests_mock):
    # Load the mocked API response from a file
    mock_response = load_test_data("QQQ-2024-08-26-5min.json")

    eastern = pytz.timezone('America/New_York')

    # Create a fixed date for August 23, 2024, in the Eastern Timezone
    fixed_date = eastern.localize(datetime(2024, 8, 23))

    # Set the start and end times (9:30 AM and 4:00 PM)
    start_of_day = fixed_date.replace(hour=9, minute=30, second=0, microsecond=0)
    end_of_day = fixed_date.replace(hour=16, minute=0, second=0, microsecond=0)

    # Convert to milliseconds since epoch
    start_date = int(start_of_day.timestamp() * 1000)
    end_date = int(end_of_day.timestamp() * 1000)

    # Mock the price history API endpoint
    url = f"{schwab_api.base_url}/marketdata/v1/pricehistory"
    requests_mock.get(url, json=mock_response)

    result = schwab_api.get_price_history(
        symbol='QQQ', 
        periodType='day',  # Deprecated camelCase
        period=1, 
        frequencyType='minute',  # Deprecated camelCase
        frequency=5, 
        needExtendedHoursData=False,  # Deprecated camelCase
        needPreviousClose=True,  # Deprecated camelCase
        startDate=start_date,  # Deprecated camelCase
        endDate=end_date  # Deprecated camelCase
    )
    
    # Verify the deprecation warnings were triggered
    warnings = [str(w.message) for w in recwarn]
    assert any("periodType" in w for w in warnings)
    assert any("frequencyType" in w for w in warnings)
    assert any("needExtendedHoursData" in w for w in warnings)
    assert any("needPreviousClose" in w for w in warnings)
    assert any("startDate" in w for w in warnings)
    assert any("endDate" in w for w in warnings)

    # Original assertions
    assert "candles" in result
    assert isinstance(result["candles"], list)
    expected_candles_count = 78
    assert len(result["candles"]) < expected_candles_count

    assert "previousClose" in result
    assert result["previousClose"] == 480.0

    assert "previousCloseDate" in result
    assert result["previousCloseDate"] == 1724389200000

    assert "symbol" in result
    assert result["symbol"] == "QQQ"

    assert "empty" in result
    assert result["empty"] is False

    assert_valid_candles(result["candles"])

def test_get_price_history_using_start_date_and_end_date_full_day(schwab_api, requests_mock):
    # Load the mocked API response from a file
    mock_response = load_test_data("QQQ-2024-08-23-5min.json")

    eastern = pytz.timezone('America/New_York')

    # Create a fixed date for August 23, 2024, in the Eastern Timezone
    fixed_date = eastern.localize(datetime(2024, 8, 23))

    # Set the start and end times (9:30 AM and 4:00 PM)
    start_of_day = fixed_date.replace(hour=9, minute=30, second=0, microsecond=0)
    end_of_day = fixed_date.replace(hour=16, minute=0, second=0, microsecond=0)

    # Convert to milliseconds since epoch
    startDate = int(start_of_day.timestamp() * 1000)
    endDate = int(end_of_day.timestamp() * 1000)

    # Mock the price history API endpoint
    url = f"{schwab_api.base_url}/marketdata/v1/pricehistory"
    requests_mock.get(url, json=mock_response)

    # Call the API
    result = schwab_api.get_price_history(
        symbol='QQQ', 
        period_type='day', 
        period=1, 
        frequency_type='minute', 
        frequency=5, 
        need_extended_hours_data=False, 
        need_previous_close=True, 
        start_date=startDate, 
        end_date=endDate
    )
    
    # 1. Assert there's a candles array with exactly 78 candles (full day)
    assert "candles" in result
    assert isinstance(result["candles"], list)
    # There are 390 minutes in a full trading day (9:30 AM to 4:00 PM), so 390 / 5 = 78 candles.
    expected_candles_count = 78
    assert len(result["candles"]) == expected_candles_count

    # 2. Assert there's a previousClose field with value 480.0
    assert "previousClose" in result
    assert result["previousClose"] == 482.5

    # 3. Assert there's a previousCloseDate field with value 1724389200000
    assert "previousCloseDate" in result
    assert result["previousCloseDate"] == 1724216400000

    # 4. Assert the symbol field matches the request (QQQ)
    assert "symbol" in result
    assert result["symbol"] == "QQQ"

    # 5. Assert the empty field is false
    assert "empty" in result
    assert result["empty"] is False

    # 6. Assert that each candle has the required fields
    assert_valid_candles(result["candles"])


def test_get_price_history_using_start_date_and_end_date_partial_day(schwab_api, requests_mock):
    # Load the mocked API response from a file
    mock_response = load_test_data("QQQ-2024-08-26-5min.json")

    eastern = pytz.timezone('America/New_York')

    # Create a fixed date for August 23, 2024, in the Eastern Timezone
    fixed_date = eastern.localize(datetime(2024, 8, 23))

    # Set the start and end times (9:30 AM and 4:00 PM)
    start_of_day = fixed_date.replace(hour=9, minute=30, second=0, microsecond=0)
    end_of_day = fixed_date.replace(hour=16, minute=0, second=0, microsecond=0)

    # Convert to milliseconds since epoch
    startDate = int(start_of_day.timestamp() * 1000)
    endDate = int(end_of_day.timestamp() * 1000)

    # Mock the price history API endpoint
    url = f"{schwab_api.base_url}/marketdata/v1/pricehistory"
    requests_mock.get(url, json=mock_response)

    # Call the method with partial data
    result = schwab_api.get_price_history(
        symbol='QQQ', 
        period_type='day', 
        period=1, 
        frequency_type='minute', 
        frequency=5, 
        need_extended_hours_data=False, 
        need_previous_close=True, 
        start_date=startDate, 
        end_date=endDate
    )
        
    # 1. Assert there's a candles array with less than 78 candles
    assert "candles" in result
    assert isinstance(result["candles"], list)
    expected_candles_count = 78
    assert len(result["candles"]) < expected_candles_count

    # 2. Assert there's a previousClose field with value 480.0
    assert "previousClose" in result
    assert result["previousClose"] == 480.0

    # 3. Assert there's a previousCloseDate field with value 1724389200000
    assert "previousCloseDate" in result
    assert result["previousCloseDate"] == 1724389200000

    # 4. Assert the symbol field matches the request (QQQ)
    assert "symbol" in result
    assert result["symbol"] == "QQQ"

    # 5. Assert the empty field is false
    assert "empty" in result
    assert result["empty"] is False

    # 6. Assert that each candle has the required fields
    assert_valid_candles(result["candles"])


def test_get_price_history_using_minimum_parameters(schwab_api, requests_mock):
    # Load the mocked API response from a file
    mock_response = load_test_data("QQQ-default.json")
    
    # Mock the price history API endpoint
    url = f"{schwab_api.base_url}/marketdata/v1/pricehistory"
    requests_mock.get(url, json=mock_response)

    # Call the method with minimum parameters
    result = schwab_api.get_price_history(symbol='QQQ')

    # 1. Assert there's a candles array with at least the expected number of candles
    assert "candles" in result
    assert isinstance(result["candles"], list)
    expected_candles_count = 9600
    assert len(result["candles"]) > expected_candles_count

    # 2. Assert the symbol field matches the request (QQQ)
    assert "symbol" in result
    assert result["symbol"] == "QQQ"

    # 3. Assert the empty field is false
    assert "empty" in result
    assert result["empty"] is False

    # 4. Assert that each candle has the required fields
    assert_valid_candles(result["candles"])


def test_get_with_retry_unauthorized(schwab_api, requests_mock):
    # Mock the GET request to always raise an HTTPError with a 401 status code
    url = f"{schwab_api.base_url}/marketdata/v1/pricehistory"
    requests_mock.get(url, status_code=401)

    # Use pytest.raises to assert that the correct exception is raised without retrying
    with pytest.raises(HTTPError) as excinfo:
        schwab_api.get_with_retry(
            url=url,
            params={"symbol": "QQQ"}
        )

    # Assert that the HTTPError has the correct status code
    assert excinfo.value.response.status_code == 401

def test_get_account_numbers(schwab_api, requests_mock):
    # Mock response data to simulate the API response
    mock_response_data = [
        {"accountNumber": "123456789", "hashValue": "abcdef12345"},
        {"accountNumber": "987654321", "hashValue": "xyz9876543"}
    ]
    
    # Mock the API endpoint for account numbers
    url = f"{schwab_api.base_url}/trader/v1/accounts/accountNumbers"
    requests_mock.get(url, json=mock_response_data)

    # Call the function
    result = schwab_api.get_account_numbers()

    # Verify that the result matches the mock response
    assert isinstance(result, list)
    assert len(result) == 2
    
    for i, account in enumerate(result):
        assert "accountNumber" in account
        assert "hashValue" in account
        assert account["accountNumber"] == mock_response_data[i]["accountNumber"]
        assert account["hashValue"] == mock_response_data[i]["hashValue"]

# Test the get_orders method
def test_get_orders(schwab_api, requests_mock):
    # Load the sample response from the file you provided
    mock_response = load_test_data("sample_orders.json")
    
    # Mock the API request for orders
    account_hash = "sample_account_hash"
    url = f"{schwab_api.base_url}/trader/v1/accounts/{account_hash}/orders"
    
    requests_mock.get(url, json=mock_response)

    # Call the get_orders method with the mocked response
    result = schwab_api.get_orders(account_hash)

    # Assertions based on the sample data
    assert isinstance(result, list)  # Ensure result is a list
    assert len(result) == 23  # Ensure there are 23 orders in the response

    # Example assertions for the first order
    first_order = result[0]
    assert first_order['session'] == "NORMAL"
    assert first_order['duration'] == "DAY"
    assert first_order['orderType'] == "LIMIT"
    assert first_order['status'] == "FILLED"
    assert first_order['quantity'] == 1.0
    assert first_order['filledQuantity'] == 1.0

    # Ensure the orderLegCollection exists and contains the correct structure
    assert "orderLegCollection" in first_order
    assert len(first_order["orderLegCollection"]) == 1
    assert first_order["orderLegCollection"][0]["instruction"] == "SELL_TO_CLOSE"

def test_post_order_success(schwab_api, requests_mock):
    # Mock the API POST request for a successful order placement
    account_hash = "sample_account_hash"
    order_payload = {"orderType": "LIMIT", "quantity": 10, "symbol": "AAPL"}
    url = f"{schwab_api.base_url}/trader/v1/accounts/{account_hash}/orders"
    
    # Mock the successful response with status 201 and no content
    requests_mock.post(url, status_code=201)

    # Call the post_order method
    result = schwab_api.post_order(account_hash, order_payload)

    # Assert that the result is None for a successful order (since there's no JSON content)
    assert result is None

def test_post_order_error(schwab_api, requests_mock):
    # Mock the API POST request for an invalid order (e.g., bad request)
    account_hash = "sample_account_hash"
    order_payload = {"orderType": "LIMIT", "quantity": 10, "symbol": "AAPL"}
    url = f"{schwab_api.base_url}/trader/v1/accounts/{account_hash}/orders"
    
    # Mock the error response with status 400
    requests_mock.post(url, status_code=400, json={"error": "Bad Request"})

    # Use pytest.raises to check if an HTTPError is raised
    with pytest.raises(HTTPError):
        schwab_api.post_order(account_hash, order_payload)

def test_place_market_order_success(schwab_api, requests_mock):
    # Mock a successful post response for a market order
    account_hash = "sample_account_hash"
    url = f"{schwab_api.base_url}/trader/v1/accounts/{account_hash}/orders"
    
    # Mock a successful response with status 201
    requests_mock.post(url, status_code=201)

    # Call place_single_order for a MARKET order
    result = schwab_api.place_single_order(
        account_hash=account_hash,
        order_type="MARKET",
        quantity=10,
        symbol="AAPL"
    )

    # Assert that the result is None (since the status code is 201 and there is no content)
    assert result is None

def test_place_limit_order_success(schwab_api, requests_mock):
    # Mock a successful post response for a limit order
    account_hash = "sample_account_hash"
    url = f"{schwab_api.base_url}/trader/v1/accounts/{account_hash}/orders"
    
    # Mock a successful response with status 201
    requests_mock.post(url, status_code=201)

    # Call place_single_order for a LIMIT order with a price
    result = schwab_api.place_single_order(
        account_hash=account_hash,
        order_type="LIMIT",
        quantity=10,
        symbol="AAPL",
        price=150.00
    )

    # Assert that the result is None (since the status code is 201 and there is no content)
    assert result is None

def test_place_sell_order_success(schwab_api, requests_mock):
    # Mock a successful post response for a SELL order
    account_hash = "sample_account_hash"
    url = f"{schwab_api.base_url}/trader/v1/accounts/{account_hash}/orders"
    
    # Mock a successful response with status 201
    requests_mock.post(url, status_code=201)

    # Call place_single_order for a SELL order
    result = schwab_api.place_single_order(
        account_hash=account_hash,
        order_type="MARKET",
        quantity=10,
        symbol="AAPL",
        instruction="SELL"
    )

    # Assert that the result is None (since the status code is 201 and there is no content)
    assert result is None

def test_place_order_with_additional_params(schwab_api, requests_mock):
    # Mock a successful post response with additional params
    account_hash = "sample_account_hash"
    url = f"{schwab_api.base_url}/trader/v1/accounts/{account_hash}/orders"
    
    # Mock a successful response with status 201
    requests_mock.post(url, status_code=201)

    # Call place_single_order with extra parameters (e.g., taxLotMethod)
    result = schwab_api.place_single_order(
        account_hash=account_hash,
        order_type="MARKET",
        quantity=10,
        symbol="AAPL",
        taxLotMethod="FIFO"  # Additional param
    )

    # Assert that the result is None (since the status code is 201 and there is no content)
    assert result is None

def test_place_order_error(schwab_api, requests_mock):
    # Mock an error response
    account_hash = "sample_account_hash"
    url = f"{schwab_api.base_url}/trader/v1/accounts/{account_hash}/orders"
    
    # Mock a 400 error response
    requests_mock.post(url, status_code=400, json={"error": "Bad Request"})

    # Call place_single_order and assert that an HTTPError is raised
    with pytest.raises(HTTPError):
        schwab_api.place_single_order(
            account_hash=account_hash,
            order_type="MARKET",
            quantity=10,
            symbol="AAPL"
        )

def test_limit_order_missing_price(schwab_api):
    # Test placing a LIMIT order without specifying a price
    account_hash = "sample_account_hash"

    # Place a LIMIT order without a price, expecting a ValueError
    with pytest.raises(ValueError, match="Price must be provided for LIMIT orders."):
        schwab_api.place_single_order(
            account_hash=account_hash,
            order_type="LIMIT",
            quantity=10,
            symbol="AAPL"
        )

def test_place_oco_order_with_stop_loss_and_profit_target(schwab_api, requests_mock):
    # Mock a successful post response
    account_hash = "sample_account_hash"
    url = f"{schwab_api.base_url}/trader/v1/accounts/{account_hash}/orders"
    
    # Mock a successful response with status 201
    requests_mock.post(url, status_code=201)

    # Call the method with both stop loss and profit target
    result = schwab_api.place_first_triggers_oco_order(
        account_hash=account_hash,
        order_type='LIMIT',
        price=490,
        quantity=1.0,
        symbol='QQQ',
        duration='DAY',  # Can also be 'GOOD_TILL_CANCEL'
        instruction='SELL_SHORT',  # Can also be 'BUY'
        stop_loss=491.00,
        profit_target=480.00
    )

    # Assert that the result is None (since the status code is 201 and there is no content)
    assert result is None

def test_place_oco_order_with_no_stop_loss_or_profit_target(schwab_api):
    # Test placing an OCO order without stop loss or profit target
    account_hash = "sample_account_hash"
    
    # Expect a ValueError or similar behavior if stop loss and profit target are both missing
    with pytest.raises(ValueError, match="Must provide both stop loss AND profit target for OCO"):
        schwab_api.place_first_triggers_oco_order(
            account_hash=account_hash,
            order_type="LIMIT",
            quantity=10,
            symbol="AAPL",
            instruction="BUY",
            price=150.00
        )

def test_place_oco_order_with_only_stop_loss(schwab_api):
    # Test placing an OCO order without stop loss or profit target
    account_hash = "sample_account_hash"
    
    # Expect a ValueError or similar behavior if stop loss and profit target are both missing
    with pytest.raises(ValueError, match="Must provide both stop loss AND profit target for OCO"):
        schwab_api.place_first_triggers_oco_order(
            account_hash=account_hash,
            order_type="LIMIT",
            quantity=10,
            symbol="AAPL",
            instruction="BUY",
            price=150.00,
            stop_loss=140.00
        )

def test_place_oco_order_with_only_profit_target(schwab_api):
    # Test placing an OCO order without stop loss or profit target
    account_hash = "sample_account_hash"
    
    # Expect a ValueError or similar behavior if stop loss and profit target are both missing
    with pytest.raises(ValueError, match="Must provide both stop loss AND profit target for OCO"):
        schwab_api.place_first_triggers_oco_order(
            account_hash=account_hash,
            order_type="LIMIT",
            quantity=10,
            symbol="AAPL",
            instruction="BUY",
            price=150.00,
            profit_target=160.00
        )

def test_place_market_oco_order(schwab_api, requests_mock):
    # Mock a successful post response for a market order
    account_hash = "sample_account_hash"
    url = f"{schwab_api.base_url}/trader/v1/accounts/{account_hash}/orders"
    
    # Mock a successful response with status 201
    requests_mock.post(url, status_code=201)

    # Call the method with MARKET as the order type
    result = schwab_api.place_first_triggers_oco_order(
        account_hash=account_hash,
        order_type='MARKET',
        quantity=1.0,
        symbol='QQQ',
        duration='DAY',  # Can also be 'GOOD_TILL_CANCEL'
        instruction='SELL_SHORT',  # Can also be 'BUY'
        stop_loss=491.00,
        profit_target=480.00
    )

    # Assert that the result is None (since the status code is 201 and there is no content)
    assert result is None

def test_place_oco_order_with_additional_params(schwab_api, requests_mock):
    # Mock a successful post response with additional params
    account_hash = "sample_account_hash"
    url = f"{schwab_api.base_url}/trader/v1/accounts/{account_hash}/orders"
    
    # Mock a successful response with status 201
    requests_mock.post(url, status_code=201)

    # Call the method with extra parameters (e.g., trailType for trailing stop loss)
    result = schwab_api.place_first_triggers_oco_order(
        account_hash=account_hash,
        order_type="LIMIT",
        quantity=10,
        symbol="AAPL",
        price=150.00,
        instruction='BUY',
        stop_loss=140.00,
        profit_target=160.00,
        trailType="PERCENT"  # Additional param
    )

    # Assert that the result is None (since the status code is 201 and there is no content)
    assert result is None

def test_place_oco_order_error(schwab_api, requests_mock):
    # Mock an error response for a failed order placement
    account_hash = "sample_account_hash"
    url = f"{schwab_api.base_url}/trader/v1/accounts/{account_hash}/orders"
    
    # Mock a 400 error response
    requests_mock.post(url, status_code=400, json={"error": "Bad Request"})

    # Call the method and assert that an HTTPError is raised
    with pytest.raises(HTTPError):
        schwab_api.place_first_triggers_oco_order(
            account_hash=account_hash,
            order_type="LIMIT",
            quantity=10,
            symbol="AAPL",
            instruction='BUY',
            price=150.00,
            stop_loss=140.00,
            profit_target=160.00
        )