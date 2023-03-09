import time


def authenticate(func):
    """
    This is a decorator function that wraps another function 'func'
    """
    def wrapper():
        # Get the path to the config.ini file in the root directory of the Django project
        config_path = os.path.join(os.path.dirname(
            os.path.dirname(os.path.abspath(__file__))), 'config.ini')
        
        # Read the Twitter API credentials from conf/ig.ini
        config = configparser.ConfigParser()
        config.read(config_path)
        consumer_key = config['TwitterAPI']['consumer_key']
        consumer_secret = config['TwitterAPI']['consumer_secret']
        access_token = config['TwitterAPI']['access_token']
        access_token_secret = config['TwitterAPI']['access_token_secret']

        # Authenticate with Twitter API
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        api = tweepy.API(auth)

        # Call the function with the authenticated API object
        func(api)
    return wrapper


def handle_rate_limit_error(func):
    """
    A decorator function that handles rate-limit errors in API requests.
    """
    def wrapper(*args, **kwargs):
        """
        A wrapper function that wraps around the decorated function and handles errors.
        """
        while True:
            try:
                # Try calling the decorated function with the provided arguments and keyword arguments.
                result = func(*args, **kwargs)
                return result
            except Exception as e:
                # If an exception is raised during the function call, handle the error.
                print( e)
                if e.args[0] == "Failed to send request: ('Connection aborted.', OSError(0, 'Error'))":
                    pass
                elif e.args[0] == "429 Too Many Requests":
                    time.sleep(15 * 60)  # Wait for 15 minutes (the time period for resetting the rate limit)
                elif "88 - Rate limit exceeded" in str(e):
                    time.sleep(15 * 60)  # Wait for 15 minutes (the time period for resetting the rate limit)
                else:
                    time.sleep(1 * 60)  # Wait for 1 minutes (the time period for resetting the rate limit)
    return wrapper



