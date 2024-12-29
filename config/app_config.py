"""
Python module that is responsible for managing the main configuration of the application.
"""

# Imports
from pydantic import Field, model_validator
from .config import Config


class AppConfig(Config):
    """
    Class that contains main configuration for the application.
    """

    dictionary_min_word_length: int = Field(
        default=5,
        ge=1,
        description="Minimum length of dictionary words (must be positive)."
    )

    dictionary_max_word_length: int = Field(
        default=200,
        ge=1,
        description="Maximum length of dictionary words (must be positive)."
    )

    dictionary_max_sum_lengths_of_all_words: int = Field(
        default=200,
        ge=1,
        description="Maximum sum of all dictionary word lengths (must be positive)."
    )

    @model_validator(mode='after')
    def validate_attributes(self):
        """
        Validates the following:
            - dictionary_max_word_length is greater than dictionary_min_word_length.
            - dictionary_max_sum_lengths_of_all_words is greater than or equal dictionary_max_word_length
        """

        if self.dictionary_min_word_length > self.dictionary_max_word_length:
            raise ValueError(f"`dictionary_max_word_length` ({self.dictionary_max_word_length}) must be greater "
                             f"than `dictionary_min_word_length` ({self.dictionary_min_word_length}).")

        if self.dictionary_max_word_length > self.dictionary_max_sum_lengths_of_all_words:
            raise ValueError(
                f"`dictionary_max_sum_lengths_of_all_words` ({self.dictionary_max_sum_lengths_of_all_words}) must be "
                f"greater than or equal to `dictionary_max_word_length` ({self.dictionary_max_word_length})."
            )

        return self
