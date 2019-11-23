import logging
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from functools import partial
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from Source.CanvasSubstance.Molecule import MolFrame
from kivy.uix.label import Label
from Source.Menu.bubble_menu import MainMenu
from Source.Menu.menu import menu
from kivy.graphics import Line
from kivy.config import Config
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')

class MainWidget(Widget):

    def __init__(self):
        super().__init__()
        self.selected_object = None
        self._components = []
        self._bubblmenu = None
        self._update_per_move = []
        self.log = logging.getLogger("MainWindow")

    def what_was_clicked(self, touch):
        for component in self._components:
            if bool(component.check_click(touch)):
                print(str(component))
                return component
        return None

    def new_comp(self, touch):
        new_sub = MolFrame(x=touch.pos[0], y=touch.pos[1])
        self.add_component(new_sub)
        self.add_widget(new_sub)

    def on_touch_down(self, touch):
        def decor_functions(func_todecorate, add_arg):
            def shell():
                return func_todecorate(add_arg)

            return shell
        ud = touch.ud
        ud['label'] = Label(size_hint=(None, None))
        self.update_touch_label(ud['label'], touch)
        self.add_widget(ud['label'])
        super().on_touch_down(touch)
        if self.collide_point(*touch.pos):
            if touch.button == 'right':
                clicked_obj = self.what_was_clicked(touch)
                if clicked_obj is None:
                    clicked_obj = "MainWindow"
                    new_comp = decor_functions(self.new_comp, touch)
                    menu = MainMenu(touch.pos, clicked_obj=clicked_obj, new=new_comp)
                else:
                    clicked_obj_name = type(clicked_obj).__name__
                    newbond = decor_functions(self.newBond, clicked_obj)
                    delFrame = decor_functions(self.delFrame, clicked_obj)
                    copyFrame = decor_functions(self.copyFrame, clicked_obj)
                    menu = MainMenu(touch.pos, clicked_obj= clicked_obj_name, newbond=newbond, delFrame=delFrame,
                                    copyFrame=copyFrame)
                self.add_component(menu)
                self._bubblmenu = menu
                self.add_widget(menu)

    def on_touch_up(self, touch):
        self.selected_object =None
        ud = touch.ud
        if self.collide_point(*touch.pos):
            self.remove_widget(ud['label'])
        super().on_touch_move(touch)

    def on_touch_move(self, touch):
        super().on_touch_move(touch)
        for redrawing in self._update_per_move:
            points = [touch.pos[0], touch.pos[1], redrawing.start_x, redrawing.start_y]
            redrawing.points = points

    def del_menu(self):
        if self._bubblmenu is not None:
            obj = self._bubblmenu
            self._components.remove(obj)
            self.remove_widget(self._bubblmenu)
            self._bubblmenu = None
            del (obj)

    def createbond(self, obj, ellips):
        points = [ellips.pos[0],ellips.pos[1], ellips.pos[0],ellips.pos[1]]
        bond_pred = Line(points=points)
        bond_pred.start_x = ellips.pos[0]
        bond_pred.start_y = ellips.pos[1]
        self._update_per_move.append(bond_pred)
        self.canvas.add(bond_pred)

    def newBond(self, clicked_obj: MolFrame):
        clicked_obj.show_bonds_marks()

    def delFrame(self, clicked_obj):
        ind = self._components.remove(clicked_obj)
        clicked_obj.remove_widget()
        del(clicked_obj)

    def copyFrame(self, clicked_ojb):
        pass
        # new_el = clicked_ojb.copy()
        # self.add_component(new_el)
        # self.add_widget(new_el)

    def update_touch_label(self, label, touch):
        label.text = 'ID: %s\nPos: (%d, %d)\nClass: %s' % (
            touch.id, touch.x, touch.y, touch.__class__.__name__)
        label.texture_update()
        label.pos = touch.pos
        label.size = label.texture_size[0] + 20, label.texture_size[1] + 20

    def add_component(self, component):
        self._components.append(component)

class MyApp(App):

    def build(self):
        wid = MainWidget()
        root = BoxLayout(orientation='vertical')
        gmenu = menu
        layout = BoxLayout(size_hint=(1, None), height=50)
        layout.add_widget(gmenu)
        root.add_widget(layout)
        root.add_widget(wid)
        return root


if __name__ == '__main__':
    MyApp().run()