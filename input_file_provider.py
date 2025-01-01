"""
Concrete implementation of InputProvider using file-based input.
"""

# Imports
import os
from typing import List
from input_provider import InputProvider


class InputFileProvider(InputProvider):
    """
    Class responsible for reading and processing input strings from a file.
    """
    def __init__(self, input_file_path: str):
        """
        Initializes the InputFileProcessor.

        Args:
            input_file_path (str): Path to the input file.
        """
        self.input_file_path: str = input_file_path
        self.inputs: List[str] = []

    def load(self) -> None:
        """
        Loads lines from the input file.

        Raises:
            FileNotFoundError: If the input file does not exist.
        """
        if not os.path.exists(self.input_file_path):
            raise FileNotFoundError(f"Input file '{self.input_file_path}' does not exist!")

        # Open the file and read line by line
        with open(self.input_file_path, mode="r", encoding="utf-8") as file:
            for line in file:
                clean_line = line.strip()

                # Skip empty lines
                if not clean_line:
                    continue

                self.inputs.append(clean_line)

        if not self.inputs:
            raise ValueError(f"Input file '{self.input_file_path}' is empty.")

    def get(self) -> List[str]:
        """
        Returns the input strings.

        Returns:
            List[str]: A list of input strings.
        """
        return self.inputs
