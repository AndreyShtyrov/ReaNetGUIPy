from kivy.properties import OptionProperty, NumericProperty, ListProperty, \
        BooleanProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.lang import Builder

lstring = '''
<Bound_pointer>:
    canvas:
        Color:
            rgba: self.color[0], self.color[1], self.color[2],  self.transparency
        Line:
            points: self.points
            width: self.linewidth
            close: self.close
'''
Builder.load_string(lstring)


class Bound_pointer(FloatLayout):
    transparency = NumericProperty(1.0)
    color = ListProperty([0.8, 0.8, 0.8])
    close = BooleanProperty(False)
    ledt_point = None
    points = ListProperty()
    linewidth = NumericProperty(1.0)

    def __init__(self, lframe, rframe):
        super().__init__()
        lframe.bind(rframe)
        rframe.bind(lframe)

    def on_update(self):
        pass



