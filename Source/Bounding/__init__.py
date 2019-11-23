from kivy.app import App
from kivy.properties import OptionProperty, NumericProperty, ListProperty, \
        BooleanProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.lang import Builder

Builder.load_string('''
<LinePlayground>:
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


class Bond(FloatLayout):
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


    def on_touch_down(self, touch):
        if super(Bond, self).on_touch_down(touch):
            return True
        touch.grab(self)
        self.points.append(touch.pos)
        return True

    def on_touch_move(self, touch):
        if touch.grab_current is self:
            self.points[-1] = touch.pos
            return True
        return super(Bond, self).on_touch_move(touch)

    def on_touch_up(self, touch):
        if touch.grab_current is self:
            touch.ungrab(self)
            return True
        return super(Bond, self).on_touch_up(touch)


class TestLineApp(App):
    def build(self):
        return Bond()


if __name__ == '__main__':
    TestLineApp().run()


