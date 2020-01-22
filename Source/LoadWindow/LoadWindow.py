from kivy.app import App
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.properties import ObjectProperty
from pathlib import Path
from kivy.base import Builder
from Source.LoadWindow.NewProjectWindow import CreateDialog


LoadDialogString = """
<LoadDialog>:
    RelativeLayout:
        size: root.size
        pos: root.pos
        orientation: "vertical"
        
        TextInput:
            id: text_input
            pos_hint: root.text_input_pos
            size_hint: root.text_input_size
        
        RelativeLayout:
            size_hint: root.filechooser_size
            pos_hint: root.filechooser_pos
            
            BoxLayout: 
                FileChooserListView:
                    id: filechooser
                    on_selection: text_input.text = self.selection and self.selection[0] or ''
                    path: root.path
                
        Button:
            id: loadbutton
            text: "Load"
            pos_hint: root.button_load_pos
            size_hint: root.button_size
            on_release: root.loadfile(filechooser.path, filechooser.selection)
            
        Button:
            id: newproject
            text: "New"
            pos_hint: root.button_new_pos
            size_hint: root.button_size
            on_release: root.newfileWindow(filechooser.path)
        
        Button:
            id: cancelbutton
            text: "Cancel"
            pos_hint: root.button_cancel_pos
            size_hint: root.button_size
            on_release: root.cancel() 
"""

Builder.load_string(LoadDialogString)

class LoadDialog(FloatLayout):
    path = ObjectProperty(None)
    cancel = ObjectProperty(None)
    loadfile = ObjectProperty(None)
    newfile = ObjectProperty(None)

    def __init__(self, **kwargs):
        default_path = Path(kwargs["default_path"])
        self.loadfile = kwargs["loadfile"]
        self.cancel = kwargs["cancel"]
        self.newfile = kwargs["new"]
        self.path = str(self._get_first_existed_dir(default_path))
        self.button_size = (0.1, 0.05)
        self.button_load_pos = {"x": 0.9, "y": 0.1}
        self.button_new_pos = {"x": 0.5, "y": 0.1}
        self.button_cancel_pos = {"x": 0.05, "y": 0.1}
        self.filechooser_pos = {"x": 0.05, "top": 0.8}
        self.filechooser_size = (0.9, 0.6)
        self.text_input_pos = {"x": 0.05, "y": 0.9}
        self.text_input_size = (0.9, 0.05)
        super().__init__()

    def _get_first_existed_dir(self, dir):
        if not dir.is_dir():
            self._get_first_existed_dir(dir.parent)
        else:
            return dir

    def newfileWindow(self, path):
        content = CreateDialog(path=path,
                             create=self.create_project,
                             cancel=self.return_tocurrentWindow)
        self._project_creater = Popup(title="Create Project",
                                     content=content,
                                     size_hint=(0.6, 0.6),
                                     pos_hint={"x": 0.25, "top": 0.7})
        self._project_creater.open()

    def create_project(self, *kvargs):
        self.newfile(*kvargs)
        self._project_creater.dismiss()

    def return_tocurrentWindow(self):
        self._project_creater.dismiss()

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