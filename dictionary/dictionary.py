"""
Module for managing a dictionary using customizable storage.
"""

# Imports
import os
from dictionary.dictionary_data_storage import DictionaryDataStorage
from dictionary.dictionary_errors import DictionaryError
from dictionary.dictionary_utils import validate_word_length_or_raise, validate_total_length_or_raise
from dictionary.dictionary_config import DictionaryConfig
from log.logger import Logger


class Dictionary:
    """
    Manages dictionary words using a customizable storage strategy.

    This class provides high-level operations for managing a dictionary, such as
    adding words, checking for duplicates, and retrieving canonical forms.
    """
    def __init__(self, storage: DictionaryDataStorage, dictionary_config: DictionaryConfig, logger: Logger):
        """
        Initializes the Dictionary with a given storage strategy.

        Args:
            storage (DictionaryDataStorage): An implementation of the dictionary data storage interface.
            dictionary_config (DictionaryConfig): Dictionary configuration.
            logger (Logger): Logger.
        """
        self.dictionary_config: DictionaryConfig = dictionary_config
        self.total_length_of_all_words: int = 0
        self.dictionary_data_storage: DictionaryDataStorage = storage
        self.logger: Logger = logger

    def add_word(self, word: str) -> None:
        """
        Adds a word to the dictionary.

        Args:
            word (str): The validated word to add.

        Raises:
            DictionaryError: If a word violates constraints (e.g., duplicate, invalid length),
                             or if the total length of all words exceeds the configured maximum.
        """
        # Validate word length
        validate_word_length_or_raise(word=word,
                                      min_word_length=self.dictionary_config.min_word_length,
                                      max_word_length=self.dictionary_config.max_word_length)

        # Check that the word is not duplicated
        if self.dictionary_data_storage.contains_word(word):
            raise DictionaryError(f"Duplicate word found: '{word}'")

        # Add the word
        self.dictionary_data_storage.add_word(word)
        self.total_length_of_all_words += len(word)

        # Validate total length
        validate_total_length_or_raise(total_length=self.total_length_of_all_words,
                                       max_allowed_length=self.dictionary_config.max_sum_lengths_of_all_words)

        self.logger.info(f"Word '{word}' added successfully.")

    def load_from_file(self, dictionary_file_path: str) -> None:
        """
        Reads and validates words from the dictionary file.

        Validates each word against length constraints, checks for duplicates,
        and ensures the total length of all words does not exceed the configured limit.

        Raises:
            FileNotFoundError: If the dictionary file does not exist.
            DictionaryError: If a word violates constraints (e.g., duplicate, invalid length),
                             or if the total length of all words exceeds the configured maximum.
        """
        if not os.path.exists(dictionary_file_path):
            raise FileNotFoundError(f"Dictionary file path '{dictionary_file_path}' does not exist!")

        # Open the file and read line by line
        with open(dictionary_file_path, mode="r", encoding="utf-8") as file:
            for line in file:
                word = line.strip()

                # Skip empty words
                if not word:
                    self.logger.warning(f"Empty word detected in {dictionary_file_path}. Skipping...")
                    continue

                self.add_word(word)

    def get_all_words(self) -> set[str]:
        """
         Retrieves all words of the dictionary.

         Returns:
             set[str]: A set containing all the original dictionary words.
         """
        return self.dictionary_data_storage.get_all_words()

    def get_canonical_word(self, word: str) -> str:
        """
        Retrieves the canonical form of the given word.

        Args:
            word (str): The word to canonicalize.

        Returns:
            str: The canonical form of the word.
        """
        return self.dictionary_data_storage.get_canonical_word(word)
