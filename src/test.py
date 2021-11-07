from pprint import pprint

document = []

document

def writeMessage(msg: str) -> None:
	childMaster: list[ list[str] ] = []
	lastIndex: int = 0

	while '<clr:' in msg:
		# if there was text before the first tag, add it
		if lastIndex == 0 and msg.find('<clr:') != 0:
			child = []
			child.append(f'<div style=" display: inline ">{msg[ 0 : msg.find("<clr:") ]}</div>')
			childMaster.append( child )
		# get color
		clrTagEnd = msg.find('>', lastIndex)
		lastIndex = clrTagEnd + 1
		clr = msg[ msg.find( '<clr:', lastIndex ) + 5 : clrTagEnd ]
		# get next clr tag
		nextClrTagStart = msg.find( '<clr:', lastIndex )
		nextClrTagStart = len(msg) if nextClrTagStart == -1 else nextClrTagStart
		# create child
		child = []
		child.append( f'<div style=" color: {clr}; display: inline ">{msg[ clrTagEnd + 1 : nextClrTagStart ]}</div>' )
		childMaster.append( child )
		msg = msg[ nextClrTagStart : ]

	if len(msg) > 0:
		child = []
		child.append( f'<div style=" display: inline ">{msg}</div>' )
		childMaster.append( child )

	pprint( childMaster )


writeMessage('[<clr:green>colored nicknames!] hello world!')
