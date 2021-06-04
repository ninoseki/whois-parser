import poetry_version

from whois_parser.parser import WhoisParser  # noqa

__version__ = str(poetry_version.extract(source_file=__file__))
