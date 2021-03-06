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


class ClientWindow(wx.Frame):

	username = os.getlogin()
	client: Client

	def __init__(self):
		super(ClientWindow, self).__init__(
			parent=None,
			title='Simple Socket Chat GUI Client'
		)
		self.SetMinSize( wx.Size(500, 400) )
		self.SetSize( wx.Size(500, 400) )
		# create menubar
		menuBar = wx.MenuBar()

		# menu: File
		fileMenu = wx.Menu()
		aboutItem = fileMenu.Append(0, 'About')
		self.Bind(wx.EVT_MENU, self.about, aboutItem)
		exitItem = fileMenu.Append(1, 'Exit')
		self.Bind(wx.EVT_MENU, self.OnClose, exitItem)
		menuBar.Append(fileMenu, 'File')

		# menu: Connection
		connMenu = wx.Menu()
		connectToItem = connMenu.Append(2, 'Connect To..')
		self.Bind(wx.EVT_MENU, self.connectTo, connectToItem)
		changeUsernameItem = connMenu.Append(3, 'Change username')
		self.Bind(wx.EVT_MENU, self.changeUsername, changeUsernameItem)
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

	def OnClose(self, evt: wx.CommandEvent = None):
		self.client.Stop()
		self.Destroy()

	def OnResize(self, evt: wx.Event):
		self.chat.SetSize( wx.Size( self.GetSize()[0], int( 0.70 * self.GetSize()[1] ) ) )
		self.input.SetSize( wx.Size( self.GetSize()[0], int( 0.30 * self.GetSize()[1] ) ) )
		self.input.SetPosition( wx.Point( 0, self.chat.GetSize()[1] + 1 ) )

	def OnEnterPressed(self, evt: wx.CommandEvent ):
		text = self.input.GetValue()
		self.client.Send( text )
		self.chat.AppendText(f'[{self.username}] {text}\n')
		self.input.Clear()

	def OnMessage(self, msg: str):
		wx.CallAfter( self.chat.AppendText, f'{msg}\n')

	def connectTo(self, evt: wx.CommandEvent):
		dialog = wx.TextEntryDialog(
			parent=self,
			message='Insert server address (host:port)',
			caption='Connect to server',
			value=self.client.GetAddress()
		)
		if dialog.ShowModal() == wx.ID_OK:
			host, port = dialog.GetValue().split(':')
			if host == '' or port == '':
				self.AppendRed(f'invalid address "{host}:{port}"!')
			else:
				self.chat.Clear()
				self.client.SetAddress(host, port)
				self.client.Send(f':CHGUNAME:{self.username}')
				self.input.Enable()

	def changeUsername(self, evt: wx.CommandEvent):
		dialog = wx.TextEntryDialog(
			parent=self,
			message='Insert new username',
			caption='Change username',
			value=self.username
		)
		if dialog.ShowModal() == wx.ID_OK:
			username = dialog.GetValue()
			if username == '':
				self.AppendRed(f'invalid username "{username}"!')
			else:
				self.username = username
				self.client.Send(f':CHGUNAME:{self.username}')

	def about(self, evt: wx.CommandEvent):
		wx.GenericMessageDialog(
			parent=self,
			message='Chat "protocol" by ENDERZOMBI102\nApp by ENDERZOMBI102\nUsed frameworks:\n - wxPython\n - socket',
			caption='About Simple Chat Client'
		).ShowModal()

	def AppendRed(self, txt: str):
		self.chat.SetDefaultStyle( wx.TextAttr( wx.Colour().Red() ) )
		self.chat.AppendText(txt)


if __name__ == '__main__':
	app = App()
	app.MainLoop()
