import logging
from Source.Core import ChCompound
from kivy.clock import Clock
from kivy.app import App
from pathlib import Path
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from functools import partial
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from Source.Core.ChProject import ChProject
from Source.CanvasSubstance.Molecule import MolFrame
from kivy.uix.label import Label
from Source.Menu.bubble_menu import bubbleMenuFrame, decorate_functions
from Source.Menu.menu import menu
from kivy.graphics import Line
from kivy.config import Config
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')

class MainWidget(Widget):

    def __init__(self, project):
        self.project:  ChProject = project
        super().__init__()
        self.selected_object = None
        self._bubblmenu = None
        self._update_per_move = []
        self.log = logging.getLogger("MainWindow")
        # self.update = Clock.schedule_once(self.project.update, 2)

    def new_comp(self, touch):
        new_sub = self.project.add_new_compound()
        new_sub_frame = MolFrame(new_sub, pos=touch.pos)
        self.add_widget(new_sub_frame)

    def on_touch_down(self, touch):
        is_made_sm = super().on_touch_down(touch)
        self.del_float_windows(touch)
        if self.collide_point(*touch.pos) and not is_made_sm:
            if touch.button == 'right' and not self._check_clicked_child(touch):
                self._make_menu(touch)

    def _check_clicked_child(self, touch):
        for child in self.children:
            if child.collide_point(*touch.pos):
                return True
            return False

    def on_touch_up(self, touch):
        grabed = super().on_touch_up(touch)
        return super().on_touch_move(touch)

    def on_touch_move(self, touch):
        super().on_touch_move(touch)
        for redrawing in self._update_per_move:
            points = [touch.pos[0], touch.pos[1], redrawing.start_x, redrawing.start_y]
            redrawing.points = points

    def del_float_windows(self, touch):
        for child in self.children:
            if type(child) is bubbleMenuFrame:
                self.remove_widget(child)

    def _make_menu(self, touch):
        calls = []
        call = dict()
        new_compound = decorate_functions(self.new_comp, touch)
        call = {"name": "New", "call": new_compound}
        calls.append(call)
        menu = bubbleMenuFrame(touch.pos, calls=calls)
        self.add_widget(menu)



class MyApp(App):

    def build(self):
        cwd = Path.cwd()
        project = ChProject(cwd)
        wid = MainWidget(project)
        root = BoxLayout(orientation='vertical')
        gmenu = menu
        layout = BoxLayout(size_hint=(1, None), height=50)
        layout.add_widget(gmenu)
        root.add_widget(layout)
        root.add_widget(wid)
        return root


if __name__ == '__main__':
    MyApp().run()