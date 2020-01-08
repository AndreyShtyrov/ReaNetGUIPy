from kivy.uix.relativelayout import RelativeLayout
from kivy.lang import Builder
from kivy.uix.bubble import Bubble, BubbleButton


Builder.load_string('''
<main_window_menu>:
    size_hint: (None, None)
''')

def decorate_functions(func_to_decorate, add_arg):
    def shell():
        return func_to_decorate(add_arg)
    return shell

class bubbleMenu(Bubble):
    def __init__(self, **kwargs):
        dheight = 80
        dweight = 100
        calls = kwargs["calls"]
        ldweight = len(calls) * dweight
        super().__init__(size=(dheight, ldweight))
        for call in calls:
            # it is need to create lambda function which take 1 argument: self and call delegate
            # otherwise it try to give it to delegate and would fall
            button = BubbleButton(text=call["name"], on_press=lambda x: call["call"]())
            self.add_widget(button)


class bubbleMenuFrame(RelativeLayout):

    def __init__(self, pos, **kwargs):
        dheight = 50
        dweight = 50
        calls = kwargs["calls"]
        ldweight = len(calls) * dweight
        super().__init__(size_hint=(None, None), size=(ldweight, dheight), pos=pos)
        self.show_bubble(**kwargs)

    def show_bubble(self, **kwargs):
        if not hasattr(self, 'bubb'):
            self.bubb = bubb = bubbleMenu(**kwargs)
            self.add_widget(bubb)
        else:
            values = ('left_top')
            index = values.index(self.bubb.arrow_pos)
            self.bubb.arrow_pos = values[(index + 1) % len(values)]
