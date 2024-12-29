"""
Python module that serves as a blueprint for all configuration types.
"""

# Imports
from pydantic import BaseModel


class Config(BaseModel):
    """
    Base class for all configuration types using Pydantic.
    Provides validation and serialization out of the box.
    """
    pass
