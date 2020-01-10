from kivy.app import App
from kivy.properties import OptionProperty, NumericProperty, ListProperty, \
        BooleanProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.lang import Builder

Builder.load_string('''
<Bond>:
    canvas:
        Color:
            rgba: .8, .8, .8, root.alpha_controlline
        Line:
            points: self.points
            close: self.close
            dash_length: self.dash_length
            dash_offset: self.dash_offset
            dashes: self.dashes
        Color:
            rgba: 1, .4, .4, root.alpha
''')


class Bond(FloatLayout, ):
    alpha_controlline = NumericProperty(1.0)
    alpha = NumericProperty(0.5)
    close = BooleanProperty(False)
    points = ListProperty([])
    points2 = ListProperty([])
    joint = OptionProperty('none', options=('round', 'miter', 'bevel', 'none'))
    cap = OptionProperty('none', options=('round', 'square', 'none'))
    linewidth = NumericProperty(10.0)
    dt = NumericProperty(0)
    dash_length = NumericProperty(1)
    dash_offset = NumericProperty(0)
    dashes = ListProperty([])

    def __init__(self, touch=None, prev_object=None):
        super().__init__()
        touch.grab(self)
        self.left = prev_object

    def update_left(self, new_pos):
        self.points[-1] = new_pos

    def update_right(self, new_pos):
        self.points[0] = new_pos

    def on_touch_down(self, touch):
        if touch.current_grab is self:
            self.points.append(touch.pos)
            if bool(self.points):
                return "Bind"
        if touch.button is "right":
            self.ungrab(self)
            return "Bind"

    def on_touch_move(self, touch):
        if touch.grab_current is self:
            self.update_left(touch.pos)
            return True

    def on_touch_up(self, touch):
        if touch.grab_current is self:
            touch.ungrab(self)
            return True




class TestLineApp(App):
    def build(self):
        return Bond()


if __name__ == '__main__':
    TestLineApp().run()


