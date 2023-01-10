from ClassLoader import ClassLoader, ClassWrapper

from modules.state.variables.Variable import Variable
from modules.view.pages.Page import Page
# TODO: change this so that it updates data correctly and often (check update_state and what it needs)


class Store:
    def __init__(self, di_container):
        self.di_container = di_container
        self.__modules = [('modules.state.variables', Variable),
                          ('modules.view.pages', Page)]
        self.__registry = {}

        # self.logged_in_user = None
        # self.error = None
        # self.is_chain_valid = False
        # self.is_block_validated = False
        # self.pending_actions = []
        # self.balance = None
        # self.chain : TransactionBlock = None
        # self.selected_transaction = None
        # self.selected_block = None
        # self.invalid_transactions = []

    def initialize_registry(self):
        for module_name, type in self.__modules:
            self.__registry.update(ClassLoader.load(module_name, type))

        for class_name in self.__registry:
            wrapper: ClassWrapper = self.__registry.get(class_name)
            wrapper.instantiate()

    def find(self, class_repr):
        try:
            return self.__registry.get(class_repr.__name__)
        except Exception as e:
            raise ValueError(f"Check if the class of type: {type(class_repr)} has been registered correctly.\nNested exception  is: {e}")

    def update(self):
        print("to implement")
