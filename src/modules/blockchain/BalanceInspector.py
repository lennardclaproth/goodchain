import State
from modules.blockchain.TransactionBlock import TransactionBlock
from modules.user.User import User
from modules.user.context import UserContext
from 
class BalanceInspector:

    @staticmethod
    def inspect(block, user = None ,pbc = None):
        if user is None:
            user = BalanceInspector.get_user(pbc)

        

    @staticmethod
    def get_transaction_amounts(block : TransactionBlock, user: User):
        transactions = {
            'in': [],
            'out': []
        }
        total_in = 0
        total_out = 0
        for tx in block.data:
            for addr, amt in tx.inputs:
                if addr == user.public_key:
                    total_in = total_in + amt
                elif pbc is None:
                    total_in = total_in + amt
            for addr, amt in tx.outputs:
                if pbc is not None and addr == pbc:
                    total_out = total_out + amt
                elif pbc is None:
                    total_out = total_out + amt
        return total_in, total_out

    @staticmethod
    def get_user(pbc):
        if pbc == None:
            raise ValueError('Error occured while trying to calculate balance. pbc and user cannot be None')
        user_context : UserContext = State.store.di_container.get_dependency('user_context')
        return user_context.find_user_by_pbc(pbc)
        