from modules.blockchain.ChainHandler import ChainHandler
from modules.p2pNetwork.messaging.MessageQueue import MessageQueue, Task
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
                    if pbc != user.public_key:
                        raise ValueError("Transaction not made by logged in user")
                index = index + 1
            if transaction_found == False:
                raise ValueError("Transaction not in pool")
            State.instance(TransactionPool).set_value(transaction_list)
            queue : MessageQueue = State.instance(MessageQueue).get_value()
            task = Task(("CLIENT", "TRANSACTION_POOL_UPDATE"), transaction_list)
            queue.lock()
            queue.enqueue(task)
            queue.release()
        except Exception as e:
            raise ValueError(f"Error occurred while trying to cancel transaction nested exception is:\n{e}")

        return self.page.options.get('2')
