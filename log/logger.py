"""
Abstract module for logger abstraction.

Defines the `Logger` interface for decoupling logging operations
from specific implementations.
"""

from abc import ABC, abstractmethod


class Logger(ABC):
    """
    Abstract base class for logging operations.
    """

    @abstractmethod
    def info(self, message: str) -> None:
        """
        Logs an informational message.

        Args:
            message (str): The message to log.
        """
        pass

    @abstractmethod
    def debug(self, message: str) -> None:
        """
        Logs a debug message.

        Args:
            message (str): The message to log.
        """
        pass

    @abstractmethod
    def warning(self, message: str) -> None:
        """
        Logs a warning message.

        Args:
            message (str): The message to log.
        """
        pass

    @abstractmethod
    def error(self, message: str) -> None:
        """
        Logs an error message.

        Args:
            message (str): The message to log.
        """
        pass

    @abstractmethod
    def critical(self, message: str) -> None:
        """
        Logs a critical message.

        Args:
            message (str): The message to log.
        """
        pass


    @abstractmethod
    def always(self, message: str) -> None:
        """
        Logs a message always.

        Args:
            message (str): The message to log.
        """
        pass
