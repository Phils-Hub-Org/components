import re

class InputSanitizer:
    def sanitizeUsername(username: str, min_length: int=3, max_length: int=20) -> tuple[bool, str]:
        # Username must be between 3 and 20 characters and can contain letters, numbers, and underscores
        if min_length <= len(username) <= max_length and re.match(r'^\w+$', username):
            return True, ""
        else:
            return False, f'Invalid username.\nMust be {min_length}-{max_length} characters long,\nContain only letters, numbers, and underscores.'

    def sanitizeEmail(email: str) -> tuple[bool, str]:
        # Basic regex pattern for email validation
        email_pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if re.match(email_pattern, email):
            return True, ""
        else:
            return False, 'Invalid email format.\nMust be a valid email address.'

    def sanitizePassword(password: str, min_length: int=8, max_length: int=16) -> tuple[bool, str]:
        # Check password length
        if len(password) < min_length or len(password) > max_length:
            return False, f'Password must be between {min_length} and {max_length} characters.'
        
        # Check for at least one uppercase letter
        if not re.search(r'[A-Z]', password):
            return False, 'Password must contain at least one uppercase letter.'

        # Check for at least one lowercase letter
        if not re.search(r'[a-z]', password):
            return False, 'Password must contain at least one lowercase letter.'

        # Check for at least one digit
        if not re.search(r'\d', password):
            return False, 'Password must contain at least one digit.'

        # Check for at least one special character (e.g., !@#$%^&*)
        special_characters = r'[!@#$%^&*(),.?":{}|<>]'
        if not re.search(special_characters, password):
            return False, 'Password must contain at least one special character.'

        # Password passed all checks
        return True, ""

# Example usage
if __name__ == '__main__':
    print(InputSanitizer.sanitizeUsername('myusername', min_length=5, max_length=10))
    print(InputSanitizer.sanitizeEmail('myemail@mydomain.com'))
    print(InputSanitizer.sanitizePassword('MyPassword1!', min_length=8, max_length=16))