import curses
import State
from DiContainer import DiContainer
import modules.view.RenderEngine as RenderEngine
from modules.components.Text import Text
from modules.components.TextBox import TextBox
from modules.view.pages.Page import Page

class ConfirmationPage(Page):

    def __init__(self):
        super().__init__()

    def get_header(self, size):
        return TextBox.get_component(size, 3, 'Are you sure you want to continue 🫵')

    def get_body(self, size):
        text = self.action.get_message()
        if(State.variables.error is not None):
            error_string = State.variables.error
        return Text.get_component(text, size)

    def get_footer(self, size):
        text = 'y: Yes I want to continue 👍\t n: no take me back to the main menu 👎\t z: redo previous action 👈'
        padding = 16
        return TextBox.get_component(size, padding, text, size[0]-3)

    def set_action(self, action):
        self.action = action

    def perform_action(self):
        render_engine:RenderEngine = self.di_container.get_dependency("render_engine")
        option = render_engine.screen.getch()
        State.variables.error = None
        return chr(option) if chr(option) == 'm' or chr(option) == 'q' or chr(option) == 'z' else chr(option)

    def render(self, size):
        self.win = curses.newwin(size[0], size[0], 0, 0)
        return (self.get_header(size), self.get_body(size),self.get_footer(size))