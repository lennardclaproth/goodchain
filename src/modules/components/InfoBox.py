import curses
from modules.components.Component import Component
import State
from modules.state.variables.LoggedInUser import LoggedInUser

class InfoBox(Component):
    
    @staticmethod
    def get_component(size, text, grid_cols):
        wallet_balance = State.instance(LoggedInUser).get_value().balance()
        wallet_text = f"Your wallet balance: "
        wallet_balance_text = f" {wallet_balance} 💵"
        pending_actions = len(State.instance(LoggedInUser).get_value().pending_actions)
        pending_actions_text = f"Pending actions: "
        pending_actions_number = f" {pending_actions} 🔔"
        title_size_y = 4
        title_size_x = len(wallet_text + wallet_balance_text)+2
        middle_screen = int(size[1]//12)*grid_cols
        title_box = curses.newwin(title_size_y, title_size_x, 3, middle_screen)
        title_box.box()
        title_box.addstr(1, 1, wallet_text)
        title_box.addstr(1, len(wallet_text), wallet_balance_text, curses.color_pair(1) if wallet_balance >= 0 else curses.color_pair(2))
        title_box.addstr(2, 1, pending_actions_text)
        title_box.addstr(2, len(wallet_text), pending_actions_number, curses.color_pair(1) if pending_actions == 0 else curses.color_pair(2))

        return title_box
