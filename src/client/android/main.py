import os

import kivy
from kivy.app import App
from kivy.core.window import WindowBase
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget

from Client import Client

kivy.require('2.0.0')  # replace with your current kivy version !


class ChatApp(App):

    client: Client
    chat: TextInput
    input: TextInput
    root_window: WindowBase
    username: str = os.getlogin()

    def build(self) -> Widget:
        """ This is basically __init__, but returns the root widget """
        self.title = 'Simple Socket Chat Android Client'
        self.client = Client()

        layout = BoxLayout(
            orientation='vertical'
        )
        layout.minimum_height = layout.height = 500
        layout.minimum_width = layout.width = 400

        self.chat = TextInput(
            multiline=True,
            readonly=True
        )
        self.chat.height = int( 0.70 * layout.height )
        self.input = TextInput(
            multiline=False,
            readonly=True
        )
        self.input.height = int( 0.30 * layout.height )
        self.input.bind(
            on_text_validate=self.OnEnterPressed
        )
        layout.add_widget( self.chat )
        layout.add_widget( self.input )

        self.client.SetListener( self.OnMessage )

        return layout

    # --- CLIENT EVENTS ---
    def OnEnterPressed( self, instance: TextInput):
        message = instance.text.strip()
        self.chat.text += f'[{self.username}] {message}\n'
        instance.text = ''
        self.client.Send(message)

    def OnMessage( self, msg: str ):
        self.chat.text += f'{msg}\n'

    # --- APP EVENTS ---
    def on_stop(self):
        """ app exit """

    def on_pause(self):
        """ app pauses exec, resume not guaranteed """

    def on_resume(self):
        """ app resumes exec """





if __name__ == '__main__':
    ChatApp().run()