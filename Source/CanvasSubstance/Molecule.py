from kivy.app import App
from kivy.graphics import Rectangle
from kivy.graphics import Color
from  kivy.uix.scatter import Scatter
from kivy.uix.relativelayout import RelativeLayout
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

class MolFrame(Scatter):
    def __init__(self, **kwargs):
        super().__init__(width=220, height=80, pos=(kwargs["x"], kwargs["y"]), do_rotation=False, do_scale=False, auto_bring_to_front=True)
        # self.main_body = FloatLayout()
        self._x = kwargs["x"]
        self._y = kwargs["y"]
        self._wight = 120
        self._height = 70
        self._mark_visible = False
        self._list_bonds = []
        # self._parent: Widget = parentWidget

        self.Name: TextInput = TextInput(text="New Substance", multiline=False,
                              background_color=(0, 0, 0, 0),
                              foreground_color=(1, 1, 1, 1))

        self.Energy: TextInput = TextInput(text=str(0.0), multiline=False,
                               background_color=(0, 0, 0, 0), pos=(0, 30),
                              foreground_color=(1, 1, 1, 1))
        self.add_widget(self.Energy)
        self.add_widget(self.Name)
        # self.rellipse: Ellipse = ellipse_box(self._x - 10, self._y + 20)
        # self.lellipse: Ellipse = ellipse_box(self._x + self._wight + 10, self._y + 20)

        # self._parent.add_widget(self.Name)
        # self._parent.add_widget(self.Energy)


    # def remove_widget(self):
    #     self._parent.remove_widget(self.Name)
    #     self._parent.remove_widget(self.Energy)

    def check_click(self, touch):
        res, _ = self.check_click_name(touch.pos)
        return res

    def on_touch_down(self, touch):
        if self._mark_visible:
            if self.lellipse.collide_point(touch.pos[0], touch.pos[1]):
                self.lellipse.col=(1, 0, 0, 0)
                self._parent.createbond(self, "left")
            if self.rellipse.collide_point(touch.pos[0], touch.pos[1]):
                self.lellipse.col = (1, 0, 0, 0)
                self._parent.createbond(self, "right")



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





    def move(self, touch):
        self.pos = (touch.pos[0], touch.pos[1])
        # self.Name.pos = (touch.pos[0] - self._wight/2, touch.pos[1] - self._height / 2)
        # self.Energy.pos = (touch.pos[0] - self._wight/2, touch.pos[1] - self._height / 2 + 30)
        self._x = touch.pos[0]
        self._y = touch.pos[1]


class MyApp(App):


    def build(self):
        root = Widget()
        t_ellips = ellipse_box(200, 200)

        root.add_widget(t_ellips)
        return root

if __name__ == '__main__':
    MyApp().run()
