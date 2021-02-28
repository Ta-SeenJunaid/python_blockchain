class Block:
    def __init__(self, timestamp, previous_hash, hash, data):
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.hash = hash
        self.data = data

    def __repr__(self):
        return (
            'Block('
            f'timestamp: {self.timestamp}, '
            f'previous_hash: {self.previous_hash}, '
            f'hash: {self.hash}, '
            f'data: {self.data}'
        )
        return f'Block - data: {self.data}'

print(f'block.py __name__: {__name__}')