import pytest
import time
from backend.blockchain.block import Block, GENESIS_DATA
from backend.util.hex_to_binary import hex_to_binary
from backend.config import MINE_RATE, SECONDS


def test_mine_block():
    previous_block = Block.genesis()
    data = "testing data"
    block = Block.mine_block(previous_block, data)

    assert isinstance(block, Block)
    assert block.data == data
    assert block.previous_hash == previous_block.hash
    assert hex_to_binary(block.hash)[0:block.difficulty] == '0' * block.difficulty


def test_genesis():
    genesis = Block.genesis()

    assert isinstance(genesis, Block)
    for key, value in GENESIS_DATA.items():
        getattr(genesis, key) == value


def test_quickly_mined_block():
    previous_block = Block.mine_block(Block.genesis(), 'foo')
    mined_block = Block.mine_block(previous_block, 'bar')

    assert mined_block.difficulty == previous_block.difficulty + 1


def test_slowly_mined_block():
    previous_block = Block.mine_block(Block.genesis(), 'foo')
    time.sleep(MINE_RATE / SECONDS)
    mined_block = Block.mine_block(previous_block, 'bar')

    assert mined_block.difficulty == previous_block.difficulty - 1


def test_mined_block_difficulty_limits_at_1():
    last_block = Block(
        time.time_ns(),
        'test_last_hash',
        'test_hash',
        'test_data',
        1,
        0
    )

    time.sleep(MINE_RATE / SECONDS)
    mined_block = Block.mine_block(last_block, 'bar')

    assert mined_block.difficulty == 1


@pytest.fixture
def previous_block():
    return Block.genesis()


@pytest.fixture
def block(previous_block):
    return Block.mine_block(previous_block, "test data")


def test_is_valid_block(previous_block, block):
    Block.is_valid_block(previous_block, block)


def test_is_valid_block_with_tampered_previous_hash(previous_block, block):
    block.previous_hash = "tampered previous hash"
    with pytest.raises(Exception, match='The block last hash must be correct'):
        Block.is_valid_block(previous_block, block)

def test_is_valid_block_with_bad_proof_of_work(previous_block, block):
    block.hash = 'fff'
    with pytest.raises(Exception, match='The proof of work requirments was not met'):
        Block.is_valid_block(previous_block, block)

def test_is_valid_block_with_jumped_difficulty(previous_block, block):
    jumped_difficulty = 10
    block.difficulty = jumped_difficulty
    block.hash = f'{"0" * jumped_difficulty}fff'
    with pytest.raises(Exception, match='The block difficulty must only adjust by 1'):
        Block.is_valid_block(previous_block, block)

def test_is_valid_block_with_tampered_block_hash(previous_block, block):
    block.hash = '0000000000000000000000000000000000000000000000000000000000000fff'
    with pytest.raises(Exception, match='The block hash must be correct'):
        Block.is_valid_block(previous_block, block)