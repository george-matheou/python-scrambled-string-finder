"""
Utility functions for dictionary operations.
"""

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
