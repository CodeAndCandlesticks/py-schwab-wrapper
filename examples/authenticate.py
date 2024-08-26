# examples/authenticate.py

import os
import sys
import json
from datetime import datetime
from flask import Flask, redirect, request, session
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
secret_key = os.getenv('FLASK_SECRET_KEY', os.urandom(24))

if not client_id or not client_secret:
    raise ValueError("Please set SCHWAB_CLIENT_ID and SCHWAB_CLIENT_SECRET environment variables")

# Flask app setup
app = Flask(__name__)
app.secret_key = secret_key  # Use environment variable or random key

@app.route('/')
def index():
    schwab = OAuth2Session(client_id, redirect_uri=redirect_uri, scope='readonly')
    authorization_url, state = schwab.authorization_url(authorization_base_url)
    session['oauth_state'] = state  # Store state in the session
    print("Redirecting to:", authorization_url)
    return redirect(authorization_url)

@app.route('/callback')
def callback():
    print("Callback received. URL:", request.url)
    
    # Verify the state to prevent CSRF attacks
    if request.args.get('state') != session.get('oauth_state'):
        print("State mismatch: expected", session.get('oauth_state'), "but got", request.args.get('state'))
        return 'State mismatch error.', 400
    
    schwab = OAuth2Session(client_id, redirect_uri=redirect_uri, state=session.get('oauth_state'))
    
    try:
        # Exchange authorization code for access token
        token = schwab.fetch_token(token_url, client_secret=client_secret, authorization_response=request.url)
        print("Fetched Token:", token)
        
        # Save token to a JSON file
        save_token_json(token)
        
        # Display token information for debugging
        token_expiry = token.get('expires_at')
        expiry_datetime = datetime.fromtimestamp(float(token_expiry)).strftime('%Y-%m-%d %H:%M:%S')
        return f'''
        <h1>Authentication successful!</h1>
        <p>You can close this window and run your script again.</p>
        <p>Your Access Token expires at: {expiry_datetime}</p>
        <pre>{json.dumps(token, indent=2)}</pre>
        '''
    except Exception as e:
        print("Error during token fetch:", e)
        return 'Authentication failed. Check console for details.', 500

def save_token_json(token):
    with open('token.json', 'w') as token_file:
        json.dump(token, token_file, indent=4)

if __name__ == '__main__':
    # Run Flask app
    app.run(debug=True, ssl_context=('cert.pem', 'key.pem'))
