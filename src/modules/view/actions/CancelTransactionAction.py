from modules.blockchain.ChainHandler import ChainHandler
from modules.transaction.PoolHandler import PoolHandler
from modules.blockchain.TransactionBlock import TransactionBlock
from modules.view.actions.IAction import IAction
import State

class CancelTransactionAction(IAction):

    def __init__(self, page, di_container):
        super().__init__(page, di_container)

    def handle(self):
        transaction_list = PoolHandler.load_pool()
        
        transaction_found = False
        index = 0
        if State.variables.logged_in_user is not None:
            for transaction in transaction_list:
                if transaction.tx_id == State.variables.selected_transaction.tx_id:
                    pbc, amt = transaction.inputs[0]
                    if pbc == State.variables.logged_in_user.get('public_key'):
                        transaction_found = True
                        transaction_list.pop(index)
                index = index + 1
        else:
            State.variables.error = "You are not logged in, please log in if you want to cancel a transaction."
            self.page.options.get('1')
        
        if transaction_found is False:
            State.variables.error = "Transaction is not in pool, if you are in a block you cannot cancel a transaction of that block."
            self.page.options.get('1')
        PoolHandler.save_pool(transaction_list)

        return self.page.options.get('2')
