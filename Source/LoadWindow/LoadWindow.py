from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.properties import ObjectProperty
from pathlib import Path
from kivy.base import Builder


LoadDialogString = """
<LoadDialog>:
    BoxLayout:
        size: root.size
        orientation: "vertical"

        TextInput:
            id: text_input
            pos_hint: {"x": 0.1, "y": 0.9}
            size_hint: (0.8, 0.05)

        FileChooserListView:
            id: filechooser
            on_selection: text_input.text = self.selection and self.selection[0] or ''
            path: root.path
            pos_hint: {"x": 0.1, "y": 0.8}
            size_hint: (0.9, 0.6)
            
            
        Button:
            id: loadbutton
            text: "Load"
            pos_hint: {"x": 0.9, "y": 0.2}
            size_hint: (0.1, 0.05)
            on_release: root.loadfile(filechooser.path, filechooser.selection) 
"""

Builder.load_string(LoadDialogString)

class LoadDialog(FloatLayout):
    path = ObjectProperty(None)
    cancel = ObjectProperty(None)
    loadfile = ObjectProperty(None)

    def __init__(self, **kwargs):
        default_path = Path(kwargs["default_path"])
        self.loadfile = kwargs["loadfile"]
        self.cancel = kwargs["cancel"]
        self.path = str(self._get_first_existed_dir(default_path))
        super().__init__()

    def _get_first_existed_dir(self, dir):
        if not dir.is_dir():
            self._get_first_existed_dir(dir.parent)
        else:
            return dir


class TestWidget(FloatLayout):

    def __init__(self):
        super().__init__()
        content = LoadDialog(default_path=Path.cwd(), loadfile=self.load_project, cancel=self.cancel_load)
        self._project_loader = Popup(title="Load Project",
                                     content=content)
        self._project_loader.open()

    def cancel_load(self):
        self._project_loader.dismiss()
        exit(0)

    def load_project(self, path_to_dir, file):
        print(str(file))
        self._project_loader.dismiss()


class TestApp(App):

    def build(self):
        wid = TestWidget()
        return wid


if __name__ == '__main__':
    TestApp().run()