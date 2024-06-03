import sqlite3
from encryption import Encryption

class Database:
    def __init__(self):
        self.conn = sqlite3.connect("pychat.db")
        self.create_tables()

    def create_tables(self):
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE,
                encrypted_password TEXT
            )
        """)
        self.conn.commit()

    def register_user(self, username, password):
        try:
            encryption = Encryption()
            encrypted_password = encryption.generate_key(password)
            cursor = self.conn.cursor()
            cursor.execute("INSERT INTO users (username, encrypted_password) VALUES (?, ?)", (username, encrypted_password))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def validate_user(self, username, password):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()
        if user:
            stored_password = user[2]
            encryption = Encryption()
            encrypted_password = encryption.generate_key(password)
            return stored_password == encrypted_password
        return False