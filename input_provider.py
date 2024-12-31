"""
Abstract module for input providers.
"""

# Imports
from abc import ABC, abstractmethod
from typing import List


class InputProvider(ABC):
    """
    Abstract class to define the interface for input providers.
    """

    @abstractmethod
    def load(self) -> None:
        """
        Loads the input data.

        Raises:
            Exception: If the input cannot be loaded.
        """
        pass

    @abstractmethod
    def get(self) -> List[str]:
        """
        Returns the input strings.

        Returns:
            List[str]: A list of input strings.
        """
        pass
