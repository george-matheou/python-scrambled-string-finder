"""
Module for finding scrambled strings.

This module defines the `ScrambledStringFinder` class, which identifies and counts
dictionary words (including their scrambled versions) that appear as substrings
in input strings.
"""

from typing import List, Tuple
from input_strings.input_provider import InputProvider
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

    def find_scrambled_strings(self) -> List[Tuple[int, int]]:
        """
        Finds scrambled substrings in the input strings.

        Returns:
                List[Tuple[int, int]]: A list of tuples where each tuple contains:
                    - The index of the input string (1-based).
                    - The count of matched dictionary words (including scrambled versions).
        """
        inputs = self.input_provider.get()

        results = []
        for index, input_string in enumerate(inputs, start=1):
            count = self._count_matches(input_string)
            results.append((index, count))

        return results

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

        # If the input string is empty, return 0
        if not input_string:
            return 0

        # Local variables
        count = 0
        input_len = len(input_string)

        for dict_word in self.dictionary.get_all_words():
            word_length = len(dict_word)

            # Skip if the dictionary word length exceeds input string length
            if word_length > input_len:
                continue

            # Sliding window to match canonical forms. The algorithm iterates through the input string and extracts
            # substrings of the same length as the dictionary word. This ensures that every potential match
            # is examined efficiently.
            for i in range(input_len - word_length + 1):
                substring = input_string[i: i + word_length]

                # The first and last letters of the substring must match those of the dictionary word to satisfy
                # the scrambling rule. Substrings that fail this check are guaranteed not to match and are
                # skipped entirely in order to improve performance.
                if not (dict_word[0] == substring[0] and dict_word[-1] == substring[-1]):
                    continue

                if ((substring == dict_word) or
                        compute_canonical_form(substring) == self.dictionary.get_canonical_word(dict_word)):
                    self.logger.debug(f"dict_word: {dict_word} | substring: {substring} | "
                                      f"substring_canonical: {compute_canonical_form(substring)} | "
                                      f"dict_word_canonical: {self.dictionary.get_canonical_word(dict_word)} "
                                      )
                    count += 1

                    # Avoid double-counting for the same dictionary word
                    break

        return count
