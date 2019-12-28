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
from Source.CalculationWindow.menu import main_window_menu, MainMenu


def decor_functions(func_todecorate, add_arg):
    def shell():
        return func_todecorate(add_arg)
    return shell

class CalculaitonFrame(Widget):

    def __init__(self, project: ChProject):
        super().__init__()
        self.project = project


    def on_touch_down(self, touch):
        print(touch.pos)
        super().on_touch_down(touch)
        print(touch.pos)
        for child in self.children:
            if type(child) is MainMenu:
                self.remove_widget(child)
        if touch.button == 'right':
            dc_new = decor_functions(self.new_calculations, touch)
            menu = MainMenu(pos=touch.pos, new=dc_new)
            print(" local " + str(self.to_local(touch.pos[0], touch.pos[1])))
            self.add_widget(menu)
            print(" located " + str(self.children[0].pos))



    def new_calculations(self, touch):
        print("create new item")
        new_step = ChCalculations(self.project.directory, "new_step")
        new_step.specification = "m11/cc-pvdz"
        cal_frame = MolFrame(new_step, pos=touch.pos)

        self.project.general_method.append(ChCalculations)
        self.add_widget(cal_frame)

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





class MyApp(App):
    def build(self):
        path = Path.cwd()
        project = ChProject(path, "new1")
        tt = CalculaitonFrame(project)
        return tt


if __name__ == '__main__':
    MyApp().run()


