from client.Client import Client
from data import Message

recvSomething: int = 0


def main() -> None:
	def onMessage(msg: Message) -> None:
		global recvSomething
		print(f'[{msg.author}]: {msg.content}')
		recvSomething += 1
	
	global recvSomething
	with Client() as client:
		client.setCloseListener( lambda: print( ' - closed' ) )
		client.setMessageListener( onMessage )
		print(' - connecting...')
		client.setAddress( '127.0.0.1', 20307 )
		client.setUsername( 'PythonTest' )
		print(' - waiting for response...')
		while recvSomething != 2:
			pass
		

if __name__ == '__main__':
	main()
	