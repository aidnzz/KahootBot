# -*- coding: utf-8 -*-

__all__ = (
    'CometD',
)

from . import constants
from .typing import UrlOrStr
from .transports import WebSocketTransport

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

    def __init__(self, transport: WebSocketTransport) -> None:
        """ Requires websocket to be connected """
        self._transport = transport

    @classmethod
    async def connect(cls: Type['CometD'], url: UrlOrStr, *, client: Optional[ClientSession] = None, **kwargs) -> 'CometD':
        """ Connect to cometd server via websocket  """
        cm = nullcontext(client) if client else ClientSession() # Client manager
        async with cm as client:
            socket = await ClientSession.ws_connect(client, url, **kwargs)
        return cls(WebSocketTransport(socket))

    async def handshake(self) -> None:
        data = await self._transport.handshake()
        self._transport.client_id = data["client_id"]

    @property
    def closed(self) -> bool:
        return self._transport.closed

    async def close(self) -> None:
        await self._transport.close()

    async def __aexit__(self, *_) -> None:
        await self.close()
