from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput
from kivy.uix.relativelayout import RelativeLayout
from kivy.app import App
from kivy.uix.widget import Widget

class Node(FloatLayout):

    def __init__(self, pos, froze=False):
        dwight = 10
        dheight = 10
        self._active = False
        self._froze = froze
        super().__init__(size_hint=(0.05, 0.05),
                             pos_hint={"left": pos[0], "top": pos[1]})

class MyCustomRL(RelativeLayout):
    def __init__(self, **kwargs):
        pos = kwargs["pos"]
        super().__init__(size_hint=(None, None), width=130, height=80, pos=pos)

        _rellips = (0.95, 0.5)
        _lellips = (0.05, 0.5)
        self.rellips = Node(_rellips, froze=True)
        self.lellips = Node(_lellips, froze=True)


        self.Name: TextInput = TextInput(text="New",
                                        multiline=False,
                                        background_color=(0, 0, 0, 0),
                                        size_hint=(1, 0.4),
                                        pos_hint={"x": 0.1, "top": 0.9},
                                        foreground_color=(1, 1, 1, 1),
                                        )
        self.Text: TextInput = TextInput(text="Text",
                                             multiline=False,
                                             size_hint=(1, 0.4),
                                             pos_hint={"x": 0.1, "top": 0.4},
                                             background_color=(0, 0, 0, 0),
                                             foreground_color=(1, 1, 1, 1))

        self.add_widget(self.lellips)
        self.add_widget(self.rellips)
        self.add_widget(self.Text)
        self.add_widget(self.Name)

class Test_Widget(Widget):

    def __init__(self, test_frame):
        super().__init__()
        self.test_frame = test_frame
        self.add_widget(test_frame)


    def on_touch_down(self, touch):
        print("Name :" + str(self.test_frame.Name.pos))
        print("Text :" + str(self.test_frame.Text.pos))
        print("rellips:" + str(self.test_frame.rellips.pos))
        print("lellips:" + str(self.test_frame.lellips.pos))

class TestLineApp(App):
    def build(self):

        test_frame = MyCustomRL(pos=(200, 200))
        wid = Test_Widget(test_frame)

        return wid


if __name__ == '__main__':
    TestLineApp().run()
