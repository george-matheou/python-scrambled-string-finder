"""
Test cases for ScrambledStringFinder.
"""

# Imports
import unittest
from unittest.mock import Mock
from dictionary.dictionary import Dictionary
from dictionary.dictionary_config import DictionaryConfig
from dictionary.set_dictionary_storage import SetDictionaryStorage
from scrambled_string_finder import ScrambledStringFinder


class TestScrambledStringFinder(unittest.TestCase):
    """
    Unit tests for the ScrambledStringFinder class.
    """

    def setUp(self):
        """Set up mocks for InputProvider, Dictionary, and Logger."""
        self.mock_input_provider = Mock()
        self.mock_logger = Mock()
        self.dictionary = Dictionary(
            storage=SetDictionaryStorage(),
            dictionary_config=DictionaryConfig(min_word_length=2,
                                               max_word_length=100, max_sum_lengths_of_all_words=300),
            logger=self.mock_logger
        )

    def test_exact_matches(self):
        """Test that exact matches are counted correctly."""
        self.dictionary.add_word("scramble")
        self.dictionary.add_word("example")
        self.mock_input_provider.get.return_value = ["scrambled|example"]

        finder = ScrambledStringFinder(
            input_provider=self.mock_input_provider,
            dictionary=self.dictionary,
            logger=self.mock_logger
        )

        # Perform the test
        results = finder.find_scrambled_strings()

        # Validate results
        self.assertEqual(results, [(1, 2)])

    def test_scrambled_matches(self):
        """Test that scrambled matches are counted correctly."""
        self.dictionary.add_word("eaxmple")
        self.dictionary.add_word("tihs")
        self.mock_input_provider.get.return_value = ["scrambled_example_this_tihs"]

        finder = ScrambledStringFinder(
            input_provider=self.mock_input_provider,
            dictionary=self.dictionary,
            logger=self.mock_logger
        )

        # Perform the test
        results = finder.find_scrambled_strings()

        # Validate results
        self.assertEqual(results, [(1, 2)])

    def test_no_matches(self):
        """Test that no matches result in counts of 0."""
        self.mock_input_provider.get.return_value = ["nothing", "matches"]

        self.dictionary.add_word("scramble")
        self.dictionary.add_word("example")

        finder = ScrambledStringFinder(
            input_provider=self.mock_input_provider,
            dictionary=self.dictionary,
            logger=self.mock_logger
        )

        # Perform the test
        results = finder.find_scrambled_strings()

        # Validate results
        self.assertEqual(results, [(1, 0), (2, 0)])

    def test_empty_dictionary(self):
        """Test that an empty dictionary results in 0 counts for all inputs."""
        # Mock input strings and dictionary words
        self.mock_input_provider.get.return_value = ["scrambled", "example"]

        finder = ScrambledStringFinder(
            input_provider=self.mock_input_provider,
            dictionary=self.dictionary,
            logger=self.mock_logger
        )

        # Perform the test
        results = finder.find_scrambled_strings()

        # Validate results
        self.assertEqual(results, [(1, 0), (2, 0)])


if __name__ == "__main__":
    unittest.main()
