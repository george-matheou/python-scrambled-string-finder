"""
Test cases for AppConfig
"""

# Imports
import unittest
from pydantic import ValidationError
from dictionary.dictionary_config import DictionaryConfig


class TestDictionaryConfig(unittest.TestCase):
    """
    Unit tests for the DictionaryConfig class.
    """
    def test_valid_config(self):
        """Test that a valid configuration is accepted."""
        config = DictionaryConfig(
            min_word_length=5,
            max_word_length=10,
            max_sum_lengths_of_all_words=50,
        )
        self.assertEqual(config.min_word_length, 5)
        self.assertEqual(config.max_word_length, 10)
        self.assertEqual(config.max_sum_lengths_of_all_words, 50)

    def test_dictionary_min_word_length_greater_than_max(self):
        """Test that an error is raised when min_word_length > max_word_length."""
        with self.assertRaises(ValidationError) as context:
            DictionaryConfig(
                min_word_length=15,
                max_word_length=10,
                max_sum_lengths_of_all_words=50,
            )
        self.assertIn(
            "`max_word_length` (10) must be greater than or equal to `min_word_length` (15).",
            str(context.exception),
        )

    def test_dictionary_max_word_length_greater_than_sum_lengths(self):
        """Test that an error is raised when max_word_length > max_sum_lengths_of_all_words."""
        with self.assertRaises(ValidationError) as context:
            DictionaryConfig(
                min_word_length=5,
                max_word_length=60,
                max_sum_lengths_of_all_words=50,
            )
        self.assertIn(
        "`max_sum_lengths_of_all_words` (50) must be greater "
                "than or equal to `max_word_length` (60).",
            str(context.exception),
        )

    def test_dictionary_min_word_length_negative(self):
        """Test that an error is raised for a negative min_word_length."""
        with self.assertRaises(ValidationError) as context:
            DictionaryConfig(
                min_word_length=-1,
                max_word_length=10,
                max_sum_lengths_of_all_words=50,
            )
        self.assertIn("Input should be greater than or equal to 1", str(context.exception))

    def test_dictionary_max_word_length_negative(self):
        """Test that an error is raised for a negative max_word_length."""
        with self.assertRaises(ValidationError) as context:
            DictionaryConfig(
                min_word_length=5,
                max_word_length=-10,
                max_sum_lengths_of_all_words=50,
            )
        self.assertIn("Input should be greater than or equal to 1", str(context.exception))

    def test_dictionary_max_sum_lengths_negative(self):
        """Test that an error is raised for a negative max_sum_lengths_of_all_words."""
        with self.assertRaises(ValidationError) as context:
            DictionaryConfig(
                min_word_length=5,
                max_word_length=10,
                max_sum_lengths_of_all_words=-50,
            )
        self.assertIn("Input should be greater than or equal to 1", str(context.exception))

    def test_default_values(self):
        """Test that default values are set correctly."""
        config = DictionaryConfig()
        self.assertEqual(config.min_word_length, 2)
        self.assertEqual(config.max_word_length, 105)
        self.assertEqual(config.max_sum_lengths_of_all_words, 105)


if __name__ == "__main__":
    unittest.main()
