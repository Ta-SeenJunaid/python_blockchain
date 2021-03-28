import time
from backend.blockchain.blockchain import Blockchain
from backend.util.hex_to_binary import hex_to_binary
from backend.config import SECONDS

blockchain = Blockchain()

times = []

for i in range(30):
    start_time = time.time_ns()
    blockchain.add_block(i)
    end_time = time.time_ns()

    time_to_mine = (end_time-start_time) / SECONDS
    times.append(time_to_mine)
    average_time_to_mine = sum(times) / len(times)

    print(f'Index number of new block: {blockchain.chain.index(blockchain.chain[-1])}')
    print(f'Difficulty of new block: {blockchain.chain[-1].difficulty}')
    print(f'Time to mine new block: {time_to_mine}')
    print(f'Average time to mine new block: {average_time_to_mine}')
    print(f'Block hash: {blockchain.chain[-1].hash}')
    print(f'Block hash binary version: {hex_to_binary(blockchain.chain[-1].hash)}\n')
