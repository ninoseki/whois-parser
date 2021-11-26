from datetime import datetime

from tests.utils import read_fixture
from whois_parser.parser import WhoisParser


def test_parse():
    hostname = "example.me"
    filename = f"{hostname}.txt"

    raw_text = read_fixture(filename)

    parser = WhoisParser()
    result = parser.parse(hostname=hostname, raw_text=raw_text)

    assert isinstance(result.registered_at, datetime)
    assert result.updated_at is None
