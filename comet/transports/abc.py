# -*- coding: utf-8 -*-

__all__ = (
    'Transport',
)

from comet.typing import Json
from comet.constants import ConnectionType

from abc import ABC, abstractmethod

class Transport(ABC):
    @property
    @abstractmethod
    def id(self) -> int:
        """ Unique message id for every request to server """

    @id.setter
    @abstractmethod
    def id(self, value: int) -> None:
        """ Set unique message id """

    @property
    @abstractmethod
    def client_id(self) -> str:
        """ Client id value assigned by server """

    @client_id.setter
    @abstractmethod
    def client_id(self, value: str) -> str:
        """ Set client id """

    @property
    def closed(self) -> bool:
        """ Checks if underlying socket is closed """

    @abstractmethod
    async def handshake(self) -> Json:
        """ Initial handshake with CometD server """

    @abstractmethod
    async def connect(self, connection_types: list[ConnectionType]) -> Json:
        """
        After a Bayeux client has discovered the server’s capabilities with a handshake exchange, a connection is established by sending a message to the /meta/connect channel. 
        This message may be transported over any of the transports indicated as supported by the server in the handshake response.
        """

    @abstractmethod
    async def disconnect(self) -> Json:
        """
        When a connected client wishes to cease operation it should send a request to the /meta/disconnect channel for the server to remove any client-related state
        """

    @abstractmethod
    async def subscribe(self) -> Json:
        """
        A connected Bayeux client may send subscribe messages to register interest in a channel and to request that messages published to that channel
        """

    @abstractmethod
    async def unsubscribe(self) -> Json:
        """ Unsubscribe from server """

    @abstractmethod
    async def publish(self) -> Json:
        """
        A connected Bayeux client may send unsubscribe messages to cancel interest in a channel and to request that messages published to that channel are not delivered to itself.
        """

    @abstractmethod
    async def close(self) -> None:
        """ Close client """
