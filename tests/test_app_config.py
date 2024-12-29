"""
Test cases for AppConfig
"""

import unittest
from pydantic import ValidationError
from config.app_config import AppConfig


class TestAppConfig(unittest.TestCase):
    """
    Unit tests for the AppConfig class.
    """
    def test_valid_config(self):
        """Test that a valid configuration is accepted."""
        config = AppConfig(
            dictionary_min_word_length=5,
            dictionary_max_word_length=10,
            dictionary_max_sum_lengths_of_all_words=50,
        )
        self.assertEqual(config.dictionary_min_word_length, 5)
        self.assertEqual(config.dictionary_max_word_length, 10)
        self.assertEqual(config.dictionary_max_sum_lengths_of_all_words, 50)

    def test_dictionary_min_word_length_greater_than_max(self):
        """Test that an error is raised when dictionary_min_word_length > dictionary_max_word_length."""
        with self.assertRaises(ValidationError) as context:
            AppConfig(
                dictionary_min_word_length=15,
                dictionary_max_word_length=10,
                dictionary_max_sum_lengths_of_all_words=50,
            )
        self.assertIn(
            "`dictionary_max_word_length` (10) must be greater than `dictionary_min_word_length` (15).",
            str(context.exception),
        )

    def test_dictionary_max_word_length_greater_than_sum_lengths(self):
        """Test that an error is raised when dictionary_max_word_length > dictionary_max_sum_lengths_of_all_words."""
        with self.assertRaises(ValidationError) as context:
            AppConfig(
                dictionary_min_word_length=5,
                dictionary_max_word_length=60,
                dictionary_max_sum_lengths_of_all_words=50,
            )
        self.assertIn(
        "`dictionary_max_sum_lengths_of_all_words` (50) must be greater "
                "than or equal to `dictionary_max_word_length` (60).",
            str(context.exception),
        )

    def test_dictionary_min_word_length_negative(self):
        """Test that an error is raised for a negative dictionary_min_word_length."""
        with self.assertRaises(ValidationError) as context:
            AppConfig(
                dictionary_min_word_length=-1,
                dictionary_max_word_length=10,
                dictionary_max_sum_lengths_of_all_words=50,
            )
        self.assertIn("Input should be greater than or equal to 1", str(context.exception))

    def test_dictionary_max_word_length_negative(self):
        """Test that an error is raised for a negative dictionary_max_word_length."""
        with self.assertRaises(ValidationError) as context:
            AppConfig(
                dictionary_min_word_length=5,
                dictionary_max_word_length=-10,
                dictionary_max_sum_lengths_of_all_words=50,
            )
        self.assertIn("Input should be greater than or equal to 1", str(context.exception))

    def test_dictionary_max_sum_lengths_negative(self):
        """Test that an error is raised for a negative dictionary_max_sum_lengths_of_all_words."""
        with self.assertRaises(ValidationError) as context:
            AppConfig(
                dictionary_min_word_length=5,
                dictionary_max_word_length=10,
                dictionary_max_sum_lengths_of_all_words=-50,
            )
        self.assertIn("Input should be greater than or equal to 1", str(context.exception))

    def test_default_values(self):
        """Test that default values are set correctly."""
        config = AppConfig()
        self.assertEqual(config.dictionary_min_word_length, 5)
        self.assertEqual(config.dictionary_max_word_length, 200)
        self.assertEqual(config.dictionary_max_sum_lengths_of_all_words, 200)


if __name__ == "__main__":
    unittest.main()
