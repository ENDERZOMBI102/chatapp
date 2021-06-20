"""
This module supports asynchronous programming in Brython, using the keywords async and await.

It replaces the asyncio module in CPython standard library, which cannot work in the browser context:

	1. It uses blocking functions such as run() or run_until_complete(), and the way browsers work make it
	impossible to define functions whose execution is suspended until an event occurs.

	2. The browser has its own implicit event loop, it is not possible to define another one as the asyncio
	modules does with the function set_event_loop().
"""
from typing import Literal, Dict, Union, Any, Coroutine, Awaitable, Generator

from browser import DOMEvent
from webtypes import T, HTTP_HEADERS, HTTP_DATA, RESPONSE_FORMAT


class Request:

	data: Union[str, bytes]
	""" The response body, with the format defined by argument format. """
	response_headers: Dict[ str, Union[str, int] ]
	""" A dictionary matching the response headers. """
	status: int
	""" HTTP response status as an integer (200, 404...). """
	status_text: str
	""" HTTP response status as a string ("200 Ok", "404 File not found"...). """


async def ajax(
		method: Literal['GET', 'POST', 'PUT'],
		url: str,
		format: RESPONSE_FORMAT = 'text',
		headers: HTTP_HEADERS = None,
		data: HTTP_DATA = None,
		cache: bool = False
) -> Request:
	"""
	req = await ajax("GET", url) inside an asynchronous function gives back control to the main program, and resumes the
	function when the Ajax request of the type method ("GET", "POST", "PUT", etc.) to the specified URL is completed.
	The return value is an instance of the class Request (see below).
	\t
	:param method: The method to use for the request.
	:param url: URL this request will request.
	:param format: The expected response format.
	:param headers: A dictionary with the HTTP headers to send with the request.
	:param data: A string or a dictionary that will be sent with the request to form the query string for
	a "GET" request, or the request body for "POST".
	:param cache: A boolean indicating if the browser cache should be used
	"""


# noinspection PyShadowingBuiltins
def get(
		url: str,
		format: Literal['text', 'binary', 'dataURL'] = 'text',
		headers: Dict[ str, Union[str, int] ] = None,
		data: Union[ str, Dict[ str, Any ] ] = None,
		cache: bool = False
		) -> Request:
	""" Shortcut for ajax("GET", url...) """


# noinspection PyShadowingBuiltins
async def post(
		url,
		format: Literal[ 'text', 'binary', 'dataURL' ] = 'text',
		headers: Dict[ str, Union[ str, int ] ] = None,
		data: Union[ str, Dict[ str, Any ] ] = None,
		) -> Request:
	""" Shortcut for ajax("POST", url...) """


async def event(element: str, name: str) -> DOMEvent:
	"""
	evt = await aio.event(element, "click") suspends execution of an asynchronous function until the
	user clicks on the specified element.
	\t
	:param element: Wait for event NAME on this elemennt.
	:param name: Wait until this specified event.
	:returns: An instance of the DOMEvent class.
	"""


async def sleep(seconds: int) -> None:
	"""
	n an asynchronous function, await sleep(n) gives back control to the main
	program and resumes function execution after n seconds.
	"""


def run(coroutine: Coroutine):
	"""
	Runs a coroutine, ie the result of a call to an asynchronous function defined by async def.
	This is a non blocking function: it doesn't wait until the asynchronous function is completed to execute the
	instructions in the following lines.
	The time when the next instructions are run is not (easily) predictable.
	"""


class Future( Awaitable[T] ):

	def __await__( self ) -> Generator[ Any, None, T ]:
		pass

	def set_result( self, result: T ):
		"""
		Mark the Future as done and set its result.

		Raises a InvalidStateError error if the Future is already done.
		"""

	def set_exception( self, exception: Exception ):
		"""
		Mark the Future as done and set an exception.

		Raises a InvalidStateError error if the Future is already done.
		"""
