from kivy.properties import OptionProperty, NumericProperty, ListProperty, \
        BooleanProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.lang import Builder
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
        self._frozen = froze
        super(FloatLayout, self).__init__(width=dwight, height=dheight, pos=pos)

    def on_touch_down(self, touch):
        print("execute Node.on_touch_down")
        print(" Name:     " + str(self.Name.text))
        print(" touch pos:" + str(touch.pos))
        print(" self  pos:" + str(self.pos))
        if self.collide_point(touch.pos[0], touch.pos[1]):
            if touch.button is "right":
                self._active = True
            if self._active and not self._frozen:
                touch.grab(self)
        return True

    def on_touch_move(self, touch):
        if touch.grab_current is self:
            self.pos = touch.pos

    def on_touch_up(self, touch):
        if touch.grab_current is self:
            touch.ungrab(self)
            self._active = False

    def get_pos(self):
        return np.array(list(self.pos))

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
        if lframe.pos[0] < rframe.pos[0]:
            rnode_pos = rframe.lellips
            lnode_pos = lframe.rellips
        else:
            rnode_pos = lframe.lellips
            lnode_pos = rframe.rellips
        self.nodes.append(Node(rnode_pos, True))
        self.nodes.append(Node(lnode_pos, True))
        self.points.append(rnode_pos)
        self.points.append(lnode_pos)

    def calculate_pos_inserting(self, curr_pos):
        for i in range(1, len(self.nodes) - 1):
            if self.nodes[i-1].compare_lengths(self.nodes[i].pos, curr_pos):
                return i
        return len(self.nodes) - 1

    def add_new_node(self, touch):
        index = self.calculate_pos_inserting(touch.pos)
        self.nodes.insert(Node(touch.pos), index)

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            print("execute Bound.on_touch_down")
            print(" pos:  " + str(touch.pos))
            pass

    def make_menu(self):
        pass