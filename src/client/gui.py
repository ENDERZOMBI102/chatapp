import os

import wx

from Client import Client


class App(wx.App):

	def OnInit(self) -> bool:
		# create window
		window = ClientWindow()
		window.Show()
		return True

	def OnExit(self) -> int:
		return 0


_wxMenuId = 0


def getWxID() -> int:
	global _wxMenuId
	id = _wxMenuId
	_wxMenuId += 1
	return id


class ClientWindow(wx.Frame):

	username = os.getlogin()
	client: Client
	menus: dict[str, wx.MenuItem]
	colors: wx.ColourDatabase

	def __init__(self):
		super(ClientWindow, self).__init__(
			parent=None,
			title='Simple Socket Chat GUI Client'
		)
		self.SetMinSize( wx.Size(500, 400) )
		self.SetSize( wx.Size(500, 400) )
		self.colors = wx.ColourDatabase()
		# create menubar
		menuBar = wx.MenuBar()
		self.menus = {}

		# menu: File
		fileMenu = wx.Menu()
		self.menus['about'] = fileMenu.Append(getWxID(), 'About')
		self.Bind(wx.EVT_MENU, self.about, self.menus['about'])
		self.menus['exit'] = fileMenu.Append(getWxID(), 'Exit')
		self.Bind(wx.EVT_MENU, self.OnClose, self.menus['exit'])
		menuBar.Append(fileMenu, 'File')

		# menu: Connection
		connMenu = wx.Menu()
		self.menus['connect'] = connMenu.Append(getWxID(), 'Connect To..')
		self.Bind(wx.EVT_MENU, self.connectTo, self.menus['connect'])
		self.menus['disconnect'] = connMenu.Append( getWxID(), 'Disconnect' )
		self.menus['disconnect'].Enable(False)
		self.Bind( wx.EVT_MENU, self.disconnect, self.menus['disconnect'] )
		self.menus['changeuname'] = connMenu.Append(getWxID(), 'Change username')
		self.Bind(wx.EVT_MENU, self.changeUsername, self.menus['changeuname'])
		menuBar.Append(connMenu, 'Connection')

		# set menu bar
		self.SetMenuBar(menuBar)
		sizer = wx.BoxSizer()
		self.chat = wx.TextCtrl(
			parent=self,
			name='chatLog',
			pos=(0, 0),
			size=wx.Size( self.GetSize()[0], int( 0.70 * self.GetSize()[1] ) ),
			style=wx.TE_READONLY | wx.TE_AUTO_URL | wx.TE_MULTILINE | wx.TE_WORDWRAP
		)
		sizer.Add(
			self.chat
		)
		staticSizer = wx.StaticBoxSizer(wx.VERTICAL, self, 'Input')
		self.input = wx.TextCtrl(
			parent=self,
			name='chatinput',
			pos=( 0, self.chat.GetSize()[1]+1 ),
			size=wx.Size( self.GetSize()[0], int( 0.30 * self.GetSize()[1] ) ),
			style=wx.TE_WORDWRAP | wx.TE_NO_VSCROLL | wx.TE_PROCESS_ENTER
		)
		self.input.Enable(False)
		staticSizer.Add(
			self.input,
			wx.SizerFlags(1).Expand()
		)
		sizer.Add(staticSizer)

		# create Client thread
		self.client = Client()
		self.client.SetListener( self.OnMessage )

		self.Bind( wx.EVT_CLOSE, self.OnClose, self )
		self.Bind( wx.EVT_SIZING, self.OnResize, self )
		self.Bind( wx.EVT_TEXT_ENTER, self.OnEnterPressed, self.input )

	def OnClose(self, evt: wx.CommandEvent = None) -> None:
		self.client.Stop()
		self.Destroy()

	def OnResize(self, evt: wx.Event) -> None:
		self.chat.SetSize( wx.Size( self.GetSize()[0], int( 0.70 * self.GetSize()[1] ) ) )
		self.input.SetSize( wx.Size( self.GetSize()[0], int( 0.30 * self.GetSize()[1] ) ) )
		self.input.SetPosition( wx.Point( 0, self.chat.GetSize()[1] + 1 ) )

	def OnEnterPressed(self, evt: wx.CommandEvent ) -> None:
		text = self.input.GetValue()
		self.client.Send( text )
		self.chat.AppendText(f'[{self.username}] {text}\n')
		self.input.Clear()

	def OnMessage( self, msg: str ) -> None:
		# add color/styles/tags
		# system messages should be blue
		if msg.startswith(':SYSTEM:'):
			self.AppendStyled( msg, self.colors.FindColour('blue') )
		else:
			self.chat.AppendText( msg + '\n' )

	def OnMessageRaw(self, msg: str) -> None:
		wx.CallAfter( self.OnMessage, msg)

	def Reset( self ) -> None:
		self.chat.Clear()
		self.input.Clear()
		self.input.Enable( False )

	def connectTo(self, evt: wx.CommandEvent) -> None:
		dialog = wx.TextEntryDialog(
			parent=self,
			message='Insert server address (host:port)',
			caption='Connect to server',
			value=self.client.GetAddress()
		)
		if dialog.ShowModal() == wx.ID_OK:
			pair: list[str] = dialog.GetValue().split(':')

			if len( pair ) == 1:
				pair.append('20307')

			host, port = pair

			# check if host/port are empty and if they're valid
			if not ( ( not ( host or port ) ) or self.client.CheckIsValid( host, port ) ):
				self.AppendStyled( f'invalid address "{host}:{port}"!', self.colors.FindColour('red') )
			else:
				self.Reset()
				self.client.SetAddress(host, port)
				self.client.Send(f':CHGUNAME:{self.username}')
				self.input.Enable()
				self.menus['disconnect'].Enable()

	def disconnect( self, evt: wx.CommandEvent ) -> None:
		self.client.Stop()
		self.menus[ 'disconnect' ].Enable( False )
		self.Reset()
		self.AppendStyled( 'disconnected from server', self.colors.FindColour('blue') )

	def changeUsername(self, evt: wx.CommandEvent) -> None:
		dialog = wx.TextEntryDialog(
			parent=self,
			message='Insert new username',
			caption='Change username',
			value=self.username
		)
		if dialog.ShowModal() == wx.ID_OK:
			username = dialog.GetValue()
			if username == '':
				self.AppendStyled( f'invalid username "{username}"!' )
			else:
				self.username = username
				self.client.Send(f':CHGUNAME:{self.username}')

	def about(self, evt: wx.CommandEvent) -> None:
		wx.GenericMessageDialog(
			parent=self,
			message='Chat "protocol" by ENDERZOMBI102\nApp by ENDERZOMBI102\nUsed frameworks:\n - wxPython\n - socket',
			caption='About Simple Chat Client'
		).ShowModal()

	def AppendStyled( self, txt: str, color: wx.Colour ) -> None:
		self.chat.SetDefaultStyle( wx.TextAttr( color ) )
		self.chat.AppendText(txt + '\n')
		self.chat.SetDefaultStyle( wx.TextAttr( wx.NullColour ) )


if __name__ == '__main__':
	app = App()
	app.MainLoop()
