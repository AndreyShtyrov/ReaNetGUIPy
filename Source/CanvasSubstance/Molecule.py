from kivy.app import App
# from kivy.input.provider import touch
from Source.Bounding.Bound_pointer import Bound_pointer
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget
from Source.Core import ChCompound
from Source.Core import ChCalculations
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.textinput import TextInput
from kivy.graphics import Ellipse
from kivy.graphics import Color
from Source.Menu.bubble_menu import bubbleMenuFrame


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
        super().__init__(size_hint=(None, None), width=130, height=80, pos=pos)
        self.core_object = core_object
        self._update_object = []
        self._bounded_objs = []
        self._rellips = (self.pos[0] + self.width, self.pos[1] + self.height/2)
        self._lellips = (self.pos[0], self.pos[1] + self.height/2)


        self.Name: TextInput = TextInput(text=core_object.Name,
                                        multiline=False,
                                        background_color=(0, 0, 0, 0),
                                        size_hint=(1, 0.4),
                                        pos_hint={"left": 0.1, "top": 0.7},
                                        foreground_color=(1, 1, 1, 1),
                                        on_text_validate=self.on_change_name)
        if type(core_object) is ChCompound:
            self.Text: TextInput = TextInput(text=str(core_object.Energy),
                                             multiline=False,
                                             size_hint=(1, 0.4),
                                             pos_hint={"left": 0.1, "top": 0.2},
                                             background_color=(0, 0, 0, 0),
                                             foreground_color=(1, 1, 1, 1))
        elif type(core_object) is ChCalculations:
            self.Text: TextInput = TextInput(text=str(core_object.specification),
                                             multiline=False,
                                             size_hint=(1, 0.4),
                                             pos_hint={"left": 0.1, "top": 0.2},
                                             background_color=(0, 0, 0, 0),
                                             foreground_color=(1, 1, 1, 1))
        self.core_object.add_gui(self)
        self.add_widget(self.Text)
        self.add_widget(self.Name)
        self.core_object.save()

    def is_connectable(self):
        return True

    @property
    def rellips(self):
        print(" rellips" + str(self.pos) + str((self.width, self.height/3.5)))
        self._rellips = (self.pos[0] + self.width, self.pos[1] + self.height/3.5)
        return self._rellips

    @rellips.setter
    def rellips(self, value):
        print(" property rellips could not be set by user")
        self._rellips = (self.pos[0] + self.width, self.pos[1] + self.height/3.5)

    @rellips.deleter
    def rellips(self):
        del self._rellips

    @property
    def lellips(self):
        print(" lellips" + str(self.pos) + str((self.width, self.height / 3.5)))
        self._lellips = (self.pos[0], self.pos[1] + self.height / 3.5)
        return self._lellips

    @lellips.setter
    def lellips(self, value):
        print(" property lellips could not be set by user")
        self._lellips = (self.pos[0], self.pos[1] + self.height / 3.5)

    @lellips.deleter
    def lellips(self):
        del self._lellips

    def get_connector_position(self, touch):
        touch.push()
        touch.apply_transform_2d(self.to_local)
        print(" touch in: " + str(touch.pos))
        print(" width is: " + str(self.width))
        if touch.pos[0] < self.width/2:
            touch.pop()
            print(" return lellips")
            return self.lellips
        else:
            touch.pop()
            print(" return rellips")
            return self.rellips

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

    def make_bound(self, another):
        self._bounded_objs.append(another)
        self.core_object.setBound(self.core_object, another.core_object)


    def on_touch_down(self, touch):

        if self.collide_point(touch.pos[0], touch.pos[1]):
            print("execute MolFrame.on_touch_down")
            print(" Name:     " + str(self.Name.text))
            print(" touch pos:" + str(touch.pos))
            print(" self  pos:" + str(self.pos))
            touch.push()
            touch.apply_transform_2d(self.to_local)
            if touch.is_double_tap:

                self.double_tap_events(touch)
            else:
                touch.grab(self)
            touch.pop()
            return False
        return False

    def on_touch_move(self, touch):
        if touch.grab_current is self:
            if not touch.button == "right":
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



    def make_menu(self, touch):
        calls = []
        call = {"name": "New Bond", "call": lambda: self.parent.add_widget(Bound_pointer())}
        # call = {"name": "New Bond", "call": lambda: self.create_bond(touch)}
        calls.append(call)
        call = {"name": "None", "call": lambda: print("No calls1")}
        calls.append(call)

        bmenu = bubbleMenuFrame(touch.pos, calls=calls)
        self.parent.add_widget(bmenu)

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
