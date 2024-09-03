import time
from datetime import datetime, timedelta
import json
import os
from dotenv import load_dotenv

# To use published library, uncomment line below:
# from py_schwab_wrapper.schwab_api import SchwabAPI
# For local development, uncomment code blow:
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from py_schwab_wrapper.schwab_api import SchwabAPI

def display_account_numbers(account_numbers):
    """
    Display account numbers and their corresponding hash values in a user-friendly format.

    Optionally, each account's details can be saved to the .env file.

    :param account_numbers: A list of dictionaries containing account numbers and hash values.
    """
    print("Account Numbers:")
    for i, account in enumerate(account_numbers):
        account_number = account.get("accountNumber", "N/A")
        hash_value = account.get("hashValue", "N/A")
        print(f"{i+1}. Account Number: {account_number}, Hash Value: {hash_value}")
        
        # Optionally save each account to .env
        append_account_to_env(i + 1, account_number, hash_value)


def append_account_to_env(key_integer, account_number, hash_value, env_file=".env"):
    """
    Append an account number and its hash value as key-value pairs to the .env file using a non-sensitive index as the key.

    :param key_integer: The non-sensitive index to associate the values with.
    :param account_number: The account number to be saved.
    :param hash_value: The hash value corresponding to the account number.
    :param env_file: The path to the .env file. Defaults to ".env".
    """
    account_key = f"ACCOUNT_NUMBER_{key_integer}"
    hash_key = f"ACCOUNT_HASH_{key_integer}"

    try:
        with open(env_file, "a") as f:
            f.write(f"{account_key}={account_number}\n")
            f.write(f"{hash_key}={hash_value}\n")
        print(f"Account details saved to {env_file} under keys {account_key} and {hash_key}")
    except Exception as e:
        print(f"An error occurred while writing to {env_file}: {e}")



def main():
    # Load environment variables from .env file
    load_dotenv()
    client_id = os.getenv('SCHWAB_CLIENT_ID')
    client_secret = os.getenv('SCHWAB_CLIENT_SECRET')
    # Initialize the API wrapper with your credentials
    schwab_api = SchwabAPI(client_id=client_id, client_secret=client_secret)

    try:
        # Retrieve account numbers
        account_numbers = schwab_api.get_account_numbers()

        # Display account numbers on the screen
        display_account_numbers(account_numbers)

    except Exception as e:
        print(f"An error occurred while retrieving account numbers: {e}")

if __name__ == "__main__":
    main()
