from modules.view.actions.TransactionAction import TransactionAction
from modules.components.TextBox import TextBox
from modules.components.Input import Input

from modules.view.pages.Page import Page
from modules.view.pages.SuccessPage import SuccessPage

class NewTransaction(Page):

    def __init__(self):
        super().__init__()
        self.options.update({
            '1':SuccessPage
        })
        self.reqd = []
        self.action = TransactionAction(self, self.di_container)

    def render_header(self, size):
        text = 'Processing transaction, please wait... 💸'
        return TextBox.get_component(size, 3, text)

    def render_body(self,size):
        self.user_out = Input.get_component('Please type a username to send money to', {'height':5, 'width':100, 'y':3, 'x': 1})
        self.reqd = Input.get_component("Please enter the usernames of users who need to sign extra seperated by a ','",{'height':5, 'width':100, 'y':6, 'x': 1})
        self.transaction_amt = Input.get_component('Please enter the amount',{'height':5, 'width':100, 'y':9, 'x': 1})
        self.transaction_costs = Input.get_component('Please enter the transaction costs',{'height':3, 'width':100, 'y':12, 'x': 1})
    
    def perform_action(self):
        return self.action.handle()

    def render(self, size):
        self.render_body(size)
        self.render_header(size)