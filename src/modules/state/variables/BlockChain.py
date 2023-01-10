from dataclasses import dataclass
from modules.blockchain.ChainHandler import ChainHandler

from modules.state.variables.Variable import Variable

@dataclass
class BlockChain(Variable):
    value = None
    subscriptable = True

    def get_value(self):
        return ChainHandler.load_chain()

    def set_value(self, new_value):
        block_chain = ChainHandler.load_chain()
        block_chain = new_value
        ChainHandler.save_chain(block_chain)
