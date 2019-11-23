from kivy.app import App
from kivy.graphics import Color, Rectangle, Canvas, ClearBuffers, ClearColor
from kivy.graphics.fbo import Fbo
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget
from kivy.uix.textinput import TextInput
from functools import partial
from kivy.graphics import Ellipse
from kivy.graphics import Color
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock

class ellipse_box(FloatLayout):

    def __init__(self, x, y):
        super(FloatLayout, self).__init__(width=10, height=10, pos=(x, y))

        with self.canvas:
            Color(0.6, 0.6, 0.6, mode='hsv')
            self.ellipse: Ellipse = Ellipse(pos=((x, y)), size=(10, 10), Color=(1, 1, 1))



    def make_visible(self):
        self._parent.add_widget(self)

    def hide(self):
        self._parent.remove_widget(self)

    def on_touch_down(self, touch):
        if self.collide_point(touch.pos[0], touch.pos[1]):
            print("touched")
        else:
            print("none")

class MolFrame(FloatLayout):
    def __init__(self, **kwargs):
        super(MolFrame, self).__init__(width=220, height=80, pos=(kwargs["x"], kwargs["y"]))
        self._x = kwargs["x"]
        self._y = kwargs["y"]
        self._wight = 120
        self._height = 70
        self._mark_visible = False
        self._list_bonds = []
        self.Name: TextInput = TextInput(text="New Substance", multiline=False,
                              background_color=(0, 0, 0, 0),
                              foreground_color=(1, 1, 1, 1))

        self.Energy: TextInput = TextInput(text=str(0.0), multiline=False,
                               background_color=(0, 0, 0, 0), pos=(0, 30),
                              foreground_color=(1, 1, 1, 1))
        self.add_widget(self.Energy)
        self.add_widget(self.Name)


    def check_click(self, touch):
        res, _ = self.check_click_name(touch.pos)
        return res

    def on_touch_down(self, touch):
        if self.collide_point(touch.pos[0], touch.pos[1]):
            print("touched")
            touch.grab(self)
            if touch.is_double_tap and bool(self.selected_object):
                self.double_tap_events(touch)
        # if self._mark_visible:
        #     if self.lellipse.collide_point(touch.pos[0], touch.pos[1]):
        #         self.lellipse.col=(1, 0, 0, 0)
        #         self._parent.createbond(self, "left")
        #     if self.rellipse.collide_point(touch.pos[0], touch.pos[1]):
        #         self.lellipse.col = (1, 0, 0, 0)
        #         self._parent.createbond(self, "right")

    def on_touch_move(self, touch):
        if touch.grab_current is self:
            self.pos = touch
            self._x = touch.pos[0]
            self._y = touch.pos[1]


    def on_touch_up(self, touch):
        if touch.grab_current is self:
            touch.ungrab(self)

    def hide_marks(self):
        self._mark_visible = False
        self._parent.remove_widget(self.lellipse)
        self._parent.remove_widget(self.rellipse)

    def show_bonds_marks(self):
        self._mark_visible = True
        self._parent.add_widget(self.lellipse)
        self._parent.add_widget(self.rellipse)
        Clock.schedule_once(self.hide_marks, 80)


    def get_specific_methods(self):
        for atr in dir(self):
            if "menu" in atr:
                yield getattr(self, atr)
        return

    def check_click_name(self, pos: tuple):
        if self.Name.collide_point(pos[0], pos[1]):
                return True, "Name"
        if self.Energy.collide_point(pos[0], pos[1]):
            return True, "Energy"
        return False, None

    def double_tap_events(self, touch):
        _, name = self.check_click_name(touch.pos)
        if hasattr(self, name):
            component = getattr(self, name)
            component.on_touch_down(touch)
        else:
            raise NotImplemented


class MyApp(App):


    def build(self):
        root = Widget()
        t_ellips = ellipse_box(200, 200)

        root.add_widget(t_ellips)
        return root

if __name__ == '__main__':
    MyApp().run()
