import pytest
import requests_mock
import os
from py_schwab_wrapper.schwab_api import SchwabAPI
import sys
import json
print(sys.executable)  # This will print the path to the Python interpreter being used


# Mock environment variables
os.environ["SCHWAB_CLIENT_ID"] = "test_client_id"
os.environ["SCHWAB_CLIENT_SECRET"] = "test_client_secret"

@pytest.fixture
def schwab_api():
    return SchwabAPI(client_id=os.getenv("SCHWAB_CLIENT_ID"), client_secret=os.getenv("SCHWAB_CLIENT_SECRET"))

def test_load_token(schwab_api, monkeypatch):
    # Mock the load_token method to simulate a missing or empty token.json file
    def mock_load_token():
        return {"access_token": "", "refresh_token": "", "expires_at": 0}
    
    monkeypatch.setattr(schwab_api, "load_token", mock_load_token)
    
    token = schwab_api.load_token()
    assert "access_token" in token
    assert token["access_token"] == ""
    assert "refresh_token" in token
    assert token["refresh_token"] == ""

def test_save_token(schwab_api, tmpdir, monkeypatch):
    # Override save_token to write to the temp directory
    def mock_save_token(token):
        token_file = tmpdir.join("token.json")
        with token_file.open('w') as f:
            json.dump(token, f, indent=4)
    
    monkeypatch.setattr(schwab_api, "save_token", mock_save_token)
    
    test_token = {"access_token": "123", "refresh_token": "abc", "expires_at": 9999999999}
    schwab_api.save_token(test_token)
    
    token_file = tmpdir.join("token.json")
    assert token_file.read() == '{"access_token": "123", "refresh_token": "abc", "expires_at": 9999999999}'

def test_get_price_history(schwab_api):
    with requests_mock.Mocker() as m:
        # Mock the price history response
        m.get(f"{schwab_api.base_url}/marketdata/v1/pricehistory", json={"symbol": "QQQ", "prices": [100, 101]})

        result = schwab_api.get_price_history(symbol="QQQ", periodType="day", period=1)
        assert result["symbol"] == "QQQ"
        assert "prices" in result
        assert result["prices"] == [100, 101]

def test_refresh_token(schwab_api):
    with requests_mock.Mocker() as m:
        # Mock the token refresh endpoint
        m.post(f"{schwab_api.token_url}", json={"access_token": "new_access", "refresh_token": "new_refresh", "expires_in": 1800})
        
        # Trigger token refresh
        schwab_api.refresh_token()
        
        assert schwab_api.token["access_token"] == "new_access"
        assert schwab_api.token["refresh_token"] == "new_refresh"
        assert schwab_api.token["expires_at"] > time.time()
