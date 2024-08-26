import json
import pytest
import requests_mock
from py_schwab_wrapper.schwab_api import SchwabAPI
from datetime import datetime
import pytz

@pytest.fixture
def schwab_api(monkeypatch):
    # Mock the token to simulate a valid token
    def mock_load_token():
        return load_test_data("mock_token.json")
    
    api = SchwabAPI(client_id="test_client_id", client_secret="test_client_secret")
    monkeypatch.setattr(api, "load_token", mock_load_token)
    return api

def load_test_data(filename):
    # Helper function to load JSON files from the test_data folder
    with open(f"tests/test_data/{filename}", "r") as f:
        return json.load(f)

def test_get_price_history_using_startDate_and_endDate_full_day(schwab_api):
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
        m.get(f"{schwab_api.base_url}/marketdata/v1/pricehistory", json=mock_response)

        result = schwab_api.get_price_history(
            symbol='QQQ', 
            periodType='day', 
            period=1, 
            frequencyType='minute', 
            frequency=5, 
            needExtendedHoursData=False, 
            needPreviousClose=True, 
            startDate=startDate, 
            endDate=endDate
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
        for candle in result["candles"]:
            assert "open" in candle
            assert "close" in candle
            assert "high" in candle
            assert "low" in candle
            assert "volume" in candle
            assert "datetime" in candle

def test_get_price_history_using_startDate_and_endDate_partial_day(schwab_api):
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
        m.get(f"{schwab_api.base_url}/marketdata/v1/pricehistory", json=mock_response)

        result = schwab_api.get_price_history(
            symbol='QQQ', 
            periodType='day', 
            period=1, 
            frequencyType='minute', 
            frequency=5, 
            needExtendedHoursData=False, 
            needPreviousClose=True, 
            startDate=startDate, 
            endDate=endDate
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
        for candle in result["candles"]:
            assert "open" in candle
            assert "close" in candle
            assert "high" in candle
            assert "low" in candle
            assert "volume" in candle
            assert "datetime" in candle

def test_get_price_history_using_minimum_parameters(schwab_api):
    # Load the mocked API response from a file
    # Only minimum parameters will result in 1 min candles for the last 10 trading days
    mock_response = load_test_data("QQQ-default.json")
    
    with requests_mock.Mocker() as m:
        # Mock the price history API endpoint
        m.get(f"{schwab_api.base_url}/marketdata/v1/pricehistory", json=mock_response)

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
        for candle in result["candles"]:
            assert "open" in candle
            assert "close" in candle
            assert "high" in candle
            assert "low" in candle
            assert "volume" in candle
            assert "datetime" in candle