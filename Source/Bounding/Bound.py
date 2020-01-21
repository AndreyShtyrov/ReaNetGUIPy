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
                             pos_hint={"x": pos[0], "top": pos[1]})
        else:
            super().__init__(width=dwight,
                             height=dheight,
                             pos=pos)



    def on_touch_down(self, touch):
        print("execute Node.on_touch_down")
        print(" touch pos:" + str(touch.pos))
        print(" self  pos:" + str(self.pos))
        if self.collide_point(touch.pos[0], touch.pos[1]):
            if not self._froze:
                touch.grab(self)
        return False

    def on_touch_move(self, touch):
        if touch.grab_current is self and not self._froze:
            self.pos = touch.pos
            self.parent.update(touch)


    def on_touch_up(self, touch):
        if touch.grab_current is self:
            touch.ungrab(self)
            self._active = False

    def get_pos(self):
        if self._froze:
            return self.parent.to_parent(*self.pos)
        else:
            return tuple(self.pos)

    def compare_lengths(self, pos1, pos2):
        len1 = np.linalg.norm(np.array(pos1) - np.array(self.get_pos()))
        len2 = np.linalg.norm(np.array(pos2) - np.array(self.get_pos()))
        if len1 > len2:
            return True
        else:
            return False

class Bound(FloatLayout):
    transparency = NumericProperty(1.0)
    color = ListProperty([0.8, 0.8, 0.8])
    close = BooleanProperty(False)
    ledt_point = None
    _right_x: int = 0
    _left_x: int = 1000000000
    points = ListProperty()
    nodes = ListProperty()
    linewidth = NumericProperty(1.0)

    def __init__(self, rframe, lframe):
        super().__init__()
        self._radius = 10
        self._limit_range = 15
        lnode, rnode = rframe.bind(lframe, self)
        self.nodes.append(lnode)
        self.nodes.append(rnode)
        self.rebuild()


    def calculate_pos_inserting(self, curr_pos):
        for i in range(1, len(self.nodes)):
            if self.nodes[i-1].compare_lengths(self.nodes[i].get_pos(), curr_pos):
                return i
        return len(self.nodes)

    def add_new_node(self, touch):
        index = self.calculate_pos_inserting(touch.pos)
        node = Node(touch.pos)
        x = node.get_pos()[0]
        self.nodes.insert(index, node)
        self.points.insert(index, Node.pos)
        self.add_widget(node)
        self.rebuild()


    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            print("execute Bound.on_touch_down")
            print(" pos:  " + str(touch.pos))
            if touch.button == "right":
                self.make_menu(touch)
            else:
                super().on_touch_down(touch)


    def _check_that_pos_in_circle(self, pos, center, radius):
        vector1 = np.array(pos)
        vector2 = np.array(center)
        if np.linalg.norm(vector2-vector1) < radius:
            return True
        return False


    def exclude_begin_end_nodes(self, pos):
        if not self._check_that_pos_in_circle(pos, self.points[0], 15):
            if not self._check_that_pos_in_circle(pos, self.points[-1], 15):
                return True
        return False


    def collide_point(self, x, y):
        if self._left_x < x < self._right_x:
            pos = (x, y)
            if self.exclude_begin_end_nodes(pos):
                for i in range(1, len(self.points)):
                    if self.check_is_pos_in_range_of_line(pos, self.points[i], self.points[i - 1]):
                        return True
        return False


    def check_is_pos_in_range_of_line(self, pos, point1, point2):
        if np.abs(point1[0] - point2[0]) < 0.001 and (np.abs(pos[0] - point2[0]) < self._limit_range):
            if point2[1] > point1[1]:
                if point2[1] + self._limit_range > pos[1] > point1[1] - self._limit_range:
                    return True
            else:
                if point1[1] - self._limit_range > pos[1] > point2[1] + self._limit_range:
                    return True
            return False

        y0 = self._calculate_y_by_points_and_x(pos[0], point1, point2)
        if y0 + self._limit_range > pos[1] > y0 - self._limit_range:
            return True
        return False


    def _calculate_y_by_points_and_x(self, x, point1, point2):
        if np.abs(point1[1] - point2[1]) < 0.01:
            return point1[0]
        try:
            y = ((x - point1[0]) / (point2[0] - point1[0])) * (point2[1] - point1[1])
        except ZeroDivisionError:
            print(" It awkwared but here division on zero is " + str((point2[0] - point1[0])))
            exit(1)
        y = y + point1[1]
        return y


    def make_menu(self, touch):
        calls = []
        call = {"name": "New Node", "call": lambda: self.add_new_node(touch)}
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
            x = node.get_pos()[0]
            if x < self._left_x:
                self._left_x = x
            elif x > self._right_x:
                self._right_x = x
            points.append(node.get_pos())
        self.points = points
