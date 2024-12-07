import logging
from typing import Any

logger = logging.getLogger(__name__)

class GlobalsManager:
    """A class for managing globals."""

    GLOBALS = {}

    @classmethod
    def register(cls, key: str, value: Any) -> None:
        """Register a key/value pair."""
        if cls.exists(key):
            raise KeyError(f'Key \'{key}\' already exists.')
        cls.GLOBALS[key] = value
    
    @classmethod
    def unregister(cls, key: str) -> None:
        """Unregister a global."""
        if not cls.exists(key):
            raise KeyError(f'Key \'{key}\' is not registered.')
        del cls.GLOBALS[key]
    
    @classmethod
    def get(cls, key: str) -> Any:
        """Retrieve a value by its key."""
        if not cls.exists(key):
            raise KeyError(f'Key \'{key}\' is not registered.')
        return cls.GLOBALS.get(key)

    @classmethod
    def update(cls, key: str, value: Any) -> None:
        """Update a global."""
        if not cls.exists(key):
            raise KeyError(f'Key \'{key}\' is not registered.')
        cls.GLOBALS[key] = value

    @classmethod
    def exists(cls, key: str) -> bool:
        """Check if a key exists."""
        return key in cls.GLOBALS
    
    @classmethod
    def print_all(cls) -> None:
        """Print the global variables."""
        for key, value in cls.GLOBALS.items():
            logger.info(f'{key}: {value}')

# Example usage
if __name__ == '__main__':
    GlobalsManager.register('key1', 'value1')
    GlobalsManager.register('key2', 'value2')
    GlobalsManager.register('key3', 'value3')
    GlobalsManager.print_all()