import pickle
import curses
import State
from DiContainer import DiContainer
from modules.db.context import DbContext
from modules.p2pNetwork.Logging import Logger
from modules.p2pNetwork.client.ClientConnectionHandler import ClientConnection
from modules.p2pNetwork.messaging.MessageQueue import MessageQueue
from modules.p2pNetwork.server.ServerConnectionHandler import ServerConnection
from modules.user.context import UserContext
from modules.blockchain.ChainHandler import ChainHandler
from modules.view.RenderEngine import Loader as RenderEngine

class Startup:

    @staticmethod
    def run(di_container: DiContainer, stdscr=None):
        State.init(di_container)
        Startup.initialize_curses(stdscr)
        Startup.initialize_di_container(di_container, stdscr)
        Startup.validate_blockchain()
        Logger.load_logs()
        State.instance(MessageQueue).set_value(MessageQueue())
        State.instance(ServerConnection).set_value(ServerConnection())
        State.instance(ClientConnection).set_value(ClientConnection())

    def initialize_curses(stdscr):
        curses.curs_set(0)
        stdscr.border(0)
        curses.start_color()
        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)
        curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_BLACK)

    @staticmethod
    def initialize_di_container(di_container: DiContainer, stdscr):
        di_container.add_dependency(DbContext(), 'db_context')
        di_container.add_dependency(UserContext(
            di_container.get_dependency('db_context')), 'user_context')
        di_container.add_dependency(RenderEngine(stdscr), 'render_engine')

    @staticmethod
    def validate_blockchain():
        block_chain = ChainHandler.load_chain()
        if block_chain is not None:
            print("not none")
        #     State.variables.is_chain_valid = block_chain.is_valid()
        #     State.variables.is_block_validated = block_chain.validated
        #     State.variables.chain = block_chain
        #     if block_chain.validated == False:
        #         State.variables.pending_actions = ['validate_block']
        # else:
        #     State.variables.is_chain_valid = True
