import State
from modules.state.variables.BlockChain import BlockChain
from modules.view.pages.Page import Page
from modules.components.TextBox import TextBox
from modules.components.Screen import Screen
from modules.blockchain.ChainHandler import ChainHandler
from modules.blockchain.TransactionBlock import TransactionBlock
from modules.view.pages.ViewBlock import ViewBlock
from modules.state.variables.SelectedBlock import SelectedBlock
class ViewChain(Page):

    def __init__(self):
        super().__init__()
        self.options.update({
            '1': ViewBlock,
        })

    def render_header(self, size):
        text = "The chain"
        TextBox.get_component(size, 3, text).refresh()

    def render_body(self, size):
        chain = State.instance(BlockChain).get_value()
        items = ['No genesis block created yet']
        if chain is not None:
            chain_arr = []
            items = []
            while chain.previousBlock is not None:
                chain_arr.append(chain)
                chain = chain.previousBlock
            chain_arr.append(chain)
            chain_arr = chain_arr[::-1]
            for i in range(len(chain_arr)):
                if chain_arr[i].previousBlock != None:
                    items.append(f' - Block {i} ({chain_arr[i].blockId})')
                else:
                    items.append(f' - Genesis block ({chain_arr[i].blockId})')
        screen = Screen(items, size, 3)
        selected_transaction = screen.run()
        try:
            if selected_transaction is 'm' or selected_transaction is 'q':
                self.selected_option = selected_transaction
            else:
                block_index = int(selected_transaction) - 1
                State.instance(SelectedBlock).set_value(chain_arr[block_index])
                self.selected_option = '1'
        except Exception as e:
            raise ValueError(f'Error occured while trying to parse the index of the selected transaction\nNested exception is: {e}')

    def render_footer(self, size):
       super().render_footer(size)

    def perform_action(self):
        if self.selected_option == 'm' or self.selected_option == 'q':
            a = False
        return self.options.get(self.selected_option)

    def render(self, size):
        super().render(size)