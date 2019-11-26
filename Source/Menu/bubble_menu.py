
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


<MolFrame_menu>:
    size_hint: (None, None)
    size: (260, 80)
    pos_hint: {'center_x': .5, 'y': .3}
    BubbleButton:
        text: 'New Bond'
        on_press: root.newbond()
    BubbleButton:
        text: 'Delete'
        on_press: root.delFrame()
    BubbleButton:
        text: 'Copy'
        on_press: root.copyFrame()
''')

class MolFrame_menu(Bubble):
    def __init__(self, **kwargs):
        super().__init__()
        self._newbond = kwargs["newbond"]
        self._del = kwargs["delFrame"]
        self._copy = kwargs["copyFrame"]

    def newbond(self):
        self._newbond()

    def delFrame(self):
        self._del()

    def copyFrame(self):
        self._copy()

class main_window_menu(Bubble):
    def __init__(self, **kwargs):
        super().__init__()
        self._new = kwargs["new"]


    def new(self):
        self._new()

class MainMenu(FloatLayout):

    def __init__(self, pos, **kwargs):
        super(MainMenu, self).__init__()
        self.show_bubble(pos, **kwargs)

    def show_bubble(self, pos, **kwargs):
        if not hasattr(self, 'bubb'):
            cliked_obj = kwargs.pop("clicked_obj")
            if cliked_obj == "MolFrame":
                self.bubb = bubb = MolFrame_menu(**kwargs)
            else:
                self.bubb = bubb = main_window_menu(**kwargs)
            self.add_widget(bubb)
        else:
            values = ('left_top')
            index = values.index(self.bubb.arrow_pos)
            self.bubb.arrow_pos = values[(index + 1) % len(values)]

    def on_touch_down(self, touch):
        self.bubb.on_touch_down(touch)

    def check_click(self, touch):
        return self.bubb.collide_point(touch.pos[0], touch.pos[1])

    def move(self, touch):
        pass

    def double_tap_events(self, touch):
        pass
