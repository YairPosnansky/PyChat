import socket
import threading

class Client:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.username = None
        self.message_callback = None

    def connect(self):
        self.client_socket.connect((self.host, self.port))
        print(f"Connected to server: {self.host}:{self.port}")

        # Start a thread to receive messages from the server
        receive_thread = threading.Thread(target=self.receive_messages)
        receive_thread.start()

    def send_message(self, message):
        self.client_socket.send(message.encode())

    def receive_messages(self):
        while True:
            try:
                message = self.client_socket.recv(1024).decode()
                if message:
                    if self.message_callback:
                        self.message_callback(message)
            except ConnectionResetError:
                break

    def set_message_callback(self, callback):
        self.message_callback = callback