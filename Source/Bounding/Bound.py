from kivy.properties import OptionProperty, NumericProperty, ListProperty, \
        BooleanProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.lang import Builder
from Source.Menu.bubble_menu import bubbleMenuFrame
import numpy as np

lstring = '''
<Bound>:
    canvas:
        Color:
            rgba: self.color[0], self.color[1], self.color[2],  self.transparency
        Line:
            points: self.points
            width: self.linewidth
            close: self.close
'''
Builder.load_string(lstring)

class Node(FloatLayout):

    def __init__(self, pos, froze=False):
        dwight = 10
        dheight = 10
        self._active = False
        self._froze = froze
        if self._froze:
            super().__init__(size_hint=(0.05, 0.05),
                             pos_hint={"left": pos[0], "top": pos[1]})
        else:
            super().__init__(width=dwight,
                             height=dheight,
                             pos=pos)




    # def on_touch_down(self, touch):
    #     print("execute Node.on_touch_down")
    #     print(" Name:     " + str(self.Name.text))
    #     print(" touch pos:" + str(touch.pos))
    #     print(" self  pos:" + str(self.pos))
    #     if self.collide_point(touch.pos[0], touch.pos[1]):
    #         if touch.button is "right":
    #             self._active = True
    #         if self._active and not self._frozen:
    #             touch.grab(self)
    #     return True
    #
    # def on_touch_move(self, touch):
    #     if touch.grab_current is self:
    #         self.pos = touch.pos
    #     return super().on_touch_move(touch)
    #
    # def on_touch_up(self, touch):
    #     if touch.grab_current is self:
    #         touch.ungrab(self)
    #         self._active = False

    def get_pos(self):
        if self._froze:
            return self.parent.to_parent(*self.pos)
        else:
            return self.pos

    def compare_lengths(self, pos1, pos2):
        len1 = np.linalg.norm(np.array(pos1) - np.array(self.pos))
        len2 = np.linalg.norm(pos2) - np.array(self.pos)
        if len1 > len2:
            return True
        else:
            return False

class Bound(FloatLayout):
    transparency = NumericProperty(1.0)
    color = ListProperty([0.8, 0.8, 0.8])
    close = BooleanProperty(False)
    ledt_point = None
    points = ListProperty()
    nodes = ListProperty()
    linewidth = NumericProperty(1.0)

    def __init__(self, rframe, lframe):
        super().__init__()
        lnode, rnode = rframe.bind(lframe, self)
        self.nodes.append(lnode)
        self.nodes.append(rnode)
        self.rebuild()


    def calculate_pos_inserting(self, curr_pos):
        for i in range(1, len(self.nodes) - 1):
            if self.nodes[i-1].compare_lengths(self.nodes[i].pos, curr_pos):
                return i
        return len(self.nodes) - 1

    def add_new_node(self, touch):
        index = self.calculate_pos_inserting(touch.pos)
        node = Node(touch.pos)
        self.nodes.insert(index, node)
        self.points.insert(index, Node.pos)
        self.parent.add_widget()
        self.rebuild()


    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            print("execute Bound.on_touch_down")
            print(" pos:  " + str(touch.pos))
            if touch.button == "right":
                self.make_menu(touch)

    def make_menu(self, touch):
        calls = []
        call = {"name": "New Node", "call": lambda: self.add_new_node(touch.pos)}
        calls = [call]
        bmenu = bubbleMenuFrame(touch.pos, calls=calls)
        self.parent.add_widget(bmenu)

    def get_node(self, position):
        if position == "begin":
            return self.nodes[0]
        elif position == "end":
            return self.nodes[-1]

    def _check_bounding_order(self):
        if self.nodes[0].pos[0] > self.nodes[-1].pos[0]:
            self.nodes = self.nodes.reverse()
        self.rebuild()

    def update(self, touch):
        self.rebuild()

    def rebuild(self):
        points = []
        for node in self.nodes:
            points.append(node.get_pos())
        self.points = points
