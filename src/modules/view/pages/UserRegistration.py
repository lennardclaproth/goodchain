import curses
from encodings import utf_8
import State
from DiContainer import DiContainer
from modules.user.context import UserContext
import modules.view.RenderEngine as RenderEngine
from modules.view.actions.RegisterAction import RegisterAction
from modules.components.Input import Input
from modules.components.Text import Text
from modules.components.TextBox import TextBox
from modules.view.pages.Page import Page
from modules.view.pages.SuccessPage import SuccessPage


class UserRegistration(Page):

    def __init__(self):
        super().__init__()
        self.options.update ({
            '1':SuccessPage
        })
        self.action = RegisterAction(self, self.di_container)

    def render_header(self, size):
        text = 'Processing request please wait... 🔨'
        TextBox.get_component(size, 3, text).refresh()

    def render_body(self, size):
        self.username = Input.get_component("Enter the username you want to use", {'height':5, 'width':100, 'y':3, 'x': 1})
        self.password = Input.get_component("Enter the password you want to use", {'height':5, 'width':100, 'y':6, 'x': 1})
        self.password_confirm = Input.get_component("Please reenter the password to confirm", {'height':5, 'width':100, 'y':9, 'x': 1})

    def perform_action(self):
        return self.action.handle()

    def render(self, size):
        self.render_body(size)
        self.render_header(size)