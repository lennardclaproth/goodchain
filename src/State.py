from modules.state.Store import Store

def init(di_container):
    global store
    store = Store(di_container)
    store.initialize_registry()

instance = lambda class_repr: store.find(class_repr).get_instance()