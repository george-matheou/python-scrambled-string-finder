"""
Test cases for InputStringsConfig.
"""

# Imports
import unittest
from pydantic import ValidationError
from input_strings.input_strings_config import InputStringsConfig


class TestInputStringsConfig(unittest.TestCase):
    """
    Unit tests for the InputStringsConfig class.
    """
    def test_valid_config(self):
        """Test creating a valid InputStringsConfig instance."""
        config = InputStringsConfig(min_line_length=5, max_line_length=100)
        self.assertEqual(config.min_line_length, 5)
        self.assertEqual(config.max_line_length, 100)

    def test_invalid_config_min_greater_than_max(self):
        """Test that a ValueError is raised when min_line_length > max_line_length."""
        with self.assertRaises(ValueError) as err:
            InputStringsConfig(min_line_length=200, max_line_length=100)
        self.assertIn("must be greater than or equal to", str(err.exception))

    def test_invalid_config_negative_values(self):
        """Test that a ValidationError is raised for negative values."""
        with self.assertRaises(ValidationError):
            InputStringsConfig(min_line_length=-5, max_line_length=100)

        with self.assertRaises(ValidationError):
            InputStringsConfig(min_line_length=5, max_line_length=0)


if __name__ == "__main__":
    unittest.main()
