# examples/authenticate.py

import os
import sys
import json
from flask import Flask, redirect, request
from requests_oauthlib import OAuth2Session
from dotenv import load_dotenv
from datetime import datetime

# Add the project root to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Load environment variables from .env file
load_dotenv()

# Configuration
client_id = os.getenv('SCHWAB_CLIENT_ID')
client_secret = os.getenv('SCHWAB_CLIENT_SECRET')
authorization_base_url = 'https://api.schwabapi.com/v1/oauth/authorize'
token_url = 'https://api.schwabapi.com/v1/oauth/token'
redirect_uri = 'https://127.0.0.1/callback'  # Ensure this matches the Schwab developer settings

if not client_id or not client_secret:
    raise ValueError("Please set SCHWAB_CLIENT_ID and SCHWAB_CLIENT_SECRET environment variables")

# Flask app setup
app = Flask(__name__)

def save_token(token):
    os.environ['SCHWAB_ACCESS_TOKEN'] = token['access_token']
    os.environ['SCHWAB_REFRESH_TOKEN'] = token.get('refresh_token', '')
    os.environ['SCHWAB_TOKEN_EXPIRY'] = str(token['expires_at'])
    with open('.env', 'a') as f:
        f.write(f'SCHWAB_ACCESS_TOKEN={token["access_token"]}\n')
        if 'refresh_token' in token:
            f.write(f'SCHWAB_REFRESH_TOKEN={token["refresh_token"]}\n')
        f.write(f'SCHWAB_TOKEN_EXPIRY={token["expires_at"]}\n')

def get_token():
    token = {
        'access_token': os.getenv('SCHWAB_ACCESS_TOKEN'),
        'refresh_token': os.getenv('SCHWAB_REFRESH_TOKEN'),
        'expires_at': float(os.getenv('SCHWAB_TOKEN_EXPIRY', 0))
    }
    return token

@app.route('/')
def index():
    schwab = OAuth2Session(client_id, redirect_uri=redirect_uri, scope='readonly')
    authorization_url, state = schwab.authorization_url(authorization_base_url)
    app.state = state
    print("Redirecting to:", authorization_url)
    return redirect(authorization_url)

@app.route('/callback')
def callback():
    print("Callback received. URL:", request.url)
    
    # Verify the state to prevent CSRF attacks
    if request.args.get('state') != app.state:
        print("State mismatch: expected", app.state, "but got", request.args.get('state'))
        return 'State mismatch error.', 400
    
    schwab = OAuth2Session(client_id, redirect_uri=redirect_uri, state=app.state)
    
    try:
        token = schwab.fetch_token(token_url, client_secret=client_secret, authorization_response=request.url)
        print("Fetched Token:", token)
        
        # Save token for use in SchwabAPI class
        save_token(token)
        
        # Display token information for debugging
        return f'''
        <h1>Authentication successful!</h1>
        <p>You can close this window and run your script again.</p>
        <pre>{json.dumps(token, indent=2)}</pre>
        '''
    except Exception as e:
        print("Error during token fetch:", e)
        return 'Authentication failed. Check console for details.', 500

if __name__ == '__main__':
    # Run Flask app on port 443
    app.run(debug=True, ssl_context=('cert.pem', 'key.pem'), port=443)
