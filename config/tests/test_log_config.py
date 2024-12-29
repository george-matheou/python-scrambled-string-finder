"""
Test cases for LogConfig
"""

# Imports
import unittest
from pydantic import ValidationError
from config.log_config import LogConfig


class TestLogConfig(unittest.TestCase):
    """
    Unit tests for the LogConfig class.
    """
    def test_log_config_valid(self):
        """Test that LogConfig loads valid values correctly."""
        config_data = {
            "log_file": "/var/log/app.log",
            "log_max_bytes": 8000000,
            "log_backup_count": 15,
            "log_enable_console": False,
            "log_level": "DEBUG"
        }
        log_config = LogConfig(**config_data)

        self.assertEqual(log_config.log_file, "/var/log/app.log")
        self.assertEqual(log_config.log_max_bytes, 8000000)
        self.assertEqual(log_config.log_backup_count, 15)
        self.assertFalse(log_config.log_enable_console)
        self.assertEqual(log_config.log_level, "DEBUG")

    def test_default_values(self):
        """Test that default values are set correctly."""
        config = LogConfig()
        self.assertEqual(config.log_file, "/var/log/scrmabled_strings/app.log")
        self.assertEqual(config.log_max_bytes, 10_000_000)
        self.assertEqual(config.log_backup_count, 5)
        self.assertTrue(config.log_enable_console)
        self.assertEqual(config.log_level, "INFO")

    def test_log_level_case_insensitivity(self):
        """Test that LogConfig handles log level case insensitivity."""
        config_data = {
            "log_file": "/var/log/app.log",
            "log_max_bytes": 8000000,
            "log_backup_count": 15,
            "log_enable_console": False,
            "log_level": "debug"
        }
        log_config = LogConfig(**config_data)
        self.assertEqual(log_config.log_level, "DEBUG")

    def test_invalid_log_level(self):
        """Test that LogConfig raises an error for invalid log levels."""
        config_data = {
            "log_file": "/var/log/app.log",
            "log_max_bytes": 8000000,
            "log_backup_count": 15,
            "log_enable_console": True,
            "log_level": "INVALID_LEVEL"
        }

        with self.assertRaises(ValueError) as context:
            LogConfig(**config_data)

        self.assertTrue("Input should be 'CRITICAL', 'ERROR', 'WARNING', 'INFO' or 'DEBUG'" in str(context.exception))

    def test_negative_log_max_bytes(self):
        """Test that a negative value for log_max_bytes raises an error."""
        with self.assertRaises(ValidationError) as context:
            LogConfig(log_max_bytes=-1)
        self.assertIn("Input should be greater than or equal to 1", str(context.exception))

    def test_negative_log_backup_count(self):
        """Test that a negative value for log_backup_count raises an error."""
        with self.assertRaises(ValidationError) as context:
            LogConfig(log_backup_count=-5)
        self.assertIn("Input should be greater than or equal to 1", str(context.exception))

    def test_empty_log_file(self):
        """Test that an empty log_file raises an error."""
        with self.assertRaises(ValidationError) as context:
            LogConfig(log_file="")
        self.assertIn("`log_file` cannot be null or an empty string", str(context.exception))

        with self.assertRaises(ValidationError) as context:
            LogConfig(log_file="   ")
        self.assertIn("`log_file` cannot be null or an empty string", str(context.exception))

if __name__ == '__main__':
    unittest.main()
