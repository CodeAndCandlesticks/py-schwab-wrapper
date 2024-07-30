# examples/authenticate.py

import os
import sys
import json
import time
from datetime import datetime
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
redirect_uri = 'https://127.0.0.1:5000/callback'  # Ensure this matches the Schwab developer settings

if not client_id or not client_secret:
    raise ValueError("Please set SCHWAB_CLIENT_ID and SCHWAB_CLIENT_SECRET environment variables")

# Flask app setup
app = Flask(__name__)

@app.route('/')
def index():
    token = get_token()
    refresh_token = token.get('refresh_token')
    token_expiry = token.get('expires_at')

    if refresh_token and token_expiry:
        try:
            if float(token_expiry) > time.time():
                # Token is still valid, no need to re-authenticate
                expiry_datetime = datetime.fromtimestamp(float(token_expiry)).strftime('%Y-%m-%d %H:%M:%S')
                return f'''
                <h1>Token is still valid!</h1>
                <p>Token expires at: {expiry_datetime}</p>
                <p>You can close this window and run your script again.</p>
                '''
            else:
                # Attempt to refresh the token
                schwab = OAuth2Session(client_id, token=token)
                new_token = schwab.refresh_token(token_url, refresh_token=refresh_token, client_id=client_id, client_secret=client_secret)
                save_token(new_token)
                save_token_json(new_token)
                return '''
                <h1>Token refreshed successfully!</h1>
                <p>You can close this window and run your script again.</p>
                '''
        except Exception as e:
            print("Error during token refresh:", e)

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
        # Exchange authorization code for access token
        token = schwab.fetch_token(token_url, client_secret=client_secret, authorization_response=request.url)
        print("Fetched Token:", token)
        
        # Save token for use in SchwabAPI class
        save_token(token)
        
        # Save token to a JSON file
        save_token_json(token)
        
        # Display token information for debugging
        return f'''
        <h1>Authentication successful!</h1>
        <p>You can close this window and run your script again.</p>
        <pre>{json.dumps(token, indent=2)}</pre>
        '''
    except Exception as e:
        print("Error during token fetch:", e)
        return 'Authentication failed. Check console for details.', 500

def save_token(token):
    os.environ['SCHWAB_ACCESS_TOKEN'] = token['access_token']
    os.environ['SCHWAB_REFRESH_TOKEN'] = token.get('refresh_token', '')
    os.environ['SCHWAB_TOKEN_EXPIRY'] = str(token['expires_at'])
    with open('.env', 'w') as f:
        f.write(f'SCHWAB_ACCESS_TOKEN={token["access_token"]}\n')
        if 'refresh_token' in token:
            f.write(f'SCHWAB_REFRESH_TOKEN={token["refresh_token"]}\n')
        f.write(f'SCHWAB_TOKEN_EXPIRY={token["expires_at"]}\n')

def save_token_json(token):
    with open('token.json', 'w') as token_file:
        json.dump(token, token_file)

def get_token():
    token = {
        'access_token': os.getenv('SCHWAB_ACCESS_TOKEN'),
        'refresh_token': os.getenv('SCHWAB_REFRESH_TOKEN'),
        'expires_at': float(os.getenv('SCHWAB_TOKEN_EXPIRY', 0))
    }
    return token

if __name__ == '__main__':
    # Run Flask app on port 5000
    app.run(debug=True, ssl_context=('cert.pem', 'key.pem'), port=5000)
