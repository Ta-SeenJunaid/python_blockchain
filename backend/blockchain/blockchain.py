from backend.blockchain.block import Block
from backend.wallet.transaction import Transaction
from backend.config import MINING_REWARD_INPUT


class Blockchain:
    def __init__(self):
        self.chain = [Block.genesis()]

    def add_block(self, data):
        self.chain.append(Block.mine_block(self.chain[-1], data))

    def __repr__(self):
        return f'Blockchain: {self.chain}'

    def replace_chain(self, chain):

        if len(chain) <= len(self.chain):
            raise Exception('Cannot replace. The incoming chain must be longer')

        try:
            Blockchain.is_valid_chain(chain)
        except Exception as e:
            raise Exception(f'Cannot replace. The incoming chain is invalid: {e}')

        self.chain = chain

    def to_json(self):
        return list(map(lambda block:block.to_json(),self.chain))

    @staticmethod
    def from_json(chain_json):
        blockchain = Blockchain()
        blockchain.chain = list(
            map(lambda block_json: Block.from_json(block_json), chain_json)
        )

        return blockchain


    @staticmethod
    def is_valid_chain(chain):

        if chain[0] != Block.genesis():
            raise Exception('The genesis block must need to be valid')

        for i in range(1, len(chain)):
            block = chain[i]
            previous_block = chain[i-1]
            Block.is_valid_block(previous_block, block)

    @staticmethod
    def is_valid_transaction_chain(chain):

        transaction_ids = set()

        for block in chain:
            has_mining_reward = False

            for transaction_json in block.data:
                transaction = Transaction.from_json(transaction_json)

                if transaction.input == MINING_REWARD_INPUT:
                    if has_mining_reward:
                        raise Exception('There can only be one mining reward per block. '\
                                        f'Check block with hash: {block.hash}')

                if transaction.input == MINING_REWARD_INPUT:
                    has_mining_reward = True

                if transaction.id in transaction_ids:
                    raise Exception(f'Transaction {transaction.id} is not unique')

                transaction_ids.add(transaction.id)

                Transaction.is_valid_transaction(transaction)



def main():
    blockchain = Blockchain()
    # blockchain.add_block("one")
    # blockchain.add_block("two")
    # blockchain.add_block("three")
    for i in range(4):
        blockchain.add_block(i)
    print(blockchain)
    print(f'blockchain.py __name__: {__name__}')


if __name__ == '__main__':
    main()