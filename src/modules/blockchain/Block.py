import random
import string
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes


class Block:

    def __init__(self, data=None, previousBlock=None):
        self.data = data
        chars = string.ascii_uppercase + string.digits
        self.blockId = f"{''.join(random.choice(chars) for _ in range(4))}-{''.join(random.choice(chars) for _ in range(4))}-{''.join(random.choice(chars) for _ in range(4))}"
        self.blockHash = None
        self.mined_by = None
        self.previousBlock = previousBlock
        self.previousHash = None
        if previousBlock != None:
            self.previousHash = previousBlock.computeHash()

    def computeHash(self):
        digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
        digest.update(bytes(str(self.mined_by), 'utf8'))
        digest.update(bytes(str(self.blockId), 'utf8'))
        digest.update(bytes(str(self.data), 'utf8'))
        digest.update(bytes(str(self.previousHash), 'utf8'))
        return digest.finalize()

    def is_valid(self, mine=False):
        if self.previousBlock == None:
            if self.blockHash == self.computeHash():
                return True
            else:
                return False
        else:
            current_block_validity = self.blockHash == self.computeHash()
            previous_block_validity = self.previousBlock.is_valid(mine)
            return current_block_validity and previous_block_validity
