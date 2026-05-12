"""
History mixin for the chat project.
"""

from datetime import datetime


class HistoryMixin:

    def start_history_session(self, filename="chat_history.txt"):
        """Start a new history session in the history file."""
        self.history_filename = filename

        session_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with open(self.history_filename, "a", encoding="utf-8") as file:
            file.write("\n")
            file.write("=" * 40 + "\n")
            file.write(f"Session: {session_time}\n")
            file.write("=" * 40 + "\n")

    def save_to_history(self, message):
        """Append a message to the history file."""
        with open(self.history_filename, "a", encoding="utf-8") as file:
            file.write(message)