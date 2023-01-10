from DiContainer import DiContainer
import State
from modules.state.variables.SelectedBlock import SelectedBlock
from modules.state.variables.ViewStack import ViewStack
from modules.user.context import UserContext
from modules.components.Text import Text
from modules.view.pages.Page import Page
from modules.components.TextBox import TextBox
from modules.components.Screen import Screen
from modules.transaction.Transaction import Transaction
from modules.state.variables.SelectedTransaction import SelectedTransaction

class ViewTransaction(Page):

    def __init__(self):
        super().__init__()

        self.options.update({
            'b': lambda : State.instance(ViewStack).get_value(-1).__class__,
        })

    def render_header(self, size):
        tx : Transaction = State.instance(SelectedTransaction).get_value()
        text = f"Selected transaction: {tx.tx_id} 🚚"
        TextBox.get_component(size, 3, text).refresh()

    def render_body(self, size):
        user_context : UserContext = self.di_container.get_dependency('user_context')
        tx : Transaction = State.instance(SelectedTransaction).get_value()
        tx_repr = ['No inputs and outputs in this transaction. Something went wrong']
        if tx is not None:
            tx_repr = []
            # if tx.tx_id in State.variables.invalid_transactions:
            #     tx_repr.append('INVALID TRANSACTION!')
            tx_repr.append('INPUTS')
            tx_repr.append('------')
            if len(tx.inputs) == 0 and tx.type == 1:
                tx_repr.append('No inputs, this is a mining reward! 🎖 ')
            for pbc, tx_amount in tx.inputs:
                if tx.type == 0:
                    user = user_context.find_user_by_pbc(pbc)
                    tx_repr.append(f"{user.username} -> {tx_amount}")
            tx_repr.append('-------')
            tx_repr.append('OUTPUTS')
            tx_repr.append('-------')
            for pbc, tx_amount in tx.outputs:
                user = user_context.find_user_by_pbc(pbc)
                tx_repr.append(f"{user.username} -> {tx_amount}")
        screen = Screen(tx_repr, size, 3)
        screen.exception_inputs = ['b']
        self.selected_option = screen.run()
        # Text.get_component(tx_string, size).refresh()

    def render_footer(self, size):
        text = 'm: back to main menu 🏡 \t q: quit the GoodChain 🛑 \t b: back to transactions 💸 '
        TextBox.get_component(size, 16, text, size[0] - 3).refresh()

    def perform_action(self):
        if self.selected_option == 'm' or self.selected_option == 'q':
            # State.variables.selected_transaction = None
            State.instance(SelectedTransaction).set_value(None)
            # State.variables.selected_block = None
            State.instance(SelectedBlock).set_value(None)
        if self.selected_option == 'b':
            return self.options.get(self.selected_option)()
        return self.options.get(self.selected_option)

    def render(self, size):
        super().render(size)