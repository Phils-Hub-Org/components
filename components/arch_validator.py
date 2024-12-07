import platform
from enum import Enum

class ArchValidationStatus:
    def __init__(self, status: 'ArchValidationStatusEnum', message: str) -> None:
        self.status = status
        self.message = message

class ArchValidationStatusEnum(Enum):
    FAILURE = 0
    SUCCESS = 1

class ArchValidator:
    """ Single utility class for architecture validation. """

    class ArchValidatorEnum(Enum):
        """ Architecture types for validation. """
        X86 = 0
        X64 = 1

    # Mapping architecture strings to enum
    __ARCH_MAP = {
        ArchValidatorEnum.X86: {'32', 'x86', 'i386', 'i686', 'arm', 'armhf'},
        ArchValidatorEnum.X64: {'64', 'amd64', 'x64', 'x86_64', 'arm64', 'aarch64', 'ppc64le', 's390x', 'mips64', 'riscv64'}
    }

    @staticmethod
    def validate(expected_arch_enum: 'ArchValidator.ArchValidatorEnum') -> tuple[bool, str]:
        """ Validate the system architecture against expected architecture and return status and message. """
        current_arch = platform.machine()

        # Check if the expected_arch_enum exists in the ARCH_MAP dictionary
        if expected_arch_enum not in ArchValidator.__ARCH_MAP:
            return ArchValidationStatus(
                ArchValidationStatusEnum.FAILURE,
                f'Unknown architecture: {expected_arch_enum}'
            )

        # Validate if the current architecture matches the expected architecture
        if current_arch.lower() in ArchValidator.__ARCH_MAP[expected_arch_enum]:
            return ArchValidationStatus(
                ArchValidationStatusEnum.SUCCESS,
                'Architecture validated.'
            )
        
        return ArchValidationStatus(
            ArchValidationStatusEnum.FAILURE,
            f"Expected architecture: '{expected_arch_enum.name}', but found: '{current_arch}'"
        )

# Example usage
if __name__ == '__main__':
    # An example where a program allows both 32-bit and 64-bit architectures
    
    arch1 = ArchValidator.validate(ArchValidator.ArchValidatorEnum.X86)
    arch2 = ArchValidator.validate(ArchValidator.ArchValidatorEnum.X64)

    if arch1.status == ArchValidationStatusEnum.FAILURE and arch2.status == ArchValidationStatusEnum.FAILURE:
        print(arch1.message, arch2.message)