# -*- coding: utf-8 -*-

from typing import Final
from enum import Enum, unique

@unique
class ConnectionType(Enum):
    LONG_POLLING = "long-polling"
    CALLBACK_POLLING = "callback-polling"
    WEBSOCKET = "websocket"
    IFRAME = "iframe"

# Websocket is currently the only transport type implemented
SUPPORTED_CONNECTION_TYPES: Final[tuple[ConnectionType]] = (
    ConnectionType.WEBSOCKET,
)

DEFAULT_CONNECTION_TYPE: Final[ConnectionType] = ConnectionType.WEBSOCKET
# Usual timeout
DEFAULT_TIMEOUT: Final[int] = 60_000
# Version 1.0
VERSION: Final[float] = 1.0
