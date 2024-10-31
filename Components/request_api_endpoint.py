import requests

def requestsApiEndpoint(config_type , url, timeout=10):
    """Fetch configuration from the web-hosted API"""

    """ Example usage:
    import Abstract.py_utility as PyUtility

    subdomain = PyUtility.requestsApiEndpoint(config_type='subdomain', url='https://phils-hub.com/variantx_client_config.php')
    port = PyUtility.requestsApiEndpoint(config_type='qt_comms_port', url='https://phils-hub.com/variantx_client_config.php')
    """
    try:
        # Fetch configuration from the web-hosted API
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()  # Check if the request was successful (HTTP 200)
        
        config = response.json()

        # Validate if the response is a dictionary and 'which' exists in the config
        if isinstance(config, dict):
            if config_type  in config:
                return config[config_type ]
            else:
                raise KeyError(f"The key '{config_type }' was not found in the configuration.")
        else:
            raise ValueError("The API response is not a valid JSON object.")

    except requests.exceptions.Timeout:
        raise TimeoutError("The request timed out. Please try again later.")
    except requests.exceptions.RequestException as e:
        raise ConnectionError(f"An error occurred while trying to reach the API: {e}")
    except ValueError as e:
        raise ValueError(f"Invalid response format: {e}")
    except KeyError as e:
        raise KeyError(f"Configuration key error: {e}")