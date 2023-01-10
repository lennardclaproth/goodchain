from dataclasses import dataclass
from modules.state.variables.Variable import Variable
from modules.user.User import User
from modules.view.pages.Page import Page


@dataclass
class LoggedInUser (Variable):
    value: User | None = None

    def get_value(self):
        return super().get_value()

    def set_value(self, new_value):
        super().set_value(new_value)
