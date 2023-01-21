from modules.blockchain.TransactionBlock import TransactionBlock
from modules.p2pNetwork.messaging.MessageQueue import MessageQueue, Task
from modules.p2pNetwork.messaging.TaskHandler import TaskHandler
from modules.state.variables.BlockChain import BlockChain
from modules.state.variables.LoggedInUser import LoggedInUser
from modules.state.variables.SelectedBlock import SelectedBlock
from modules.state.variables.TransactionPool import TransactionPool
from modules.user.context import UserContext
from modules.view.actions.IAction import IAction
from modules.blockchain.ChainHandler import ChainHandler
from modules.transaction.PoolHandler import PoolHandler
import State

class InvalidateBlockAction(IAction):

    # TODO: refactor

    def __init__(self, page, di_container):
        super().__init__(page, di_container)

    def handle(self):
        chain : TransactionBlock = State.instance(BlockChain).get_value()
        user = State.instance(LoggedInUser).get_value()
        try:
            if user is not None:
                if State.instance(SelectedBlock).get_value().blockId == chain.blockId:
                    for transaction in State.instance(SelectedBlock).get_value().data:
                        State.instance(TransactionPool).set_value(transaction)
                    queue : MessageQueue = State.instance(MessageQueue).get_value()
                    task = Task(("CLIENT", "TRANSACTION_POOL_UPDATE"), State.instance(TransactionPool).get_value())
                    queue.lock()
                    queue.enqueue(task)
                    queue.release()
                    State.instance(BlockChain).set_value(chain.previousBlock)
                    task = Task(("CLIENT", "BLOCKCHAIN_UPDATE"), chain)
                    queue.lock()
                    queue.enqueue(task)
                    queue.release()
                    return self.page.options.get('3')
                else:
                    raise ValueError("Failed to invalidate block. This block has already been mined and validated by three or more users.")
            else:
                raise ValueError("You are not logged in, log in first if you want to validate a block.")
        except Exception as e:
            raise ValueError(f"An exception occured while invalidating the block. Nested exception is:\n{e}")