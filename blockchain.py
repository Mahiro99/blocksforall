import hashlib
import json
from time import time


class BlockChain(object):

    def __init__(self):
        # constructor creates an initially empty list to store our blockchain
        self.chain = []

        # we have another list to store current transactions
        self.transactions = []

        # the first block(genesys block) would have to be initalized with no predecessors, and proof-of-work(mining) provided
        self.add_block(proof=100, previous_hash=1)

    # consensus algorithm

    # What does a BLOCK look like?
    # --> Each block has an index, a timestamp, list of transactions, a proof,
        # hash of previous block(gives the immutability factor)
        # block = {
        # 'index': 1,
        # 'timestamp': 1506057125.900785, --> in unix
        # 'transactions': [
        #     {
        #         'sender': "8527147fe1f5426f9dd545de4b27ee00",
        #         'recipient': "a77f5cdfa2934df3954a5c7c7da5df1f",
        #         'amount': 5,
        #     }
        # ],
        # 'proof': 324984774000, --> I am guessing this is the so called "nonce" --> related to mining/and validity-->proof of work
        # 'previous_hash': "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824"
        #  what about the current hash?
        # }

    # create a block and add to chain, returns the block(dictionary)

    def add_block(self, proof, previous_hash=None):

        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.transactions,
            'proof': proof,  # The proof given by the Proof of Work algorithm
            'previous_hash': previous_hash or self.hash(self.latest_block)
        }

        # Reset the current list of transactions, why though?
        self.transactions = []

        self.chain.append(block)
        return block

    # hashes the whole block

    @staticmethod
    def hasher(self, block):

        # converts block to string, and orders the dictionary, or it'll introduce inconsistent hashes
        blockInString = json.dumps(block, sort_keys=True).encode()

        # Creates a SHA-256 hash of a Block
        return hashlib.sha256(blockInString).hexdigest()

    def add_transaction(self, sender, receiver, mony):

        self.transactions.append(
            {
                'sender': sender,
                'recipient': receiver,
                'amount': mony,
            }
        )

        # returns the index of the block(the next one to be mined) that holds this transaction
        return self.latest_block['index'] + 1

    # returns the last block in the chain

    @property
    def latest_block(self):
        return self.chain[-1]

    # Using  proof-of-work algorithm(POW), new blocks are created/mined on the blockchain. The goal of PoW is to figure out
    # the number which would solve a problem. Computationally, this number should be difficult to find, but easy to verify
    # by the network.

    # In general, the difficulty is determined by the number of characters searched for in a string.

    # --> in this case, we decided that the multiplication of hashed x and y should end with 0
    # x = 5
    # y = 0  # We don't know what y should be

    # so while the multiplication of the hashed values does not return a value of 0 at  index[-1] (the last character) , then increment
    # while sha256(f'{x*y}'.encode()).hexdigest()[-1] != "0":
    #     y += 1
    # print(f'The solution is y = {y}')

    # Algorithm
    # Find a number p' such that hash(pp') contains leading 4 0s, where p is the previous p'
    # p is the previous proof, and p' is the new proof

    def proof_of_work(self, last_proof):
        proof = 0
        while self.proofing(last_proof, proof) is False:
            proof += 1
        return proof

    @staticmethod
    # returns: <bool> True if correct, False if not.
    def proofing(last_proof, proof):

        guess = f'{last_proof}{proof}'.encode()
        guessHashed = hashlib.sha256(guess).hexdigest()

        return guessHashed[:4] == "0000"
