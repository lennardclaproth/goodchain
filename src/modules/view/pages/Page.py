from ClassLoader import ClassWrapper
import DiContainer
from modules.components.TextBox import TextBox
import State
from modules.state.variables.ViewStack import ViewStack

class Page:

    def __init__(self):
        from modules.view.pages.MainMenu import MainMenu 
        
        self.di_container : DiContainer = State.store.di_container
        self.action = None
        self.options = {
            'm':MainMenu,
            'q':'q',
            'z': lambda : State.instance(ViewStack).get_value().__class__
        }

    def render_header(self, size):
        pass

    def render_body(self, size):
        pass

    def render_footer(self, size):
        text = 'm: back to main menu 🏡 \t q: quit the GoodChain 🛑'
        TextBox.get_component(size, 10, text, size[0] - 3).refresh()

    def perform_action(self):
       pass

    def render(self, size):
        self.render_header(size)
        self.render_footer(size)
        self.render_body(size)