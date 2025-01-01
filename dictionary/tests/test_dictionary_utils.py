"""
Test cases for Dictionary utility functions
"""

# Imports
import unittest
from dictionary.dictionary_utils import (
    compute_canonical_form,
    validate_word_length_or_raise,
    validate_total_length_or_raise,
)
from dictionary.dictionary_errors import DictionaryError


class TestDictionaryUtils(unittest.TestCase):
    """Unit tests for utility functions in dictionary_utils."""

    def test_compute_canonical_form(self):
        """Test that canonical forms are computed correctly."""
        self.assertEqual(compute_canonical_form("a"), "a")
        self.assertEqual(compute_canonical_form("ab"), "ab")
        self.assertEqual(compute_canonical_form("acb"), "acb")
        self.assertEqual(compute_canonical_form("acab"), "aacb")
        self.assertEqual(compute_canonical_form("scramble"), "sabclmre")

    def test_validate_word_length_or_raise(self):
        """Test that word length validation works as expected."""
        validate_word_length_or_raise("test", 2, 10)  # Should pass
        with self.assertRaises(DictionaryError):
            validate_word_length_or_raise("t", 2, 10)  # Too short
        with self.assertRaises(DictionaryError):
            validate_word_length_or_raise("this_is_a_very_long_word", 2, 10)  # Too long

    def test_validate_total_length_or_raise(self):
        """Test that total length validation works as expected."""
        validate_total_length_or_raise(50, 100)  # Should pass
        with self.assertRaises(DictionaryError):
            validate_total_length_or_raise(150, 100)  # Exceeds max length


if __name__ == "__main__":
    unittest.main()
