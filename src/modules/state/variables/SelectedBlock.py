from dataclasses import dataclass
from modules.state.variables.Variable import Variable
from modules.blockchain.TransactionBlock import TransactionBlock

@dataclass
class SelectedBlock (Variable):
    value: TransactionBlock | None = None

    def get_value(self):
        return super().get_value()

    def set_value(self, new_value):
        super().set_value(new_value)
