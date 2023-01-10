import State
from modules.components.Screen import Screen
from modules.components.TextBox import TextBox
from DiContainer import DiContainer
from modules.state.variables.BlockChain import BlockChain
from modules.state.variables.SelectedBlock import SelectedBlock
from modules.view.pages.Page import Page
from modules.view.pages.BlockTransactions import BlockTransactions
from modules.view.pages.ValidateBlock import ValidateBlock

class ViewBlock(Page):

    def __init__(self):
        super().__init__()

        from modules.view.pages.ViewChain import ViewChain

        self.options.update({
            '1': BlockTransactions,
            '2': ValidateBlock,
            # '3':'balance_check',
            'b': ViewChain
        })

    def render_header(self, size):
        selected_block = State.instance(SelectedBlock).get_value()
        if selected_block is not None:
            return TextBox.get_component(size, 3, f'Block: {selected_block.blockId}').refresh()
        else:
            raise ValueError('No block selected.')

    def render_body(self, size):
        text_list = [' 🚚 - View transactions ',' 👌 - Validate block ',' 👀 - Check balance when this block was mined ' ]
        screen = Screen(text_list, size, 3)
        screen.exception_inputs = ['b']
        self.selected_option = screen.run()

    def render_footer(self, size):
        text = 'm: back to main menu 🏡 \t q: quit the GoodChain 🛑'
        if State.instance(BlockChain).get_value() is not None:
            text = 'm: back to main menu 🏡 \t q: quit the GoodChain 🛑 \t b: back to chain '
        TextBox.get_component(size, 16, text, size[0] - 3).refresh()

    def perform_action(self):
        # if self.selected_option == 'm' or self.selected_option == 'q':
            # State.variables.selected_transaction = None
            # State.variables.selected_block = None
            # return self.selected_option
        return self.options.get(self.selected_option)

    def render(self, size):
        super().render(size)