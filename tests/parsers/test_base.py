from datetime import datetime

from tests.utils import read_fixture
from whois_parser.parser import WhoisParser


def test_parse(parser: WhoisParser):
    hostname = "google.com"
    filename = f"{hostname}.txt"

    raw_text = read_fixture(filename)

    result = parser.parse(hostname=hostname, raw_text=raw_text)
    assert result.registrant.organization == "Google LLC"
    assert isinstance(result.expires_at, datetime)
    assert isinstance(result.registered_at, datetime)
    assert isinstance(result.updated_at, datetime)
    assert len(result.name_servers) == 4
