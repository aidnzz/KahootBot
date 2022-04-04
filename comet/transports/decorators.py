# -*- coding: utf-8 -*-

from .abc import Transport
from comet.typing import Json
from comet.exceptions import BayeuxConnectionError

from functools import wraps
from typing import Callable, Awaitable

def connection_required(fn: Callable[..., Awaitable[Json]]) -> Callable[..., Awaitable[Json]]:
    @wraps(fn)
    async def wrapper(self: Transport, *args, **kwargs) -> Json:
        if self.client_id:
            return await fn(self, *args, **kwargs)
        raise BayeuxConnectionError("Client id not set")
    return wrapper
