# py-schwab-wrapper
A Python wrapper for seamless integration with Schwab's Developer APIs.

# Set Environment Variables
You can set environment variables directly in the terminal or by using a .env file with a library like python-dotenv.

## Option 1: Set Environment Variables in Terminal
Set the environment variables in the terminal before running the script:

On Windows:
```
    set SCHWAB_CLIENT_ID=your_client_id
    set SCHWAB_CLIENT_SECRET=your_client_secret
```
On macOS and Linux:
```
    export SCHWAB_CLIENT_ID=your_client_id
    export SCHWAB_CLIENT_SECRET=your_client_secret
```

## Option 2: Use a .env File with python-dotenv
Install python-dotenv:
```
    pip install python-dotenv
```

Create a .env File:
In the root of your project, create a .env file with the following content:
```
    SCHWAB_CLIENT_ID=your_client_id
    SCHWAB_CLIENT_SECRET=your_client_secret
```

# Configure your application's callback

Yes, you can configure the callback URL to be `https://127.0.0.1:5000/callback`, but you'll need to set up HTTPS for your local Flask server. Here's how you can achieve this:

```
    openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes
```
Follow the prompts to provide the necessary information. This will create key.pem (private key) and cert.pem (certificate) files.



# Example usage:
```
 python authenticate.py // spins up a webserver to obtain initial authentication token

 python token_refresh.py // attempts to retrieve a new token if a token already exists

  python test_api.py // attempts a history quote call using existing token (no auto refresh)
```