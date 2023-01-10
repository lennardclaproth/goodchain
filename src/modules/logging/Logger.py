import State
from modules.state.variables.Logs import Logs
class Logger:

    @staticmethod
    def log(instance, action, message):
        State.instance(Logs).set_value(f'({instance}) - [{action}] - {message}')