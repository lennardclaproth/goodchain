from dataclasses import dataclass
from modules.state.variables.Variable import Variable
from modules.transaction.Transaction import Transaction

@dataclass
class SelectedTransaction (Variable):
    value: Transaction | None = None

    def get_value(self):
        return super().get_value()

    def set_value(self, new_value):
        super().set_value(new_value)
