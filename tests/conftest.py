import pytest

from whois_parser.parser import WhoisParser


@pytest.fixture
def parser() -> WhoisParser:
    return WhoisParser()
