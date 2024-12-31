"""
Module for dictionary file provider.
"""

# Imports
import os
from dictionary.dictionary_provider import DictionaryProvider
from dictionary.dictionary_errors import DictionaryError
from dictionary.dictionary_word import DictionaryWord
from dictionary.dictionary_utils import compute_canonical_form
from dictionary.dictionary_config import DictionaryConfig


class DictionaryFileProvider(DictionaryProvider):
    """
    Class responsible for reading and processing dictionary data from a file.

    This class implements the `DictionaryProvider` interface and validates
    the dictionary based on configuration constraints.
    """
    def __init__(self, dictionary_file_path: str, dictionary_config: DictionaryConfig):
        """
        Initializes the DictionaryFileProvider.

        Args:
            dictionary_file_path (str): Path to the dictionary file.
            dictionary_config (DictionaryConfig): Dictionary configuration.
        """
        self.dictionary_file_path: str = dictionary_file_path
        self.dictionary_config: DictionaryConfig = dictionary_config
        self.total_length_of_all_words: int = 0
        self.dictionary: dict[str, DictionaryWord] = {}

    def load(self) -> None:
        """
        Loads and validates words from the dictionary file.

        Raises:
            FileNotFoundError: If configuration file does not exist.
            DictionaryError: If duplicate words are found, invalid words are present,
                             or if the total length of all words exceeds the allowed maximum.
        """
        if not os.path.exists(self.dictionary_file_path):
            raise FileNotFoundError(f"Dictionary file path = {self.dictionary_file_path} does not exist!")

        min_word_length = self.dictionary_config.min_word_length
        max_word_length = self.dictionary_config.max_word_length
        max_sum_lengths_of_all_words = self.dictionary_config.max_sum_lengths_of_all_words

        # Open the file and read line by line
        with open(self.dictionary_file_path, mode="r", encoding="utf-8") as file:
            for line in file:
                word = line.strip()

                # Skip empty words
                if not word:
                    continue

                word_length = len(word)

                # Check word length
                if not min_word_length <= word_length <= max_word_length:
                    raise DictionaryError(
                        f"Word '{word}' does not meet the length constraints "
                        f"({min_word_length} <= len(word) <= {max_word_length})."
                    )

                # Check that the word is not duplicated
                if word in self.dictionary:
                    raise DictionaryError(f"Duplicate word found: '{word}'")

                # Add the word in dictionary
                canonical_word = compute_canonical_form(word)
                self.dictionary[word] = DictionaryWord(value=canonical_word)
                self.total_length_of_all_words += word_length

                # Check total length constraint
                if self.total_length_of_all_words > max_sum_lengths_of_all_words:
                    raise DictionaryError(f"The total length of all words ({self.total_length_of_all_words}) "
                                          f"exceeds the allowed limit of {max_sum_lengths_of_all_words}.")

    def get(self) -> dict[str, DictionaryWord]:
        """
        Returns the dictionary.

        Returns:
            dict[str, DictionaryWord]: A dictionary with all the words present in the dictionary.
        """
        return self.dictionary
