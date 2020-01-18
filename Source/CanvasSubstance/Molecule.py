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
from Source.Bounding.Bound import Node
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
        self._binded_objs = []
        _rellips = (0.85, 0.5)
        _lellips = (0.05, 0.5)
        self.rellips = Node(_rellips, froze=True)
        self.lellips = Node(_lellips, froze=True)


        self.Name: TextInput = TextInput(text=core_object.Name,
                                        multiline=False,
                                        background_color=(0, 0, 0, 0),
                                        size_hint=(1, 0.4),
                                        pos_hint={"left": 0.1, "top": 1},
                                        foreground_color=(1, 1, 1, 1),
                                        on_text_validate=self.on_change_name)
        if type(core_object) is ChCompound:
            self.Text: TextInput = TextInput(text=str(core_object.Energy),
                                             multiline=False,
                                             size_hint=(1, 0.4),
                                             pos_hint={"left": 0.1, "top": 0.45},
                                             background_color=(0, 0, 0, 0),
                                             foreground_color=(1, 1, 1, 1))
        elif type(core_object) is ChCalculations:
            self.Text: TextInput = TextInput(text=str(core_object.specification),
                                             multiline=False,
                                             size_hint=(1, 0.4),
                                             pos_hint={"left": 0.1, "top": 0.45},
                                             background_color=(0, 0, 0, 0),
                                             foreground_color=(1, 1, 1, 1))
        self.core_object.add_gui(self)
        self.add_widget(self.lellips)
        self.add_widget(self.rellips)
        self.add_widget(self.Text)
        self.add_widget(self.Name)
        self.core_object.save()

    def add_binded_objs(self, binded_obj):
        self._binded_objs.append(binded_obj)

    def bind(self, other, bound):
        self.add_binded_objs(bound)
        other.add_binded_objs(bound)
        if self.pos[0] > other.pos[0]:
            rnode = self.lellips
            lnode = other.rellips
        else:
            rnode = other.lellips
            lnode = self.rellips
        return lnode, rnode

    def is_connectable(self):
        return True

    def get_connector_position(self, touch):
        touch.push()
        touch.apply_transform_2d(self.to_local)
        print(" rellips in:" + str(self.rellips.pos))
        print(" lellips in:" + str(self.lellips.pos))
        print(" Name in   :" + str(self.Name.pos))
        print(" Text in   :" + str(self.Text.pos))
        print(" touch in: " + str(touch.pos))
        print(" width is: " + str(self.width))
        if touch.pos[0] < self.width/2:
            touch.pop()
            print(" return lellips")
            return self.to_parent(*self.lellips.pos)
        else:
            touch.pop()
            print(" return rellips")
            return self.to_parent(*self.rellips.pos)

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
        for binded_obj in self._binded_objs:
            binded_obj.update(touch)



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
