from dataclasses import dataclass
from modules.state.variables.Variable import Variable
from modules.server.Server import Server

@dataclass
class Server (Variable):
    value: Server | None = None

    def get_value(self):
        return super().get_value()

    def set_value(self, new_value):
        super().set_value(new_value)
