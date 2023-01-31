import State
from modules.state.variables.Logs import Logs
from datetime import datetime
class Logger:

    @staticmethod
    def log(instance, action, message):
        State.instance(Logs).set_value(f'({instance}) - [{action}] - {message}')

    @staticmethod
    def load_logs():
        try:
            Logger.create_file()    
        except Exception as e:
            raise ValueError(f'Error while trying to load transaction pool from file.\nNested exception is: {e}')

    @staticmethod
    def create_file():
        with open("data/logs.txt", "w+") as file:
            file.write("")
            file.close()

    @staticmethod
    def save_logs(log):
        now = datetime.now()
        # dd/mm/YY H:M:S
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        with open("data/logs.txt", "a+") as file:
            file.write(f"<{dt_string}> - {log}\n")
            file.close()
