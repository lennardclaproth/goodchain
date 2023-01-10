from hashlib import sha256
from modules.blockchain.TransactionBlock import TransactionBlock
from modules.view.actions.IAction import IAction
from modules.state.variables.LoggedInUser import LoggedInUser
import State

class LogInAction(IAction):

    def __init__(self, page, di_container):
        super().__init__(page, di_container)

    def validate_password(self, user):
        password_sha = sha256(self.page.password).hexdigest()
        if password_sha == user.password:
            State.instance(LoggedInUser).set_value(user)
            return True
        return False

    # def update_state(self, user):
    #     State.instance(LoggedInUser).set_value(user)
    #     chain : TransactionBlock = State.variables.chain
    #     if chain is not None:
    #         State.variables.balance = chain.get_balance()
    #     else:
    #         State.variables.balance = 50.0
    #     pass

    def handle(self):
        try: 
            user = self.di_container.get_dependency('user_context').find_user(self.page.username)
            if user is None:
                raise ValueError('This user does not exist')
            if self.validate_password(user):
                # State.variables.invalid_transactions = []
                # State.variables.pending_actions = []
                # State.variables.update_state()
                return self.page.options.get('1')
            else:
                raise ValueError('Password does not match')
        except Exception as e:
            raise ValueError(f'A error occured while logging in.\nNested exception is:{e}')
