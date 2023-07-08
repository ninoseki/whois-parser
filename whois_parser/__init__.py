import importlib.metadata as importlib_metadata

from whois_parser.parser import WhoisParser  # noqa

__version__ = importlib_metadata.version(__name__)
