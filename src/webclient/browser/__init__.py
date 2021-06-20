from typing import Any, List, Dict, Optional, Union


def alert(message: str) -> None:
	"""
	A function that shows a message in a pop-up window
	\t
	:param message: Message to show
	:returns: None
	"""


def bind(target: str, event: str):
	""" A function used as a decorator for event binding. """


def confirm(message: str) -> bool:
	"""
	A function that prints the message in a window, and two buttons (ok/cancel)
	Returns True if ok, False if cancel
	"""


class _Console:

	def log(self, msg: Any) -> None:
		pass


console: _Console
"""
	An object with methods to interact with the browser console.
	Its interface is browser-specific.
	It exposes at least the method log(msg), which prints the message msg in the console
"""


class DOMEvent:
	""" The class of DOM events """


class DOMNode:
	""" The class of DOM nodes """
	attrs: Dict[ str, Any ]
	# --- brython specific properties ---
	abs_left: int
	""" Position of the element relatively to the document left border (1) """
	abs_top: int
	""" Position of the element relatively to the document top border (1) """
	bind = bind
	children: List['DOMNode']
	child_nodes: List['DOMNode']
	class_name: str
	height: int
	""" Element height in pixels (2) """
	html: str
	left: int
	parent: Optional[ 'DOMNode' ]
	""" The element's parent (None for doc) """
	scrolled_left: int
	""" Position of the element relatively to the left border of the visible part of the document (1) """
	scrolled_top: int
	""" Position of the element relatively to the top border of the visible part of the document (1) """
	text: str
	top: int
	width: int
	""" Element width in pixels (2) """

	def clear( self ):
		"""  removes all the descendants of the element """

	def closest( self, tag_name: str ) -> 'DOMNode':
		"""
		Find the first element with the requested tag name.
		\t
		:param tag_name: tag to search for
		:returns: the first parent element with the requested tag name
		:raises KeyError: if no element is found.
		"""

	def index( self, selector: str = None ) -> int:
		"""
		returns the index (an integer) of the element among its parent's children.
		If selector is specified, only the elements matching the CSS selector are taken into account;
		in this case, if no element matches, the method returns -1.
		"""

	def inside( self, other: 'DOMNode' ) -> bool:
		"""
		Tests if self is contained inside element other
		\t
		:param other: The node to check
		:returns: wether this element is inside other
		"""

	def get( self, name: str = '', selector: str = '' ) -> List[ 'DOMNode' ]:
		""" selects elements """

	def select( self, css_selector: str ) -> List['DOMNode']:
		return self.get( selector=css_selector )

	def select_one( self, css_selector: str ) -> Union[ None, List['DOMNode'] ]:
		""" Returns the elements matching the specified CSS selector, otherwise None """

	def __le__(self, other: 'DOMNode') -> None:
		""" add a child to this element """
		pass

	def __iter__(self) -> 'DOMNode':
		pass

	def __next__(self) -> 'DOMNode':
		pass

	def __delitem__(self, key: str) -> None:
		pass


class _Document(DOMNode):

	def getElementById(self, elt_id: str) -> DOMNode:
		pass

	def createElement(self, tagName) -> DOMNode:
		"""
		Creates and return a new element.
		\t
		:param tagName: Type of the element to create
		"""

	def appendChild(self, elt: DOMNode) -> None:
		"""
		Appends an element to the document.
		\t
		:param elt: The element to append
		"""

	def __getitem__(self, item: str):
		pass

	def __setitem__(self, key: str, value: DOMNode):
		pass


document: _Document
""" An object that represents the HTML document currently displayed in the browser window. """


def load(script_url: str) -> None:
	"""
	Load the Javascript library at address script_url.
	This function uses a blocking Ajax call.
	It must be used when one can't load the Javascript library in the html page by <script src="prog.js"></script>.
	The names inserted by the library inside the global Javascript namespace are available in the Brython script as
	attributes of the window object.
	\t
	:param script_url: the url of the js file to load
	"""


def prompt(message: str, default: str = '') -> str:
	"""
	A function that prints the message in a window, and an entry field.
	Returns the entered value; if no value was entered, return default if defined, else the empty string
	\t
	:param message: the message the prompt will display
	:param default: default value, used if the user didn't input anything
	"""


def run_script(src: str, name: str = '') -> None:
	"""
	This function executes the Python source code in src with an optional name.
	It can be used as an alternative to exec(), with the benefit that the indexedDB cache is used for
	importing modules from the standard library.
	\t
	:param src: python code
	:param name: optional module name (?)
	"""


class window:
	""" An object that represents the browser window """
