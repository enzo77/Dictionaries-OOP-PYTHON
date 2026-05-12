"""
Useful decorators for the chat project.
"""

from functools import wraps


def censor_words(forbidden_words):
    """
    Return a decorator that replaces forbidden words with "***".

    The replacement is case-insensitive and also matches words that contain
    the forbidden text as a substring.
    """
    # Store all forbidden words in lowercase for case-insensitive matching.
    forbidden_words = [word.lower() for word in forbidden_words]

    def decorator(function):

        @wraps(function)
        def wrapper(*args, **kwargs):
            # We use *args and **kwargs so that the decorator works with both
            # regular functions and instance methods.
            #
            # Function example:
            #     echo(message)
            #
            # Method example:
            #     send_message(self, message)
            #
            # In both cases, the message is assumed to be the last positional
            # argument, so args[-1] always contains the text to be censored.
            message = args[-1]

            # Work on a copy of the original message.
            censored_message = message

            # Lowercase copy used only for searching.
            lower_message = censored_message.lower()

            # Process every forbidden word.
            for word in forbidden_words:

                # Continue replacing while the substring appears.
                while word in lower_message:
                    index = lower_message.find(word)

                    # Replace the matching substring with "***".
                    censored_message = (
                        censored_message[:index]
                        + "***"
                        + censored_message[index + len(word):]
                    )

                    # Rebuild the lowercase version after each replacement.
                    lower_message = censored_message.lower()

            # Rebuild the positional arguments replacing only the last one.
            new_args = args[:-1] + (censored_message,)

            # Call the original function with the censored message.
            return function(*new_args, **kwargs)

        return wrapper

    return decorator