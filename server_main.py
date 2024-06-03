from server import Server
import threading

if __name__ == "__main__":
    server = Server("localhost", 8888)
    server_thread = threading.Thread(target=server.start)
    server_thread.start()