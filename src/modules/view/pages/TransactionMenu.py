from modules.components.Screen import Screen
from modules.components.TextBox import TextBox
from DiContainer import DiContainer
from modules.state.variables.SelectedTransaction import SelectedTransaction
from modules.view.pages.CancelTransaction import CancelTransaction
from modules.view.pages.Page import Page
from modules.blockchain.ChainHandler import ChainHandler
import State
from modules.view.pages.ViewTransaction import ViewTransaction

class TransactionMenu(Page):

    def __init__(self):
        super().__init__()
        self.options = {
            '1':ViewTransaction,
            '2':CancelTransaction,
        }

    def render_header(self, size):
        return TextBox.get_component(size, 3, f'Selected transaction: {State.instance(SelectedTransaction).get_value().tx_id}').refresh()

    def render_body(self, size):
        text_list = [' 👀 - View transaction ',' 💸 - Cancel transaction ']
        screen = Screen(text_list, size, 3)
        self.selected_option = screen.run()
        # return Text.get_component(text, size)

    def render_footer(self, size):
        super().render_footer(size)

    def perform_action(self):
        if self.selected_option == 'm' or self.selected_option == 'q':
            return self.selected_option
        # State.variables.selected_block = ChainHandler.load_chain()
        return self.options.get(self.selected_option)

    def render(self, size):
        super().render(size)