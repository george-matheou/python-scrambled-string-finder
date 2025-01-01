"""
Module for implementing data storage using a hash table.
"""

# Imports
from dictionary.dictionary_data_storage import DictionaryDataStorage
from dictionary.dictionary_utils import compute_canonical_form


class HashDictionaryStorage(DictionaryDataStorage):
    """
    Implements a dictionary data storage using a hash table.

    This implementation precomputes and stores the canonical form of each word for
    efficient lookup and comparison during scrambled word matching.
    """
    def __init__(self):
        """
        Initializes the HashDictionaryStorage.
        """
        self.storage: dict[str, str] = {}

    def add_word(self, word: str) -> None:
        """
        Adds a word to the storage.

        Args:
            word (str): The word to add.
        """
        self.storage[word] = compute_canonical_form(word)

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
         Retrieves all original words from the storage.

         Returns:
             set[str]: A set of all words in the storage.
         """
        return set(self.storage.keys())


    def get_canonical_word(self, word: str) -> str:
        """
        Retrieves the canonical form of the given word.

        If the word exists in the dictionary, its precomputed canonical form is returned.
        Otherwise, the canonical form is computed dynamically.

        Args:
            word (str): The word to canonicalize.

        Returns:
            str: The canonical form of the word.
        """
        return self.storage.get(word, compute_canonical_form(word))
