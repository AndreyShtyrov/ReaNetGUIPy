import logging
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from functools import partial
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from Source.CanvasSubstance.Molecule import MolFrame
from kivy.uix.label import Label
from Source.Menu.bubble_menu import MainMenu
from Source.Menu.menu import menu
from kivy.graphics import Line
from kivy.config import Config
from .menu import menu



class CalculaitonFrame(FloatLayout):

    def __init__(self, project):
        self.project = project
        super().__init__()


    def on_touch_down(self, touch):
        def decor_functions(func_todecorate, add_arg):
            def shell():
                return func_todecorate(add_arg)
            return shell
        if touch.button == 'right':
            decor_functions()

    def new_calculations(self):
        self.p

