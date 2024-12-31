"""
Python module that is responsible for reading a configuration file.
"""

# Imports
import configparser
import os
from typing import Type
from .config import Config


class ConfigReader:
    """
    Class that is responsible for reading a configuration file.

    Raises:
        FileNotFoundError: If configuration file does not exist.
    """
    def __init__(self, config_file_path: str):
        if not os.path.exists(config_file_path):
            raise FileNotFoundError(f"Config file path = {config_file_path} does not exist!")

        self._config = configparser.ConfigParser()
        # Read the config file
        self._config.read(config_file_path)

    def get_config(self, section: str, config_object_type: Type[Config]) -> Config:
        """
        Fetches the configuration for the given section and returns a Config object holding the configuration data.

        Args:
            section (str): The name of the section in the configuration file.
            config_object_type (Type[Config]): The type of the configuration object that will be returned.

        Returns:
            Config: The configuration object holding the configuration data.

        Raises:
            ValueError: If section is not found in the configuration file.
        """
        if not self._config.has_section(section):
            raise ValueError(f"Section '{section}' not found in the configuration file.")

        # Convert the section data to a flat dictionary with lowercase keys
        config_data = {key.lower(): value for key, value in self._config.items(section)}

        # Create and return an instance of the Pydantic model
        return config_object_type(**config_data)
