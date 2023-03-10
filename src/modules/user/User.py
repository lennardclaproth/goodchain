from dataclasses import dataclass
import State
from modules.state.variables.BlockChain import BlockChain

@dataclass
class User:
    user_id: str
    username: str
    password: str
    private_key: str
    public_key: str
    pending_actions = []
    balance = lambda x: State.instance(BlockChain).get_value().get_balance() if State.instance(BlockChain).get_value() is not None else 50
