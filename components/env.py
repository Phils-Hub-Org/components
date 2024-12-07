from enum import Enum
import logging

logger = logging.getLogger(__name__)

class EnvStateEnum(Enum):
    DEVELOPMENT = 'DEV'
    PRODUCTION = 'PROD'

class Env:
    """Environment configuration manager."""
    
    _state: EnvStateEnum = None  # Initialize to None, forcing explicit set

    @classmethod
    def get(cls) -> EnvStateEnum:
        """Retrieve the current environment state."""
        cls._ensureStateIsSet()
        return cls._state

    @classmethod
    def set(cls, env: EnvStateEnum) -> None:
        """Set the environment state."""
        if isinstance(env, EnvStateEnum):
            cls._state = env
            logger.debug(f'Environment set to: {cls._state.value}')
        else:
            logger.warning('Invalid environment state provided; defaulting to DEVELOPMENT.')
            cls._state = EnvStateEnum.DEVELOPMENT

    @classmethod
    def getStr(cls) -> str:
        """Get the environment state as a string."""
        return cls.get().value

    @classmethod
    def _ensureStateIsSet(cls) -> None:
        """Ensure the environment state is set, defaulting to DEVELOPMENT if unset."""
        if cls._state is None:
            logger.warning('Environment state not set. Defaulting to DEVELOPMENT.')
            cls._state = EnvStateEnum.DEVELOPMENT

# Example usage
if __name__ == '__main__':
    Env.set(EnvStateEnum.DEVELOPMENT)
    print(Env.getStr())
    