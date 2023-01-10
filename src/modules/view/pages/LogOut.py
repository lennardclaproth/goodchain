from modules.state.variables.LoggedInUser import LoggedInUser
from modules.components.TextBox import TextBox
from modules.components.Text import Text
from modules.view.pages.Page import Page
from modules.view.pages.SuccessPage import SuccessPage
import State

class LogOut(Page):

    def __init__(self):
        super().__init__()
        self.options = {
            '1':SuccessPage
        }

    def render_header(self, size):
        extra_padding = 3
        text = 'Logging out please wait... 🔨'
        return TextBox.get_component(size, extra_padding, text).refresh()

    def render_body(self, size):
        text = 'Processing...'
        return Text.get_component(text, size)

    def render_footer(self, size):
        super().render_footer(size)

    def perform_action(self):
        State.instance(LoggedInUser).set_value(None)
        return self.options.get('1')

    def render(self, size):
        super().render(size)