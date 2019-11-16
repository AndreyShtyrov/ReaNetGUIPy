from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from functools import partial
from kivy.uix.boxlayout import BoxLayout
from Source.CanvasSubstance.Molecule import MolFrame
from kivy.uix.label import Label
from Source.Menu.bubble_menu import MainMenu
from Source.Menu.menu import menu

class MainWidget(Widget):

    def __init__(self):
        super().__init__()
        self.selected_object = None
        self._components = []
        self._bubblmenu = None

    def what_was_clicked(self, touch):
        for component in self._components:
            if bool(component.check_click(touch)):
                return component
        return None

    def new_comp(self):
        new_sub = MolFrame(self)
        self.add_component(new_sub)

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            if touch.button == 'right':
                menu = MainMenu(touch.pos, new=self.new_comp)
                self.add_component(menu)
                self._bubblmenu = menu
                self.add_widget(menu)
            else:
                ud = touch.ud
                ud['label'] = Label(size_hint=(None, None))
                self.update_touch_label(ud['label'], touch)
                self.add_widget(ud['label'])

                self.selected_object = self.what_was_clicked(touch)
                if self.selected_object:
                    self.selected_object.on_touch_down(touch)
                    if touch.is_double_tap and bool(self.selected_object):
                        self.selected_object.double_tap_events(touch)
                        self.selected_object = None
                self.del_menu()

    def del_menu(self):
        if self._bubblmenu is not None:
            self.remove_widget(self._bubblmenu)
            del (self._bubblmenu)
            self._bubblmenu = None


    def update_touch_label(self, label, touch):
        label.text = 'ID: %s\nPos: (%d, %d)\nClass: %s' % (
            touch.id, touch.x, touch.y, touch.__class__.__name__)
        label.texture_update()
        label.pos = touch.pos
        label.size = label.texture_size[0] + 20, label.texture_size[1] + 20


    def on_touch_up(self, touch):
        self.selected_object =None
        ud = touch.ud
        if self.collide_point(*touch.pos):
            self.remove_widget(ud['label'])

    def on_touch_move(self, touch):
        if self.collide_point(*touch.pos):
            if self.selected_object:
                self.selected_object.move(touch)

    def add_component(self, component):
        self._components.append(component)

class MyApp(App):

    def create_new_substance(self, wid: MainWidget, *largs):
        new_sub = MolFrame(wid)



    def build(self):
        wid = MainWidget()
        gmenu = menu
        root = BoxLayout(orientation='vertical')
        layout = BoxLayout(size_hint=(1, None), height=50)
        layout.add_widget(gmenu)
        root.add_widget(layout)
        root.add_widget(wid)
        return root


if __name__ == '__main__':
    MyApp().run()