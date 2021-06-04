from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Optional, Type, Union

from pyparsing import ParserElement, Regex, White

from .. import dataclasses
from .utils import build_common_prefix_pattern, find, find_all, parse_datetime


def normalize_raw_text(raw_text: str) -> str:
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
        self.raw_text = raw_text
        self._normalized_raw_text = normalize_raw_text(raw_text)

    @classmethod
    def parse(cls, raw_text: str) -> dataclasses.WhoisRecord:
        instance = cls(raw_text)
        return instance._parse()

    def _parse(self) -> dataclasses.WhoisRecord:
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
        pass

    @abstractmethod
    def _find_admin(self) -> dataclasses.Admin:
        pass

    @abstractmethod
    def _find_registrant(self) -> dataclasses.Registrant:
        pass

    @abstractmethod
    def _find_abuse(self) -> dataclasses.Abuse:
        pass

    @abstractmethod
    def _find_domain(self) -> Optional[str]:
        pass

    @abstractmethod
    def _find_registered_at(self) -> Optional[Union[str, datetime]]:
        pass

    @abstractmethod
    def _find_updated_at(self) -> Optional[Union[str, datetime]]:
        pass

    @abstractmethod
    def _find_expires_at(self) -> Optional[Union[str, datetime]]:
        pass

    @abstractmethod
    def _find_registrar(self) -> Optional[str]:
        pass

    @abstractmethod
    def _find_statuses(self) -> List[str]:
        pass

    @abstractmethod
    def _find_name_servers(self) -> List[str]:
        pass

    def _find(
        self,
        prefix: Type[ParserElement],
        *,
        delimiter: Optional[Type[ParserElement]] = White(),
        target: Type[ParserElement] = Regex(".+")
    ) -> Optional[str]:
        grammar = prefix
        if delimiter is not None:
            grammar += delimiter
        grammar += target("value")
        return find(text=self._normalized_raw_text, grammar=grammar)

    def _find_datetime(
        self,
        prefix: Type[ParserElement],
        *,
        delimiter: Optional[Type[ParserElement]] = White(),
        target: Type[ParserElement] = Regex(".+")
    ) -> Optional[Union[str, datetime]]:
        value = self._find(prefix, delimiter=delimiter, target=target)
        if value is None:
            return None

        return parse_datetime(value)

    def _find_all(
        self,
        prefix: Type[ParserElement],
        *,
        delimiter: Optional[Type[ParserElement]] = White(),
        target: Type[ParserElement] = Regex(".+")
    ) -> List[str]:
        grammar = prefix
        if delimiter is not None:
            grammar += delimiter
        grammar += target("value")
        return find_all(text=self._normalized_raw_text, grammar=grammar)

    def _find_by_keywords(
        self,
        keywords: List[str],
        *,
        delimiter: Optional[str] = ":",
        is_case_sensitive: bool = False,
        is_line_start_sensitive: bool = True
    ) -> Optional[str]:
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
        delimiter: Optional[str] = ":",
        is_case_sensitive: bool = False,
        is_line_start_sensitive: bool = True
    ) -> Optional[Union[datetime, str]]:
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
        delimiter: Optional[str] = ":",
        is_case_sensitive: bool = False,
        is_line_start_sensitive: bool = True
    ) -> List[str]:
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
