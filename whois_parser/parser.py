from typing import Dict, Optional, Type

from whois_parser.parsers.be import BeParser
from whois_parser.parsers.uk import UkParser

from . import dataclasses
from .parsers import BaseParser, JpParser

PARSERS_MAP: Dict[str, Type[BaseParser]] = {
    "jp": JpParser,
    "uk": UkParser,
    "be": BeParser,
}


def get_default_parsers_map() -> Dict[str, Type[BaseParser]]:
    return PARSERS_MAP


def get_parser(
    tld: Optional[str], parsers_map: Dict[str, Type[BaseParser]]
) -> Type[BaseParser]:
    if tld is None:
        return BaseParser

    return parsers_map.get(tld, BaseParser)


class WhoisParser:
    def __init__(self, parsers_map: Dict[str, Type[BaseParser]] = PARSERS_MAP):
        self.parsers_map = parsers_map

    def parse(
        self, raw_text: str, *, hostname: Optional[str] = None
    ) -> dataclasses.WhoisRecord:
        """Parse a whois record and return it as a data class object

        Args:
            raw_text (str): Whois record
            hostname (Optional[str], optional): Defaults to None.

        Returns:
            dataclasses.WhoisRecord:
        """
        tld: Optional[str] = None
        if hostname is not None:
            tld = hostname.split(".")[-1]

        parser = get_parser(tld, parsers_map=self.parsers_map)
        return parser.parse(raw_text)
