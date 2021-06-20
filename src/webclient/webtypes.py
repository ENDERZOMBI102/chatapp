from typing import Final, TypeVar, Union, Callable, Dict, Any, Literal

from browser import DOMEvent

T = TypeVar('T')

ENUM_ELEMENT = Final[T]
EVENT_CALLBACK = Union[ Callable[ [], None ], Callable[ [DOMEvent], None ] ]
HTTP_HEADERS = Dict[ str, Union[str, int] ]
HTTP_DATA = Union[ str, Dict[ str, Any ] ]
RESPONSE_FORMAT = Literal['text', 'binary', 'dataURL']


class MessageEvent(DOMEvent):
	isTrusted: bool
	data: str
	origin: str
	lastEventId: str
	source: object
	ports: list
	userActivation: object
	type: str