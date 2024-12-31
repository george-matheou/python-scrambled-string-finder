"""
Python module that contains custom exceptions for dictionary.
"""


class DictionaryError(Exception):
    """
    Exception raised for dictionary processing errors.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message):
        self.message = message
