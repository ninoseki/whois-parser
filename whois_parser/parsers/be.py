from typing import Optional

from pyparsing import Regex

from .base import BaseParser


class BeParser(BaseParser):
    def _find_registrar(self) -> Optional[str]:
        prefix = Regex("Registrar:\nName:")
        return self._find(prefix, delimiter=None)

    def _find_registrant_name(self) -> Optional[str]:
        prefix = Regex("r'Registrant:\n")
        return self._find(prefix, delimiter=None)
