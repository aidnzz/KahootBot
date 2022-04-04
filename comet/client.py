# -*- coding: utf-8 -*-

__all__ = (
    'CometD',
)

import logging

from . import constants
from .typing import UrlOrStr, Json
from .models import HandshakeResponse
from .exceptions import HandshakeError
from .transports import Transport, WebSocketTransport

from functools import wraps
from aiohttp import ClientSession, ClientWebSocketResponse
from contextlib import AbstractAsyncContextManager, nullcontext

from typing import (
    Callable,
    Optional,
    TypeVar,
    Type
)

log = logging.getLogger(__name__)

class CometD(AbstractAsyncContextManager):
    """
    Websocket CometD implementation
    """

    __slots__ = (
        '_client',
        '_transport',
    )

    def __init__(self, transport: Transport, *, client: Optional[ClientSession] = None) -> None:
        """ Requires transport to be connected """
        self._transport = transport
        self._client: ClientSession | nullcontext = client or nullcontext(client)

    @classmethod
    def from_socket(cls: Type['CometD'], socket: ClientWebSocketResponse, *, client: Optional[ClientSession] = None) -> 'CometD':
        return cls(WebSocketTransport(socket), client=client)

    @classmethod
    async def ws_connect(cls: Type['CometD'], url: UrlOrStr, *, client: Optional[ClientSession] = None, **kwargs) -> 'CometD':
        """ Connect to Cometd server via websocket  """
        http = client or ClientSession() # We need to retain http client
        socket = await http.ws_connect(url, **kwargs)
        if not client:
            return cls.from_socket(socket, client=http)
        return cls.from_socket(socket)

    async def handshake(self) -> None:
        response: HandshakeResponse = await self._transport.handshake()
        self._transport.client_id = response.get("client_id")
        log.info("Handshake completed: client_id={0.client_id}, id={0.id}".format(self._transport))

    async def connect(self) -> None:
        await self._transport.connect()

    async def disconnect(self) -> None:
        await self._transport.disconnect()

    async def publish(self, channel: str | list[str], data: Json) -> None:
        response: PublishResponse = await self._transport.publish(channel, data)
        logging.info("Published to server")

    @property
    def closed(self) -> bool:
        return self._transport.closed

    async def close(self) -> None:
        # Close transport then close client if not null
        async with self._client:
            await self._transport.close()

    async def __aexit__(self, *_) -> None:
        await self.close()
