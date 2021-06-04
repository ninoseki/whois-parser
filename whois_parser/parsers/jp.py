from datetime import datetime
from typing import List, Optional, Union

from .base import BaseParser
from .utils import build_common_prefix_pattern


class JpParser(BaseParser):
    def _find_domain(self) -> Optional[str]:
        prefix = build_common_prefix_pattern(
            "[ドメイン名]",
            is_line_start_sensitive=False,
            delimiter=None,
        )
        value = self._find(prefix, delimiter=None)
        if value is not None:
            value = value.lower()

        return value

    def _find_registrant_organization(self) -> Optional[str]:
        prefix = build_common_prefix_pattern(
            "[組織名]",
            is_line_start_sensitive=False,
            delimiter=None,
        )
        return self._find(prefix, delimiter=None)

    def _find_registered_at(self) -> Optional[Union[str, datetime]]:
        prefix = build_common_prefix_pattern(
            "[登録年月日]",
            is_line_start_sensitive=False,
            delimiter=None,
        )
        return self._find_datetime(prefix, delimiter=None)

    def _find_updated_at(self) -> Optional[Union[str, datetime]]:
        prefix = build_common_prefix_pattern(
            "[最終更新]",
            is_line_start_sensitive=False,
            delimiter=None,
        )
        return self._find_datetime(prefix, delimiter=None)

    def _find_statuses(self) -> List[str]:
        prefix = build_common_prefix_pattern(
            "[状態]",
            is_line_start_sensitive=False,
            delimiter=None,
        )
        return self._find_all(prefix, delimiter=None)

    def _find_name_servers(self) -> List[str]:
        prefix = build_common_prefix_pattern(
            "[ネームサーバ]",
            is_line_start_sensitive=False,
            delimiter=None,
        )
        return self._find_all(prefix, delimiter=None)
