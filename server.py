import socket
import threading
from database import Database
from encryption import Encryption

class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients = {}
        self.encryption = Encryption()

    def start(self):
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print(f"Server started on {self.host}:{self.port}")

        while True:
            client_socket, address = self.server_socket.accept()
            print(f"New client connected: {address}")
            client_thread = threading.Thread(target=self.handle_client, args=(client_socket,))
            client_thread.start()

    def handle_client(self, client_socket):
        database = Database()  # Create a new database connection for each client thread
        while True:
            try:
                message = client_socket.recv(1024).decode()
                if message:
                    if message.startswith("/login"):
                        _, username, password = message.split(' ', 2)
                        if database.validate_user(username, password):
                            self.clients[client_socket] = username
                            client_socket.send("Login successful".encode())
                        else:
                            client_socket.send("Invalid username or password".encode())
                    elif message.startswith("/register"):
                        _, username, password = message.split(' ', 2)
                        if database.register_user(username, password):
                            client_socket.send("Registration successful".encode())
                        else:
                            client_socket.send("Username already exists".encode())
                    elif message.startswith("/pm"):
                        self.handle_private_message(client_socket, message)
                    else:
                        self.broadcast_message(message, client_socket)
            except ConnectionResetError:
                self.remove_client(client_socket)
                break

    def handle_private_message(self, sender_socket, message):
        _, recipient, content = message.split(' ', 2)
        recipient_socket = None
        for client_socket, username in self.clients.items():
            if username == recipient:
                recipient_socket = client_socket
                break

        if recipient_socket:
            encrypted_message = self.encryption.encrypt(f"(Private) {self.clients[sender_socket]}: {content}", self.encryption.generate_key(self.clients[sender_socket]))
            recipient_socket.send(encrypted_message.encode())
            sender_socket.send("Private message sent successfully".encode())
        else:
            sender_socket.send("Recipient not found".encode())

    def broadcast_message(self, message, sender_socket):
        for client_socket in self.clients:
            if client_socket != sender_socket:
                client_socket.send(message.encode())

    def remove_client(self, client_socket):
        if client_socket in self.clients:
            del self.clients[client_socket]
            client_socket.close()