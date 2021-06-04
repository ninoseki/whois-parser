from tests.utils import read_fixture
from whois_parser.parser import WhoisParser


def test_parse():
    hostname = "google.be"
    filename = f"{hostname}.txt"

    raw_text = read_fixture(filename)

    parser = WhoisParser()
    result = parser.parse(hostname=hostname, raw_text=raw_text)

    assert result.registrar == "MarkMonitor Inc."
