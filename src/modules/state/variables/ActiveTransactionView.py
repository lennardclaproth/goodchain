from dataclasses import dataclass, field

from modules.state.variables.Variable import Variable
from modules.transaction.PoolHandler import PoolHandler

import State

@dataclass
class ActiveTransactionView(Variable):
    value = None
    subscriptable = True
    watchers : list = field(default_factory=list)

    def get_value(self):
        return super().get_value()

    def set_value(self, new_value):
        super().set_value(new_value)
        self.dispatch()

    def subscribe(self, class_repr, func):
        self.watchers.append((class_repr, func))

    def dispatch(self):
        for class_repr, func in self.watchers:
            func()
