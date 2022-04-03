# -*- coding: utf-8 -*-

from comet.typing import UrlOrStr, Json
from comet.exceptions import BayeuxError
from comet.transports.abc import Transport

from comet.constants import (
    VERSION,
    DEFAULT_CONNECTION_TYPE,
    ConnectionType
)

from functools import wraps
from typing import final, Optional, Callable, Awaitable
from aiohttp import ClientWebSocketResponse, ClientSession

def bayeux_message(fn: Callable[..., Awaitable[Json]]) -> Callable[..., Awaitable[Json]]:
    """ Sends request waits for response and checks for errors """
    @wraps(fn)
    async def wrapper(self: 'WebSocketTransport', *args, **kwargs) -> Json:
        await fn(*args, **kwargs)
        data = await self._socket.recieve_json()
        # Increment after complete handshake flow
        self.id += 1
        if (error := data.get("error")):
            raise BayeuxError(error)
        return data
    return wrapper

@final
class WebSocketTransport(Transport):
    __slots__ = (
        '_socket',
        '_id',
        '_client_id',
    )

    def __init__(self, socket: ClientWebSocketResponse) -> None:
        self._socket = socket
        self._id: int = 1
        self._client_id: Optional[str] = None

    @bayeux_message
    async def handshake(self, connection_types: list[ConnectionType]) -> Json:
        await self._socket.send_json({
            "id": self.id,
            "channel": "/meta/handshake",
            "version": VERSION,
            "mininumVersion": VERSION,
            "supportedConnectionTypes": connection_types
        })

    @bayeux_message
    async def connect(self) -> Json:
        await self._socket.send_json({
            "id": self.id,
            "channel": "/meta/connect",
            "connectionType": DEFAULT_CONNECTION_TYPE,
            "clientId": self.client_id
        })

    @bayeux_message
    async def disconnect(self) -> Json:
        await self._socket.send_json({
            "id": self.id,
            "channel": "/meta/disconnect",
            "clientId": self.client_id
        })

    async def close(self) -> None:
        await self._socket.close()

    @property
    def closed(self) -> bool:
        return self._socket.closed

    @property
    def id(self) -> int:
        return self._id

    @id.setter
    def id(self, value: int) -> None:
        self._id = value

    @property
    def client_id(self) -> Optional[str]:
        return self._client_id

    @client_id.setter
    def client_id(self, value: str) -> None:
        self._client_id = value
