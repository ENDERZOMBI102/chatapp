"""
This module allows running Ajax requests.

The standard Web API syntax can be used (see below) but Brython proposes a more concise syntax:
	for each request method (GET, POST, etc.) the module defines a specific function.
"""
from typing import Union, Literal

from webtypes import HTTP_HEADERS, RESPONSE_FORMAT


def get(
		url: str,
		blocking: bool = False,
		headers: HTTP_HEADERS = {},
		mode: Literal['text', 'binary', 'json', 'document'] = 'text',
		encoding="utf-8",
		timeout=None,
		cache=False,
		data="",
		**callbacks
		) -> None:
	pass