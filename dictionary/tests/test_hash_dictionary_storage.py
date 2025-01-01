"""
Test cases for HashDictionaryStorage.
"""

# Imports
import unittest
from dictionary.hash_dictionary_storage import HashDictionaryStorage


class TestHashDictionaryStorage(unittest.TestCase):
    """
    Unit tests for the HashDictionaryStorage class.
    """

    def setUp(self):
        """Set up a fresh instance of HashDictionaryStorage for each test."""
        self.storage = HashDictionaryStorage()

    def test_add_and_contains_word(self):
        """Test adding words and checking their existence in the storage."""
        self.storage.add_word("test")
        self.assertTrue(self.storage.contains_word("test"))
        self.assertFalse(self.storage.contains_word("not_in_storage"))

    def test_get_all_words(self):
        """Test that all stored words are retrieved correctly."""
        self.storage.add_word("test")
        self.storage.add_word("example")
        self.assertEqual(self.storage.get_all_words(), {"test", "example"})

    def test_get_canonical_word(self):
        """Test retrieval of canonical forms for both existing and non-existing words."""
        self.storage.add_word("scramble")
        self.assertEqual(self.storage.get_canonical_word("scramble"), "sabclmre")
        self.assertEqual(self.storage.get_canonical_word("not_in_storage"), "n__aginoorstte")  # Dynamic computation


if __name__ == "__main__":
    unittest.main()
