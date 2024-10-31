"""
How to Use:
    Server-side (DigitalSigning):
        Generate a key pair (server generates its private and public key):
            private_key, public_key = DigitalSigning.generate_key_pair()

        Save the keys to files:
            DigitalSigning.save_key_to_file(private_key, 'private_key.pem', private=True)
            DigitalSigning.save_key_to_file(public_key, 'public_key.pem')

        Sign the data (e.g., an executable):
            data = b"binary data or executable content"
            signature = DigitalSigning.sign_data(data, private_key)
            Send the public key and signature to the client.
"""

"""
How to Use:
    Client-side (SignatureVerification):
        Load the public key:
            public_key = DigitalSigning.load_key_from_file('public_key.pem')

        Verify the signature:
            is_valid = SignatureVerification.verify_signature(data, signature, public_key)
            if is_valid:
                print("Signature is valid!")
            else:
                print("Signature is invalid!")
"""

"""
Conclusion:
    The DigitalSigning class on the server side handles key generation and signing.
    The SignatureVerification class on the client side handles signature verification.
    The modules are modular, so they can be reused across projects for any server/client architecture.
    You can add more utility functions if needed, but this structure provides a clean and simple approach for digital signing and verification.
"""

import logging
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.hazmat.backends import default_backend

logger = logging.getLogger(__name__)

class DigitalSigning:
    
    @staticmethod
    def generate_key_pair():
        """Generates and returns a private and public key pair"""
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )
        public_key = private_key.public_key()
        return private_key, public_key

    @staticmethod
    def save_key_to_file(key, path, private=False):
        """Saves a private or public key to a file"""
        if private:
            pem = key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            )
        else:
            pem = key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            )
        with open(path, 'wb') as f:
            f.write(pem)

    @staticmethod
    def load_key_from_file(path, private=False):
        """Loads a private or public key from a file"""
        with open(path, 'rb') as f:
            key_bytes = f.read()
        
        if private:
            return serialization.load_pem_private_key(key_bytes, password=None, backend=default_backend())
        else:
            return serialization.load_pem_public_key(key_bytes, backend=default_backend())

    @staticmethod
    def sign_data(data, private_key):
        """Signs the data using the provided private key"""
        signature = private_key.sign(
            data,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return signature

    @staticmethod
    def save_signature_to_file(signature, path):
        """Saves the signature to a file"""
        with open(path, 'wb') as f:
            f.write(signature)
    
    @staticmethod
    def load_signature_from_file(path):
        """Loads the signature from a file"""
        with open(path, 'rb') as f:
            signature = f.read()
        return signature

    @staticmethod
    def verify_signature(data, signature, public_key):
        """Verifies the provided signature using the public key"""
        try:
            public_key.verify(
                signature,
                data,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
            return True
        except Exception as e:
            print(f"Verification failed: {e}")
            return False

if __name__ == '__main__':
    import os, sys
    proj_root = os.getcwd()
    if proj_root not in sys.path:
        sys.path.insert(0, proj_root)
    import Utils.py_utility as PyUtility

    # Server-side (DigitalSigning):

    # Generate a key pair (server generates its private and public key):
    private_key, public_key = DigitalSigning.generate_key_pair()

    # Save the keys to files:
    DigitalSigning.save_key_to_file(private_key, os.path.join(os.getcwd(), 'Tests', 'client_exe_private_key.pem'), private=True)
    DigitalSigning.save_key_to_file(public_key, os.path.join(os.getcwd(), 'Tests', 'client_exe_public_key.pem'))

    # Get the data to sign (e.g., an executable):
    data = PyUtility.readFromFile(os.path.join(os.getcwd(), 'Tests', 'fake_exe.py')).encode()
    # print(f"Data to sign: {data}")

    data = PyUtility.readFromFile(os.path.join(os.getcwd(), 'Tests', 'digital_signing.py')).encode()
    print(f"Data to sign: {data}")

    # Sign the data (e.g., an executable):
    signature = DigitalSigning.sign_data(data, private_key)

    # Save the signature to a file:
    DigitalSigning.save_signature_to_file(signature, os.path.join(os.getcwd(), 'Tests', 'client_exe_signature.bin'))

    # Send the public key and signature to the client.

    ####################

    # # Client-side (SignatureVerification):
    
    # # Load the public key:
    # public_key = DigitalSigning.load_key_from_file(os.path.join(os.getcwd(), 'Tests', 'client_exe_public_key.pem'))
    # signature = DigitalSigning.load_signature_from_file(os.path.join(os.getcwd(), 'Tests', 'client_exe_signature.bin'))

    # # Get the data to verify:
    # data = PyUtility.readFromFile(os.path.join(os.getcwd(), 'Tests', 'fake_exe.py')).encode()
    # # data = b"binary data or executable content"

    # # Verify the signature:
    # is_valid = DigitalSigning.verify_signature(data, signature, public_key)
    # if is_valid:
    #     print("Signature is valid!")
    # else:
    #     print("Signature is invalid!")