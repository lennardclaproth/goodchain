from modules.blockchain.ChainHandler import ChainHandler
from modules.state.variables.SelectedTransaction import SelectedTransaction
from modules.state.variables.TransactionPool import TransactionPool
from modules.transaction.PoolHandler import PoolHandler
from modules.blockchain.TransactionBlock import TransactionBlock
from modules.user.User import User
from modules.view.actions.IAction import IAction
from modules.state.variables.LoggedInUser import LoggedInUser
import State

class CancelTransactionAction(IAction):

    # TODO: refactor

    def __init__(self, page, di_container):
        super().__init__(page, di_container)

    def handle(self):
        transaction_list = State.instance(TransactionPool).get_value()
        
        transaction_found = False
        index = 0
        try:
            user : User = State.instance(LoggedInUser).get_value()
            if user is None:
                raise(ValueError('Error occured while trying to cancel a transaction, user cannot be None'))
            for transaction in transaction_list:
                if transaction.tx_id == State.instance(SelectedTransaction).get_value().tx_id:
                    pbc, amt = transaction.inputs[0]
                    if pbc == user.public_key:
                        transaction_found = True
                        transaction_list.pop(index)
                    if pbc is not user.public_key:
                        raise ValueError("Transaction not made by logged in user")
                index = index + 1
            if transaction_found == False:
                raise ValueError("Transaction not in pool")
            State.instance(TransactionPool).set_value(transaction_list)
        except Exception as e:
            raise ValueError(f"Error occurred while trying to cancel transaction nested exception is:\n{e}")
        # if State.instance(LoggedInUser) is not None:
        #     for transaction in transaction_list:
        #         if transaction.tx_id == State.instance()variables.selected_transaction.tx_id:
        #             pbc, amt = transaction.inputs[0]
        #             if pbc == State.variables.logged_in_user.get('public_key'):
        #                 transaction_found = True
        #                 transaction_list.pop(index)
        #         index = index + 1
        # else:
        #     State.variables.error = "You are not logged in, please log in if you want to cancel a transaction."
        #     self.page.options.get('1')
        
        # if transaction_found is False:
        #     State.variables.error = "Transaction is not in pool, if you are in a block you cannot cancel a transaction of that block."
        #     self.page.options.get('1')
        # PoolHandler.save_pool(transaction_list)

        return self.page.options.get('2')
