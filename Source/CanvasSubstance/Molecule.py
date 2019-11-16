from kivy.app import App
from kivy.graphics import Rectangle
from kivy.graphics import Color
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from functools import partial
from kivy.graphics import Ellipse
from kivy.uix.boxlayout import BoxLayout

class ellipse_box(Widget):

    def __init__(self, pos, parent):
        super(Widget, self).__init__(height=30, width = 30, pos=pos)
        self.ellipse: Ellipse = Ellipse(pos=(self._x-self._wight/2,self.y-self._height/2+30))
        self._parent = parent


    def make_visible(self):
        self._parent.add_widget(self)

    def hide(self):
        self._parent.remove_widget(self)

class MolFrame():
    def __init__(self, parentWidget, **kwargs):
        self._x = 50
        self._y = 100
        self._wight = 120
        self._height = 70
        self._parent: Widget = parentWidget
        self.Name: TextInput = TextInput(text="New Substance", width=120, height=30, pos=(self._x, self._y), multiline=False,
                              size_hint=(0.8, 0.5), background_color=(0, 0, 0, 0),
                              foreground_color=(1, 1, 1, 1))

        self.Energy: TextInput = TextInput(text=str(0.0),  width=120, height=30, multiline=False, pos=(self._x, self._y + 30),
                              size_hint=(0.8, 0.5), background_color=(0, 0, 0, 0),
                              foreground_color=(1, 1, 1, 1))
        # self.rellipse: ellipse_box = ellipse_box(pos=(self._x-self._wight/2,self.y-self._height/2+30))
        # self.lellipse: ellipse_box = ellipse_box(pos=(self._y + self._wight/2, self._y - self._height/2 + 30))

        self._parent.add_widget(self.Name)
        self._parent.add_widget(self.Energy)


    def check_click(self, touch):
        res, _ = self.check_click_name(touch.pos)
        return res

    def on_touch_down(self, touch):
        # if self.lellipse.collide_point(touch.pos[0], touch.pos[1]):
        #     pass
        # if self.rellipse.collide_point(touch.pos[0], touch.pos[1]):
            pass

    def menu_add_bonds(self):
        self._parent.add_widget(self.lellipse)
        self._parent.add_widget(self.rellipse)


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
        self.Name.pos = (touch.pos[0] - self._wight/2, touch.pos[1] - self._height / 2)
        self.Energy.pos = (touch.pos[0] - self._wight/2, touch.pos[1] - self._height / 2 + 30)
        self._x = touch.pos[0] - self._wight / 2
        self._y = touch.pos[1] - self._height / 2
