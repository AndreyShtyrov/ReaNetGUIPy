from pathlib import Path
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from Source.CalculationWindow.Core.ChProject import ChProject
from Source.CanvasSubstance.Molecule import MolFrame
from kivy.app import App
from Source.Bounding.Bound_pointer import Bound_pointer


class Test_Widget(Widget):
    def __init__(self):
        super().__init__()

    def on_touch_down(self, touch):
        print("execute Test_Widget.on_touch_down")
        print(" pos:  " + str(touch.pos))
        return super().on_touch_down(touch)




class TestLineApp(App):
    def build(self):
        main_path = Path().cwd()
        wid = Test_Widget()
        project = ChProject(main_path)
        root = BoxLayout(orientation='vertical')
        root.add_widget(wid)
        new_sub = project.add_new_compound()
        Mol1 = MolFrame(new_sub, pos=(200, 300))
        wid.add_widget(Mol1)
        new_sub = project.add_new_compound()
        Mol2 = MolFrame(new_sub, pos=(500, 500))
        wid.add_widget(Mol2)
        line = Bound_pointer(wid.children)
        wid.add_widget(line)
        return root



if __name__ == '__main__':
    TestLineApp().run()


