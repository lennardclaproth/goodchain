from modules.p2pNetwork.messaging.MessageQueue import Task
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
        pass

    @staticmethod
    def handle_blockchain_update(task: Task):
        pass
