"""
Project: Simple chat client.

The client connects to the server, sends messages, and
prints messages received from others.
"""

import socket
import threading


class ChatClient:

    def __init__(self, host="127.0.0.1", port=5000):
        self.host = host
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self, nick):
        """Connect to the server and send nickname."""
        self.client_socket.connect((self.host, self.port))
        self.client_socket.sendall((nick + "\n").encode())

    def send_message(self, message):
        """Send a message to the server."""
        self.client_socket.sendall((message + "\n").encode())

    def receive_messages(self):
        """Continuously receive messages from the server."""
        while True:
            try:
                message = self.client_socket.recv(1024)

                if not message:
                    break

                print(message.decode(), end="")

            except Exception:
                break

    def close(self):
        """Close the connection."""
        self.client_socket.close()


if __name__ == "__main__":
    nick = input("Enter your nickname: ")

    client = ChatClient()
    client.connect(nick)

    # Thread to receive messages
    thread = threading.Thread(
        target=client.receive_messages,
        daemon=True
    )
    thread.start()

    # Main loop: send messages
    while True:
        message = input()

        if message.lower() == "exit":
            break

        client.send_message(message)

    client.close()