import State
from DiContainer import DiContainer
from modules.state.variables.ActiveTransactionView import ActiveTransactionView
from modules.state.variables.LoggedInUser import LoggedInUser
import modules.view.RenderEngine as RenderEngine
from modules.components.InfoBox import InfoBox
from modules.components.Screen import Screen
from modules.components.TextBox import TextBox
from modules.view.pages.LogOut import LogOut
from modules.view.pages.NewTransaction import NewTransaction
from modules.view.pages.Page import Page
from modules.view.pages.PoolTransactions import PoolTransactions
from modules.view.pages.ViewChain import ViewChain
from modules.view.pages.MineBlock import MineBlock
from modules.view.pages.PendingActions import PendingActions


class UserMenu(Page):

    def __init__(self):
        super().__init__()
        self.options.update({
            '1': NewTransaction,
            '2': PoolTransactions,
            '3': ViewChain,
            '4': MineBlock,
            '5': PendingActions,
            '6': LogOut
        })

    def render_header(self, size):
        text = f"Welcome to the GoodChain: {State.instance(LoggedInUser).get_value().username}"
        TextBox.get_component(size, 2, text).refresh()

    def render_body(self, size):
        menu_options = [' 🚚 - Transfer coins ', ' 🏊 - Check transaction pool  ', ' 👀 - Look at the chain ', ' 🛠  - Mine block ', ' 😴 - Pending actions ', ' 🚪 - log out ']
        screen = Screen(menu_options, size, 3, 30)
        InfoBox.get_component(size, '', 8).refresh()
        self.selected_option = screen.run()

    def render_footer(self, size):
        super().render_footer(size)

    def perform_action(self):
        return self.options.get(self.selected_option)

    def render(self, size):
        super().render(size)
