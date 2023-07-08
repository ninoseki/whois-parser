from tests.utils import read_fixture
from whois_parser.parser import WhoisParser


def test_parse(parser: WhoisParser):
    hostname = "google.uk"
    filename = f"{hostname}.txt"

    raw_text = read_fixture(filename)

    result = parser.parse(hostname=hostname, raw_text=raw_text)
    assert (
        result.registrar == "Markmonitor Inc. t/a MarkMonitor Inc. [Tag = MARKMONITOR]"
    )
