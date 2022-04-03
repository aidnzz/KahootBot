# -*- coding: utf-8 -*-

__all__ = (
    'JoinError',
    'KahootException'
)

class KahootException(Exception):
    pass

class JoinError(KahootException):
    pass
