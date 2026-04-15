"""
Project: Simple chat server.

The server accepts multiple clients and broadcasts messages
to all connected users.

https://docs.python.org/3/library/socket.html
https://docs.python.org/3/library/threading.html
"""

import socket
import threading
from datetime import datetime


class ChatServer:

    def __init__(self, host="0.0.0.0", port=5000):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.clients = []   # list of sockets
        self.nicks = {}     # socket -> nickname

    def start(self):
        """Start the server and accept clients."""
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen()

        print(f"Server started on {self.host}:{self.port}")

        while True:
            client_socket, address = self.server_socket.accept()
            print(f"Connection from {address}")

            thread = threading.Thread(target=self.handle_client, args=(client_socket,), daemon=True)
            thread.start()

    def broadcast(self, message):
        """Send a message to all clients."""
        for client in self.clients:
            try:
                client.sendall(message.encode())
            except Exception:
                self.remove_client(client)

    def handle_client(self, client_socket):
        """Handle a single client connection."""
        try:
            # First message = nickname
            nick = client_socket.recv(1024).decode().strip()

            self.clients.append(client_socket)
            self.nicks[client_socket] = nick

            self.broadcast(f"[SYSTEM] {nick} has joined the chat.\n")

            while True:
                message = client_socket.recv(1024)

                if not message:
                    break

                text = message.decode().strip()
                time_str = datetime.now().strftime("%H:%M:%S")

                full_message = f"[{time_str}] {nick}: {text}\n"
                self.broadcast(full_message)

        except Exception:
            pass

        finally:
            self.remove_client(client_socket)

    def remove_client(self, client_socket):
        """Remove a client and notify others."""
        if client_socket in self.clients:
            nick = self.nicks.get(client_socket, "Unknown")

            self.clients.remove(client_socket)
            self.nicks.pop(client_socket, None)

            self.broadcast(f"[SYSTEM] {nick} has left the chat.\n")

            client_socket.close()


if __name__ == "__main__":
    server = ChatServer()
    server.start()