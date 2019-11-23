from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.factory import Factory
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.filechooser import FileChooserListView
from pathlib import Path
import json
import os




class SaveDialog(FloatLayout):
    path = ObjectProperty(None)
    rootpath = ObjectProperty(None)
    filechooser : FileChooserListView = ObjectProperty(None)

    def __init__(self, **kwargs):
        self.project = Path(kwargs["rootpath"])
        if not self.project.is_dir():
            self.project.mkdir(self, parents=True, exist_ok=True)
        super().__init__(**kwargs)

    def get_selected(self):
        for sel in self.filechooser.selection:
            yield self.filechooser.selection

    def create_sub(self, name) -> Path:
        path = Path(self.rootpath)
        path = Path(path/name)
        path.mkdir()
        return path

    def rename(self, sub, new_name):
        pass

    def save(self):
        pass

    def on_touch_down(self, touch):
        if self.collide_point(touch.pos[0], touch.pos[1]):
            y = touch.pos[1]
            if y > self.pos[1] + (self.height * 0.8):
                touch.grab(self)
                print("grab")

    def on_touch_move(self, touch):
        if touch.grab_current is self:
            self.parent.parent.parent.parent.pos = touch.pos
            print("move")

    def on_touch_up(self, touch):
        if touch.grab_current is self:
            touch.ungrab(self)
            print("ungrab")

    def create_component(self, name) -> Path:
        path = Path(self.rootpath)
        sub = name.parent.name
        path = Path(path/ sub /name)
        path.mkdir()
        return path


Factory.register('SaveDialog', cls=SaveDialog)


class Editor(App):

    def build(self):
        wid = FloatLayout()
        content = SaveDialog(path=os.getcwd(), rootpath=os.getcwd())
        wid._popup = Popup(title="Project", content=content, auto_dismiss=False,
                            size_hint=(0.3, 0.5), pos_hint={"x": 0.7, "top": 0.7})
        wid._popup.open()
        return wid





if __name__ == '__main__':
    Editor().run()