from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Optional, Type, Union

from pyparsing import ParserElement

from .. import dataclasses
from .constants import ANY_CHARACTERS, DEILIMITER, SPACE_OR_TAB
from .utils import build_common_prefix_pattern, find, find_all, parse_datetime


def normalize_raw_text(raw_text: str) -> str:
    """Normalize raw text

    Args:
        raw_text (str): whois record in plain text

    Returns:
        str: Returns whois record without the whois server section
    """
    reversed_lines = raw_text.splitlines()
    reversed_lines.reverse()

    # find first comment which starts with "#"
    sharp_index: Optional[int] = None
    for index in range(len(reversed_lines)):
        line = reversed_lines[index]
        if line.startswith("#"):
            sharp_index = index + 1
            break

    if sharp_index is None:
        return raw_text

    lines: List[str] = []
    for line in reversed_lines[:sharp_index]:
        lines.append(line.strip())

    # revert reversed lines
    lines.reverse()

    return "\n".join(lines)


class AbstractParser(ABC):
    def __init__(self, raw_text: str):
        self.raw_text: str = raw_text
        self._normalized_raw_text: str = normalize_raw_text(raw_text)

    @classmethod
    def parse(cls, raw_text: str) -> dataclasses.WhoisRecord:
        """Parse a whois record and return it as a data class object

        Args:
            raw_text (str): Whois record

        Returns:
            dataclasses.WhoisRecord: Parsed whois record
        """
        instance = cls(raw_text)
        return instance._parse()

    def _parse(self) -> dataclasses.WhoisRecord:
        """Parse a whois record and return it as a data class object

        Returns:
            dataclasses.WhoisRecord: Parsed whois record
        """
        return dataclasses.WhoisRecord(
            raw_text=self.raw_text,
            abuse=self._find_abuse(),
            admin=self._find_admin(),
            domain=self._find_domain(),
            expires_at=self._find_expires_at(),
            name_servers=self._find_name_servers(),
            registered_at=self._find_registered_at(),
            registrant=self._find_registrant(),
            registrar=self._find_registrar(),
            statuses=self._find_statuses(),
            tech=self._find_tech(),
            updated_at=self._find_updated_at(),
        )

    @abstractmethod
    def _find_tech(self) -> dataclasses.Tech:
        """Find tech fields

        Returns:
            dataclasses.Tech:
        """

    @abstractmethod
    def _find_admin(self) -> dataclasses.Admin:
        """Find admin fields

        Returns:
            dataclasses.Admin:
        """

    @abstractmethod
    def _find_registrant(self) -> dataclasses.Registrant:
        """Find registrant fields

        Returns:
            dataclasses.Registrant:
        """

    @abstractmethod
    def _find_abuse(self) -> dataclasses.Abuse:
        """Find abuse fields

        Returns:
            dataclasses.Abuse:
        """

    @abstractmethod
    def _find_domain(self) -> Optional[str]:
        """Find domain field

        Returns:
            Optional[str]:
        """

    @abstractmethod
    def _find_registered_at(self) -> Optional[Union[str, datetime]]:
        """Find registered at field

        Returns:
            Optional[Union[str, datetime]]: Returns str if it's not possible to covert it as a datetime
        """

    @abstractmethod
    def _find_updated_at(self) -> Optional[Union[str, datetime]]:
        """Find updated at field

        Returns:
            Optional[Union[str, datetime]]: Returns str if it's not possible to covert it as a datetime
        """

    @abstractmethod
    def _find_expires_at(self) -> Optional[Union[str, datetime]]:
        """Find expires at field

        Returns:
            Optional[Union[str, datetime]]: Returns str if it's not possible to covert it as a datetime
        """

    @abstractmethod
    def _find_registrar(self) -> Optional[str]:
        """Find registrar field

        Returns:
            Optional[str]:
        """

    @abstractmethod
    def _find_statuses(self) -> List[str]:
        """Find a list of status filed

        Returns:
            List[str]: Returns an empty list if found nothing
        """

    @abstractmethod
    def _find_name_servers(self) -> List[str]:
        """Find a list of name server field

        Returns:
            List[str]: Returns an empty list if found nothing
        """

    def _find(
        self,
        prefix: Type[ParserElement],
        *,
        delimiter: Optional[Type[ParserElement]] = SPACE_OR_TAB,
        target: Type[ParserElement] = ANY_CHARACTERS
    ) -> Optional[str]:
        """Find text which matches with PyParsing expression

        Args:
            prefix (Type[ParserElement]): [description]
            delimiter (Optional[Type[ParserElement]], optional): [description]. Defaults to White().
            target (Type[ParserElement], optional): [description]. Defaults to Regex(".+").

        Returns:
            Optional[str]: Returns a first matched text. Returns None if nothing matched.
        """
        grammar = prefix
        if delimiter is not None:
            grammar += delimiter
        grammar += target("value")
        return find(text=self._normalized_raw_text, grammar=grammar)

    def _find_datetime(
        self,
        prefix: Type[ParserElement],
        *,
        delimiter: Optional[Type[ParserElement]] = SPACE_OR_TAB,
        target: Type[ParserElement] = ANY_CHARACTERS
    ) -> Optional[Union[str, datetime]]:
        """Find text which matches with PyParsing expression and return it as a datetime

        Args:
            prefix (Type[ParserElement]): [description]
            delimiter (Optional[Type[ParserElement]], optional): [description]. Defaults to White().
            target (Type[ParserElement], optional): [description]. Defaults to Regex(".+").

        Returns:
            Optional[str]: Returns a first matched text as a datetime. Returns str if it's not possible to convert. Also, returns None if nothing matched.
        """
        value = self._find(prefix, delimiter=delimiter, target=target)
        if value is None:
            return None

        return parse_datetime(value)

    def _find_all(
        self,
        prefix: Type[ParserElement],
        *,
        delimiter: Optional[Type[ParserElement]] = SPACE_OR_TAB,
        target: Type[ParserElement] = ANY_CHARACTERS
    ) -> List[str]:
        """Find a list of text which matches with a PyParsing expression

        Args:
            prefix (Type[ParserElement]): [description]
            delimiter (Optional[Type[ParserElement]], optional): [description]. Defaults to White().
            target (Type[ParserElement], optional): [description]. Defaults to Regex(".+").

        Returns:
            Optional[str]: Returns a list of matched text. Returns en empty list if nothing matched.
        """
        grammar = prefix
        if delimiter is not None:
            grammar += delimiter
        grammar += target("value")
        return find_all(text=self._normalized_raw_text, grammar=grammar)

    def _find_by_keywords(
        self,
        keywords: List[str],
        *,
        delimiter: Optional[str] = DEILIMITER,
        is_case_sensitive: bool = False,
        is_line_start_sensitive: bool = True
    ) -> Optional[str]:
        """Find text which matches with a keyword

        Args:
            keywords (List[str]): [description] A list of keyword for prefix. A keyword is converted to a PyPyarsing expression.
            delimiter (Optional[str], optional): Defaults to ":".
            is_case_sensitive (bool, optional): Defaults to False.
            is_line_start_sensitive (bool, optional): Defaults to True.

        Returns:
            Optional[str]: Returns a first matched text. Returns None if nothing matched.
        """
        for keyword in keywords:
            value = self._find(
                build_common_prefix_pattern(
                    keyword,
                    is_case_sensitive=is_case_sensitive,
                    is_line_start_sensitive=is_line_start_sensitive,
                    delimiter=delimiter,
                )
            )
            if value is not None:
                return value

        return None

    def _find_datetime_by_keywords(
        self,
        keywords: List[str],
        *,
        delimiter: Optional[str] = DEILIMITER,
        is_case_sensitive: bool = False,
        is_line_start_sensitive: bool = True
    ) -> Optional[Union[datetime, str]]:
        """Find text which matches with a keyword and return it as a datetime

        Args:
            keywords (List[str]): [description] A list of keyword for prefix. A keyword is converted to a PyPyarsing expression.
            delimiter (Optional[str], optional): Defaults to ":".
            is_case_sensitive (bool, optional): Defaults to False.
            is_line_start_sensitive (bool, optional): Defaults to True.

        Returns:
            Optional[Union[datetime, str]]: Returns a first matched text as a datetime. Returns str if it's not possible to convert. Also, returns None if nothing matched.
        """
        for keyword in keywords:
            value = self._find_datetime(
                build_common_prefix_pattern(
                    keyword,
                    is_case_sensitive=is_case_sensitive,
                    is_line_start_sensitive=is_line_start_sensitive,
                    delimiter=delimiter,
                )
            )
            if value is not None:
                return value

        return None

    def _find_all_by_keywords(
        self,
        keywords: List[str],
        *,
        delimiter: Optional[str] = DEILIMITER,
        is_case_sensitive: bool = False,
        is_line_start_sensitive: bool = True
    ) -> List[str]:
        """Find a list of text which matches with a keyword

        Args:
            keywords (List[str]): [description] A list of keyword for prefix. A keyword is converted to a PyPyarsing expression.
            delimiter (Optional[str], optional): Defaults to ":".
            is_case_sensitive (bool, optional): Defaults to False.
            is_line_start_sensitive (bool, optional): Defaults to True.

        Returns:
            List[str]: Returns a list of matched text. Returns en empty list if nothing matched.
        """
        for keyword in keywords:
            values = self._find_all(
                build_common_prefix_pattern(
                    keyword,
                    is_case_sensitive=is_case_sensitive,
                    is_line_start_sensitive=is_line_start_sensitive,
                    delimiter=delimiter,
                )
            )
            if len(values) > 0:
                return values

        return []
