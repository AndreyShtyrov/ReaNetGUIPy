'''
Bubble
======

Test of the widget Bubble.
'''
from Source.CanvasSubstance.Molecule import MolFrame
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.lang import Builder
from kivy.uix.bubble import Bubble

Builder.load_string('''
<cut_copy_paste>
    size_hint: (None, None)
    size: (160, 120)
    pos_hint: {'center_x': .5, 'y': .6}
    BubbleButton:
        text: 'New'
        on_press: root.new()
    BubbleButton:
        text: 'Rename'
    BubbleButton:
        text: 'Copy'
''')


class cut_copy_paste(Bubble):

    def __init__(self, **kwargs):
        super().__init__()
        self._new = kwargs["new"]

    def add_specific_methods(self, obj):
        for tbutton in obj.get_specific_methods():
            pass

    def new(self):
        self._new()


class MainMenu(FloatLayout):

    def __init__(self, pos, **kwargs):
        super(MainMenu, self).__init__()

        self.show_bubble(pos, **kwargs)

    def show_bubble(self, pos, **kwargs):
        if not hasattr(self, 'bubb'):
            self.bubb = bubb = cut_copy_paste(**kwargs)
            self.pos = pos
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

class TestBubbleApp(App):
    def build(self):
        return MainMenu()


if __name__ == '__main__':
    TestBubbleApp().run()
