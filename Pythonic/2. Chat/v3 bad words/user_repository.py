"""
Simple SQLite user repository.

This version stores passwords as plain text for teaching purposes only.
In a real application, passwords should never be stored in plain text.
They should be stored as secure hashes.
If the database file does not exist, SQLite creates it automatically.
If the database file already exists, it is opened and reused.
The existing data is preserved.
"""

import sqlite3


class UserRepository:

    def __init__(self, filename="users.db"):
        # Store the SQLite database filename.
        self.filename = filename

        # Create the table if it does not already exist.
        self.create_table()

    def create_table(self):
        """Create the users table if it does not already exist."""
        # sqlite3.connect() creates the database file automatically if needed.
        # If the file already exists, SQLite opens and reuses it.
        with sqlite3.connect(self.filename) as connection:
            cursor = connection.cursor()

            # IF NOT EXISTS preserves the existing table and its data.
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    username TEXT PRIMARY KEY,
                    password TEXT NOT NULL
                )
            """)

    def add_user(self, username, password):
        """
        Insert a new user.

        Return True if the user was added successfully.
        Return False if the username already exists.
        """
        with sqlite3.connect(self.filename) as connection:
            cursor = connection.cursor()

            try:
                # The username is the primary key and must be unique.
                cursor.execute(
                    "INSERT INTO users (username, password) VALUES (?, ?)",
                    (username, password)
                )
                return True

            except sqlite3.IntegrityError:
                # The username already exists.
                return False

    def validate_user(self, username, password):
        """Return True if the username and password are valid."""
        with sqlite3.connect(self.filename) as connection:
            cursor = connection.cursor()

            # Parameterized queries prevent SQL injection attacks.
            cursor.execute(
                """
                SELECT username
                FROM users
                WHERE username = ? AND password = ?
                """,
                (username, password)
            )

            # fetchone() returns None if no matching row is found.
            return cursor.fetchone() is not None

    def delete_user(self, username):
        """Delete a user by username."""
        with sqlite3.connect(self.filename) as connection:
            cursor = connection.cursor()

            # Delete the row whose username matches the given value.
            cursor.execute(
                "DELETE FROM users WHERE username = ?",
                (username,)
            )

    def list_users(self):
        """Return all users as a list of (username, password) tuples."""
        with sqlite3.connect(self.filename) as connection:
            cursor = connection.cursor()

            # ORDER BY username returns the users in alphabetical order.
            cursor.execute("""
                SELECT username, password
                FROM users
                ORDER BY username
            """)

            # fetchall() returns all rows as a list of tuples.
            return cursor.fetchall()