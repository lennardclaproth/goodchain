from dataclasses import dataclass, field
from modules.state.variables.Variable import Variable


@dataclass
class Error (Variable):
    value: list = field(default_factory=list)

    def set_value(self, new_value):
        self.value.append(new_value)

    def get_value(self):
        return self.value[-1]
