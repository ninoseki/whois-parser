import importlib.metadata as importlib_metadata

from .dataclasses import WhoisRecord  # noqa: F401
from .parser import WhoisParser  # noqa: F401

__version__ = importlib_metadata.version(__name__)
