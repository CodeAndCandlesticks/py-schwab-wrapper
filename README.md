# py-schwab-wrapper

`py-schwab-wrapper` is a Python wrapper for Schwab's API, designed to handle authentication, token management, and data retrieval from Schwab's market data services. The initial version provides functionality to get price history for a symbol, with OAuth2-based authentication flow.

## Features

Be sure to check out our CHANGELOG for full details on functionality

- OAuth2 authentication and token refresh.
- Fetch historical price data for a symbol.
- Get account information
- Get orders for a specific account
- Place orders with user friendly abstractions.

## Installation

You can install the `py-schwab-wrapper` package via `pip`:

```bash
pip install py-schwab-wrapper
```

## Usage

### Initial Setup

1. **Obtain OAuth Credentials**: You need to get your `client_id` and `client_secret` from Schwab's developer portal.
2. **Set Environment Variables**: You can store these credentials in a `.env` file in your project root.

Example `.env` file:

```bash
SCHWAB_CLIENT_ID=<your_client_id>
SCHWAB_CLIENT_SECRET=<your_client_secret>
```

3. **Authenticate and Generate `token.json`**:
   The first time you use the API, you need to authenticate using Schwab’s OAuth2 flow to generate a `token.json` file. You can use the included `authenticate.py` to handle this process.


## OAuth2 Authentication Flow

Before making API requests, you need to authenticate via Schwab's OAuth2 flow and store the access/refresh tokens in a `token.json` file. Here's how you can do it using the included `authenticate.py` script:

1. Run `authenticate.py` to start the OAuth2 flow:
    ```bash
    python authenticate.py
    ```
2. Follow the instructions in the browser to authorize the application and obtain the tokens.

### A note on authentication
Be mindful if you configure your application's callback URL to be secure `https://127.0.0.1:5000/callback`, you'll need to set up HTTPS for your local Flask server. Here's how you can achieve this:
```
    openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes
```
Follow the prompts to provide the necessary information. This will create key.pem (private key) and cert.pem (certificate) files. And be sure to include them in your .gitignore file!

#### Additional .gitignore recommendations
```
# ...your boilerplate .gitignore file for python...

# Ignore .pem files
cert.pem
key.pem
.pem

# Ignore token.json file if you decide to do local storage of the token
token.json
```

## Example API Usage

Once authenticated, you can use the wrapper to get historical market data, get account information, or place an order. Be sure to check out our examples/ folder.

```python
from py_schwab_wrapper.schwab_api import SchwabAPI
from datetime import datetime, timedelta

# Initialize the API wrapper with your credentials
schwab_api = SchwabAPI(client_id="<your_client_id>", client_secret="<your_client_secret>")

# Define the time range
now = datetime.now()
start_of_day = now.replace(hour=9, minute=30, second=0, microsecond=0)
end_of_day = now.replace(hour=16, minute=0, second=0, microsecond=0)
start_date = int(start_of_day.timestamp() * 1000)
end_date = int(end_of_day.timestamp() * 1000)

# Fetch price history
price_history = schwab_api.get_price_history(
    symbol='QQQ', 
    period_type='day', 
    period=1, 
    frequency_type='minute', 
    frequency=5, 
    need_extended_hours_data=False, 
    need_previous_close=True, 
    start_date=start_date, 
    end_date=end_date
)

print(price_history)
```

## Best Practices for Logging Management

This library uses Python's built-in `logging` module to handle logging messages such as errors, warnings, and debug information. By default, the library does not configure logging on its own, leaving the responsibility of setting up logging to the user. This ensures that logging behavior can be customized to suit your application's needs.

### How Logging Works in the Library

- The library creates its own logger specific to the module using:
  
  ```python
  logger = logging.getLogger(__name__)
  ```

- This allows users to control logging for this library independently of other modules in their application.

### Configuring Logging in Your Application

To enable and control logging for the library, you must configure the logging settings in your application. Here’s a basic example of how to do this:

```python
import logging

# Configure logging for the entire application, including the library
logging.basicConfig(
    level=logging.INFO,  # Set to INFO, DEBUG, or ERROR depending on verbosity required
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]  # Add a FileHandler if needed
)

# Optionally, configure a specific logger for this library
logger = logging.getLogger('schwab_api')  # Replace with the correct logger name
logger.setLevel(logging.DEBUG)  # Set to DEBUG or another level as needed
```

### Best Practices for Logging Management

1. **Leave Logging Configuration to the Application**: 
   - The library does not configure logging (e.g., no `logging.basicConfig()` calls). Users should configure logging as part of their application's setup.

2. **Use Log Levels Appropriately**:
   - The library emits logs at appropriate levels:
     - **DEBUG**: For detailed diagnostic information.
     - **INFO**: For general operational information.
     - **WARNING**: For potentially harmful situations.
     - **ERROR**: For error events that may require attention.
   
   Users can adjust the log level to control verbosity.

3. **Log Output Destinations**:
   - By default, logging outputs to the console, but you can configure logs to be written to a file, external logging services, or other destinations by adding `FileHandler`, `StreamHandler`, or custom handlers.
   
   Example:
   ```python
   logging.basicConfig(
       level=logging.DEBUG,
       format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
       handlers=[
           logging.FileHandler('app.log'),  # Logs to a file
           logging.StreamHandler()  # Also logs to the console
       ]
   )
   ```

4. **Silencing Logs**:
   - If you don’t want to see logs from the library, you can silence them by setting the log level for the library’s logger to `WARNING` or higher:
   
   ```python
   logging.getLogger('schwab_api').setLevel(logging.WARNING)
   ```

### Example Use Case

Here’s an example of configuring logging in a typical application using this library:

```python
import logging
from schwab_api import SchwabAPI

# Set up logging for the application
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Initialize the library
api = SchwabAPI(client_id='your_client_id', client_secret='your_client_secret')

# Perform operations...
```

This gives you full control over how logging is handled in your application and ensures that log messages are informative without being intrusive.


## Contributing

Feel free to contribute by submitting issues or pull requests on the [GitHub repository](https://github.com/CodeAndCandlesticks/py-schwab-wrapper).

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgements

This project was developed with assistance from ChatGPT by OpenAI. 
Also special thanks to [rderik](https://rderik.com/) for the motivation to pursue this project.