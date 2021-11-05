import traceback


def getException( exc: BaseException ) -> str:
	return '\n'.join(
		traceback.format_exception(
			type( exc ),
			exc,
			exc.__traceback__
		)
	)