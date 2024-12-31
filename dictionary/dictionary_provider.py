"""
Abstract module for dictionary providers.
"""

from abc import ABC, abstractmethod
from typing import Dict
from dictionary.dictionary_word import DictionaryWord


class DictionaryProvider(ABC):
    """
    Abstract class to define the interface for dictionary providers.

    Classes inheriting from this must implement methods to load and retrieve
    dictionary data.
    """

    @abstractmethod
    def load(self) -> None:
        """
        Loads the dictionary data.

        Raises:
            Exception: If the dictionary cannot be loaded or processed.
        """
        pass

    @abstractmethod
    def get(self) -> Dict[str, DictionaryWord]:
        """
        Returns the dictionary.

        Returns:
            Dict[str, DictionaryWord]: A dictionary with all the words present in the dictionary.
        """
        pass
