from datetime import datetime
from typing import List, Optional, Union, cast

import dateparser
from pyparsing import And, CaselessLiteral, LineStart, Literal, White, ZeroOrMore


def build_common_prefix_pattern(
    keyword: str,
    *,
    delimiter: Optional[str] = ":",
    is_case_sensitive: bool = False,
    is_line_start_sensitive: bool = True
) -> And:
    prefix = Literal(keyword) if is_case_sensitive else CaselessLiteral(keyword)

    grammar = prefix + ZeroOrMore(White())

    if delimiter is not None:
        grammar += Literal(delimiter)

    if is_line_start_sensitive:
        return LineStart() + grammar

    return grammar


def find(text: str, grammar: And, *, id: str = "value") -> Optional[str]:
    results = grammar.scanString(text, maxMatches=1)
    for tokens, _start, _end in results:
        value = tokens.asDict().get(id)
        return cast(str, value)

    return None


def find_all(text: str, grammar: And, *, id: str = "value") -> List[str]:
    values: List[str] = []

    results = grammar.scanString(text)
    for tokens, _start, _end in results:
        value = tokens.asDict().get(id)
        values.append(cast(str, value))

    return values


def parse_datetime(date_string: str) -> Union[datetime, str]:
    # remove ". " to support the following format
    # "2007. 03. 02."
    date_string = date_string.replace(" .", "")

    dt = dateparser.parse(date_string)
    if dt is None:
        return date_string

    return dt
