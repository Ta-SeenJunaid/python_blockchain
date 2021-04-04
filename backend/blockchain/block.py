import time
from backend.util.crypto_hash import crypto_hash
from backend.util.hex_to_binary import hex_to_binary
from backend.config import MINE_RATE

genesis_timestamp = time.time_ns()
GENESIS_DATA = {
    'timestamp' : genesis_timestamp,
    'previous_hash' : '0000000000000000000000000000000000000000000000000000000000000000',
    'hash' : crypto_hash(genesis_timestamp, '0000000000000000000000000000000000000000000000000000000000000000', [], 0, 3),
    'data' : [],
    'difficulty' : 3,
    'nonce': 0
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

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def to_json(self):
        return self.__dict__

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

    @staticmethod
    def is_valid_block(previous_block, block):

        if block.previous_hash != previous_block.hash:
            raise Exception('The block last hash must be correct')
        if hex_to_binary(block.hash)[0 : block.difficulty ] != '0'*block.difficulty:
            raise Exception('The proof of work requirments was not met')
        if abs(previous_block.difficulty - block.difficulty) > 1:
            raise Exception('The block difficulty must only adjust by 1')
        reconstructed_hash = crypto_hash(block.timestamp, block.previous_hash,
                                         block.data, block.nonce, block.difficulty)
        if block.hash != reconstructed_hash:
            raise Exception('The block hash must be correct')


def main():
    genesis_block = Block.genesis()
    block = Block.mine_block(genesis_block, "Our data")
    print(block)
    print(f'block.py __name__: {__name__}')

    tempered_block = block
    tempered_block.previous_hash = "tempered_hash"

    try:
        Block.is_valid_block(genesis_block, tempered_block)
    except Exception as e:
        print(f'is_valid_block: {e}')

if __name__ == '__main__':
    main()