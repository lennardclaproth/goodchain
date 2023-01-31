import pickle
from DiContainer import DiContainer
import State
from modules.blockchain.TransactionBlock import TransactionBlock
from modules.view.actions.InvalidateBlockAction import InvalidateBlockAction
from modules.components.Screen import Screen
from modules.view.pages.Page import Page
from modules.components.TextBox import TextBox
from modules.view.pages.ErrorPage import ErrorPage
from modules.view.pages.SuccessPage import SuccessPage

class InvalidateBlock(Page):

    def __init__(self):
        super().__init__()
        self.action = InvalidateBlockAction(self, self.di_container)
        from modules.view.pages.MainMenu import MainMenu
        self.options.update({
            '1': ErrorPage,
            '2': MainMenu,
            '3': SuccessPage
        })
        self.reqd = []
        self.time_start = None

    def render_header(self, size):
        text = 'The block could not be validated.'
        return TextBox.get_component(size, 3, text)

    def render_body(self, size):
        text_options = [' 👎 - Invalidate block', ' 👈 - back to menu ']
        screen = Screen(text_options, size, 3, 30)
        self.selected_option = screen.run()

    def perform_action(self):
        if self.selected_option == '1':
            return self.action.handle()
        else:
            return self.options.get(self.selected_option)

    def render(self, size):
        super().render(size)
