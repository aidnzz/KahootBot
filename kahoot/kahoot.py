# -*- coding: utf-8 -*-

__all__ = (
    'Kahoot',
)

from comet import CometD

from .exceptions import JoinError
from .models import ReservationResponse

from operator import itemgetter
from functools import partial, wraps
from aiohttp import ClientSession, ContentTypeError
from contextlib import AbstractAsyncContextManager

from typing import (
    TypeVar,
    TypeAlias,
    Callable,
    Optional,
    Awaitable
)

KahootClient = partial(ClientSession, base_url="https://kahoot.it")

T = TypeVar('T')

def map_exceptions(*excs):
    def inner(fn: Callable[..., T]) -> Callable[..., T]:
        @wraps(fn)
        async def wrapper(*args, **kwargs) -> T:
            exceptions = tuple(map(itemgetter(0), excs))
            try:
                return await fn(*args, **kwargs)
            except exceptions as exc:
                raise next(v for k, v in excs if isinstance(exc, k)) from exc
        return wrapper
    return inner

# Type alias for handler
Handler: TypeAlias = Callable[[dict], Awaitable[None]]

class Kahoot(AbstractAsyncContextManager):
    """ Asynchronous Kahoot client  """

    __slots__ = (
        'comet',
        'handlers',
    )

    def __init__(self, *, comet: Optional[CometD] = None) -> None:
        self.handlers: dict[str, Handler] = {}
        self.comet: Optional[CometD] = comet

    @map_exceptions((ContentTypeError, JoinError))
    async def join(cls: 'Kahoot', pin: str | int, *, nickname: str = '') -> None:
        async with KahootClient() as client:
            async with client.get(f"/reserve/session/{pin}") as r:
                response: ReservationResponse = await r.json()
            self.comet = await CometD.connect(f"/cometd/{pin}/", client=client)

    def on(self, event: str, handler: Optional[Handler] = None) -> Handler:
        def inner(fn: Handler) -> Handler:
            self.handlers[event] = fn
            return fn
        return inner(handler) if handler else inner

    @property
    def closed(self) -> bool:
        return getattr(self.comet, 'closed', True)

    async def run(self) -> None:
        while not self.closed:
            pass

    async def close(self) -> None:
        if not self.closed:
            await self.comet.close()

    async def __aexit__(self, *_) -> None:
        await self.close()
