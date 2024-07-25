import unittest
from py_schwab_wrapper.schwab_api import SchwabAPI

class TestSchwabAPI(unittest.TestCase):
    def setUp(self):
        self.api = SchwabAPI('your_client_id', 'your_client_secret', 'https://api.schwab.com')

    def test_get_account_info(self):
        response = self.api.get_account_info()
        self.assertIsNotNone(response)

    def test_place_order(self):
        order_data = {
            "symbol": "AAPL",
            "qty": 10,
            "side": "buy",
            "type": "market",
            "time_in_force": "gtc"
        }
        response = self.api.place_order('your_account_id', order_data)
        self.assertIsNotNone(response)

    def test_get_market_data(self):
        response = self.api.get_market_data("AAPL")
        self.assertIsNotNone(response)

if __name__ == '__main__':
    unittest.main()
