import logging
from kivy.app import App
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from functools import partial
from kivy.uix.boxlayout import BoxLayout
from Source.CanvasSubstance.Molecule import MolFrame
from kivy.uix.label import Label
from Source.Menu.bubble_menu import MainMenu
from Source.Menu.menu import menu
from kivy.graphics import Line


class test_widget(RelativeLayout):

    def __init__(self, **kwargs):
        super(RelativeLayout, self).__init__(width=220, height=80)
        with self.canvas:
            self.Name: TextInput = TextInput(text="New Substance", multiline=False,
                                  background_color=(0, 0, 0, 0),
                                  foreground_color=(1, 1, 1, 1))

            self.Energy: TextInput = TextInput(text=str(0.0), multiline=False,
                                   background_color=(0, 0, 0, 0), pos=(0, 30),
                                  foreground_color=(1, 1, 1, 1))

class dWidget(Widget):

    def on_touch_up(self, touch):
        tt = test_widget()
        self.add_widget(tt)


class MyApp(App):


    def build(self):
        wid = dWidget()
        gmenu = menu
        root = BoxLayout(orientation='vertical')
        layout = BoxLayout(size_hint=(1, None), height=50)
        layout.add_widget(gmenu)
        root.add_widget(layout)
        root.add_widget(wid)
        return root


if __name__ == '__main__':
    MyApp().run()