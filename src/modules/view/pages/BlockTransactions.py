import State
from modules.blockchain.TransactionBlock import TransactionBlock
from modules.state.variables.ActiveTransactionView import ActiveTransactionView
from modules.state.variables.SelectedBlock import SelectedBlock
from modules.state.variables.SelectedTransaction import SelectedTransaction
from modules.view.pages.Page import Page
from modules.components.TextBox import TextBox
from modules.components.Screen import Screen
from modules.state.variables.TransactionPool import TransactionPool
from modules.view.pages.ViewTransaction import ViewTransaction

class BlockTransactions(Page):

    def __init__(self):
        super().__init__()

        from modules.view.pages.ViewBlock import ViewBlock

        self.options.update({
            '1': ViewTransaction,
            'b': ViewBlock
        })

    def render_header(self, size):
        text = f"Block Transactions ({State.instance(SelectedBlock).get_value().blockId}) 💸"
        TextBox.get_component(size, 3, text).refresh()

    def render_body(self, size):
        # TODO: refactor
        block : TransactionBlock = State.instance(SelectedBlock).get_value()
        transactions = block.data
        if len(transactions) is not 0:
            items = []
            for index in range(len(transactions)):
                items.append(f' - Tx {index+1} ({transactions[index].tx_id}) ')
        screen = Screen(items, size, 3)
        screen.exception_inputs = ['b']
        selected_transaction = screen.run()
        try:
            if selected_transaction is 'm' or selected_transaction is 'q' or selected_transaction is 'b':
                self.selected_option = selected_transaction
            else:
                tx_index = int(selected_transaction) - 1
                State.instance(SelectedTransaction).set_value(transactions[tx_index])
                self.selected_option = '1'
        except Exception as e:
            raise ValueError(f'An error occured while trying to parse the index.\nNested exception is: {e}')

    def render_footer(self, size):
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
