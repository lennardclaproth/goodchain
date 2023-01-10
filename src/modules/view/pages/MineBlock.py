import pickle
from DiContainer import DiContainer
import State
from modules.view.actions.MineBlockAction import MineBlockAction
from modules.components.Text import Text
from modules.view.pages.Page import Page
from modules.components.TextBox import TextBox
from datetime import datetime, timedelta

from modules.view.pages.SuccessPage import SuccessPage

class MineBlock(Page):

    def __init__(self):
        super().__init__()
        self.options.update({
            '1': SuccessPage
        })
        self.reqd = []
        self.time_start = datetime.now()
        self.time_now = datetime.now()

    def render_header(self, size):
        text = 'Mining block, please wait... 🛠'
        return TextBox.get_component(size, 3, text)

    def render_body(self, size):
        text = f'elapsed time: {timedelta(seconds = (self.time_now - self.time_start).total_seconds())}⏳'
        Text.get_component(text, size).refresh()

    def perform_action(self):
        self.time_start = datetime.now()
        action = MineBlockAction(self, self.di_container)
        return action.handle()

    def render(self, size):
        self.size = size
        self.render_header(size)
        self.render_body(size)