import requests

def requestsApiEndpoint(config_type: str, url: str, timeout: int = 10) -> dict:
    """ Fetch configuration from the web-hosted API. """
    try:
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()  # Check if the request was successful

        config = response.json()  # Parse JSON response once

        # Check if the config_type is 'all_links' and handle accordingly
        if config_type == 'all':
            # Validate if the response is a dictionary
            if isinstance(config, dict):
                return config  # Return the entire dictionary of links
            else:
                raise ValueError('The API response for all_links is not a valid JSON object.')
        else:
            if isinstance(config, dict):
                if config_type in config:
                    return config[config_type]
                else:
                    raise KeyError(f"The key '{config_type}' was not found in the configuration.")
            else:
                raise ValueError('The API response is not a valid JSON object.')

    except requests.exceptions.Timeout:
        print('The request timed out. Please try again later.')
        raise TimeoutError('The request timed out. Please try again later.')
    except requests.exceptions.RequestException as e:
        print(f'An error occurred while trying to reach the API: {e}')
        raise ConnectionError(f'An error occurred while trying to reach the API: {e}')
    except ValueError as e:
        print(f'Invalid response format: {e}')
        raise ValueError(f'Invalid response format: {e}')
    except KeyError as e:
        print(f'Configuration key error: {e}')
        raise KeyError(f'Configuration key error: {e}')

# Example usage
if __name__ == '__main__':
    # print(requestsApiEndpoint(config_type='subdomain', url='https://phils-hub.com/variantx_client_config.php'))
    # print(requestsApiEndpoint(config_type='port#53563', url='https://phils-hub.com/variantx_client_config.php'))

    try:
        print(requestsApiEndpoint(config_type='all', url='https://phils-hub.com/phils_hub_links.php'))
    except Exception as e:
        print(f'Error: {e}')