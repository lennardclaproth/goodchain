from dataclasses import dataclass
from modules.state.variables.Variable import Variable
from modules.p2pNetwork.messaging.MessageQueue import MessageQueue
@dataclass
class MessageQueue (Variable):
    value: MessageQueue | None = None

    def get_value(self):
        return super().get_value()

    def set_value(self, new_value):
        super().set_value(new_value)
