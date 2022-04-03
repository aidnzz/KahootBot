# -*- coding: utf-8 -*-

__all__ = (
    'CometD',
)

from . import constants
from .typing import UrlOrStr
from .exceptions import HandshakeError
from .models import HandshakeResponse

from transports import Transport, WebSocketTransport

from functools import wraps
from aiohttp import ClientSession, ClientWebSocketResponse
from contextlib import AbstractAsyncContextManager, nullcontext

from typing import (
    Callable, 
    Optional, 
    TypeVar, 
    Type
)

class CometD(AbstractAsyncContextManager):
    """
    Websocket CometD implementation
    """

    __slots__ = (
        '_transport',
    )

    def __init__(self, transport: Transport) -> None:
        """ Requires transport to be connected """
        self._transport = transport

    @classmethod
    def from_socket(cls: Type['CometD'], socket: ClientWebSocketResponse) -> 'CometD':
        return cls(WebSocketTransport(socket))

    @classmethod
    async def connect(cls: Type['CometD'], url: UrlOrStr, *, client: Optional[ClientSession] = None, **kwargs) -> 'CometD':
        """ Connect to cometd server via websocket  """
        cm = nullcontext(client) if client else ClientSession() # Client manager
        async with cm as client:
            socket = await client.ws_connect(url, **kwargs)
        return cls.from_socket(socket)

    async def handshake(self) -> None:
        response: HandshakeResponse = await self._transport.handshake()
        if not (self._transport.client_id := response.get("client_id")):
            raise HandshakeError("Invalid handshake response")

    @property
    def closed(self) -> bool:
        return self._transport.closed

    async def close(self) -> None:
        await self._transport.close()

    async def __aexit__(self, *_) -> None:
        await self.close()
