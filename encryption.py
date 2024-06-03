import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

class Encryption:
    def __init__(self):
        self.salt = b'salt_'

    def generate_key(self, password):
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=self.salt,
            iterations=100000
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        return key

    def encrypt(self, message, key):
        f = Fernet(key)
        encrypted_message = f.encrypt(message.encode()).decode()
        return encrypted_message

    def decrypt(self, encrypted_message, key):
        f = Fernet(key)
        decrypted_message = f.decrypt(encrypted_message.encode()).decode()
        return decrypted_message