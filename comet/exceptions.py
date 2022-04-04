# -*- coding: utf-8 -*-

__all__ = (
    'BayeuxError',
    'BayeuxConnectionError',
    'HandshakeError',
)

class BayeuxError(Exception):
    pass


class BayeuxConnectionError(Exception):
    pass


class HandshakeError(BayeuxError):
    pass
