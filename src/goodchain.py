from curses import wrapper
import State
from DiContainer import DiContainer
from Startup import Startup
from modules.view.pages.ErrorPage import ErrorPage
from modules.view.pages.MainMenu import MainMenu
from modules.state.variables.Error import Error

# TODO: startup start server create IP table poll hosts/servers and establish connections
# TODO: should start client, client should connect with server after server started
# TODO: should run on different threads

def main(stdscr):
    di_container = DiContainer()
    Startup.run(di_container,stdscr)
    render_engine = di_container.get_dependency('render_engine')
    next_action = render_engine.load(MainMenu)
    while next_action != 'q':
        try:    
            next_action = render_engine.load(next_action)        
        except Exception as e:
            State.instance(Error).set_value(e)
            next_action = render_engine.load(ErrorPage)

if __name__ == "__main__":
    wrapper(main)
