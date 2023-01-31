from modules.components.Screen import Screen
from modules.components.TextBox import TextBox
from DiContainer import DiContainer
from modules.state.variables.SelectedBlock import SelectedBlock
from modules.view.pages.CancelTransaction import CancelTransaction
from modules.view.pages.Page import Page
from modules.blockchain.ChainHandler import ChainHandler
import State
from modules.view.pages.ValidateBlock import ValidateBlock
from modules.view.pages.BlockTransactions import BlockTransactions
from modules.state.variables.BlockChain import BlockChain
class PendingActions(Page):

    def __init__(self):
        super().__init__()
        self.options = {
            '1':ValidateBlock,
            '2':CancelTransaction,
        }

    def render_header(self, size):
        return TextBox.get_component(size, 4, 'Pending actions 🔔').refresh()

    def render_body(self, size):
        text_list = [' 👍 - validate block ',' 💸 - cancel transaction ']
        screen = Screen(text_list, size, 3)
        self.selected_option = screen.run()
        # return Text.get_component(text, size)

    def render_footer(self, size):
        super().render_footer(size)

    def perform_action(self):
        if self.selected_option == 'm' or self.selected_option == 'q':
            return self.options.get(self.selected_option)
        State.instance(SelectedBlock).set_value(State.instance(BlockChain).get_value())
        return self.options.get(self.selected_option)

    def render(self, size):
        super().render(size)