"""
Module for finding scrambled strings.

This module defines the `ScrambledStringFinder` class, which identifies and counts
dictionary words (including their scrambled versions) that appear as substrings
in input strings.
"""

from typing import List
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

    def find_scrambled_strings(self) -> List[str]:
        """
        Finds scrambled substrings in the input strings.

        Returns:
            List[str]: A list of results in the format "Case #x: y", where x is the input
                       string index (1-based) and y is the count of matched dictionary
                       words (including scrambled versions).
        """
        inputs = self.input_provider.get()

        results = []
        for case_index, input_string in enumerate(inputs, start=1):
            result = self._process_input(case_index, input_string)
            results.append(result)

        return results

    def output_scrambled_strings(self) -> None:
        """
        Outputs scrambled substrings in the input strings.
        """
        inputs = self.input_provider.get()

        for case_index, input_string in enumerate(inputs, start=1):
            result = self._process_input(case_index, input_string)
            self.logger.always(result)

    def _process_input(self, case_index: int, input_string: str) -> str:
        """
        Processes a single input string to find scrambled strings.

        Args:
            case_index (int): The index of the case (1-based).
            input_string (str): The input string to process.

        Returns:
            str: The result in the format "Case #x: y".
        """
        if not input_string:
            return f"Case #{case_index}: 0"

        count = self._count_matches(input_string)
        return f"Case #{case_index}: {count}"

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
                if compute_canonical_form(substring) ==  self.dictionary.get_canonical_word(dict_word):
                    count += 1
                    break # Avoid double-counting for the same word

        return count
