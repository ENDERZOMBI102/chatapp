import json
from dataclasses import dataclass
from typing import Optional, Protocol


@dataclass
class Message:
	author: str
	content: str
	sentAt: Optional[float] = None

	@classmethod
	def fromJson( cls, data: str ) -> 'Message':
		return Message( **json.loads( data ) )

	def toJson( self ) -> str:
		return json.dumps( self.__dict__ )

	def __repr__(self) -> str:
		return self.content


class MessageListener(Protocol):
	def __call__( self, msg: Message ) -> None: ...


class CloseListener(Protocol):
	def __call__( self ) -> None: ...
