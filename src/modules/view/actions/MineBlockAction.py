from modules.blockchain.ChainHandler import ChainHandler
from modules.p2pNetwork.messaging.MessageQueue import MessageQueue, Task
from modules.state.variables.BlockChain import BlockChain
from modules.state.variables.LoggedInUser import LoggedInUser
from modules.state.variables.TransactionPool import TransactionPool
from modules.transaction.PoolHandler import PoolHandler
from modules.blockchain.TransactionBlock import TransactionBlock
from modules.view.actions.IAction import IAction
from datetime import datetime
import State

class MineBlockAction(IAction):

    def __init__(self, page, di_container):
        super().__init__(page, di_container)

    def calc_time_difference(self):
        self.page.time_now = datetime.now()
        self.page.render_body(self.page.size)

# TODO: refactor

    def handle(self):
        transaction_list = PoolHandler.load_pool()
        block_chain : TransactionBlock = ChainHandler.load_chain()
        validated_by_size = 0
        if block_chain is not None:
            validated_by_size = len(block_chain.validated_by)
        if block_chain is not None and validated_by_size >= 3:
            B = TransactionBlock(block_chain)
        elif block_chain is None:
            B = TransactionBlock(None)
        elif block_chain is not None and len(block_chain.validated_by) < 3:
            raise ValueError('The previous block has not been validated yet, this needs to be validated before a new block can be mined.')
            
        for tx in transaction_list:
            B.addTx(tx)

        B.blockHash = B.computeHash()

        # TODO: log invalid transactions on the block
        block_is_valid = B.is_valid(True)
        
        if block_is_valid:
            leading_zeros = 2
            nonce = B.calculate_nonce(leading_zeros)
            while nonce is not True:
                nonce = B.calculate_nonce(leading_zeros, nonce + 1)
                self.calc_time_difference()
            B.mine(State.instance(LoggedInUser).get_value().public_key)
            # transaction_list = []
            # PoolHandler.save_pool(transaction_list)
            State.instance(TransactionPool).set_value([], reset=True)
            queue : MessageQueue = State.instance(MessageQueue).get_value()
            task = Task(("CLIENT", "TRANSACTION_POOL_UPDATE"), "reset")
            queue.lock()
            queue.enqueue(task)
            queue.release()
            # State.variables.update_state()
        else:
            raise ValueError('An error occured while trying to mine the block.')
        State.instance(BlockChain).set_value(B)
        queue : MessageQueue = State.instance(MessageQueue).get_value()
        task = Task(("CLIENT", "BLOCKCHAIN_UPDATE"), B)
        queue.lock()
        queue.enqueue(task)
        queue.release()
        # TODO: Broadcast block to network
        return self.page.options.get('1')
