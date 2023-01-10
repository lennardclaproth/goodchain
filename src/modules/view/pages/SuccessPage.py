import modules.view.RenderEngine as RenderEngine
from modules.components.Text import Text
from modules.components.TextBox import TextBox
from modules.view.pages.Page import Page


class SuccessPage(Page):

    def __init__(self):
        super().__init__()

    def render_header(self, size):
        text = 'Succesfully handled your request 🎊'
        TextBox.get_component(size, 3, text).refresh()

    def render_body(self, size):
        text = 'Successfully handled your request.If you press m you will be automatically redirected to the main menu.'
        Text.get_component(text, size).refresh()

    def render_footer(self, size):
        text = 'm: back to main menu 🏡 \t q: quit the GoodChain 🛑'
        TextBox.get_component(size, 10, text, size[0]-3).refresh()

    def perform_action(self):
        render_engine: RenderEngine = self.di_container.get_dependency(
            "render_engine")
        option = render_engine.screen.getch()
        return self.options.get(chr(option))

    def render(self, size):
        super().render(size)
