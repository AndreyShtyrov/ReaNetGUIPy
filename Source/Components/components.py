from Source.CanvasSubstance.Molecule import MolFrame
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.lang import Builder
from kivy.uix.textinput import TextInput
from Source.IO import data

Builder.load_string('''
<AddComponent>:
    TextInput:
        text: "New Component"
        size_hint: 0.3, 0.8
        pos_hint: {"x": 0.1, "top": 0.9}
    Button:
        text: "Associate with file"
        size_hint: 0.25, 0.25
        pos_hint: {"x": 0.1, "top": 0.25}
        on_press: root.load_file
    Button:
        text: "Input Geometry"
        size_hint: 0.25, 0.25
        pos_hint: {"x": 0.4, "top": 0.25}
        on_press: root.load_geom
    Button:
        text: "Slip"
        size_hint: 0.25, 0.25
        pos_hint: {"x": 0.7, "top": 0.25}
        on_press: root.skip   
''')

class AddComponent():
    pass


class MComponent(data):

    def __init__(self, parent):
        self._elenergy = 0.0
        self._energy = 0.0
        self._name = "New Component"
        parent.AddComponent()
        self._name = parent.AddComponent.getname()
        self.dir = parent.getdir() / self._name
        self.createdir()

    def add_geom(self):
        pass

    def associate_with_file(self):
        pass

    def get_energy(self):
        pass


