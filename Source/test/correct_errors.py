from kivy.app import App
from kivy.uix.widget import Widget
from Source.CanvasSubstance.Molecule import MolFrame


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
