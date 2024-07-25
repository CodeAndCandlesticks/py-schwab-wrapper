# examples/authenticate.py

import os
import sys
import json
from flask import Flask, redirect, request
from requests_oauthlib import OAuth2Session
from dotenv import load_dotenv

# Add the project root to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Load environment variables from .env file
load_dotenv()

# Configuration
client_id = os.getenv('SCHWAB_CLIENT_ID')
client_secret = os.getenv('SCHWAB_CLIENT_SECRET')
authorization_base_url = 'https://api.schwabapi.com/v1/oauth/authorize'
token_url = 'https://api.schwabapi.com/v1/oauth/token'
redirect_uri = 'https://127.0.0.1:5000/callback'

if not client_id or not client_secret:
    raise ValueError("Please set SCHWAB_CLIENT_ID and SCHWAB_CLIENT_SECRET environment variables")

# Flask app setup
app = Flask(__name__)

@app.route('/')
def index():
    # Redirect user to Schwab authorization URL
    schwab = OAuth2Session(client_id, redirect_uri=redirect_uri, scope='readonly')
    authorization_url, state = schwab.authorization_url(authorization_base_url)
    # Save the state for later verification
    app.state = state
    print("Redirecting to:", authorization_url)
    return redirect(authorization_url)

@app.route('/callback')
def callback():
    # Verify the state to prevent CSRF attacks
    schwab = OAuth2Session(client_id, redirect_uri=redirect_uri, state=app.state)
    print("Authorization Response URL:", request.url)
    
    try:
        token = schwab.fetch_token(token_url, client_secret=client_secret,
                                   authorization_response=request.url)
        # Debug: Print the fetched token
        print("Fetched Token:", token)
        
        # Save token for use in SchwabAPI class
        with open('token.json', 'w') as token_file:
            json.dump(token, token_file)
        
        return 'Authentication successful! You can close this window and run your script again.'
    except Exception as e:
        print("Error during token fetch:", e)
        return 'Authentication failed. Check console for details.'

if __name__ == '__main__':
    app.run(debug=True, ssl_context=('cert.pem', 'key.pem'))
