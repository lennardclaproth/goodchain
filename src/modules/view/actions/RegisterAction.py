from modules.user.context import UserContext
from modules.view.actions.IAction import IAction

class RegisterAction(IAction):

    def __init__(self, page, di_container):
        super().__init__(page, di_container)

    def validate_password(self):
        if(self.page.password != self.page.password_confirm):
            raise ValueError('Passwords do not match, make sure the passwords match.')
        return True

    def handle(self):
        user_context:UserContext = self.di_container.get_dependency('user_context')
        try: 
            if(self.validate_password()):
                user_context.create_user(self.page.username, self.page.password)
                return self.page.options.get('1')
        except Exception as e:
            raise ValueError(f'Failed to create a new user.\nNested exception: {e}')
