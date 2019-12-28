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
        super(RelativeLayout, self).__init__(size_hint=(None, None), width=220, height=80, pos=(200, 200))

        self.Name: TextInput = TextInput(text="New Substance", multiline=False,
                              background_color=(0, 0, 0, 0),
                              foreground_color=(1, 1, 1, 1), pos=(0, -30))

        self.Energy: TextInput = TextInput(text=str(0.0), multiline=False,
                               background_color=(0, 0, 0, 0),
                              foreground_color=(1, 1, 1, 1))
        self.add_widget(self.Name)
        self.add_widget(self.Energy)

    def on_touch_down(self, touch):
        if self.collide_point(touch.pos[0], touch.pos[1]):
            touch.grab(self)
            print("grab")
        return True

    def on_touch_up(self, touch):
        if touch.grab_current is self:
            print("ungrab")
            touch.ungrab(self)

    def on_touch_move(self, touch):
        if touch.grab_current is self:
            self.pos = (touch.pos[0], touch.pos[1])


class dWidget(Widget):

    def on_touch_down(self, touch):
        print("something")
        super().on_touch_down(touch)

    def on_touch_move(self, touch):
        super().on_touch_move(touch)

    def on_touch_up(self, touch):
        super().on_touch_up(touch)

class MyApp(App):
    def build(self):
        root = FloatLayout()
        tt = MolFrame(x=200, y=200)
        # tt = test_widget()
        sep_w = dWidget()

        root.add_widget(sep_w)
        sep_w.add_widget(tt)

        return root


if __name__ == '__main__':
    MyApp().run()