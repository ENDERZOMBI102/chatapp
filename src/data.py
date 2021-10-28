import json
from dataclasses import dataclass
from enum import Enum, auto
from typing import Optional


class OS(Enum):
	UNKNOWN = auto()
	WINDOWS = auto()
	MACOS = auto()
	LINUX = auto()
	ANDROID = auto()
	FREEBDS = auto()
	WEB = auto()


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
		return f'[{self.author}] {self.content}'
