import time

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

