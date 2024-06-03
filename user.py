class User:
    def __init__(self, username, encrypted_password):
        self.username = username
        self.encrypted_password = encrypted_password
        self.encryption_key = None