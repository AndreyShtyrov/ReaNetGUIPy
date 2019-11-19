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
        super(RelativeLayout, self).__init__(size_hint=(None, None), width=220, height=80, pos=(200,200))

        self.Name: TextInput = TextInput(text="New Substance", multiline=False,
                              background_color=(0, 0, 0, 0),
                              foreground_color=(1, 1, 1, 1), pos=(0, 30))

        self.Energy: TextInput = TextInput(text=str(0.0), multiline=False,
                               background_color=(0, 0, 0, 0),
                              foreground_color=(1, 1, 1, 1))
        self.add_widget(self.Name)
        self.add_widget(self.Energy)

    def on_touch_up(self, touch):
        if self.collide_point(touch.pos[0], touch.pos[1]):
            print("touched")
        else:
            print("None")

class dWidget(BoxLayout):
    pass



class MyApp(App):
    def build(self):
        root = FloatLayout()
        b1 = Button(pos_hint={'x': 0, 'center_y': .6})
        b2 = Button(pos_hint={'right': 1, 'center_y': .3})
        root.add_widget(b1)
        root.add_widget(b2)
        return root


if __name__ == '__main__':
    MyApp().run()