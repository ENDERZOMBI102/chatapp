""" Web sockets, defined in HTML5, are a way to handle bi directional communication between client and server. """

from typing import Literal, Callable, Final

from browser import DOMEvent
from webtypes import ENUM_ELEMENT, EVENT_CALLBACK

supported: bool = True
""" Indicates if the protocol is supported by the browser. """

# noinspection PyFinal
class EventSource:

	readyState: Final[ Literal[0, 1, 2] ]
	CONNECTING: ENUM_ELEMENT[ int ] = 0
	OPEN: ENUM_ELEMENT[ int ] = 1
	CLOSED: ENUM_ELEMENT[ int ] = 2
	url: str
	withCredentials: Final[bool]
	# event handlers
	onopen: Callable[ [ ], None ]
	onerror: Callable[ [ ], None ]
	onmessage: Callable[ [ DOMEvent ], None ]

	def __init__(self, url: str, configuration: dict = None):
		pass

	def addEventListener( self, name: str, callback: EVENT_CALLBACK ) -> None:
		"""
		Appends an event listener for events whose type attribute value is type.
		The callback argument sets the callback that will be invoked when the event is dispatched.
		\t
		:param name: name of the event to listen for
		:param callback: self-explanatory
		"""

	def dispatchEvent( self, event: DOMEvent ) -> bool:
		"""
		Dispatches an Event at the specified EventTarget, (synchronously) invoking the affected
		EventListeners in the appropriate order.
		The normal event processing rules (including the capturing and optional bubbling phase) also apply
		to events dispatched manually with dispatchEvent().
		\t
		:returns: The return value is false if event is cancelable and at least one of the event
		handlers which received event called Event.preventDefault(). Otherwise it returns true.
		"""

	def removeEventListener( self, name: str, callback: EVENT_CALLBACK ):
		""" Removes the event listener in target's event listener list with the same type and callback """


# noinspection PyFinal
class WebSocket(EventSource):
	readyState: Final[ Literal[0, 1, 2, 3] ]
	bufferedAmount: int
	extensions: ''
	protocol: ''
	binaryType: Literal['blob']
	CLOSING: ENUM_ELEMENT[int] = 2
	CLOSED: ENUM_ELEMENT[int] = 3
	# event handlers
	onclose: Callable[ [ ], None ]

	def __init__( self, host: str ):
		"""
		Returns a WebSocket object.
		\t
		:param host: The location of a server that supports the WebSocket protocol.
		:raise NotImplementedError: If the browser doesn't support WebSocket
		"""
		super().__init__( host )

	def bind(
			self,
			evt: Literal['open', 'error', 'message', 'close'],
			function: EVENT_CALLBACK
	) -> None:
		"""
		Attaches a function to an event
		\t
		:param evt: Event to connect the callback to
		:param function: Function to connect to the event
		"""

	def send( self, data: str ) -> None:
		"""
		Used to send data to the connected server.
		\t
		:param data: String to send to the server
		"""

	def close( self ) -> None:
		""" Closes the connection """
