# -*- coding: utf-8 -*-

__all__ = (
    'BayeaxError',
    'HandshakeError',
)

class BayeuxError(Exception):
    pass

class HandshakeError(BayeuxError):
    pass
