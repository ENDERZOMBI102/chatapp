import wx

from Client import Client


class App(wx.App):

	instance = None
	client: Client

	def OnInit(self) -> bool:
		# create window
		window = ClientWindow()
		window.Show()
		# create Client thread
		self.client = Client()
		self.client.SetListener( window.OnMessage )
		App.instance = self
		return True

	def OnExit(self) -> int:
		return 0


class ClientWindow(wx.Frame):
	
	def __init__(self):
		super(ClientWindow, self).__init__(
			parent=None,
			title='Simple Socket Chat GUI Client'
		)
		self.SetMinSize( wx.Size(500, 400) )
		sizer = wx.BoxSizer()
		self.chat = wx.TextCtrl(
			parent=self,
			name='chatLog',
			pos=(0, 0),
			size=wx.Size( self.GetSize()[0], 0.70 * self.GetSize()[1] ),
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
			size=wx.Size( self.GetSize()[0], 0.30 * self.GetSize()[1] ),
			style=wx.TE_WORDWRAP | wx.TE_NO_VSCROLL | wx.TE_PROCESS_ENTER
		)
		staticSizer.Add(
			self.input,
			wx.SizerFlags(1).Expand()
		)
		sizer.Add(staticSizer)

		self.Bind( wx.EVT_SIZING, self.OnSizing, self )
		self.Bind( wx.EVT_TEXT_ENTER, self.OnEnterPressed, self.input )

	def OnSizing(self, evt: wx.Event):
		self.chat.SetSize( wx.Size( self.GetSize()[0], 0.70 * self.GetSize()[1] ) )
		self.input.SetSize( wx.Size( self.GetSize()[0], 0.30 * self.GetSize()[1] ) )
		self.input.SetPosition( wx.Point( 0, self.chat.GetSize()[1]+1 ) )

	def OnEnterPressed(self, evt: wx.CommandEvent ):
		text = self.input.GetValue()
		App.instance.client.Send( text )
		self.chat.AppendText(f'[you] {text}\n')
		self.input.Clear()

	def OnMessage(self, msg: str):
		wx.CallAfter(self.chat.AppendText, f'{msg}\n')


if __name__ == '__main__':
	app = App()
	app.MainLoop()

