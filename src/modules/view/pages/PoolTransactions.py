import State
from modules.state.variables.ActiveTransactionView import ActiveTransactionView
from modules.state.variables.SelectedBlock import SelectedBlock
from modules.state.variables.SelectedTransaction import SelectedTransaction
from modules.view.pages.Page import Page
from modules.components.TextBox import TextBox
from modules.components.Screen import Screen
from modules.state.variables.TransactionPool import TransactionPool
from modules.view.pages.ViewTransaction import ViewTransaction

class PoolTransactions(Page):

    def __init__(self):
        super().__init__()

        self.options.update({
            '1': ViewTransaction,
            # 'b': ViewBlock
        })

    def render_header(self, size):
        text = "Pool Transactions 🏊"
        TextBox.get_component(size, 3, text).refresh()

    def render_body(self, size):
        # TODO: refactor
        pool = State.instance(TransactionPool).get_value()
        items = ['No transactions in the transaction pool']
        if len(pool) is not 0:
            items = []
            for tx in range(len(pool)):
                items.append(f' - Tx {tx+1} ({pool[tx].tx_id})')
        screen = Screen(items, size, 3)
        screen.exception_inputs = ['b']
        selected_transaction = screen.run()
        try:
            if selected_transaction is 'm' or selected_transaction is 'q' or selected_transaction is 'b':
                self.selected_option = selected_transaction
            else:
                tx_index = int(selected_transaction) - 1
                State.instance(SelectedTransaction).set_value(pool[tx_index])
                self.selected_option = '1'
        except Exception as e:
            raise ValueError(f'An error occured while trying to parse the index.\nNested exception is: {e}')

    def render_footer(self, size):
        text = 'm: back to main menu 🏡 \t q: quit the GoodChain 🛑'
        if State.instance(ActiveTransactionView).get_value() is 'BlockTransactions':
            text = 'm: back to main menu 🏡 \t q: quit the GoodChain 🛑 \t b: back to block '
        TextBox.get_component(size, 16, text, size[0] - 3).refresh()

    def perform_action(self):
        if self.selected_option == 'm' or self.selected_option == 'q':
            # State.variables.selected_transaction = None
            State.instance(SelectedTransaction).set_value(None)
            # State.variables.selected_block = None
            State.instance(SelectedBlock).set_value(None)
        return self.options.get(self.selected_option)

    def render(self, size):
        super().render(size)
