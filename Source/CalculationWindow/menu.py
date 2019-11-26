from Source.CanvasSubstance.Molecule import MolFrame
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.lang import Builder
from kivy.uix.bubble import Bubble


Builder.load_string('''
<main_window_menu>:
    size_hint: (None, None)
    size: (160, 80)
    pos_hint: {'center_x': .5, 'y': .3}
    BubbleButton:
        text: 'New'
        on_press: root.new()

''')


class main_window_menu(Bubble):
    def __init__(self, **kwargs):
        super().__init__()
        self._new = kwargs["new"]


    def new(self):
        self._new()

class MainMenu(FloatLayout):

    def __init__(self, pos, **kwargs):
        print(kwargs)
        super().__init__(pos=pos)
        self.show_bubble(**kwargs)

    def show_bubble(self, **kwargs):
        if not hasattr(self, 'bubb'):
            self.bubb = bubb = main_window_menu(**kwargs)
            self.add_widget(bubb)
        else:
            values = ('left_top')
            index = values.index(self.bubb.arrow_pos)
            self.bubb.arrow_pos = values[(index + 1) % len(values)]

    def on_touch_down(self, touch):
        self.bubb.on_touch_down(touch)


