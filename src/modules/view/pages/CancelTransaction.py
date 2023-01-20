from modules.view.actions.CancelTransactionAction import CancelTransactionAction
from modules.components.TextBox import TextBox
from modules.components.Text import Text
from modules.view.pages.Page import Page
from modules.view.pages.ErrorPage import ErrorPage
from modules.view.pages.SuccessPage import SuccessPage
import State


class CancelTransaction(Page):

    # TODO: refactor

    def __init__(self):
        super().__init__()
        self.action = CancelTransactionAction(self, self.di_container)
        self.options.update({
            '1': ErrorPage,
            '2': SuccessPage
        })

    def render_header(self, size):
        extra_padding = 3
        text = 'Cancelling transaction please wait... 🔨'
        return TextBox.get_component(size, extra_padding, text).refresh()

    def render_body(self, size):
        text = 'Processing...'
        return Text.get_component(text, size)

    def render_footer(self, size):
        super().render_footer(size)

    def perform_action(self):
        # State.variables.update_state()
        self.action.handle()
        return self.options.get('2')

    def render(self, size):
        super().render(size)
