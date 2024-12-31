"""
Python module that is responsible for managing the dictionary.
"""

# Imports
from pydantic import Field, model_validator
from config.config import Config


class DictionaryConfig(Config):
    """
    Class that contains configuration for the dictionary.
    """

    min_word_length: int = Field(
        default=5,
        ge=1,
        description="Minimum length of dictionary words (must be positive)."
    )

    max_word_length: int = Field(
        default=200,
        ge=1,
        description="Maximum length of dictionary words (must be positive)."
    )

    max_sum_lengths_of_all_words: int = Field(
        default=200,
        ge=1,
        description="Maximum sum of all dictionary word lengths (must be positive)."
    )

    @model_validator(mode='after')
    def validate_attributes(self):
        """
        Validates the following:
            - max_word_length is greater than min_word_length.
            - max_sum_lengths_of_all_words is greater than or equal max_word_length
        """

        if self.min_word_length > self.max_word_length:
            raise ValueError(f"`max_word_length` ({self.max_word_length}) must be greater "
                             f"than `min_word_length` ({self.min_word_length}).")

        if self.max_word_length > self.max_sum_lengths_of_all_words:
            raise ValueError(
                f"`max_sum_lengths_of_all_words` ({self.max_sum_lengths_of_all_words}) must be "
                f"greater than or equal to `max_word_length` ({self.max_word_length})."
            )

        return self
