# -*- coding: utf-8 -*-

__all__ = (
    'HandshakeResponse',
    'ConnectResponse',
    'DisconnectResponse',
    'SubscribeResponse',
    'UnsubscribeResponse',
    'PublishResponse'
)

from typing import TypedDict

class HandshakeResponse(TypedDict):
    channel: str
    version: str
    supportedConnectionTypes: list[str]
    clientId: str
    successful: bool
    minimumVersion: str
    advice: dict
    ext: dict
    id: int
    authSuccessful: bool


class ConnectResponse(TypedDict):
    pass


class DisconnectResponse(TypedDict):
    pass


class SubscribeResponse(TypedDict):
    pass


class UnsubscribeResponse(TypedDict):
    pass


class PublishResponse(TypedDict):
    pass
