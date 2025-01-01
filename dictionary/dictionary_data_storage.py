"""
Abstract module for dictionary data storage.
"""

from abc import ABC, abstractmethod


class DictionaryDataStorage(ABC):
    """
    Abstract class to define the interface for dictionary data storage.
    Defines the interface for storing and retrieving dictionary words.
    """

    @abstractmethod
    def add_word(self, word: str) -> None:
        """
        Adds a word to the storage.

        Args:
            word (str): The word to add.
        """
        pass

    @abstractmethod
    def contains_word(self, word: str) -> bool:
        """
        Checks if the storage contains the given word.

        Args:
            word (str): The word to check.

        Returns:
            bool: True if the word exists, False otherwise.
        """
        pass

    @abstractmethod
    def get_all_words(self) -> set[str]:
        """
         Retrieves all original words from the storage.

         Returns:
             set[str]: A set of all words in the storage.
         """
        pass

    @abstractmethod
    def get_canonical_word(self, word: str) -> str:
        """
        Retrieves the canonical form of the given word.

        Args:
            word (str): The word to canonicalize.

        Returns:
            str: The canonical form of the word.

        Note:
            If the storage does not contain precomputed canonical forms,
            this method should compute the canonical form dynamically.
        """
        pass
