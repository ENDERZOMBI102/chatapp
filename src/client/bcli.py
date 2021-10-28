from typing import List

from blessed import Terminal

from .Client import Client


class App:
	term: Terminal
	shouldContinue: bool = True
	inpLoc: List[int]
	client: Client

	def __init__(self):
		self.term = Terminal()
		self.client = Client()

	def MainLoop(self) -> None:
		with self.term.fullscreen(), self.term.cbreak(), self.term.hidden_cursor(), self.term.location():
			while self.shouldContinue:
				self.term.move_xy( 0, self.term.height )
				print(f'current server: {self.client.ADDR}:{self.client.PORT}')
				#self.term.


if __name__ == '__main__':
	App().MainLoop()
