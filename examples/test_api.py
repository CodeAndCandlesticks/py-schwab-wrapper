# examples/test_api.py

import os
from py_schwab_wrapper.schwab_api import SchwabAPI

def main():
    client_id = os.getenv('SCHWAB_CLIENT_ID')
    client_secret = os.getenv('SCHWAB_CLIENT_SECRET')

    schwab_api = SchwabAPI(client_id, client_secret)

    try:
        account_info = schwab_api.get_account_info()
        print(account_info)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
