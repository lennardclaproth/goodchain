import State
from ClassLoader import ClassWrapper
from modules.state.variables.ViewStack import ViewStack
from modules.view.pages.ConfirmationPage import ConfirmationPage
from modules.view.pages.ErrorPage import ErrorPage
from modules.view.pages.Page import Page
from modules.view.pages.MainMenu import MainMenu
from modules.view.pages.SuccessPage import SuccessPage
from modules.view.pages.UserMenu import UserMenu
from modules.state.variables.LoggedInUser import LoggedInUser
from modules.user.User import User


class Loader:

    def __init__(self, stdscr):
        self.screen = stdscr
        self.size = stdscr.getmaxyx()
        self.view_stack = State.store.find(ViewStack).get_instance()

    def prepare_screen(self):
        self.screen.clear()
        self.screen.border(0)
        self.screen.refresh()

    def render_window(self, view):
        view.render(self.size)

    def get_menu(self):
        logged_in_user: User | None = State.store.find(
            LoggedInUser).get_instance().get_value()
        if logged_in_user is not None:
            return State.store.find(UserMenu).get_instance()
        return State.store.find(MainMenu).get_instance()

    def update_view_stack(self, view):
        if view.__class__ == ErrorPage or view.__class__ == SuccessPage or view.__class__ == ConfirmationPage:
            return
        self.view_stack.set_value(view)

    def load(self, view):
        if view is 'q':
            return view
        wrapper: ClassWrapper = State.store.find(view)
        view = wrapper.get_instance()

        if view.__class__ == MainMenu:
            view = self.get_menu()
        self.prepare_screen()
        self.update_view_stack(view)
        view.render(self.size)
        return view.perform_action()
