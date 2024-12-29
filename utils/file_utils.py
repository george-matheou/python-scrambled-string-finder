"""
Python module that includes utility functions for file manipulation.
"""

# Imports
import os


def create_parent_directories(path: str) -> None:
    """Creates parent directories of a path if they do not exist."""

    try:
        # Create the parent directories if they do not exist
        os.makedirs(os.path.dirname(path), exist_ok=True)
    except Exception as err:
        raise OSError(f"Failed to create parent directories for '{path}': {err}") from err
