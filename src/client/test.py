from client.Client import Client
from data import Message

recvSomething: bool = False


def main() -> None:
	def onMessage(msg: Message) -> None:
		global recvSomething
		print(f'[{msg.author}]: {msg.content}')
		recvSomething = True
	
	global recvSomething
	with Client() as client:
		client.SetCloseListener( lambda: print(' - closed') )
		client.SetMessageListener( onMessage )
		print(' - connecting...')
		client.SetAddress('127.0.0.1', 20307)
		client.SetUsername('PythonTest')
		print(' - waiting for response...')
		while not recvSomething:
			pass
		

if __name__ == '__main__':
	main()
	