from DiContainer import DiContainer
from modules.view.actions.LogInAction import LogInAction
from modules.components.Input import Input
from modules.components.TextBox import TextBox

from modules.view.pages.Page import Page
from modules.view.pages.SuccessPage import SuccessPage

class LogIn(Page):

    def __init__(self):
        super().__init__()
        self.options.update({
            '1':SuccessPage
        })

    def render_header(self, size):
        extra_padding = 3
        text = 'Logging in please wait... 🔨'
        return TextBox.get_component(size, extra_padding, text)

    def render_body(self, size):
        self.username = Input.get_component("Enter your username", {'height':5, 'width':100, 'y':3, 'x': 1})
        self.password = Input.get_component("Enter your password", {'height':5, 'width':100, 'y':6, 'x': 1})

    def render_footer(self, size):
        super().render_footer(size)

    def perform_action(self):
        log_in_user_action = LogInAction(self, self.di_container)
        return log_in_user_action.handle()

    def render(self, size):
        super().render(size)