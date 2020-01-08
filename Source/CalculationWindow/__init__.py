import logging
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from functools import partial
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.graphics import Line
from kivy.config import Config
from Source.CanvasSubstance.Molecule import MolFrame
from Source.Core import ChProject
from Source.Core import ChCalculations
from pathlib import Path
from Source.Bounding import Bond
from Source.Menu.bubble_menu import bubbleMenuFrame, decorate_functions


class CalculationFrame(Widget):

    def __init__(self, project: ChProject):
        super().__init__()
        self.project = project

    def on_touch_down(self, touch):
        print(touch.pos)
        super().on_touch_down(touch)
        self.del_float_windows(touch)
        if touch.button == 'right':
            print(" local " + str(self.to_local(touch.pos[0], touch.pos[1])))
            self._make_menu(touch)
            print(" located " + str(self.children[0].pos))

    def on_touch_up(self, touch):
        grabed = super().on_touch_up(touch)
        if isinstance(grabed, Bond):
            clicked = super().on_touch_down(touch)
            if isinstance(clicked, MolFrame):
                update = grabed.create(clicked)
                touch.ungrabe(grabed)
                clicked.add_updated(update)
            else:
                grabed.delete()
                touch.ungrabe(grabed)

    def del_float_windows(self, touch):
        for child in self.children:
            if type(child) is bubbleMenuFrame:
                self.remove_widget(child)

    def new_calculations(self, touch):
        print("create new item")
        new_step = ChCalculations(self.project.directory, "new_step")
        new_step.specification = "m11/cc-pvdz"
        cal_frame = MolFrame(new_step, pos=touch.pos)
        self.project.general_method.append(ChCalculations)
        self.add_widget(cal_frame)

    def _make_menu(self, touch):
        calls = []
        call = dict()
        new_compound = decorate_functions(self.new_calculations, touch)
        call = {"name": "New", "call": new_compound}
        calls.append(call)
        menu = bubbleMenuFrame(touch.pos, calls=calls)
        self.add_widget(menu)

class MyApp(App):
    def build(self):
        path = Path.cwd()
        project = ChProject(path, "new1")
        tt = CalculationFrame(project)
        return tt

if __name__ == '__main__':
    MyApp().run()


