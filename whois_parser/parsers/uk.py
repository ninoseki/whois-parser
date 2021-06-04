from typing import Optional

from pyparsing import Regex

from .base import BaseParser


class UkParser(BaseParser):
    def _find_registrar(self) -> Optional[str]:
        prefix = Regex("Registrar:\n")
        return self._find(prefix, delimiter=None)

    def _find_registrant_name(self) -> Optional[str]:
        prefix = Regex("Registrant:\n")
        return self._find(prefix, delimiter=None)
