"""
Test cases for ConfigReader
"""

# Imports
import unittest
from unittest.mock import patch, MagicMock
from config.config_reader import ConfigReader
from config.config import Config


class TestConfigReader(unittest.TestCase):
    """
    Unit tests for the ConfigReader class.
    """

    @patch("os.path.exists")
    def test_init_file_not_found(self, mock_exists):
        """Tests that a FileNotFoundError is raised when the config file does not exist."""
        mock_exists.return_value = False  # Simulate that the file does not exist

        with self.assertRaises(FileNotFoundError):
            ConfigReader("non_existent_file.ini")

    @patch("os.path.exists")
    @patch("configparser.ConfigParser.read")
    def test_init_file_exists(self, mock_read, mock_exists):
        """Tests that the config file is read when the file exists."""
        mock_exists.return_value = True  # Simulate that the file exists
        mock_read.return_value = None  # Simulate successful reading of the file

        # This should not raise an exception
        config_reader = ConfigReader("existent_file.ini")
        self.assertIsInstance(config_reader, ConfigReader)  # Verify that an instance of ConfigReader is created

    @patch("os.path.exists")
    @patch("configparser.ConfigParser.sections")
    @patch("configparser.ConfigParser.items")
    def test_get_config_section_not_found(self, mock_items, mock_sections, mock_exists):
        """Tests that a ValueError is raised if the section is not found in the config file."""
        mock_exists.return_value = True
        mock_sections.return_value = ["other_section"]  # Simulate that the section doesn't exist
        mock_items.return_value = []  # Simulate no items in the section

        config_reader = ConfigReader("existent_file.ini")

        with self.assertRaises(ValueError):
            config_reader.get_config("non_existent_section", Config)

    @patch("os.path.exists")
    @patch("configparser.ConfigParser.sections")
    @patch("configparser.ConfigParser.items")
    @patch("configparser.ConfigParser.has_section")
    def test_get_config_success(self, mock_has_section, mock_items, mock_sections, mock_exists):
        """Tests that the correct configuration object is returned if the section exists."""
        mock_exists.return_value = True  # Simulate that path exists
        mock_sections.return_value = ["valid_section"]  # Simulate that "valid_section" exists
        mock_items.return_value = [("key1", "value1"), ("key2", "value2")]  # Simulate section data
        mock_has_section.return_value = True  # Simulate that has_section returns True for "valid_section"

        config_reader = ConfigReader("existent_file.ini")

        # Mock the config_object_type (Config class or subclass)
        mock_config = MagicMock(Config)
        mock_config.return_value = mock_config

        # Test if get_config correctly returns the config object
        result = config_reader.get_config("valid_section", Config)
        self.assertIsInstance(result, Config)  # Check that the returned object is of the correct type

if __name__ == "__main__":
    unittest.main()
