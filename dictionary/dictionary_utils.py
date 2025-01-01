"""
Utility functions for dictionary operations.
"""

# Imports
from dictionary.dictionary_errors import DictionaryError


def compute_canonical_form(word: str) -> str:
    """
    Computes the canonical form of a word.

    The canonical form keeps the first and last letters fixed,
    while sorting the middle characters.

    Args:
        word (str): The word to process.

    Returns:
        str: The canonical form of the word.
    """
    if len(word) <= 2:
        return word  # Words with 2 or fewer characters cannot be scrambled
    return word[0] + "".join(sorted(word[1:-1])) + word[-1]


def validate_word_length_or_raise(word: str, min_word_length: int, max_word_length: int) -> None:
    """
    Validates the length of a word and raises an exception if it is invalid.

    Args:
        word (str): The word to validate.
        min_word_length (int): Minimum allowed length of the word.
        max_word_length (int): Maximum allowed length of the word.

    Raises:
        DictionaryError: If the word's length does not meet the constraints.
    """
    word_length = len(word)
    if not min_word_length <= word_length <= max_word_length:
        raise DictionaryError(
            f"Word '{word}' does not meet the length constraints "
            f"({min_word_length} <= len(word) <= {max_word_length})."
        )


def validate_total_length_or_raise(total_length: int, max_allowed_length: int) -> None:
    """
    Validates the total length of words and raises an exception if it exceeds the allowed limit.

    Args:
        total_length (int): The current total length of all words.
        max_allowed_length (int): The maximum allowed total length of all words.

    Raises:
        DictionaryError: If the total length exceeds the allowed limit.
    """
    if total_length > max_allowed_length:
        raise DictionaryError(
            f"The total length of all words ({total_length}) exceeds the allowed limit of {max_allowed_length}."
        )
