"""
Python module that contains utility functions for configuration.
"""

# Imports
from .config import Config


def print_config(config_name: str, config: Config) -> None:
    """
    Prints configuration information about the given configuration.

    Args:
        config_name (str): The name of the configuration.
        config (Config): The configuration object.
    """
    title = f"{config_name} configuration:"

    print(title)
    print(f"{'-' * len(title)}")
    for key, value in config.model_dump().items():
        print(f"  {key}: {value}")
