from modules.components.Screen import Screen
from modules.components.TextBox import TextBox
from modules.view.pages.LogIn import LogIn
from modules.view.pages.Page import Page
from modules.view.pages.UserRegistration import UserRegistration
from modules.view.pages.ViewChain import ViewChain

class MainMenu(Page):

    def __init__(self):
        super().__init__()
        self.options = {
            '1': UserRegistration,
            '2': LogIn,
            '3': ViewChain
        }

    def render_header(self, size):
        return TextBox.get_component(size, 2, 'Welcome to the GoodChain').refresh()

    def render_body(self, size):
        text_list = [' 📋 - Register ',' 👤 - Log in ',' 👀 - Look at the chain ' ]
        screen = Screen(text_list, size, 3)
        self.selected_option = screen.run()
        # return Text.get_component(text, size)

    def render_footer(self, size):
        super().render_footer(size)

    def perform_action(self):
        if self.selected_option == 'm' or self.selected_option == 'q':
            return self.selected_option
        return self.options.get(self.selected_option)

    def render(self, size):
        super().render(size)