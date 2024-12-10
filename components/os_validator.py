from enum import Enum
import platform

class OSValidationStatus:
    def __init__(self, status: 'OSValidationStatusEnum', message: str) -> None:
        self.status = status
        self.message = message

class OSValidationStatusEnum(Enum):
    FAILURE = 0
    SUCCESS = 1

class OSValidator:
    """Single utility class for operating system validation."""

    class OSValidatorEnum(Enum):
        """Operating system types for validation."""
        WINDOWS = 0
        LINUX = 1
        MAC = 2

    # Mapping OSValidatorEnum to sets of system OS strings
    __OS_MAP = {
        OSValidatorEnum.WINDOWS: {'windows', 'win32', 'cygwin'},
        OSValidatorEnum.LINUX: {'linux', 'linux'},
        OSValidatorEnum.MAC: {'darwin', 'macos', 'mac os x'}
    }

    @staticmethod
    def validate(expected_os_enum: 'OSValidator.OSValidatorEnum') -> tuple[bool, str]:
        """Validate the operating system against the expected OS."""
        current_os = platform.system()

        # Check if the expected_os_enum exists in the OS_MAP dictionary
        if expected_os_enum not in OSValidator.__OS_MAP:
            return OSValidationStatus(
                OSValidationStatusEnum.FAILURE,
                f'Unknown operating system: {expected_os_enum}'
            )

        # Validate if the current OS matches the expected OS
        if current_os.lower() in OSValidator.__OS_MAP[expected_os_enum]:
            return OSValidationStatus(
                OSValidationStatusEnum.SUCCESS,
                'Operating system validated.'
            )
        
        return OSValidationStatus(
            OSValidationStatusEnum.FAILURE,
            f'Expected operating system: \'{expected_os_enum.name}\', but found: \'{current_os}\''
        )

# Example usage
if __name__ == '__main__':
    result = OSValidator.validate(OSValidator.OSValidatorEnum.WINDOWS)
    
    if result.status == OSValidationStatusEnum.SUCCESS:
        print(result.message)
    else:
        print(result.message)