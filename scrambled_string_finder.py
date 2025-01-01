"""
Module for finding scrambled strings.

This module defines the `ScrambledStringFinder` class, which identifies and counts
dictionary words (including their scrambled versions) that appear as substrings
in input strings.
"""

from typing import List, Tuple
from input_provider import InputProvider
from dictionary.dictionary import Dictionary
from dictionary.dictionary_utils import compute_canonical_form
from log.logger import Logger


class ScrambledStringFinder:
    """
    Class to find scrambled substrings in input strings.

    This class uses an `InputProvider` to fetch input strings and a `Dictionary` to fetch dictionary data.
    It identifies dictionary words and their scrambled versions in the input strings.
    """

    def __init__(self, input_provider: InputProvider, dictionary: Dictionary, logger: Logger):
        """
        Initializes the ScrambledStringFinder.

        Args:
            input_provider (InputProvider): Instance of InputProvider to fetch input strings.
            dictionary (Dictionary): Instance of Dictionary to fetch dictionary data.
            logger (Logger): Logger.
        """
        self.input_provider = input_provider
        self.dictionary = dictionary
        self.logger: Logger = logger

    def find_scrambled_strings(self) ->  List[Tuple[int, int]]:
        """
        Finds scrambled substrings in the input strings.

        Returns:
                List[Tuple[int, int]]: A list of tuples where each tuple contains:
                    - The index of the input string (1-based).
                    The count of matched dictionary words (including scrambled versions).
        """
        inputs = self.input_provider.get()

        results = []
        for index, input_string in enumerate(inputs, start=1):
            count = self._process_input(input_string)
            results.append((index, count))

        return results

    def _process_input(self, input_string: str) -> int:
        """
        Processes a single input string to find scrambled strings.

        Args:
            input_string (str): The input string to process.

        Returns:
            int: The count of matched scrambled words.
        """
        if not input_string:
            return 0

        return self._count_matches(input_string)

    def _count_matches(self, input_string: str) -> int:
        """
        Counts how many of the words from the dictionary appear as substrings in the input string
        either in their original form or in their scrambled form. The scrambled form of the
        dictionary word must adhere to the following rule: the first and last letter must be maintained
        while the middle characters can be reorganised.

        Args:
            input_string (str): The input string to search.

        Returns:
            int: The count of matched scrambled words.
        """
        count = 0
        input_len = len(input_string)

        for dict_word in self.dictionary.get_all_words():
            word_length = len(dict_word)

            # Sliding window to match canonical forms
            for i in range(input_len - word_length + 1):
                substring = input_string[i: i + word_length]
                if (substring == dict_word or
                        compute_canonical_form(substring) == self.dictionary.get_canonical_word(dict_word)):
                    self.logger.debug(f"dict_word: {dict_word} | substring: {substring} | "
                                      f"substring_canonical: {compute_canonical_form(substring)} | "
                                      f"dict_word_canonical: {self.dictionary.get_canonical_word(dict_word)} "
                                      )
                    count += 1
                    break # Avoid double-counting for the same word

        return count
