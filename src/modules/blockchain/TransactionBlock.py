from modules.blockchain.Block import Block
from modules.signing.Signature import Signature
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from modules.state.variables.LoggedInUser import LoggedInUser
import State

# TODO: refactor class

from modules.transaction.Transaction import Transaction

REWARD_VALUE = 25.0
leading_zeros = 2
next_char_limit = 20

class TransactionBlock (Block):

    def __init__(self, previousBlock):
        self.nonce = "A random nonce"
        self.validated_by = []
        self.validated = False
        super().__init__([], previousBlock)

    def addTx(self, Tx_in):
        self.data.append(Tx_in)

    def get_balance(self, stack=None, pbc = None):
        if pbc is None:
            user = State.instance(LoggedInUser).get_value()
            if user is not None:
                pbc = user.public_key
        if stack is None:
            stack = {
                'in': [],
                'out':[]
            }
        total_in, total_out = self.__count_totals(pbc)
        stack['in'].append(total_in)
        stack['out'].append(total_out)
        if self.previousBlock is None:
            spent = 0
            received = 50
            for item in stack['in']:
                spent += item
            for item in stack['out']:
                received += item
            return received - spent
        else:
            return self.previousBlock.get_balance(stack)

    def __count_totals(self, pbc = None):
        total_in = 0
        total_out = 0
        for tx in self.data:
            for addr, amt in tx.inputs:
                if pbc is not None and addr == pbc:
                    total_in = total_in + amt
                elif pbc is None:
                    total_in = total_in + amt
            for addr, amt in tx.outputs:
                if pbc is not None and addr == pbc:
                    total_out = total_out + amt
                elif pbc is None:
                    total_out = total_out + amt
        return total_in, total_out

    def validate(self, pbc):
        block_valid = self.is_valid()
        if block_valid:
            if pbc in self.validated_by:
                raise ValueError('You have already validated this block. You cannot validate it twice.')
            else:
                self.validated_by.append(pbc)
        if(len(self.validated_by) >= 3):
            self.validated = True
        if not block_valid:
            raise ValueError('The block is not valid. This could be either due to a transaction not being valid or the chain has been tampered with.')
        return block_valid

    def is_valid(self, mine = False):
        if not super(TransactionBlock, self).is_valid(True):
            return False
        pbc_list = []
        for tx in self.data:
            transaction = tx
            if len(transaction.inputs) > 0:
                pbc, amt = transaction.inputs[0]
            pbc_list.append(pbc)
            if not tx.is_valid():
                return False
        for pbc in pbc_list:
            if self.get_balance(None, pbc) < 0:
                # State.instance(InvalidTransaction).set().invalid_transactions.append(tx.tx_id)
                raise ValueError("Transaction is invalid. One or more transactions need to be cancelled.")
                
        # if len(State.variables.invalid_transactions) > 0 and mine is False:
        #     return False

        total_in, total_out = self.__count_totals()
        
        Tx_Balance = round(total_out - total_in, 10)
        
        # if  Tx_Balance > REWARD_VALUE:
        #     return False
        return True

    def calculate_nonce(self, leading_zeros, nonce = 0):
        found = False
        digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
        digest.update(bytes(str(self.data), 'utf8'))
        digest.update(bytes(str(self.previousHash), 'utf8'))
        digest_temp = digest.copy()
        digest_temp.update(bytes(str(nonce), 'utf8'))
        hash = digest_temp.finalize()
        # print(hash)
        zeros = bytes('0' * leading_zeros, 'utf8')
        if hash[:leading_zeros] == zeros:
            found = True
            self.nonce = nonce 
        del digest_temp

        if found is True:
            return True
        else:
            return nonce

    def mine(self, pbc):
        tx = Transaction(1)
        tx.add_output(pbc, REWARD_VALUE)
        self.addTx(tx)
        self.blockHash = self.computeHash()
        return True

