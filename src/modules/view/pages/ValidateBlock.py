from modules.view.actions.ValidateBlockAction import ValidateBlockAction
from modules.components.Text import Text
from modules.view.pages.InvalidateBlock import InvalidateBlock
from modules.view.pages.Page import Page
from modules.components.TextBox import TextBox
from modules.view.pages.SuccessPage import SuccessPage


class ValidateBlock(Page):

    def __init__(self):
        super().__init__()
        self.options = {
            '1': SuccessPage,
        }
        self.reqd = []
        self.time_start = None

    def render_header(self, size):
        text = 'Validating block, please wait... 🛠'
        return TextBox.get_component(size, 3, text)

    def render_body(self, size):
        text = 'processing'
        Text.get_component(text, size).refresh()

    def perform_action(self):
        action = ValidateBlockAction(self, self.di_container)
        return action.handle()

    def render(self, size):
        super().render(size)
