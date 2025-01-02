"""
Python module that is responsible for the configuration of input strings.
"""

# Imports
from pydantic import Field, model_validator
from config.config import Config


class InputStringsConfig(Config):
    """
    Class that contains configuration for the input strings.
    """

    min_line_length: int = Field(
        default=2,
        ge=1,
        description="Minimum length of input strings (must be positive)."
    )

    max_line_length: int = Field(
        default=500,
        ge=1,
        description="Maximum length of input words (must be positive)."
    )

    @model_validator(mode='after')
    def validate_attributes(self):
        """
        Validates the following:
            - max_line_length is greater than min_line_length.
        """

        if self.min_line_length > self.max_line_length:
            raise ValueError(
                f"`max_line_length` ({self.max_line_length}) must be greater than or equal to "
                f"`min_line_length` ({self.min_line_length})."
            )

        return self
