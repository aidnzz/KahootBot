# -*- coding: utf-8 -*-

__all__ = (
    'Json',
    'UrlOrStr'
)

from yarl import URL
from typing import TypeAlias, Any

Json: TypeAlias = dict[str, Any]
UrlOrStr: TypeAlias = URL | str
