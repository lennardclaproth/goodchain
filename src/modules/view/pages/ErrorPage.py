import curses
import State
from modules.state.variables.Error import Error
import modules.view.RenderEngine as RenderEngine
from modules.components.Text import Text
from modules.components.TextBox import TextBox
from modules.view.pages.Page import Page

class ErrorPage(Page):

    def __init__(self):
        super().__init__()

    def render_header(self, size):
        TextBox.get_component(size, 3, 'An error occured 😥').refresh()

    def render_body(self, size):
        error_string = str(State.instance(Error).get_value())
        Text.get_component(error_string, size).refresh()

    def render_footer(self, size):
        text = 'm: back to main menu 🏡 \t q: quit the GoodChain 🛑'
        padding = 10
        # TODO: refactor
        text = 'm: back to main menu 🏡 \t q: quit the GoodChain 🛑 \t z: redo previous action 👈'
        padding = 16
        TextBox.get_component(size, padding, text, size[0]-3).refresh()

    def perform_action(self):
        render_engine:RenderEngine = self.di_container.get_dependency("render_engine")
        option = render_engine.screen.getch()
        options_chr = chr(option)
        if options_chr == 'z':
            return self.options.get(options_chr)()
        return self.options.get(chr(option))

    def render(self, size):
        super().render(size)