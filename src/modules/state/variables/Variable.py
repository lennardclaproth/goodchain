from dataclasses import dataclass
import State

@dataclass
class Variable:
    value = None
    subscriptable = False

    def get_value(self):
        return self.value

    def set_value(self, new_value):
        self.value = new_value
        # State.store.update()
