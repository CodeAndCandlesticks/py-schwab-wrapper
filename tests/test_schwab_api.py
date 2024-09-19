import json
import pytest
import requests_mock
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
            "access_token": "mock_access_token",
            "expires_in": 3600,
            "token_type": "Bearer"
        }
    )
    
    def mock_load_token():
        return load_test_data("sample_token.json")
    
    api = SchwabAPI(client_id="test_client_id", client_secret="test_client_secret")
    monkeypatch.setattr(api, "load_token", mock_load_token)
    return api

def load_test_data(filename):
    # Helper function to load JSON files from the test_data folder
    with open(f"tests/test_data/{filename}", "r") as f:
        return json.load(f)

def mock_price_history(m, api_url, mock_response):
    m.get(f"{api_url}/marketdata/v1/pricehistory", json=mock_response)

def assert_valid_candles(candles):
    for candle in candles:
        assert "open" in candle
        assert "close" in candle
        assert "high" in candle
        assert "low" in candle
        assert "volume" in candle
        assert "datetime" in candle


def test_get_price_history_camel_case_compatibility(schwab_api, recwarn):
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

    with requests_mock.Mocker() as m:
        # Mock the price history API endpoint
        mock_price_history(m, schwab_api.base_url, mock_response)

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

        for candle in result["candles"]:
            assert "open" in candle
            assert "close" in candle
            assert "high" in candle
            assert "low" in candle
            assert "volume" in candle
            assert "datetime" in candle

def test_get_price_history_using_start_date_and_end_date_full_day(schwab_api):
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

    with requests_mock.Mocker() as m:
        # Mock the price history API endpoint
        mock_price_history(m, schwab_api.base_url, mock_response)

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


def test_get_price_history_using_start_date_and_end_date_partial_day(schwab_api):
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

    with requests_mock.Mocker() as m:
        # Mock the price history API endpoint
        mock_price_history(m, schwab_api.base_url, mock_response)

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


def test_get_price_history_using_minimum_parameters(schwab_api):
    # Load the mocked API response from a file
    # Only minimum parameters will result in 1 min candles for the last 10 trading days
    mock_response = load_test_data("QQQ-default.json")
    
    with requests_mock.Mocker() as m:
        # Mock the price history API endpoint
        mock_price_history(m, schwab_api.base_url, mock_response)

        result = schwab_api.get_price_history(
            symbol='QQQ'
        )
        
        # 1. Assert there's a candles array with exactly 169 candles
        assert "candles" in result
        assert isinstance(result["candles"], list)
        # There are 390 minutes in a RTH day + ETH are 570 candles so there should be a minimum of 9600, the response returns 10038 not sure why
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

def test_get_with_retry_unauthorized(schwab_api):
    with requests_mock.Mocker() as m:
        # Mock the GET request to always raise an HTTPError with a 401 status code
        m.get(f"{schwab_api.base_url}/marketdata/v1/pricehistory", status_code=401)

        # Use pytest.raises to assert that the correct exception is raised without retrying
        with pytest.raises(HTTPError) as excinfo:
            schwab_api.get_with_retry(
                url=f"{schwab_api.base_url}/marketdata/v1/pricehistory",
                params={"symbol": "QQQ"}
            )

        # Assert that the HTTPError has the correct status code
        assert excinfo.value.response.status_code == 401
