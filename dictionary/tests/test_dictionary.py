"""
Test cases for Dictionary.
"""

# Imports
import unittest
from unittest.mock import Mock
from unittest.mock import mock_open, patch
from dictionary.dictionary import Dictionary
from dictionary.dictionary_config import DictionaryConfig
from dictionary.hash_dictionary_storage import HashDictionaryStorage
from dictionary.set_dictionary_storage import SetDictionaryStorage
from dictionary.dictionary_errors import DictionaryError
from dictionary.dictionary_data_storage import DictionaryDataStorage
from log.standard_logger import StandardLogger


class TestDictionary(unittest.TestCase):
    """Unit tests for the Dictionary class."""

    def setUp(self):
        """Set up common test data and mocks."""
        self.logger = Mock(spec=StandardLogger)
        self.config = DictionaryConfig(min_word_length=2, max_word_length=10, max_sum_lengths_of_all_words=50)

    def generic_test_integration(self, dictionary_storage: DictionaryDataStorage):
        """Generic function for testing integration"""
        dictionary = Dictionary(dictionary_storage, self.config, self.logger)
        dictionary.add_word("scramble")
        self.assertTrue(dictionary.dictionary_data_storage.contains_word("scramble"))
        self.assertEqual(dictionary.get_canonical_word("scramble"), "sabclmre")
        self.assertEqual(dictionary.total_length_of_all_words, len("scramble"))

    def test_integration_with_set_storage(self):
        """Test integration with SetDictionaryStorage."""
        self.generic_test_integration(dictionary_storage=SetDictionaryStorage())

    def test_integration_with_hash_storage(self):
        """Test integration with HashDictionaryStorage."""
        self.generic_test_integration(dictionary_storage=HashDictionaryStorage())

    def test_add_duplicate_word(self):
        """Test that adding duplicate words raises an error."""
        storage = HashDictionaryStorage()
        dictionary = Dictionary(storage, self.config, self.logger)

        dictionary.add_word("test")
        with self.assertRaises(DictionaryError):
            dictionary.add_word("test")

    def test_large_words_exceeding_length_range(self):
        """Test that words exceeding the allowed length range raise an error."""
        storage = HashDictionaryStorage()
        dictionary = Dictionary(storage, self.config, self.logger)

        # Word too short
        with self.assertRaises(DictionaryError):
            dictionary.add_word("a")  # Too short, min_word_length=2

        # Word too long
        with self.assertRaises(DictionaryError):
            dictionary.add_word("thisisaverylongword")  # Too long, max_word_length=10

    def test_total_allowed_length_exceeded(self):
        """Test that adding words whose total length exceeds the limit raises an error."""
        storage = HashDictionaryStorage()
        dictionary = Dictionary(storage, self.config, self.logger)
        allowed_total_length = dictionary.dictionary_config.max_sum_lengths_of_all_words
        max_word_length = dictionary.dictionary_config.max_word_length

        # Add words within the allowed range
        for ind in range(int(allowed_total_length/max_word_length)):
            dictionary.add_word(f"{ind}" * max_word_length)

        # Adding this word exceeds the max_sum_lengths_of_all_words
        with self.assertRaises(DictionaryError):
            dictionary.add_word("_" * max_word_length)

    @patch("os.path.exists", return_value=True)
    @patch("builtins.open", new_callable=mock_open, read_data="test\nexample\nanother\n")
    def test_load_from_file(self, mock_file, mock_exists):
        """Test loading words from a file."""
        storage = SetDictionaryStorage()
        dictionary = Dictionary(storage, self.config, self.logger)
        dictionary.load_from_file("mocked_file.txt")
        self.assertTrue(storage.contains_word("test"))
        self.assertTrue(storage.contains_word("example"))
        self.assertTrue(storage.contains_word("another"))
        self.assertEqual(dictionary.total_length_of_all_words, len("test") + len("example") + len("another"))

        # Ensure the file was opened
        mock_file.assert_called_once_with("mocked_file.txt", mode="r", encoding="utf-8")
        mock_exists.assert_called_once_with("mocked_file.txt")

    @patch("os.path.exists", return_value=True)
    @patch("builtins.open", new_callable=mock_open, read_data="")
    def test_load_from_empty_file(self, mock_file, mock_exists):
        """Test loading from an empty file."""
        storage = SetDictionaryStorage()
        dictionary = Dictionary(storage, self.config, self.logger)

        dictionary.load_from_file("mocked_empty_file.txt")
        self.assertEqual(dictionary.total_length_of_all_words, 0)
        self.assertEqual(storage.get_all_words(), set())

        # Ensure the file was opened
        mock_file.assert_called_once_with("mocked_empty_file.txt", mode="r", encoding="utf-8")
        mock_exists.assert_called_once_with("mocked_empty_file.txt")


if __name__ == "__main__":
    unittest.main()
