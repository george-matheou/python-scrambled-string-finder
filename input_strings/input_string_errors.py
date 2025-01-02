"""
Python module that contains custom exceptions for input strings.
"""


class InputStringError(Exception):
    """
    Exception raised for input string processing errors.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message):
        self.message = message
