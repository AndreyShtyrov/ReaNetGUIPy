from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.base import Builder
from kivy.app import App


string_for_build ="""
<ErrorMessagePopUp>:
    size_hint: .2, .2
    title: "Message"
    auto_dismiss: False
    BoxLayout:
        orientation: 'horizontal'
        Label:
            id: popup_message
            text: "test"
"""
Builder.load_string(string_for_build)

class CalcRoot(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def run(self):
        popup = ErrorMessagePopUp()
        popup.open()


class ErrorMessagePopUp(Popup):
    popup_message = ObjectProperty()

    def on_touch_down(self, touch):
        if self.collide_point(touch.pos[0], touch.pos[1]):
            y = touch.pos[1]
            if y > self.pos[1] + (self.height * 0.8):
                touch.grab(self)
                print("grab")
            super().on_touch_down(touch)

    def on_touch_move(self, touch):
        if touch.grab_current is self:
            self.pos = touch.pos
            print("move")

    def on_touch_up(self, touch):
        if touch.grab_current is self:
            touch.ungrab(self)
            print("ungrab")


class TestApp(App):
    def build(self):
        test_w = BoxLayout()
        popup = ErrorMessagePopUp()
        popup.open()
        return test_w


if __name__ == '__main__':
    TestApp().run()