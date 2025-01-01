"""
Python module that is responsible for logging functionalities.
"""

# Imports
import logging
import sys
from logging import handlers
from log.logger import Logger
from log.log_config import LogConfig
from utils.file_utils import create_parent_directories


class StandardLogger(Logger):
    """
    Singleton class that manages a global logger instance for the application.
    """
    _instance = None

    def __new__(cls, log_config: LogConfig, logger_name: str):
        """
        Creates a new instance of Logger if it doesn't exist or returns the existing instance.

        Args:
            log_config (LogConfig): The LogConfig object used to configure the logger.
            logger_name (str): The name of the logger.

        Returns:
            Logger: The single instance of Logger.
        """
        # If instance doesn't exist, create it
        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls)
            # Use the provided LogConfig to initialize the logger
            cls._instance._logger = cls._initialize_logger(log_config, logger_name)
        return cls._instance

    @classmethod
    def reset_instance(cls):
        """Resets the singleton instance."""
        cls._instance = None

    @staticmethod
    def _initialize_logger(log_config: LogConfig, logger_name: str) -> logging.Logger:
        """
         Initializes the logger based on the provided LogConfig.

         This method sets up a file handler, console handler (optional), and other logger properties such as level,
         based on the settings provided in the LogConfig.

         Args:
             log_config (LogConfig): The configuration object used to configure the logger.

         Returns:
             logging.Logger: The configured logger instance.
         """
        # Create logger
        logger = logging.getLogger(logger_name)

        try:
            level = logging.getLevelName(log_config.log_level)
            logger.setLevel(level)
        except Exception as err:
            print(f"Error while trying to set log level to {log_config.log_level}. {err}")

        # Set the format of the log output
        log_format = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

        # Customize the date format without milliseconds
        log_format.datefmt = "%Y-%m-%d %H:%M:%S"

        # Enable stdout logging
        if log_config.log_enable_console:
            stdout_handler = logging.StreamHandler(sys.stdout)
            stdout_handler.setFormatter(log_format)
            logger.addHandler(stdout_handler)

        # Enable file logging
        create_parent_directories(log_config.log_file)
        file_handler = handlers.RotatingFileHandler(filename=log_config.log_file,
                                                    maxBytes=log_config.log_max_bytes,
                                                    backupCount=log_config.log_backup_count)
        file_handler.setFormatter(log_format)
        logger.addHandler(file_handler)

        return logger

    def info(self, message: str) -> None:
        """Logs an informational message."""
        self._logger.info(message) # pylint: disable=no-member

    def debug(self, message: str) -> None:
        """Logs a debug message."""
        self._logger.debug(message) # pylint: disable=no-member

    def warning(self, message: str) -> None:
        """Logs a warning message."""
        self._logger.warning(message) # pylint: disable=no-member

    def error(self, message: str) -> None:
        """Logs an error message."""
        self._logger.error(message) # pylint: disable=no-member

    def critical(self, message: str) -> None:
        """Logs a critical message."""
        self._logger.critical(message) # pylint: disable=no-member

    def always(self, message: str) -> None:
        """Logs a message always."""
        self._logger.log(100, message)  # Custom log level higher than CRITICAL # pylint: disable=no-member
