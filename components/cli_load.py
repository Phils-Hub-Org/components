import argparse
import logging
import os

logger = logging.getLogger(__name__)

def authenticate() -> bool:
    # Argument parser for the CLI authentication
    parser = argparse.ArgumentParser(description='CLI Authentication Tool')
    parser.add_argument('-u', '--username', required=True, type=str, help='The username for login')
    parser.add_argument('-p', '--password', required=True, type=str, help='The password for login')
    
    # Parse login arguments
    args = parser.parse_args()
    logger.info(f'Authentication attempted for user: {args.username}')

    return validate(args.username, args.password)

def validate(username: str, password: str) -> bool:
    # Get environment variables for authentication
    env_username = os.getenv('CLI_AUTH_USERNAME')
    env_password = os.getenv('CLI_AUTH_PASSWORD')

    if env_username is None or env_password is None:
        logger.error('Error: Environment variables for authentication are not set.')
        return False

    # Check if the provided username and password match the environment variables
    return username == env_username and password == env_password

# Example usage
if __name__ == '__main__':
    if authenticate():
        print('Authentication successful!')
    else:
        print('Authentication failed.')

# python Components\cli_load.py -u admin -p pw
# python Components\cli_load.py -h -u USERNAME -p PASSWORD