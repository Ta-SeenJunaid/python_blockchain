import time
from backend.util.crypto_hash import crypto_hash

GENESIS_DATA = {
    'timestamp' : 1,
    'previous_hash' : 'genesis_previous_hash',
    'hash' : 'gensis_hash',
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
        difficulty = previous_block.difficulty
        nonce = 0
        hash = crypto_hash(timestamp, previous_hash, data, nonce, difficulty)

        while hash[0:difficulty] != '0' * difficulty :
            nonce += 1
            timestamp = time.time_ns()
            hash = crypto_hash(timestamp, previous_hash, data, nonce, difficulty)

        return Block(timestamp, previous_hash, hash, data, difficulty, nonce)

    @staticmethod
    def genesis():
        return Block(**GENESIS_DATA)

def main():
    genesi_block = Block.genesis()
    block = Block.mine_block(genesi_block, "Our data")
    print(block)
    print(f'block.py __name__: {__name__}')

if __name__ == '__main__':
    main()