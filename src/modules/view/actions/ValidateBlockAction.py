from modules.p2pNetwork.messaging.MessageQueue import MessageQueue, Task
from modules.state.variables.BlockChain import BlockChain
from modules.state.variables.LoggedInUser import LoggedInUser
from modules.state.variables.SelectedBlock import SelectedBlock
from modules.blockchain.TransactionBlock import TransactionBlock
from modules.view.actions.IAction import IAction
import State

class ValidateBlockAction(IAction):

    def __init__(self, page, di_container):
        super().__init__(page, di_container)

    def handle(self):
        block : TransactionBlock = State.instance(SelectedBlock).get_value()
        if block is None:
            raise ValueError('Block which is None cannot be validated. Please make sure to have selected a block.')
        if State.instance(LoggedInUser).get_value() is None:
            raise ValueError('You need to be logged in to validate a block. Please go back to the main menu and log in.')

        block.validate(State.instance(LoggedInUser).get_value().public_key)
        chain : TransactionBlock = State.instance(BlockChain).get_value()
        self.update_chain(block, chain)
        State.instance(BlockChain).set_value(chain)
        queue : MessageQueue = State.instance(MessageQueue).get_value()
        task = Task(("CLIENT", "BLOCKCHAIN_UPDATE"), chain)
        queue.lock()
        queue.enqueue(task)
        queue.release()
        return self.page.options.get('1')

    def update_chain(self, block: TransactionBlock, chain: TransactionBlock):
        if chain.blockId == block.blockId:
                chain.validated_by = block.validated_by
        if chain.previousBlock is not None:
            return self.update_chain(block, chain.previousBlock)
        return chain
