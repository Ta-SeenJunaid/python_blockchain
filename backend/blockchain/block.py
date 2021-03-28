import time
from backend.util.crypto_hash import crypto_hash
from backend.util.hex_to_binary import hex_to_binary
from backend.config import MINE_RATE

GENESIS_DATA = {
    'timestamp' : 1,
    'previous_hash' : 'genesis_previous_hash',
    'hash' : '0000000000000000000000000000000000000000000000000000000000000000',
    'data' : [],
    'difficulty' : 3,
    'nonce': 'genesis_nonce'
}
class Block:
    def __init__(self, timestamp, previous_hash, hash, data, difficulty, nonce):
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.hash = hash
        self.data = data
        self.difficulty = difficulty
        self.nonce = nonce

    def __repr__(self):
        return (
            'Block('
            f'timestamp: {self.timestamp}, '
            f'previous_hash: {self.previous_hash}, '
            f'hash: {self.hash}, '
            f'data: {self.data}, '
            f'difficulty: {self.difficulty}, '
            f'nonce: {self.nonce})'
        )

    @staticmethod
    def mine_block(previous_block, data):
        timestamp = time.time_ns()
        previous_hash = previous_block.hash
        difficulty = Block.adjust_difficulty(previous_block, timestamp)
        nonce = 0
        hash = crypto_hash(timestamp, previous_hash, data, nonce, difficulty)

        while (hex_to_binary(hash))[0:difficulty] != '0' * difficulty :
        # while hash[0:difficulty] != '0' * difficulty :
            nonce += 1
            timestamp = time.time_ns()
            difficulty = Block.adjust_difficulty(previous_block, timestamp)
            hash = crypto_hash(timestamp, previous_hash, data, nonce, difficulty)

        return Block(timestamp, previous_hash, hash, data, difficulty, nonce)

    @staticmethod
    def adjust_difficulty(previous_block, new_timestamp):
        if(new_timestamp - previous_block.timestamp) < MINE_RATE:
            return previous_block.difficulty + 1

        if(previous_block.difficulty - 1) > 0:
            return previous_block.difficulty - 1

        return 1


    @staticmethod
    def genesis():
        return Block(**GENESIS_DATA)

def main():
    genesis_block = Block.genesis()
    block = Block.mine_block(genesis_block, "Our data")
    print(block)
    print(f'block.py __name__: {__name__}')

if __name__ == '__main__':
    main()