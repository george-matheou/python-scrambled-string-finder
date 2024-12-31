"""
Python module that is responsible for managing the log configuration.
"""

# Imports
from typing import Literal
from pydantic import Field, field_validator
from config.config import Config


class LogConfig(Config):
    """
    Class that manages configuration data for logging.
    """

    # Fields
    log_file: str = Field(
        default="/var/log/scrmabled_strings/app.log",
        description="Path to the log file."
    )

    log_max_bytes: int = Field(
        default=10_000_000,
        ge=1,
        description="Maximum size of the log file in bytes (must be positive)."
    )

    log_backup_count: int = Field(
        default=5,
        ge=1,
        description="Number of backup log files to retain (must be positive)."
    )

    log_enable_console: bool = Field(
        default=True,
        description="Whether to enable console logging."
    )

    log_level: Literal["CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG"] = Field(
        default="INFO",
        description="Logging level (must be one of CRITICAL, ERROR, WARNING, INFO, DEBUG)."
    )

    @field_validator("log_level", mode="before")
    # pylint: disable=no-self-argument
    def normalize_log_level(cls, value: str) -> str:
        """
        Converts the log_level attribute to uppercase.
        """
        return value.upper()

    @field_validator("log_file", mode="before")
    # pylint: disable=no-self-argument
    def validate_log_file(cls, value: str) -> str:
        """
        Ensures that log_file is not null or an empty string.
        """
        if not value or not value.strip():
            raise ValueError("`log_file` cannot be null or an empty string.")
        return value
