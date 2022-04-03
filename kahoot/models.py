# -*- coding: utf-8 -*-

__all__ = (
    'ReservationResponse',
    'Message'
)

from typing import TypedDict

class ReservationResponse(TypedDict):
    twoFactorAuth: bool
    namerator: bool
    participantId: bool
    smartPractice: bool
    collaborations: bool
    liveGameId: str
    challenge: str


class Message(TypedDict):
    pass
