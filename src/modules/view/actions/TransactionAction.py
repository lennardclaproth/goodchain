from hashlib import sha256
from modules.p2pNetwork.messaging.MessageQueue import MessageQueue, Task
from modules.state.variables.LoggedInUser import LoggedInUser
from modules.state.variables.TransactionPool import TransactionPool
from modules.transaction.PoolHandler import PoolHandler
from modules.transaction.Transaction import Transaction
from modules.view.actions.IAction import IAction
import State
class TransactionAction(IAction):

    def __init__(self, page, di_container):
        super().__init__(page, di_container)

    def add_io(self, tx):
        user_context = self.di_container.get_dependency('user_context')
        user_to = user_context.find_user(self.page.user_out)
        try:
            tx.add_input(State.instance(LoggedInUser).get_value().public_key,float(self.page.transaction_amt) +  float(self.page.transaction_costs))
            tx.add_output(user_to.public_key,float(self.page.transaction_amt))
        except Exception as e:
            raise ValueError(f'Something went wrong while calculating the total amount.\nNested exception is: {e}')

    def add_reqd(self, tx):
        user_context = self.di_container.get_dependency('user_context')
        logged_in_user = State.instance(LoggedInUser).get_value()
        try:
            self.page.reqd = self.page.reqd.split(b',')
            length = len(self.page.reqd)
            if length > 1:
                for reqd in self.page.reqd:
                    reqd_u = user_context.find_user(reqd)
                    tx.add_reqd(reqd_u.public_key)
                tx.sign(logged_in_user.private_key)
                for reqd in self.page.reqd:
                    reqd_u = user_context.find_user(reqd)
                    tx.sign(reqd_u.private_key)
            else:
                tx.sign(logged_in_user.private_key)
        except Exception as e:
            raise ValueError(f'Something went wrong while trying to sign the transaction.\nNested exception is: {e}')
            

    def handle(self):
        tx = Transaction()
        self.add_io(tx)
        self.add_reqd(tx)
        State.instance(TransactionPool).set_value(tx)
        queue : MessageQueue = State.instance(MessageQueue).get_value()
        task = Task(("CLIENT", "TRANSACTION_POOL_UPDATE"), tx)
        queue.lock()
        queue.enqueue(task)
        queue.release()
        return self.page.options.get('1')