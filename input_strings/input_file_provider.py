"""
Concrete implementation of InputProvider using file-based input.
"""

# Imports
import os
from typing import List
from input_strings.input_provider import InputProvider
from input_strings.input_strings_config import InputStringsConfig
from input_strings.input_string_errors import InputStringError


class InputFileProvider(InputProvider):
    """
    Class responsible for reading and processing input strings from a file.
    """
    def __init__(self, input_file_path: str, input_strings_config: InputStringsConfig):
        """
        Initializes the InputFileProcessor.

        Args:
            input_file_path (str): Path to the input file.
            input_strings_config (InputStringsConfig): Configuration of the input strings.
        """
        self.input_file_path: str = input_file_path
        self.inputs: List[str] = []
        self.input_strings_config: InputStringsConfig = input_strings_config

    def load(self) -> None:
        """
        Loads lines from the input file.

        Raises:
            FileNotFoundError: If the input file does not exist.
            InputStringError: If a line violates constraints (e.g., invalid length)
        """
        if not os.path.exists(self.input_file_path):
            raise FileNotFoundError(f"Input file '{self.input_file_path}' does not exist!")

        min_line_length = self.input_strings_config.min_line_length
        max_line_length = self.input_strings_config.max_line_length

        # Open the file and read line by line
        with open(self.input_file_path, mode="r", encoding="utf-8") as file:
            for line in file:
                # Validate line length
                line_length = len(line)
                if not min_line_length <= line_length <= max_line_length:
                    raise InputStringError(
                        f"Line '{line}' does not meet the length constraints "
                        f"({min_line_length} <= len(line) <= {max_line_length})."
                    )

                self.inputs.append(line)

        if not self.inputs:
            raise InputStringError(f"Input file '{self.input_file_path}' is empty.")

    def get(self) -> List[str]:
        """
        Returns the input strings.

        Returns:
            List[str]: A list of input strings.
        """
        return self.inputs
