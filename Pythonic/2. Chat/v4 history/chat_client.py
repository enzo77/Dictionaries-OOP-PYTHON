"""
Project: Simple chat client.

The client connects to the server, sends messages, and
prints messages received from others.
"""

import socket
import threading
from decorators import censor_words
from history_mixin import HistoryMixin

class ChatClient(HistoryMixin):

    def __init__(self, host="127.0.0.1", port=5000):
        self.host = host
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self, nick, password):
        """Connect to the server and send login data."""
        self.client_socket.connect((self.host, self.port))

        login_message = f"LOGIN {nick} {password}\n"
        self.client_socket.sendall(login_message.encode())

        response = self.client_socket.recv(1024).decode().strip()

        if response.startswith("[ERROR]"):
            print(response)
            self.client_socket.close()
            return False

        print(response)
        return True

    @censor_words(["bad", "ugly", "spam"])
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

                text = message.decode()
                print(text, end="")
                self.save_to_history(text)

            except Exception:
                break

    def close(self):
        """Close the connection."""
        self.client_socket.close()


if __name__ == "__main__":
    nick = input("Enter your nickname: ")
    password = input("Enter your password: ")

    client = ChatClient()
    client.start_history_session()

    if not client.connect(nick, password):
        exit()

    thread = threading.Thread(
        target=client.receive_messages,
        daemon=True
    )
    thread.start()

    while True:
        message = input()

        if message.lower() == "exit":
            client.send_message("QUIT")
            break

        client.send_message(message)

    client.close()