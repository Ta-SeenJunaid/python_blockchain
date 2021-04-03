import pytest
from backend.blockchain.blockchain import Blockchain
from backend.blockchain.block import GENESIS_DATA


def test_blockchain_instance():
    blockchain = Blockchain()

    assert blockchain.chain[0].hash == GENESIS_DATA['hash']


def test_add_block():
    blockchain = Blockchain()
    data = 'test_data'
    blockchain.add_block(data)

    assert blockchain.chain[-1].data == data


@pytest.fixture
def blockchain_with_five_blocks():
    blockchain = Blockchain()
    for i in range(4):
        blockchain.add_block(i)
    return blockchain


def test_is_valid_chain_with_tampered_genesis(blockchain_with_five_blocks):
    blockchain_with_five_blocks.chain[0].hash = 'tampered hash'
    with pytest.raises(Exception, match='The genesis block must need to be valid'):
        Blockchain.is_valid_chain(blockchain_with_five_blocks.chain)


def test_is_valid_chain(blockchain_with_five_blocks):
    Blockchain.is_valid_chain(blockchain_with_five_blocks.chain)


def test_replace_chain(blockchain_with_five_blocks):
    blockchain = Blockchain()
    blockchain.replace_chain(blockchain_with_five_blocks.chain)

    assert blockchain.chain == blockchain_with_five_blocks.chain

def test_replace_chain_with_not_longer(blockchain_with_five_blocks):
    blockchain = Blockchain()

    with pytest.raises(Exception, match='Cannot replace. The incoming chain must be longer'):
        blockchain_with_five_blocks.replace_chain(blockchain.chain)


def test_replace_chain_with_tampered_chain(blockchain_with_five_blocks):
    blockchain = Blockchain()
    blockchain_with_five_blocks.chain[1].hash = 'tampered hash'

    with pytest.raises(Exception, match='The incoming chain is invalid'):
        blockchain.replace_chain(blockchain_with_five_blocks.chain)