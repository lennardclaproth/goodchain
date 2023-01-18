from dataclasses import dataclass

from modules.state.variables.Variable import Variable
from modules.transaction.PoolHandler import PoolHandler

@dataclass
class TransactionPool(Variable):
    value = None
    subscriptable = True

    def get_value(self):
        return PoolHandler.load_pool()

    def set_value(self, new_value, reset = False):
        if reset:
            PoolHandler.save_pool([])
        else:
            transaction_pool = PoolHandler.load_pool()
            transaction_pool.append(new_value)
            PoolHandler.save_pool(transaction_pool)

