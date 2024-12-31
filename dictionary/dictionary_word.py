"""
Python module that is responsible for implementing the DictionaryWord class.
"""

# Imports
from dataclasses import dataclass, field


@dataclass
class DictionaryWord:
    """
    Class representing a dictionary word.
    """
    value: str
    value_length: int = field(init=False)

    def __post_init__(self):
        """Post initialization."""
        self.value_length = len(self.value)

        # Ensures that the original word cannot be empty
        if self.value_length <= 0:
            raise ValueError("The word value be empty.")
