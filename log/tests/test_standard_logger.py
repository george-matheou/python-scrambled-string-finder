"""
Test cases for StandardLogger
"""

# Imports
import unittest
from unittest.mock import patch, MagicMock
import logging
from log.log_config import LogConfig
from log.standard_logger import StandardLogger


class TestStandardLogger(unittest.TestCase):
    """
    Unit tests for the StandardLogger class.
    """
    def setUp(self):
        """
        Set up a sample LogConfig for testing.
        """
        self.log_config = LogConfig(
            log_file="test.log",
            log_max_bytes=1024,
            log_backup_count=3,
            log_enable_console=True,
            log_level="INFO"
        )

    @patch("log.standard_logger.logging.getLogger")
    @patch("log.standard_logger.create_parent_directories")
    def test_singleton_behavior(self, _, mock_get_logger):
        """
        Test that StandardLogger behaves as a singleton.
        """
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger

        logger1 = StandardLogger(self.log_config, "test_logger_name")
        logger2 = StandardLogger(self.log_config, "test_logger_name")

        self.assertIs(logger1, logger2, "StandardLogger is not behaving as a singleton.")

    @patch("log.standard_logger.logging.getLogger")
    @patch("log.standard_logger.create_parent_directories")
    def test_logger_initialization(self, mock_create_parent_dirs, mock_get_logger):
        """
        Test that the logger is initialized correctly with the provided configuration.
        """
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger

        StandardLogger(self.log_config, "test_logger_name")

        # Ensure logger's methods are called correctly
        mock_get_logger.assert_called_with("test_logger_name")
        mock_logger.setLevel.assert_called_with(logging.getLevelName("INFO"))
        mock_create_parent_dirs.assert_called_with("test.log")

    @patch("log.standard_logger.create_parent_directories")  # Mock directory creation
    @patch("log.standard_logger.logging.getLogger")  # Mock the logger
    def test_logging_methods(self, mock_get_logger, _):
        """
        Test that logging methods call the appropriate logger methods.
        """
        # Reset the singleton instance to ensure a fresh start
        StandardLogger.reset_instance()

        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger

        logger = StandardLogger(self.log_config, "test_logger_name")

        # Test info
        logger.info("This is an info message")
        mock_logger.info.assert_called_with("This is an info message")

        # Test debug
        logger.debug("This is a debug message")
        mock_logger.debug.assert_called_with("This is a debug message")

        # Test warning
        logger.warning("This is a warning message")
        mock_logger.warning.assert_called_with("This is a warning message")

        # Test error
        logger.error("This is an error message")
        mock_logger.error.assert_called_with("This is an error message")

        # Test critical
        logger.critical("This is a critical message")
        mock_logger.critical.assert_called_with("This is a critical message")


if __name__ == "__main__":
    unittest.main()
