from kivy.app import App
from kivy.lang import Builder

menu = Builder.load_string('''
ActionBar:
    pos_hint: {'top':1}
    ActionView:
        use_separator: True
        ActionPrevious:
            title: 'Example App'
            with_previous: False
        ActionButton:
            text: 'File'
        ActionButton:
            text: 'Edit'
        ActionGroup:
            text: 'Tools' 
            mode: 'spinner'
            ActionButton:
                text: 'Tool1'
            ActionButton:
                text: 'Tool2'
            ActionButton:
                text: 'Tool3'
            ActionButton:
                text: 'Tool4'
''')

class ExampleApp(App):
    def build(self):
        return menu



if __name__ =='__main__':
    ExampleApp().run()

