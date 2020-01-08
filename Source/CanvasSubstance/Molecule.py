from kivy.app import App
from kivy.graphics import Color, Rectangle, Canvas, ClearBuffers, ClearColor
from kivy.graphics.fbo import Fbo
# from kivy.input.provider import touch
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget
from Source.Core.ChCompound import ChCompound
from kivy.properties import StringProperty
from Source.Core.ChCalculations import ChCalculations
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.textinput import TextInput
from functools import partial
from kivy.graphics import Ellipse
from kivy.graphics import Color
from Source.Menu.bubble_menu import bubbleMenuFrame, decorate_functions

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

class MolFrame(RelativeLayout):
    def __init__(self, core_object, **kwargs):
        pos = kwargs["pos"]
        super().__init__(size_hint=(None, None), width=220, height=80, pos=pos)
        self.core_object = core_object
        self._update_object = []

        self.Name: TextInput = TextInput(text=core_object.Name,
                                        multiline=False,
                                        background_color=(0, 0, 0, 0),
                                        size_hint=(0.8, 0.4),
                                        pos_hint={"left": 0.1, "top": 0.7},
                                        foreground_color=(1, 1, 1, 1),
                                        on_text_validate=self.on_change_name)
        if type(core_object) is ChCompound:
            self.Text: TextInput = TextInput(text=str(core_object.Energy),
                                             multiline=False,
                                             size_hint=(0.8, 0.4),
                                             pos_hint={"left": 0.1, "top": 0.2},
                                             background_color=(0, 0, 0, 0),
                                             foreground_color=(1, 1, 1, 1))
        elif type(core_object) is ChCalculations:
            self.Text: TextInput = TextInput(text=str(core_object.specification),
                                             multiline=False,
                                             size_hint=(0.8, 0.4),
                                             pos_hint={"left": 0.1, "top": 0.2},
                                             background_color=(0, 0, 0, 0),
                                             foreground_color=(1, 1, 1, 1))
        self.core_object.add_gui(self)
        self.add_widget(self.Text)
        self.add_widget(self.Name)
        self.core_object.save()

    def on_change_name(self, instance):
        self.core_object.rename(instance.text)

    def check_click_name(self, pos: tuple):
        if self.Name.collide_point(pos[0], pos[1]):
                return True, "Name"
        if self.Text.collide_point(pos[0], pos[1]):
            return True, "Text"
        return False, "None"

    def update(self, touch):
        self.pos = touch.pos
        self._update_bind_objects(touch)

    def on_touch_down(self, touch):
        print("execute MolFrame.on_touch_down")
        print("position" + str(self.pos))
        if self.collide_point(touch.pos[0], touch.pos[1]):
            touch.push()
            touch.apply_transform_2d(self.to_local)
            self.try_click_on_menu(touch)
            self.del_float_windows(touch)
            if touch.is_double_tap:
                self.double_tap_events(touch)
            elif touch.button == 'right':
                self._make_menu(touch)
            else:
                touch.grab(self)

            touch.pop()
            return True
        self.del_float_windows(touch)

    def try_click_on_menu(self, touch):
        for child in self.children:
            if type(child) is bubbleMenuFrame:
                if child.collide_point(*touch.pos):
                    child.on_touch_down(touch)
                    self.remove_widget(child)

    def on_touch_move(self, touch):
        if touch.grab_current is self:
            self.update(touch)

    def on_touch_up(self, touch):
        if touch.grab_current is self:
            touch.ungrab(self)

    def double_tap_events(self, touch):
        is_pointed, Name = self.check_click_name(touch.pos)
        if is_pointed:
            if hasattr(self, Name):
                component = getattr(self, Name)
                component.on_touch_down(touch)
            else:
                raise NotImplemented

    def check_click(self, touch):
        res, _ = self.check_click_name(touch.pos)
        return res

    def convert_in_dictionary(self):
        result = dict()
        result.update({"x": self.pos[0]})
        result.update({"y": self.pos[1]})
        return result

    def del_float_windows(self, touch):
        for child in self.children:
            if type(child) is bubbleMenuFrame:
                self.remove_widget(child)

    def _make_menu(self, touch):
        calls = []
        call = {"name": "None", "call": lambda: print("No calls")}
        bmenu = bubbleMenuFrame(touch.pos, calls=[call])
        self.add_widget(bmenu)

    def _update_bind_objects(self, touch):
        for update in self._update_object:
            update(self, touch)



    # def hide_marks(self):
    #     self._mark_visible = False
    #     self._parent.remove_widget(self.lellipse)
    #     self._parent.remove_widget(self.rellipse)
    #
    # def show_bonds_marks(self):
    #     self._mark_visible = True
    #     self._parent.add_widget(self.lellipse)
    #     self._parent.add_widget(self.rellipse)
    #     Clock.schedule_once(self.hide_marks, 80)
    #
    # def get_lbind_point(self):
    #     return self._x , self._y + self._height / 2
    #
    # def get_rbind_point(self):
    #     return self._x + self._wight, self._y + self._height / 2


class MyApp(App):

    def build(self):
        root = Widget()
        t_ellips = ellipse_box(200, 200)

        root.add_widget(t_ellips)
        return root

if __name__ == '__main__':
    MyApp().run()
