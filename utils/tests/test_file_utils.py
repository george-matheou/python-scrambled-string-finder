"""
Test cases for file utilities.
"""

# Imports
import unittest
from unittest.mock import patch
from utils.file_utils import create_parent_directories


class TestFileUtils(unittest.TestCase):
    """
    Unit tests for the file_utils module.
    """
    @patch("os.makedirs")  # Mocking os.makedirs to avoid actual directory creation
    def test_create_parent_directories_success(self, mock_makedirs):
        """Test that create_parent_directories calls os.makedirs correctly."""
        path = "/path/to/file.txt"

        # Call the function
        create_parent_directories(path)

        # Assert that os.makedirs was called with the expected directory path
        mock_makedirs.assert_called_once_with("/path/to", exist_ok=True)

    @patch("os.makedirs")
    def test_create_parent_directories_already_exists(self, mock_makedirs):
        """Test that create_parent_directories doesn't create directories if they already exist."""
        path = "/path/to/existing/file.txt"

        # Simulate that the directory already exists by making os.makedirs do nothing
        mock_makedirs.return_value = None

        # Call the function
        create_parent_directories(path)

        # Assert that os.makedirs was called once
        mock_makedirs.assert_called_once_with("/path/to/existing", exist_ok=True)

    @patch("os.makedirs")
    def test_create_parent_directories_error(self, mock_makedirs):
        """Test that create_parent_directories raises an OSError if directory creation fails."""
        path = "/path/to/file.txt"

        # Simulate an error when creating directories
        mock_makedirs.side_effect = OSError("Permission denied")

        # Call the function and assert that it raises an OSError
        with self.assertRaises(OSError):
            create_parent_directories(path)


if __name__ == "__main__":
    unittest.main()
