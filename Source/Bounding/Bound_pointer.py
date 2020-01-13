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

    def __init__(self, visible_objects):
        super().__init__()
        self.point_is_ready = False
        self._pointed_objs = []
        self.visible_objects = visible_objects

    def on_touch_down(self, touch):
        print("execute LinePlayground.on_touch_down")
        print(" pos:  " + str(touch.pos))
        if not bool(self.points):
            for point in self.visible_objects:
                if point.collide_point(*touch.pos):
                    touch.grab(self)
                    self.points.append(point.pos)
                    self.points.append(point.pos)
                    self._pointed_objs.append(point)
                    return True
        return False

    def on_touch_move(self, touch):
        if touch.grab_current is self:
            self.points[-1] = touch.pos
            return True
        return super().on_touch_move(touch)

    def on_touch_up(self, touch):
        print("execute LinePlayground.on_touch_up")
        print(" pos:  " + str(touch.pos))
        if touch.grab_current is self:
            for point in self.visible_objects:
                if point.collide_point(*touch.pos):
                    touch.ungrab(self)
                    self._pointed_objs.append(point)
                    print(" End object pointing")
                    print(" Pointed objs:  " + str(len(self._pointed_objs)))
                    return False
            print(" Restart pointer line")
            touch.ungrab(self)
            self.points = []
            return True

    def get_pointed_objs(self):
        return self._pointed_objs[0], self._pointed_objs[1]




