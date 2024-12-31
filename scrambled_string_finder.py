"""
Module for finding scrambled strings.

This module defines the `ScrambledStringFinder` class, which identifies and counts
dictionary words (including their scrambled versions) that appear as substrings
in input strings.
"""

from typing import List
from input_provider import InputProvider
from dictionary.dictionary_provider import DictionaryProvider
from dictionary.dictionary_utils import compute_canonical_form
from dictionary.dictionary_word import DictionaryWord


class ScrambledStringFinder:
    """
    Class to find scrambled substrings in input strings.

    This class uses an `InputProvider` to fetch input strings and a `DictionaryProvider`
    to fetch dictionary data. It identifies dictionary words and their scrambled
    versions in the input strings.
    """

    def __init__(self, input_provider: InputProvider, dictionary_provider: DictionaryProvider):
        """
        Initializes the ScrambledStringFinder.

        Args:
            input_provider (InputProvider): Instance of InputProvider to fetch input strings.
            dictionary_provider (DictionaryProvider): Instance of DictionaryProvider to fetch dictionary data.
        """
        self.input_provider = input_provider
        self.dictionary_provider = dictionary_provider

    def find_scrambled_strings(self) -> List[str]:
        """
        Finds scrambled substrings in the input strings.

        Returns:
            List[str]: A list of results in the format "Case #x: y", where x is the input
                       string index (1-based) and y is the count of matched dictionary
                       words (including scrambled versions).
        """
        # Fetch inputs and dictionary data
        inputs = self.input_provider.get()
        dictionary = self.dictionary_provider.get()

        results = []
        for case_index, input_string in enumerate(inputs, start=1):
            count = self._count_matches(input_string, dictionary)
            results.append(f"Case #{case_index}: {count}")

        return results

    def _count_matches(self, input_string: str, dictionary: dict[str, DictionaryWord]) -> int:
        """
        Counts how many of the words from the dictionary appear as substrings in the input string
        either in their original form or in their scrambled form. The scrambled form of the
        dictionary word must adhere to the following rule: the first and last letter must be maintained
        while the middle characters can be reorganised.

        Args:
            input_string (str): The input string to search.
            dictionary (dict[str, DictionaryWord]): A set of scrambled words.

        Returns:
            int: The count of matched scrambled words.
        """
        count = 0
        input_len = len(input_string)

        for dict_word in dictionary.values():
            # Sliding window to match canonical forms
            for i in range(input_len - dict_word.value_length + 1):
                substring = input_string[i: i + dict_word.value_length]
                if compute_canonical_form(substring) == dict_word.value:
                    count += 1
                    break # Avoid double-counting for the same word

        return count
