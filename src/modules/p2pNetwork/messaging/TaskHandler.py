from modules.p2pNetwork.messaging.MessageQueue import Task
from modules.state.variables.BlockChain import BlockChain
from modules.state.variables.TransactionPool import TransactionPool
from modules.user.context import UserContext

import State

class TaskHandler:

    @staticmethod 
    def handle(task : Task):
        task_initiator, task_action = task.action
        match task_action:
            case "SYNC":
                TaskHandler.handle_sync(task)
            case "USER_CREATE":
                TaskHandler.handle_user_create(task)
            case "TRANSACTION_POOL_UPDATE":
                TaskHandler.handle_transaction_pool_update(task)
            case "BLOCKCHAIN_UPDATE":
                TaskHandler.handle_blockchain_update(task)
    
    @staticmethod
    def handle_sync(task: Task):
        pass

    @staticmethod
    def handle_user_create(task: Task):
        user_context : UserContext = State.store.di_container.get_dependency('user_context')
        user_context.insert_user(task.data)

    @staticmethod
    def handle_transaction_pool_update(task: Task):
        if type(task.data) == str:
            State.instance(TransactionPool).set_value([],reset=True)
            return
        State.instance(TransactionPool).set_value(task.data)

    @staticmethod
    def handle_blockchain_update(task: Task):
        State.instance(BlockChain).set_value(task.data)
