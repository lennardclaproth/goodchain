from dataclasses import dataclass


from modules.state.variables.Variable import Variable
from modules.transaction.PoolHandler import PoolHandler

@dataclass
class Logs(Variable):
    value = None
    subscriptable = True

    def get_value(self):
        from modules.p2pNetwork.Logging import Logger
        return Logger.load_logs()

    def set_value(self, new_value):
        from modules.p2pNetwork.Logging import Logger
        Logger.save_logs(new_value)
