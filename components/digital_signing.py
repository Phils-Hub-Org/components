from typing import Tuple
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.hazmat.backends import default_backend

class DigitalSigning:
    
    @staticmethod
    def generateKeyPair() -> Tuple[rsa.RSAPrivateKey, rsa.RSAPublicKey]:
        """ Generates and returns a private and public key pair. """
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )
        public_key = private_key.public_key()
        return private_key, public_key

    @staticmethod
    def saveKeyToFile(key: rsa.RSAPrivateKey, path: str, private: bool=False) -> None:
        """ Saves a private or public key to a file. """
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
    def loadKeyFromFile(path, private: bool=False) -> Tuple[rsa.RSAPrivateKey, rsa.RSAPublicKey]:
        """ Loads a private or public key from a file. """
        with open(path, 'rb') as f:
            key_bytes = f.read()
        
        if private:
            return serialization.load_pem_private_key(key_bytes, password=None, backend=default_backend())
        else:
            return serialization.load_pem_public_key(key_bytes, backend=default_backend())

    @staticmethod
    def signData(data, private_key: rsa.RSAPrivateKey) -> bytes:
        """ Signs the data using the provided private key. """
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
    def saveSignatureToFile(signature: bytes, path: str) -> None:
        """ Saves the signature to a file. """
        with open(path, 'wb') as f:
            f.write(signature)
    
    @staticmethod
    def loadSignatureFromFile(path: str) -> bytes:
        """ Loads the signature from a file. """
        with open(path, 'rb') as f:
            signature = f.read()
        return signature

    @staticmethod
    def verifySignature(data: bytes, signature: bytes, public_key: rsa.RSAPublicKey) -> bool:
        """ Verifies the provided signature using the public key. """
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
            print(f'Verification failed: {e}')
            return False

# Example usage
if __name__ == '__main__':
    import os

    ENV = 'CLIENT'

    if ENV == 'SERVER':
        # Server-side (DigitalSigning):

        # Generate a key pair (server generates its private and public key):
        private_key, public_key = DigitalSigning.generateKeyPair()

        # Save the keys to files:
        DigitalSigning.saveKeyToFile(private_key, os.path.join(os.getcwd(), 'Tests', 'DigitslSigning', 'client_exe_pvt_key.pem'), private=True)
        DigitalSigning.saveKeyToFile(public_key, os.path.join(os.getcwd(), 'Tests', 'DigitslSigning', 'client_exe_pub_key.pem'))

        # Get the data to sign (e.g., an executable):
        with open(os.path.join(os.getcwd(), 'Tests', 'DigitslSigning', 'fake_exe.txt'), 'rb') as f:
            data = f.read()
            print(f'Data to sign: {data}')

        # Sign the data (e.g., an executable):
        signature = DigitalSigning.signData(data, private_key)

        # Save the signature to a file:
        DigitalSigning.saveSignatureToFile(signature, os.path.join(os.getcwd(), 'Tests', 'DigitslSigning', 'client_exe_signature.bin'))

        # Send the public key and signature to the client.

    elif ENV == 'CLIENT':
        # Client-side (SignatureVerification):
        
        # Load the public key:
        public_key = DigitalSigning.loadKeyFromFile(os.path.join(os.getcwd(), 'Tests', 'DigitslSigning', 'client_exe_pub_key.pem'))
        signature = DigitalSigning.loadSignatureFromFile(os.path.join(os.getcwd(), 'Tests', 'DigitslSigning', 'client_exe_signature.bin'))

        # Get the data to verify:
        with open(os.path.join(os.getcwd(), 'Tests', 'DigitslSigning', 'fake_exe.txt'), 'rb') as f:
            data = f.read()

        # Verify the signature:
        is_valid = DigitalSigning.verifySignature(data, signature, public_key)
        if is_valid:
            print('Signature is valid!')
        else:
            print('Signature is invalid!')