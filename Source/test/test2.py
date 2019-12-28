from kivy.app import App
from kivy.lang import Builder
from kivy.uix.bubble import Bubble
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.floatlayout import FloatLayout

Builder.load_string('''
<main_window_menu>:
    size_hint: (None, None)
    size: (160, 80)
    BubbleButton:
        text: 'New'
        on_press: root.new()
''')


class main_window_menu(Bubble):
    def __init__(self, **kwargs):
        super().__init__()
        self._new = kwargs["new"]

    def new(self):
        self._new()



class Menu(RelativeLayout):

    def __init__(self, pos, **kwargs):
        super().__init__(pos=pos)
        self.show_bubble(**kwargs)

    def show_bubble(self, **kwargs):
        self.bubb = main_window_menu(**kwargs)
        self.add_widget(self.bubb)

    def on_touch_down(self, touch):
        pass


class Frame(FloatLayout):
    def __init__(self):
        super().__init__()

    def on_touch_down(self, touch):
        print(touch.pos)
        if touch.button == 'right':
            menu = Menu(pos=touch.pos, new=self.new_operation)
            self.add_widget(menu)
        else:
            return super(Frame, self).on_touch_down(touch)

    def new_operation(self):
        print("do something")

class MyApp(App):
    def build(self):
        tt = Frame()
        return tt

if __name__ == '__main__':
    MyApp().run()