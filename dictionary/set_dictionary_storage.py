"""
Module for implementing data storage using a set.
"""

# Imports
from dictionary.dictionary_data_storage import DictionaryDataStorage
from dictionary.dictionary_utils import compute_canonical_form


class SetDictionaryStorage(DictionaryDataStorage):
    """
    Implements a dictionary data storage using a set.

    Unlike other implementations, this class does not precompute or store canonical forms
    of the words, opting instead to compute them dynamically when needed. This approach
    prioritizes storage efficiency while maintaining flexibility for scrambled word matching.
    """

    def __init__(self):
        """
        Initializes the SetDictionaryStorage.
        """
        self.storage: set[str] = set()

    def add_word(self, word: str) -> None:
        """
        Adds a word to the storage.

        Args:
            word (str): The word to add.
        """
        self.storage.add(word)

    def contains_word(self, word: str) -> bool:
        """
        Checks if the storage contains the given word.

        Args:
            word (str): The word to check.

        Returns:
            bool: True if the word exists, False otherwise.
        """
        return word in self.storage

    def get_all_words(self) -> set[str]:
        """
        Retrieves all original words in the dictionary.

        Returns:
            set[str]: A set containing all the original dictionary words.
        """
        return self.storage

    def get_canonical_word(self, word: str) -> str:
        """
        Computes and returns the canonical form of the given word.

        Args:
            word (str): The word to canonicalize.

        Returns:
            str: The canonical form of the word.
        """
        return compute_canonical_form(word)
