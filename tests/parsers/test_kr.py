from datetime import datetime

from tests.utils import read_fixture
from whois_parser.parser import WhoisParser


def test_parse():
    hostname = "google.kr"
    filename = f"{hostname}.txt"

    raw_text = read_fixture(filename)

    parser = WhoisParser()
    result = parser.parse(hostname=hostname, raw_text=raw_text)

    assert result.registrant.name == "Google Korea, LLC"

    assert isinstance(result.registered_at, datetime)
    assert isinstance(result.updated_at, datetime)
