import logging
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from functools import partial
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from Source.CanvasSubstance.Molecule import MolFrame
from kivy.uix.label import Label
from kivy.graphics import Line
from kivy.config import Config
from Source.Core import ChProject
from Source.Core import ChCalculations
from pathlib import Path
from Source.Bounding import Bond
from Source.CalculationWindow.menu import main_window_menu, MainMenu


class corframe(Widget):

    def __init__(self):
        super().__init__()


    def new_compound(self, touch):
        mol = MolFrame(x=touch.pos[0], y=touch.pos[1])
        self.add_widget(mol)

    def on_touch_down(self, touch):
        super().on_touch_down(touch)
        if touch.button == "right":
            self.new_compound(touch)

class MyApp(App):
    def build(self):
        tt = corframe()
        return tt

if __name__ == '__main__':
    MyApp().run()
