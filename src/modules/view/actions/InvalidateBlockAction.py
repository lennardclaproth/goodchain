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
        chain = ChainHandler.load_chain()
        pool = PoolHandler.load_pool()
        if State.variables.logged_in_user is not None:
            if State.variables.selected_block.blockId == chain.blockId:
                for transaction in State.variables.selected_block.data:
                    pool.append(transaction)
                ChainHandler.save_chain(chain.previousBlock)
                PoolHandler.save_pool(pool)
                State.variables.update_state()
                return self.page.options.get('3')
            else:
                State.variables.error = "Failed to invalidate block. This block has already been mined and validated by three or more users."
                return self.page.options.get('1')
        else:
            State.variables.error = "You are not logged in, log in first if you want to validate a block."
            return self.page.options.get('1')