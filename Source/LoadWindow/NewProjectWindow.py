from kivy.app import App
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.properties import ObjectProperty
from pathlib import Path
from kivy.base import Builder


NewDialogString = """
<CreateDialog>:
    RelativeLayout:
        size: root.size
        pos: root.pos
        orientation: "vertical"

        TextInput:
            id: text_input
            text: "New Project"
            pos_hint: root.text_input_pos
            size_hint: root.text_input_size

       
        Button:
            id: create
            text: "Create"
            pos_hint: root.button_create_pos
            size_hint: root.button_size
            on_release: root.createfile(root.path, text_input.text)
        
        Button:
            id: cancelbutton
            text: "Cancel"
            pos_hint: root.button_cancel_pos
            size_hint: root.button_size
            on_release: root.cancel() 

"""

Builder.load_string(NewDialogString)


class CreateDialog(FloatLayout):
    path = ObjectProperty(None)
    cancel = ObjectProperty(None)
    createfile = ObjectProperty(None)


    def __init__(self, **kwargs):
        self.path = kwargs["path"]
        self.cancel = kwargs["cancel"]
        self.createfile = kwargs["create"]
        self.button_size = (0.15, 0.1)
        self.button_create_pos = {"x": 0.8, "y": 0.1}
        self.button_cancel_pos = {"x": 0.05, "y": 0.1}
        self.text_input_pos = {"x": 0.05, "y": 0.7}
        self.text_input_size = (0.9, 0.1)
        super().__init__()








class TestWidget(FloatLayout):

    def __init__(self):
        super().__init__()
        content = CreateDialog(default_path=Path.cwd(), loadfile=self.load_project, cancel=self.cancel_load)
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