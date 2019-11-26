from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.lang import Builder
from kivy.uix.bubble import Bubble
from kivy.uix.widget import Widget

Builder.load_string('''
<main_window_menu>:
    size_hint: (None, None)
    size: (160, 80)
    pos_hint: {'center_x': .5, 'y': .3}
    BubbleButton:
        text: 'New'
        on_press: root.new()

''')

class main_window_menu(Bubble):
    def __init__(self, **kwargs):
        super().__init__(pos=kwargs.pop("pos"))
        self._new = kwargs["new"]


    def new(self):
        self._new()

class Menu(FloatLayout):

    def __init__(self, **kwargs):
        super().__init__()
        self.show_bubble(**kwargs)

    def show_bubble(self, **kwargs):
        self.bubb = main_window_menu(**kwargs)
        self.add_widget(self.bubb)

    def on_touch_down(self, touch):
        self.bubb.on_touch_down(touch)

class Frame(Widget):
    def __init__(self):
        super().__init__()

    def on_touch_down(self, touch):
        print(touch.pos)
        super().on_touch_down(touch)
        print(touch.pos)
        for child in self.children:
            if type(child) is main_window_menu:
                self.remove_widget(child)
        if touch.button == 'right':
            menu = main_window_menu(pos=touch.pos, new=self.new_operation)
            self.add_widget(menu)


    def new_operation(self):
        pass

class MyApp(App):
    def build(self):
        tt = Frame()
        return tt

if __name__ == '__main__':
    MyApp().run()