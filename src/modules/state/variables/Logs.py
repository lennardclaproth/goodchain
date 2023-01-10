from dataclasses import dataclass, field
from modules.state.variables.Variable import Variable

@dataclass
class Logs(Variable):

    value: list = field(default_factory=list)

    def get_value(self, shift=0):
        if shift != 0:
            return self.value[len(self.value)-1+shift]
        return self.value[-1]

    def set_value(self, new_value):
        self.value.append(new_value)
