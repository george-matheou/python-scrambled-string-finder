"""
Test cases for TestInputFileProvider.
"""

# Imports
import unittest
from unittest.mock import mock_open, patch
from input_strings.input_file_provider import InputFileProvider
from input_strings.input_strings_config import InputStringsConfig
from input_strings.input_string_errors import InputStringError


class TestInputFileProvider(unittest.TestCase):
    """
    Unit tests for the InputFileProvider class.
    """
    def setUp(self):
        """Set up test configuration and provider."""
        self.config = InputStringsConfig(min_line_length=3, max_line_length=10)
        self.file_path = "test_file.txt"

    @patch("os.path.exists", return_value=True)
    @patch("builtins.open", new_callable=mock_open, read_data="valid_str")
    def test_load_valid_file(self, mock_file, mock_exists):
        """Test loading a valid file."""
        provider = InputFileProvider(self.file_path, self.config)
        provider.load()
        self.assertEqual(provider.get(), ["valid_str"])

    @patch("os.path.exists", return_value=True)
    @patch("builtins.open", new_callable=mock_open, read_data="too_long_line_exceeds\nvalid\n")
    def test_line_too_long(self, mock_file, mock_exists):
        """Test loading a file with a line exceeding the max length."""
        provider = InputFileProvider(self.file_path, self.config)
        with self.assertRaises(InputStringError):
            provider.load()

    @patch("os.path.exists", return_value=True)
    @patch("builtins.open", new_callable=mock_open, read_data="")
    def test_empty_file(self, mock_file, mock_exists):
        """Test loading an empty file."""
        provider = InputFileProvider(self.file_path, self.config)
        with self.assertRaises(InputStringError):
            provider.load()

    @patch("os.path.exists", return_value=False)
    def test_file_not_found(self, mock_exists):
        """Test file not found."""
        provider = InputFileProvider(self.file_path, self.config)
        with self.assertRaises(FileNotFoundError):
            provider.load()


if __name__ == "__main__":
    unittest.main()
