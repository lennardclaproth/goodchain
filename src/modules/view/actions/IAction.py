class IAction:

    def __init__(self, page, di_container):
        self.page = page
        self.di_container = di_container

    def handle(self):
        pass
